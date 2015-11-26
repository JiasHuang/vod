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
    xargs = ''
    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
        xargs = xdef.mpv_ytdl
    if url == '':
        print '[xplay] invalid url'
        return 0
    if not checkProcessRunning('mpv'):
        os.system('%s \'%s\' --user-agent=\'%s\' --referrer=\'%s\' --input-file=%s %s'
            %(xdef.mpv, url, xdef.ua, ref, xdef.mpv_fifo, xargs))
    else:
        os.system('echo loadfile \"%s\" > %s' %(url, xdef.mpv_fifo))
    return 0

def runPIPE(url, ref):
    os.system("youtube-dl -o - \'%s\' | %s -" %(url, xdef.mpv))
    return 0

def runDBG(url, ref):
    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
    print '\n[xplay][dbg][url]\n\n\t%s' %(url)
    print '\n[xplay][dbg][ref]\n\n\t%s' %(ref)
    return 0

def playURL(url, ref):

    if url == None or url == '':
        return 0

    if xdef.player == 'smp':
        return runSMP(url, ref)

    if xdef.player == 'mpv':
        return runMPV(url, ref)

    if xdef.player == 'xbmc':
        return runXBMC(url, ref)

    if xdef.player == 'pipe':
        return runPIPE(url, ref)

    return runDBG(url, ref)

