#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess

import xdef
import xproc
import mpv
import omxp
import ffplay
import youtubedl

def getPlayer():

    conf = xdef.getConf('player')
    if conf:
        return conf

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

def playURL(url, ref, cookies=None):

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

    player = getPlayer()
    print('\n[xplay][setAct]\n\n\t'+ '%s,%s,%s' %(player, act, val))

    if player == 'mpv' and xproc.checkProcessRunning('mpv'):
        return mpv.setAct(act, val)

    if player == 'omxp' and xproc.checkProcessRunning('omxplayer.bin'):
        return omxp.setAct(act, val)

    if player == 'ffplay' and xproc.checkProcessRunning('ffplay'):
        return ffplay.setAct(act, val)

