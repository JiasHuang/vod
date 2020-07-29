#!/usr/bin/env python
# coding: utf-8

import re

from .utils import *

VALID_URL = r'drive\.google\.com'

def getImage(url):
    m = re.search(r'http(s|)://drive.google.com/file/d/(\w*)', url)
    if m:
        #return search(r'<meta property="og:image" content="([^"]*)">', load(m.group()))
        return 'https://drive.google.com/thumbnail?authuser=0&sz=w320&id='+m.group(2)
    return None

def extract(url):
    objs = []
    txt = load(url)
    drive_ivd = re.search(r'window\[\'_DRIVE_ivd\'\] = \'(.*?)\'', txt, re.DOTALL | re.MULTILINE)
    if drive_ivd:
        drive_ivd_txt = drive_ivd.group(1).decode('string_escape')
        drive_ivd_txt = re.sub('null', 'None', drive_ivd_txt)
        try:
            for d in eval(drive_ivd_txt):
                if not isinstance(d, list):
                    continue
                for item in d:
                    if len(item) < 4:
                        continue
                    vid, parent, title, mimeType = item[0], item[1], item[2], item[3]
                    if not isinstance(mimeType, str):
                        continue
                    if mimeType.startswith('video'):
                        addVideo(req, getLink('googledrive', vid), title)
                        objs.append(entryObj(link, title))
                    if mimeType.endswith('folder'):
                        link = 'https://drive.google.com/drive/folders/'+vid
                        objs.append(pageObj(link, title, 'folder-video-icon.png'))
        except:
            log('Exception:\n'+drive_ivd_txt)

    return objs

def search_gdrive(q, start=None):
    objs = []
    url = 'http://www.google.com/search?num=250&hl=en&q=site%3Adrive.google.com%20'+q
    if start:
        url = url+'&start='+start
    txt = load(url)
    for m in re.finditer(r'<a href="(https://drive.google.com/[^"]*)".*?>(.*?)</a>', txt):
        link, desc = m.group(1), m.group(2)
        m2 = re.search(r'<h3.*?>(.*?)</h3>', desc)
        title = m2.group(1).rstrip('- Google Drive') if m2 else None
        link = re.sub('preview', 'view', link)
        if link and title:
            objs.append(entryObj(link, title, getImage(link)))

    return objs
