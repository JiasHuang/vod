#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import subprocess
import xdef

def setAct(act, val):
    if act == 'pause':
        cmd = 'p'
    elif act == 'stop':
        cmd = 'q'
    elif act == 'forward' and val:
        cmd = '\x1b[C'
    elif act == 'backward' and val:
        cmd = '\x1b[D'
    else:
        print 'unsupported: %s %s' %(act, val)
        return

    os.system('echo %s > %s' %(cmd, xdef.fifo))

def main():

    url = None
    ref = None

    if len(sys.argv) < 2:
        print 'usage: omxp.py url'
        return

    url = sys.argv[1]

    if len(sys.argv) >= 3:
        ref = sys.argv[2]

    cmd = 'omxplayer -o hdmi \'%s\'' %(url)
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
    pipe = proc.stdin
    fifo = open(xdef.fifo)

    while proc.poll() == None:
        line = fifo.read()
        if line:
            line = line.rstrip()
            proc.stdin.write(line)
        time.sleep(1)


if __name__ == '__main__':
    main()
