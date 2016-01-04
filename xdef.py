#!/usr/bin/env python
# -*- coding: utf-8 -*-

player   = 'mpv'
workdir  = '/tmp/'
cookies  = workdir+'vod.cookies'
json     = workdir+'vod.json'
ytdl     = '/usr/local/bin/youtube-dl'
fifo     = '/opt/vod/vod.fifo'
fifo_bs  = '/opt/vod/vod.bs.fifo'

wget     = 'wget -w 10 -T 10 -q -c '
ua       = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'
smp      = 'smplayer -fullscreen'
mpv      = 'mpv --fs --ontop --hwdec=vdpau --cache=16384 --cache-secs=10'
mpv_ytdl = '--ytdl=no --cookies --cookies-file=%s' %(cookies)
