#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import hashlib

import xarg
import xdef
import xproc
import xurl
import mpv
import omxp
import ffplay
import youtubedl

def getPlayer():

    if xarg.player != 'def':
        return xarg.player

    if re.search(r'raspberrypi', subprocess.check_output('uname -a', shell=True)):
        return 'omxp'

    if os.path.exists('/usr/bin/mpv') or os.path.exists('/usr/local/bin/mpv'):
        return 'mpv'

    if os.path.exists('/usr/bin/ffplay'):
        return 'ffplay'

    return 'err'

def runDBG(url, ref, cookies=None):
    if youtubedl.checkURL(url):
        url, cookies = youtubedl.extractURL(url)
    youtubedl.extractSUB(url)
    return

def isPlayerRunning():
    player = getPlayer()
    if player == 'mpv' and xproc.checkProcessRunning('mpv'):
        return True
    if player == 'omxp' and xproc.checkProcessRunning('omxplayer.bin'):
        return True
    if player == 'ffplay' and xproc.checkProcessRunning('ffplay'):
        return True
    return False

def getNext(playing, playlist):

    if playlist != xurl.readLocal(xdef.playlist, 0):
        return None

    if isPlayerRunning():
        return None

    playbackMode = xurl.readLocal(xdef.playbackMode, 0)

    if playbackMode == 'LoopOne':
        return playing

    if playbackMode in ['AutoNext', 'LoopAll']:
        lines = playlist.splitlines()
        try:
            index = lines.index(playing)
            if index < (len(lines) - 1):
                return lines[index+1]
            if playbackMode == 'LoopAll' and index == (len(lines) - 1):
                return lines[0]
        except:
            return None

    return None

def playURL_core(url, ref, cookies=None):

    player = getPlayer()

    print('\n[xplay][%s]\n' %(player))
    print('\turl : %s' %(url or ''))
    print('\tref : %s' %(ref or ''))

    if url == None or url == '':
        return

    if player == 'mpv':
        return mpv.play(url, ref, cookies)

    if player == 'omxp':
        return omxp.play(url, ref, cookies)

    if player == 'ffplay':
        return ffplay.play(url, ref, cookies)

    return runDBG(url, ref, cookies)

def playURL(url, ref, cookies=None):

    if isPlayerRunning():
        if os.path.exists(xdef.playlist):
            setAct('stop', None)

    if xarg.pagelist:
        playlist = xurl.readLocal(xarg.pagelist)
        xurl.saveLocal(xdef.playlist, playlist, 0)
        while url != None:
            playURL_core(url, ref, cookies)
            url = ref = getNext(url, playlist)
    else:
        playURL_core(url, ref, cookies)

    return

def checkActVal(act, val):

    if act == 'percent':
        if not val:
            return False
        if int(val) < 0 or int(val) > 100:
            return False

    return True

def setAct(act, val):

    if checkActVal(act, val) == False:
        print('\n[xplay][setAct] invalid command: %s %s\n' %(act, val))
        return

    if act == 'stop' and val != '#':
        if os.path.exists(xdef.playlist):
            os.remove(xdef.playlist)

    player = getPlayer()
    print('\n[xplay][setAct]\n\n\t'+ '%s,%s,%s' %(player, act, val))

    if player == 'mpv' and xproc.checkProcessRunning('mpv'):
        return mpv.setAct(act, val)

    if player == 'omxp' and xproc.checkProcessRunning('omxplayer.bin'):
        return omxp.setAct(act, val)

    if player == 'ffplay' and xproc.checkProcessRunning('ffplay'):
        return ffplay.setAct(act, val)

