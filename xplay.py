#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import hashlib

import xdef
import xproc
import xurl
import mpv
import omxp
import ffplay
import youtubedl

def getPlayer():

    if xdef.player != 'def':
        return xdef.player

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

def getNext():

    if xdef.autonext != 'yes':
        return None

    player = getPlayer()
    if player == 'mpv' and xproc.checkProcessRunning('mpv'):
        return None
    if player == 'omxp' and xproc.checkProcessRunning('omxplayer.bin'):
        return None
    if player == 'ffplay' and xproc.checkProcessRunning('ffplay'):
        return None

    playing  = xurl.readLocal(xdef.playing)
    playlist = xurl.readLocal(xdef.playlist)

    if xdef.listhash != hashlib.md5(playlist).hexdigest():
        return None

    lines = playlist.splitlines()

    try:
        index = lines.index(playing)
        if index < (len(lines) - 1):
            return lines[index+1]
    except:
        return None

    return None

def playURL_core(url, ref, cookies=None):

    player = getPlayer()

    xurl.saveLocal(xdef.playing, url)

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

    if xdef.autonext == 'yes' and xdef.pagelist:
        txt = xurl.readLocal(xdef.pagelist)
        xurl.saveLocal(xdef.playlist, txt)
        xdef.listhash = hashlib.md5(txt).hexdigest()
    else:
        if os.path.exists(xdef.playlist):
            os.remove(xdef.playlist)

    while url != None:
        playURL_core(url, ref, cookies)
        url = ref = getNext()

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

