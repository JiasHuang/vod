#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

workdir  = '/var/tmp/'
codedir  = '/opt/vod/'
dldir    = '/var/tmp/'
fifo     = codedir+'vod.fifo'
log      = workdir+'vod_%s.log' %(os.getuid())
mpv      = 'mpv --fs --ontop --ytdl=no --demuxer-lavf-o=protocol_whitelist=\\"file,http,https,tcp,tls,crypto\\" --input-file=%s --save-position-on-quit' %(fifo)
omxp     = 'omxplayer -b -o both -I -s'
ffplay   = 'ffplay -fs -window_title ffplay'
playlist = workdir+'vod_%s_playlist' %(os.getuid())
playbackMode = workdir+'vod_%s_playbackMode' %(os.getuid())
playing  = workdir+'vod_%s_playing' %(os.getuid())

