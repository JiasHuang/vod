#!/usr/bin/env python

import os

vodpath = '/opt/vod/'
workdir = '/tmp/'

vod         = vodpath+'vod.py'
src         = vodpath+'src.py'
run         = vodpath+'run.py'
act         = vodpath+'act.py'
cmd         = vodpath+'cmd.py'
log         = workdir+'view.log'
json        = workdir+'view.json'
cookie      = workdir+'view.cookie'
log_wget    = workdir+'view.wget.log'

ua          = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)'

wget_base   = 'wget -T 10 -c -S '
wget_base   = wget_base + '--header=\'Accept-Language:zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7\' '
wget_base   = wget_base + '--save-cookies %s --load-cookies %s ' %(cookie, cookie)
wget_base   = wget_base + '-o %s ' %(log_wget)
wget        = wget_base + '-U \'%s\' ' %(ua)
wget_noUA   = wget_base

playbackMode = workdir+'vod_%s_playbackMode' %(os.getuid())
