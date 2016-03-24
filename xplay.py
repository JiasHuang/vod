#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import subprocess
import xdef
import youtubedl

def checkFileArgs(url):
    xargs = xdef.mpv_ytdl
    if re.search(r'.m3u', url):
        fd = open(url, 'r')
        txt = fd.read()
        if re.search(r'dailymotion', txt):
            xargs = ''
        fd.close()
        return xargs

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

    if url[0] == '/':
        xargs = checkFileArgs(url)

    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
        xargs = xdef.mpv_ytdl

    if url == '':
        print '[xplay] invalid url'
        return 0

    if not checkProcessRunning('mpv'):

        xargs = xargs + ' --user-agent=\'%s\'' %(xdef.ua)
        xargs = xargs + ' --referrer=\'%s\'' %(ref)
        xargs = xargs + ' --input-file=\'%s\'' %(xdef.fifo)

        sub = youtubedl.extractSUB(ref)
        if sub:
            xargs = '%s --sub-file=\'%s\'' %(xargs, sub)

        os.system('%s %s \'%s\'' %(xdef.mpv, xargs, url))

    else:
        os.system('echo sub-remove > %s' %(xdef.fifo))
        os.system('echo loadfile \"%s\" > %s' %(url, xdef.fifo))

        sub = youtubedl.extractSUB(ref)
        if sub:
            os.system('echo sub-add \"%s\" select > %s' %(sub, xdef.fifo))

    return 0

def runPIPE(url, ref):
    subprocess.Popen(['wget', '-q', '-O', xdef.fifo_bs, url])
    setAct('stop')
    os.system('%s \'%s\' --input-file=%s' %(xdef.mpv, xdef.fifo_bs, xdef.fifo))
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

