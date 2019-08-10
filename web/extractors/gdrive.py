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

def findGoogleNextPage(url):
    objs = []
    navcnt = re.search(r'<div id="navcnt">(.*?)</div>', load(url), re.DOTALL | re.MULTILINE)
    if navcnt:
        for m in re.finditer(r'<td.*?</td>', navcnt.group(1)):
            label = re.search(r'(\w+)(</span>|)(</a>|)</td>', m.group())
            label = label.group(1) if label else None
            link = re.search(r'href="([^"]*)"', m.group())
            link = urljoin(url, link.group(1)) if link else None
            if label:
                objs.append(navObj(label, link))

    return objs

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
            print('Exception:\n'+drive_ivd_txt)

    return objs

def search_google(q, start=None):
    objs = []
    url = 'http://www.google.com/search?num=50&hl=en&q=site%3Adrive.google.com%20'+q
    if start:
        url = url+'&start='+start
    txt = load(url)
    for m in re.finditer(r'<a href="([^"]*)".*?>(.*?)</a>', txt):
        link, title = m.group(1), m.group(2)
        m2 = re.search(r'<h3.*?>(.*?)</h3>', title)
        if m2:
            title = m2.group(1)
        link = re.sub('preview', 'view', link)
        title = re.sub('- Google Drive', '', title).rstrip()
        q1 = re.sub('\*', '+', q)
        for x in re.split('\+', q1):
            if not re.search(re.escape(x), title, re.IGNORECASE):
                link = title = None
                break
        if link and title and not re.search(r'(pdf|doc)$', title, re.IGNORECASE):
            objs.append(entryObj(link, title, getImage(link)))

    objs.extend(findGoogleNextPage(url))

    return objs
