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

def play_with_buffering(url, ref=None):
    fp = open(defvals.lock, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except:
        return False

    if url:
        player = xplay.getPlayer()
        player_cmd = {
            'mpv'   : '%s -o - \'%s\' | %s - ' %(xdef.ytdlcmd(), url, xdef.mpv),
            'ffplay': '%s -o - \'%s\' | %s - ' %(xdef.ytdlcmd(), url, xdef.ffplay)
        }
        cmd = player_cmd[player]
        print(cmd)
        proc = subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', cmd])
        return True

    fp.close()
    return True

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
    (options, args) = parser.parse_args()

    if options.url:
        play(options.url, options.ref)

