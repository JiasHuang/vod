#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import subprocess
import xdef
import youtubedl
import mpv, omxp

def getPlayer():

    if xdef.player != 'def':
        return xdef.player

    if os.path.exists('/usr/bin/mpv'):
        return 'mpv'

    if os.path.exists('/usr/bin/omxplayer'):
        return 'omxp'

    return 'err'

def checkFileArgs(url):
    xargs = xdef.mpv_ytdl
    if re.search(r'.m3u', url):
        fd = open(url, 'r')
        txt = fd.read()
        if re.search(r'dailymotion', txt):
            xargs = ''
        fd.close()
        return xargs
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
    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
    if url == '':
        print '[xplay] invalid url'
        return 0
    subprocess.Popen(['smplayer', '-fullscreen', url])
    return 0

def runMPV(url, ref):

    p = None
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

        p = subprocess.Popen('%s %s \'%s\'' %(xdef.mpv, xargs, url), shell=True)

    else:
        os.system('echo loadfile \"%s\" > %s' %(url, xdef.fifo))
        os.system('echo sub-remove > %s' %(xdef.fifo))

    sub = youtubedl.extractSUB_keepvid(ref)
    if sub:
        os.system('echo sub-add \"%s\" select > %s' %(sub, xdef.fifo))

    if p:
        p.communicate()

    return 0

def runPIPE(url, ref):
    subprocess.Popen(['wget', '-q', '-O', xdef.fifo_bs, url])
    setAct('stop', None)
    os.system('%s \'%s\' --input-file=%s' %(xdef.mpv, xdef.fifo_bs, xdef.fifo))
    return 0

def runOMXP(url, ref):
    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
    if checkProcessRunning('omxplayer.bin'):
        omxp.setAct('stop', None)
    sub = youtubedl.extractSUB_keepvid(ref)
    if sub:
        os.system('omxplayer -o hdmi -I --subtitle \'%s\' \'%s\' 2>&1 | tee %s' %(sub, url, xdef.log))
    else:
        os.system('omxplayer -o hdmi -I \'%s\' 2>&1 | tee %s' %(url, xdef.log))
    return 0

def runDBG(url, ref):
    if youtubedl.checkURL(url):
        youtubedl.extractURL(url)
    return 0

def playURL(url, ref):

    player = getPlayer()

    print '\n[xplay][%s][url]\n\n\t%s' %(player, url)
    print '\n[xplay][%s][ref]\n\n\t%s' %(player, ref)

    if url == None or url == '':
        return 0

    #if re.search(r'vizplay', url):
    #    player = 'pipe'

    if player == 'smp':
        return runSMP(url, ref)

    if player == 'mpv':
        return runMPV(url, ref)

    if player == 'xbmc':
        return runXBMC(url, ref)

    if player == 'pipe':
        return runPIPE(url, ref)

    if player == 'omxp':
        return runOMXP(url, ref)

    return runDBG(url, ref)

def setAct(act, val):

    player = getPlayer()
    print('\n[xplay]\n\n\t'+ '%s,%s,%s' %(player, act, val))

    if player == 'mpv' and checkProcessRunning('mpv'):
        return mpv.setAct(act, val)

    if player == 'omxp' and checkProcessRunning('omxplayer.bin'):
        return omxp.setAct(act, val)

