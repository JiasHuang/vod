#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import time
import fcntl

from optparse import OptionParser
from multiprocessing import Process, Value

import xdef

class defvals:
    lock = xdef.workdir+'vod_play_with_buffering'
    fifo = '/home/jias_huang/work/vod/test.fifo'

def dispatch():
    for i in range(3):
        print('playing '+ str(i))
        time.sleep(1)

def readCmd(gFlags, proc):
    fp = open(defvals.fifo, "r")
    flag = fcntl.fcntl(fp, fcntl.F_GETFL)
    fcntl.fcntl(fp, fcntl.F_SETFL, flag | os.O_NONBLOCK)
    while gFlags.value == 0:
        cmd = fp.read().strip()
        if cmd:
            if cmd == 'stop':
                print('terminating current playback')
                proc.terminate()
                break
            elif cmd == 'start':
                continue
            else:
                print('unknown command : \'%s\'' %(cmd))
        else:
            time.sleep(1)
    fp.close()
    print('readCmd End')
    return

def playURL(gFlags, url, ref=None):
    dispatch()
    gFlags.value = 1
    print('playURL End')
    return

def play_with_buffering(url, ref=None):
    fp = open(defvals.lock, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        return False

    if url:
        gFlags = Value('i', 0)
        proc_playURL = Process(target=playURL, args=(gFlags, url, ref))
        proc_readCmd = Process(target=readCmd, args=(gFlags, proc_playURL))
        proc_playURL.start()
        proc_readCmd.start()
        os.system('echo start > %s' %(defvals.fifo))
        proc_readCmd.join()

    fp.close()
    return True

def setAct(act, val=None):
    if play_with_buffering(None):
        print('No running instance')
        return
    os.system('echo %s > %s' %(act, defvals.fifo))
    return

def play(url, ref):
    if not play_with_buffering(url, ref):
        print('Another instance is running. Stop it ...')
        setAct('stop')
        time.sleep(2)
        play_with_buffering(url, ref)
    return

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--url", dest="url")
    parser.add_option("--ref", dest="ref")
    parser.add_option("--act", dest="act")
    parser.add_option("--val", dest="val")
    (options, args) = parser.parse_args()

    if options.url:
        play(options.url, options.ref)

    if options.act:
        setAct(options.act, options.val)

