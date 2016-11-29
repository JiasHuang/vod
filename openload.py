#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import xurl

# https://openload.co/embed/M0_oxCn3xAU/NBA.2015.11.19.Warriors.vs.Clippers.720p.NBAHD.com_%281%29-001.mkv.mp4

def getSource(url):
    media_id = re.search(r'https://openload.co/embed/([0-9a-zA-Z-_]*)', url).group(1)
    print('media_id: %s' %(media_id))
    ticket_url = 'https://api.openload.io/1/file/dlticket?file=%s' % (media_id)
    print('ticket: %s' %(ticket_url))
    result = xurl.load(ticket_url)
    js_result = json.loads(result)
    if js_result['status'] != 200:
        print('ticket_url fail')
        return ''

    video_url = 'https://api.openload.io/1/file/dl?file=%s&ticket=%s' % (media_id, js_result['result']['ticket'])
    print('video: %s' %(video_url))
    return video_url

def search(txt):
    m = re.search(r'https://openload.co/embed/([0-9a-zA-Z-_]*)', txt)
    if m:
        return m.group()
    return

