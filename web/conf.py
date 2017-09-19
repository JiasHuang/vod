#!/usr/bin/env python

import os

vodpath = '/opt/vod/'
workdir = '/tmp/'

vod  = vodpath+'vod.py'
src  = vodpath+'src.py'
run  = vodpath+'run.py'
act  = vodpath+'act.py'
cmd  = vodpath+'cmd.py'
log  = workdir+'view.log'
json = workdir+'view.json'

wget = 'wget -T 10 -q -c '
ua   = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)'

playbackMode = workdir+'vod_%s_playbackMode' %(os.getuid())
