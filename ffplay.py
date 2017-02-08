#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess

import xdef
import xproc
import youtubedl

def setAct(act, val):

    pid = xproc.checkProcessRunning('ffplay')
    if not pid:
        print('\n[ffplay][secAct] no pid')
        return

    wid = xproc.checkOutput('xdotool search --name ffplay', r'([0-9]*)$')
    if not wid:
        print('\n[ffplay][secAct] no wid')
        return

    os.system('xdotool windowactivate --sync %s' %(wid))

    if act == 'stop':
        os.system('xdotool key q')
    elif act == 'pause':
        os.system('xdotool key p')
    elif act == 'forward':
        os.system('xdotool key Up')
    elif act == 'backward':
        os.system('xdotool key Down')
    elif act == 'percent' and val:
        geometry = xproc.checkOutput('xdotool getwindowgeometry %s' %(wid), r'Geometry: ([0-9x]*)')
        if not geometry:
            print('\n[ffplay][setAct] no geometry')
            return
        w = int(geometry.split('x')[0])
        h = int(geometry.split('x')[1])
        x = str(w * int(val) / 100)
        y = str(h / 2)
        os.system('xdotool mousemove --sync --window %s %s %s click 1' %(wid, x, y))
    else:
        print('\n[ffplay][setAct] unsupported: %s %s' %(act, val))
    return

def play(url, ref):

    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)

    if not url:
        print('\n[ffplay][play] invalid url')
        return

    if xproc.checkProcessRunning('ffplay'):
        setAct('stop', None)

    cmd = '%s \'%s\'' %(xdef.ffplay, url)
    print('\n[ffplay][cmd]\n\n\t'+cmd+'\n')
    subprocess.Popen(cmd, shell=True).communicate()

    return

