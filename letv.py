#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re
import xdef

def getSource(url):
    id = re.search(r'([0-9]*).html', url).group(1)
    m3u = xdef.workdir+'letv_'+id+'.m3u'
    os.system('you-get -y \'http://111.13.109.52:80\' -u -F 720p %s > %s_' %(url, m3u))
    os.system('grep http %s_ > %s' %(m3u, m3u))
    return m3u

