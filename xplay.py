#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import subprocess
import xdef
import youtubedl

def checkProcessRunning(process):
    cmd = 'pidof %s' %(process)
    try:
        result = subprocess.check_output(cmd, shell=True)
        return True
    except:
        return False

def runIdle():
    subprocess.Popen(['smplayer', '-send-action', 'stop'])
    subprocess.Popen(['xbmc-send', '-a', 'Stop'])
    return

def runXBMC(url, ref):
     # start xbmc if necessary
    if not checkProcessRunning('kodi.bin'):
        subprocess.Popen(['kodi'])
        time.sleep(8)
    cmd = 'PlayMedia(%s|Referer=%s)' %(url, ref)
    subprocess.Popen(['xbmc-send', '-a', cmd])
    return 0

def runSMP(url, ref):
    subprocess.Popen(['smplayer', '-fullscreen', url])
    return 0

def runMPV(url, ref):
    xargs = xdef.mpv_ytdl
    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
    if url == '':
        print '[xplay] invalid url'
        return 0
    if not checkProcessRunning('mpv'):
        os.system('%s \'%s\' --user-agent=\'%s\' --referrer=\'%s\' --input-file=%s %s'
            %(xdef.mpv, url, xdef.ua, ref, xdef.fifo, xargs))
    else:
        os.system('echo loadfile \"%s\" > %s' %(url, xdef.fifo))
    return 0

def runPIPE(url, ref):
    subprocess.Popen(['wget', '-q', '-O', xdef.fifo_bs, url])
    if not checkProcessRunning('mpv'):
        os.system('%s \'%s\' --input-file=%s' %(xdef.mpv, xdef.fifo_bs, xdef.fifo))
    else:
        os.system('echo loadfile \"%s\" > %s' %(url, xdef.fifo))
    return 0

def runDBG(url, ref):
    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
    return 0

def playURL(url, ref):

    print '\n[xplay][%s][url]\n\n\t%s' %(xdef.player, url)
    print '\n[xplay][%s][ref]\n\n\t%s' %(xdef.player, ref)

    if url == None or url == '':
        return 0

    if re.search(r'vizplay', url):
        xdef.player = 'pipe'

    if xdef.player == 'smp':
        return runSMP(url, ref)

    if xdef.player == 'mpv':
        return runMPV(url, ref)

    if xdef.player == 'xbmc':
        return runXBMC(url, ref)

    if xdef.player == 'pipe':
        return runPIPE(url, ref)

    return runDBG(url, ref)

def setAct(act):
    if checkProcessRunning('mpv'):
        os.system('echo %s > %s' %(act, xdef.fifo))
    return 0

