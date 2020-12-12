#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json

import xurl

VALID_URL = r'bilibili\.com'

def getSource(url, fmt, ref):
    txt = xurl.load(url)
    video = []
    audio = []
    video_ids = ['64', '32', '16']
    audio_ids = ['30280', '30216']
    video_id = None
    audio_id = None
    for m in re.finditer(r'"id":(\d+),"baseUrl":"([^"]*)"', txt):
        _id, _url = m.group(1), m.group(2)
        if _id in video_ids:
            if not video_id:
                video_id = _id
            if _id == video_id:
                video.append(_url)
        if _id in audio_ids:
            if not audio_id:
                audio_id = _id
            if _id == audio_id:
                audio.append(_url)

    local_a = xurl.genLocal(url, prefix='vod_list_', suffix='.audio.m3u8')
    local_v = xurl.genLocal(url, prefix='vod_list_', suffix='.video.m3u8')
    local = xurl.genLocal(url, prefix='vod_list_', suffix='.m3u8')

    xurl.saveM3U8(local_a, audio)
    xurl.saveM3U8(local_v, video)

    s = []
    s.append('#EXTM3U')
    s.append('#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",LANGUAGE="eng",URI="%s"' %(local_a))
    s.append('#EXT-X-STREAM-INF:AUDIO="audio"')
    s.append(local_v)
    xurl.saveLocal(local, '\n'.join(s))

    return local

