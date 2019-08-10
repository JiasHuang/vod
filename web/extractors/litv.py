#!/usr/bin/env python
# coding: utf-8

import re
import json

from .utils import *

VALID_URL = r'litv'

def extract(url):
    objs = []
    m = re.search(r'(\?|&)content_id=([a-zA-Z0-9]*)', url)
    if m:
        contentId = m.group(2)
        dataURL = 'https://www.litv.tv/vod/ajax/getProgramInfo?contentId='+contentId
        data = load(dataURL)
        seriesId = re.search(r'"seriesId":"(.*?)"', load(dataURL))
        if seriesId:
            dataURL = 'https://www.litv.tv/vod/ajax/getSeriesTree?seriesId='+seriesId.group(1)
            data = load(dataURL)
        for m in re.finditer(r'{"contentId":"([^"]*)",.*?}', data, re.DOTALL):
            link = url.replace(contentId, m.group(1))
            title = re.search(r'"subtitle":"([^"]*)"', m.group()) or re.search(r'"episode":"([^"]*)"', m.group())
            title = title[1] if title else None
            image = re.search(r'"videoImage":"([^"]*)"', m.group())
            image = image[1] if image else None
            objs.append(entryObj(link, title, image, None))
    else:
        progs = re.search(r'var programs = (.*?});', load(url))
        if progs:
            data = json.loads(progs.group(1))
            try:
                for vod in data['vodList']:
                    contentId, title, image = darg(vod, 'contentId', 'title', 'imageFile')
                    link = 'https://www.litv.tv/vod/drama/content.do?content_id='+contentId
                    objs.append(entryObj(link, title, image, None, False))
            except:
                print('Exception:\n'+str(data))
    return objs


