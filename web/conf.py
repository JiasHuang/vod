#!/usr/bin/env python

import os

vodpath = '/opt/vod/'
workdir = '/var/tmp/'

vod         = vodpath+'vod.py'
src         = vodpath+'src.py'
run         = vodpath+'run.py'
act         = vodpath+'act.py'
cmd         = vodpath+'cmd.py'

playbackMode = workdir+'vod_%s_playbackMode' %(os.getuid())
