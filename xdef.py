#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

workdir  = '/var/tmp/'
codedir  = '/opt/vod/'
dldir    = '/var/tmp/'
fifo     = codedir+'vod.fifo'
log      = workdir+'vod_%s.log' %(os.getuid())
ytdlarg  = '--no-warnings'
ytdlm3u  = '.youtubedl.m3u'
ytdlsub  = '--no-warnings --write-sub --skip-download --sub-lang=en,en-US'
#mpv      = 'mpv --fs --ontop --ytdl=no'
mpv      = 'mpv'
omxp     = 'omxplayer -b -o both -I'
ffplay   = 'ffplay -fs -window_title ffplay'
playlist = workdir+'vod_%s_playlist' %(os.getuid())
playbackMode = workdir+'vod_%s_playbackMode' %(os.getuid())

def ytdlcmd():
    if os.path.exists('/usr/bin/python3'):
        for f in ['/usr/local/bin/youtube-dl', os.path.expanduser('~/bin/youtube-dl')]:
            if os.path.exists(f):
                return 'python3 ' + f
    return 'youtube-dl'
