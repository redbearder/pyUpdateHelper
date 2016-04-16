#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import getopt
import requests
import zipfile
#import psutil
import StringIO
from datetime import datetime

def Usage():
    print 'updatehelper usage:'
    print '-u,--url: check and download update package from this url address.'
    print '-v, --version: program current version'
    print '-p, --program: program name'
    print '-i, --identification: program identification'
    print '-P, --proxy: proxy for update'
    print '-V: Print updatehelper versio'

def killProcessByName(programname):
    os.system("ps -C "+programname+" -o pid=|xargs kill -9")

    '''
    process_name=iChat
    os.system('pkill '+process_name)

    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == programname:
            proc.kill()

    import os
    ret_text_list = os.popen("ps | grep "+programname)
    pid_list = []
    for line in ret_text_list:
        pid_list.append(line)
    cmd_list = pid_list[0].split()
    pid_num = cmd_list[1]
    print pid_num
    os.system("kill -9 %s"%pid_num)
    '''

def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir): os.mkdir(unziptodir, 0777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\','/')

        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir= os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir) : os.mkdir(ext_dir,0777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()

def main(argv):
    updateurl = ''
    version = ''
    program = ''
    identification=''
    proxies=''
    try:
        opts, args = getopt.getopt(argv[1:], 'u:v:p:i:V:', ['url=', 'version=', 'program=','identification='])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-u', '--url'):
            updateurl = a
            continue
        if o in ('-v', '--version'):
            version = a
            continue
        if o in ('-p', '--program'):
            program  = a
            continue
        if o in ('-i', '--identification'):
            identification  = a
            continue
        if o in ('-P', '--proxy'):
            proxies = {
                          "http": a,
                          "https": a,
                        }
            continue
        if o in ('-V'):
            print updatehelperversion
            sys.exit(0)
    try:
        if proxies == '':
            r = requests.get(updateurl+'?version='+version+'&program='+program+'&identification='+identification, stream=True)
            pass
        else:
            r = requests.get(updateurl+'?version='+version+'&program='+program+'&identification='+identification, stream=True,proxies=proxies)
            pass
        if(r.status_code == 200):
            print 'found new update and do update at '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            killProcessByName(program)
            z = zipfile.ZipFile(StringIO.StringIO(r.content))
            z.extractall()
            #unzip_file('update.zip','./')
            os.system('./'+program+' >>updatehelper.log &')
            pass
        else:
            print 'no availiable update at '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pass
    except Exception,e:
        print 'no availiable update or update fail at '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        killProcessByName(program)
        os.system('./'+program+' >>updatehelper.log &')
        pass
    sys.exit(0)

if __name__ == '__main__':
    updatehelperversion = 1.0
    main(sys.argv)