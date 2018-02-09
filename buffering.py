#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import time
import fcntl
import signal

from optparse import OptionParser
from multiprocessing import Process, Value

import xdef
import xplay

class defvals:
    lock = xdef.workdir+'vod_play_with_buffering'
    fifo = xdef.fifo

def setupPipe():
    os.system('echo start > %s' %(defvals.fifo))

def readCmd(proc):
    fp = open(defvals.fifo, "r")
    flag = fcntl.fcntl(fp, fcntl.F_GETFL)
    fcntl.fcntl(fp, fcntl.F_SETFL, flag | os.O_NONBLOCK)
    while 1:
        time.sleep(1)
        cmd = fp.read().strip()
        if proc.poll() != None:
            break
        if cmd:
            if cmd == 'stop':
                print('terminating current playback')
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                break
            else:
                print('unknown command : \'%s\'' %(cmd))
    fp.close()
    print('readCmd End')
    return

def play_with_buffering(url, ref=None):
    fp = open(defvals.lock, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except:
        return False

    if url:
        p = Process(target=setupPipe)
        p.start()
        data = {'omxp' : xdef.omxp, 'mpv' : xdef.mpv, 'ffplay' : xdef.ffplay}
        cmd = '%s -o - \'%s\' | %s - ' %(xdef.ytdlcmd(), url, data[xplay.getPlayer()])
        proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
        readCmd(proc)
        p.join()
        return True

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

