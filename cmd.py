#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

def update():
    os.chdir('/opt/vod')
    os.system('sudo git pull')
    os.system('sudo ./install.sh')
    os.system('sudo ./sync.sh')
    return

def reset():
    os.system('sudo rm /tmp/vod*')
    update()

def showInfo():
    for i in range(1, 30):
        print('Retry: '+str(i))
        os.system('ifconfig')
        os.system('sleep 10')
    return

def main():

    if len(sys.argv) < 2:
        return

    cmd = sys.argv[1]

    if cmd == 'update':
        update()
    elif cmd == 'showInfo':
        showInfo()
    elif cmd == 'reset':
        reset()

    return

if __name__ == '__main__':
    main()
