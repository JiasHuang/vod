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

def runDBG(url, ref):
    if youtubedl.checkURL(url):
        youtubedl.extractURL(url)
    youtubedl.extractSUB(url)
    return

def playURL(url, ref):

    player = getPlayer()

    print('\n[xplay][%s][url]\n\n\t%s' %(player, url))
    print('\n[xplay][%s][ref]\n\n\t%s' %(player, ref))

    if url == None or url == '':
        return

    if player == 'mpv':
        return mpv.play(url, ref)

    if player == 'omxp':
        return omxp.play(url, ref)

    if player == 'ffplay':
        return ffplay.play(url, ref)

    return runDBG(url, ref)

def setAct(act, val):

    player = getPlayer()
    print('\n[xplay]\n\n\t'+ '%s,%s,%s' %(player, act, val))

    if player == 'mpv' and xproc.checkProcessRunning('mpv'):
        return mpv.setAct(act, val)

    if player == 'omxp' and xproc.checkProcessRunning('omxplayer.bin'):
        return omxp.setAct(act, val)

    if player == 'ffplay' and xproc.checkProcessRunning('ffplay'):
        return ffplay.setAct(act, val)

