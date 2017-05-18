#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import hashlib
import json
import time
import base64
import timeit

from optparse import OptionParser

import xdef
import xurl

def checkURL(url):
    site = xurl.findSite(url)
    return re.compile('(youtube|dailymotion|facebook|bilibili|vimeo|youku|openload|litv|drive|iqiyi|letv)').search(site)

def redirectURL(url):
    if re.search(r'youku', url):
        url = re.sub('player.youku.com/embed/', 'v.youku.com/v_show/id_', url)
    return url

def parseParameters(url):
    match = re.search(r'(.*?)&ytdl_password=(.*?)$', url)
    if match:
        url = match.group(1)
        return '--video-password ' + match.group(2)
    return None

def getFmt(url):
    return xdef.ytdlfmt

def genM3U(url, result):
    local = xdef.workdir+'vod_list_'+hashlib.md5(url).hexdigest()+'.m3u'
    fd = open(local, 'w')
    fd.write('#EXTM3U\n')
    for r in result:
        fd.write('#EXTINF:-1,0\n')
        fd.write(r+'\n')
    fd.close()
    return local

def parseJson(path):

    print('\n[ytdl][parseJson]\n')

    results = []
    cookies = None

    fd = open(path, "r")
    lines = fd.readlines()
    fd.close()

    for line in lines:

        try:
            data = json.loads(line)
            urls = data['url']
        except:
            print('\texception')
            continue

        try:
            cookies = data['http_headers']['Cookie'].encode('utf8')
        except:
            cookies = None

        if not isinstance(urls, basestring):
            results.append(urls)
        else:
            encoded = re.search(r'data:application/vnd.apple.mpegurl;base64,([a-zA-Z0-9+/=]*)', urls)
            if encoded:
                local = xdef.workdir+'vod_list_'+hashlib.md5(path).hexdigest()+'.m3u'
                decoded = base64.b64decode(encoded.group(1))
                xurl.saveLocal(local, decoded)
                results.append(local)
            else:
                results.append(urls)

    if cookies:
        print('\thdr : %s' %(cookies))

    if len(results) == 0:
        print('\tNo results')
        return None, None
    elif len(results) == 1:
        print('\tret : %s' %(results[0]))
        return results[0], cookies
    else:
        m3u = genM3U(path, results)
        print('\tret : %s' %(m3u))
        return m3u, cookies

def extractPlayList(local, url):
    txt = xurl.load2(url)
    links = []
    descs = []

    for m in re.finditer(r'<tr (.*?)</tr>', txt, re.DOTALL|re.MULTILINE):
        video = re.search(r'data-video-id="([^"]*)"', m.group())
        title = re.search(r'data-title="([^"]*)"', m.group())
        if video and title:
            links.append('https://www.youtube.com/watch?v='+video.group(1))
            descs.append(title.group(1))

    for index,link in enumerate(links):
        src, cookies = extractURL(link)
        desc = descs[index]
        if src:
            if not os.path.exists(local):
                fd = open(local, 'w')
                fd.write('#EXTM3U\n')
                fd.write('#EXTINF:-1,%s\n' %(desc))
                fd.write(src+'\n')
                fd.close()
            else:
                fd = open(local, 'a')
                fd.write('#EXTINF:-1,%s\n' %(desc))
                fd.write(src+'\n')
                fd.close()

    if not os.path.exists(local):
        fd = open(local, 'w')
        fd.write('#EXTM3U\n')
        fd.close()

    return

def createSubprocess(url):
    local = xdef.workdir+'vod_list_'+hashlib.md5(url).hexdigest()+'.m3u'
    cmd = 'python %s -p %s -l %s' %(os.path.realpath(__file__), url, local)
    p = subprocess.Popen(cmd, shell=True)
    while not os.path.exists(local):
        time.sleep(1)
    print('\n[ytdl][createSubprocess]\n')
    print('\tret : %s' %(local))
    return local, None

def extractURL(url):

    if re.search(r'youtube.com/playlist\?list=', url):
        return createSubprocess(url)

    print('\n[ytdl][extractURL]\n')

    url = redirectURL(url)
    arg = parseParameters(url)
    fmt = getFmt(url)
    local = xdef.workdir+'vod_list_'+hashlib.md5(url+fmt).hexdigest()+'.json'

    if arg:
        print('\targ : %s' %(arg or ''))

    if fmt:
        print('\tfmt : %s' %(fmt or ''))

    if os.path.exists(local) and not xurl.checkExpire(local):
        print('\tret : %s' %(local))
        return parseJson(local)

    cmd = '%s -f \"%s\" -i -j --no-playlist %s \'%s\' > %s' %(xdef.ytdl, fmt, arg or '', url, local)

    try:
        start_time = timeit.default_timer()
        output = subprocess.check_output(cmd, shell=True)
        elapsed = timeit.default_timer() - start_time
    except:
        elapsed = timeit.default_timer() - start_time
        print('\texception')

    print('\tsec : %s' %(str(elapsed)))
    print('\tret : %s' %(local))

    return parseJson(local)

def extractSUB(url):

    if not url or not re.search(r'youtube.com/watch\?v=', url):
        return None

    print('\n[ytdl][extracSUB]\n')

    sub = 'vod_sub_'+hashlib.md5(url).hexdigest()

    for files in os.listdir(xdef.workdir):
        if files.startswith(sub):
            print('\tsub: '+xdef.workdir+files)
            return files

    try:
        cmd = '%s --sub-lang=en,en-US,en-GB,en-AU,en-CA --write-sub --write-auto-sub --skip-download -o %s%s \'%s\'' %(xdef.ytdl, xdef.workdir, sub, url)
        start_time = timeit.default_timer()
        output = subprocess.check_output(cmd, shell=True)
        elapsed = timeit.default_timer() - start_time
        print('\tsec: '+str(elapsed))
    except:
        print('\texception')
        return None

    m = re.search(r'Writing video subtitles to: (.*)', output)
    if m:
        local = m.group(1)
        print('\tsub: '+local)
        return local

    return None


def main():
    parser = OptionParser()
    parser.add_option("-p", "--playlist", dest="playlist")
    parser.add_option("-l", "--local", dest="local")
    (options, args) = parser.parse_args()
    if options.local and options.playlist:
        extractPlayList(options.local, options.playlist)
    return

if __name__ == '__main__':
    main()
