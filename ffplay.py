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

    wid = xproc.checkOutput('xdotool search ffplay', r'([0-9]*)$')
    if not wid:
        print('\n[ffplay][secAct] no wid')
        return

    if act == 'stop':
        os.system('xdotool key --window %s q' %(wid))
    elif act == 'pause':
        os.system('xdotool key --window %s p'%(wid))
    elif act == 'forward':
        os.system('xdotool key --window %s Up' %(wid))
    elif act == 'backward':
        os.system('xdotool key --window %s Down' %(wid))
    elif act == 'percent' and val:
        w = xproc.checkOutput('xdotool getwindowgeometry '+wid, r'Geometry: ([0-9]*)x')
        if not w:
            print('\n[ffplay][secAct] no width')
            return
        x = str(int(w) * int(val) / 100)
        os.system('xdotool mousemove --window %s %s 1 click --window %s 1' %(wid, x, wid))
    else:
        print('unsupported: %s %s' %(act, val))
    return

def play(url, ref):
    if youtubedl.checkURL(url):
        url = youtubedl.extractURL(url)
    if not url:
        print('\n[ffplay][play] invalid url')
        return 0
    if xproc.checkProcessRunning('ffplay'):
        setAct('stop', None)
    p = subprocess.Popen('%s \'%s\' 2>&1 | tee %s' %(xdef.ffplay, url, xdef.log), shell=True)
    if p:
        p.communicate()
    return

