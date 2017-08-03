#!/usr/bin/env python

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
ua   = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
