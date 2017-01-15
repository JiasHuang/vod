#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass

player   = 'def'
workdir  = '/tmp/'
codedir  = '/opt/vod/'
dldir    = '/var/tmp/'
cookies  = workdir+'vod_%s.cookies' %(getpass.getuser())
json     = workdir+'vod_%s.json' %(getpass.getuser())
ytdl     = 'youtube-dl'
fifo     = '/opt/vod/vod.fifo'
fifo_bs  = '/opt/vod/vod.bs.fifo'
sub      = 'on'
log      = workdir+'vod.log'

wget     = 'wget -w 10 -T 10 -q -c '
ua       = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)'
smp      = 'smplayer -fullscreen'
mpv      = 'mpv --fs --ontop --cache=16384 --cache-secs=10'
mpv_ytdl = '--ytdl=no --cookies --cookies-file=%s' %(cookies)
mpv_rpi  = 'mpv --vo=rpi --fs --ontop --cookies --cookies-file=%s' %(cookies)
omxp     = 'omxplayer -b -o both -I'
