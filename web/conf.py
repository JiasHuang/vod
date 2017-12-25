#!/usr/bin/env python

import os

vodpath = '/opt/vod/'
workdir = '/var/tmp/'

vod         = vodpath+'vod.py'
src         = vodpath+'src.py'
run         = vodpath+'run.py'
act         = vodpath+'act.py'
cmd         = vodpath+'cmd.py'
log         = workdir+'vod_view.log'
json        = workdir+'vod_view.json'

playbackMode = workdir+'vod_%s_playbackMode' %(os.getuid())
