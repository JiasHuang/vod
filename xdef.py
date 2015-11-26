#!/usr/bin/env python
# -*- coding: utf-8 -*-

player   = 'none'
workdir  = '/home/jias_huang/temp/'
cookies  = workdir+'__cookies__'
json     = workdir+'__json__'
ytdl     = '/home/jias_huang/opensource/youtube-dl/youtube-dl'

wget     = 'wget -w 10 -T 10 -q -c '
ua       = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'
smp      = 'smplayer -fullscreen'
mpv      = 'mpv --fs --ontop --hwdec=vdpau --cache=16384 --cache-secs=10'
mpv_fifo = '/home/revo/.config/mpv/fifo'
mpv_ytdl = '--ytdl=no --cookies --cookies-file=%s' %(cookies)
