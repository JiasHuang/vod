#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
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
mpv      = 'mpv --fs --ontop'
omxp     = 'omxplayer -b -o both -I'
ffplay   = 'ffplay -fs'

def getConf(key):
    conf = os.path.expanduser('~')+'/.vodconf'
    if os.path.exists(conf):
        fd = open(conf, 'r')
        txt = fd.read()
        fd.close()
        m = re.search(re.escape(key)+r'\s*:\s*([^\n]*)', txt)
        if m:
            return m.group(1)
    return None
