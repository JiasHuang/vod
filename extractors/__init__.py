#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import glob
import subprocess

import youtubedl

mods = []

files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
for f in files:
    if os.path.isfile(f) and not f.endswith('__.py'):
        name = os.path.basename(f)[:-3]
        __import__('%s.%s' %(__package__, name))
        mod = globals()[name]
        if hasattr(mod, 'VALID_URL') and hasattr(mod, 'getSource'):
            mods.append(mod)

def getRedirectLink(url):
    cmd = 'curl -I \"%s\"' %(url)
    output = subprocess.check_output(cmd, shell=True)
    cookies = []
    cookies_str = None
    for m in re.finditer('Set-Cookie: (.*?)(\n|\r)', output):
        cookies.append(m.group(1))
    if len(cookies) > 0:
        cookies_str = '; '.join(cookies)
    m = re.search('Location: (.*?)\n', output)
    if m:
        return m.group(1), cookies_str
    return url, None

def removeHashTag(url):
    m = re.search('(.*?)#', url)
    if m:
        return m.group(1)
    return url

def getSource(url, ref):
    for m in mods:
        if re.search(m.VALID_URL, url):
            return m.getSource(url), None, None
    src, cookies = youtubedl.extractURL(url, ref=ref)
    ref = url
    if re.search('dailymotion', src):
        src, extra_cookies = getRedirectLink(src)
        src = removeHashTag(src)
        if extra_cookies:
            cookies = extra_cookies

    if not src:
        src = getIframeSrc(url)

    if src:
        return src, cookies, ref

    return None, None, None

def getSub(url):
    return youtubedl.extractSUB(url)

def getIframeSrc(url):
    if url[0:4] != 'http':
        return None
    return search(r'<iframe.*?src="([^"]*)"', xurl.load(url))
