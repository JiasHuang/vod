#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

workdir  = '/tmp/'
codedir  = '/opt/vod/'
dldir    = '/var/tmp/'
fifo     = codedir+'vod.fifo'
log      = workdir+'vod_%s.log' %(os.getuid())
ytdl     = 'youtube-dl --no-warnings'
ytdlm3u  = '.youtubedl.m3u'
ytdlsub  = 'youtube-dl --no-warnings --write-sub --skip-download --sub-lang=en,en-US'
wget     = 'wget -w 10 -T 10 -q -c '
ua       = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
mpv      = 'mpv --fs --ontop'
omxp     = 'omxplayer -b -o both -I'
ffplay   = 'ffplay -fs -window_title ffplay'
playlist = workdir+'vod_%s_playlist' %(os.getuid())
playing  = workdir+'vod_%s_playing' %(os.getuid())
