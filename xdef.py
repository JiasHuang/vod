#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass

player   = 'def'
workdir  = '/tmp/'
codedir  = '/opt/vod/'
dldir    = '/var/tmp/'
cookies  = workdir+'vod_%s.cookies' %(getpass.getuser())
fifo     = codedir+'vod.fifo'
log      = workdir+'vod_%s.log' %(getpass.getuser())
ytdl     = 'youtube-dl'
ytdlfmt  = 'best[ext!=webm][protocol^=http]/best[ext!=webm]'
wget     = 'wget -w 10 -T 10 -q -c '
ua       = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)'
mpv      = 'mpv --fs --ontop'
omxp     = 'omxplayer -b -o both -I'
ffplay   = 'ffplay -fs -window_title ffplay'

