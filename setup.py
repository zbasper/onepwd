#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import platform

setup_modules = os.popen('pip3 list').read().split("\n")
setup_modules = [m.split(" ", 1)[0] for m in setup_modules[2:len(setup_modules)-1]]
setup_modules = set(setup_modules)

with open("require.txt", "r") as f:
    for content in f.readlines():
        module3 = content.strip()
        if module3 not in setup_modules:
            os.system('pip3 install ' + module3)

if platform.system() == 'Windows':
    with open("onepwd.vbs", "w") as f:
        f.write('set ws=WScript.CreateObject("WScript.Shell")\n')
        f.write('ws.Run "{} {}", 0'.format(sys.executable, os.getcwd()+'\\'+'onepwd.py'))
elif platform.system() == 'Darwin':
    with open("onepwd.sh", "w") as f:
        f.write('#!/usr/bin/env sh\n')
        f.write('{} {}'.format(sys.executable, os.getcwd()+'/'+'onepwd.sh'))
