#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import json
import urlparse

import meta

entryCnt = 0
bCluster = -1

def autoCluster_cmd(req, cmd):
    global bCluster
    global entryCnt
    if cmd == 'create':
        bCluster = 0
    elif cmd == 'destroy':
        autoCluster_cmd(req, 'close')
        autoCluster_cmd(req, 'exit')
        bCluster = -1
    elif cmd == 'init':
        if bCluster == 0:
            req.write('<div class="bxslider">')
            bCluster = 1
    elif cmd == 'exit':
        if bCluster > 0:
            req.write('</div>\n')
            bCluster = 0
    elif cmd == 'open':
        if entryCnt == 0:
            req.write('<div class="entryCluster">\n')
            entryCnt = 1
    elif cmd == 'close':
        if entryCnt:
            req.write('</div>\n')
            entryCnt = 0

def autoCluster(req, entryMax=5):
    global bCluster
    global entryCnt
    if bCluster > 0:
        entryCnt = entryCnt + 1
        if entryCnt > entryMax:
            autoCluster_cmd(req, 'close')
            autoCluster_cmd(req, 'open')
    if bCluster == 0:
        autoCluster_cmd(req, 'init')
        autoCluster_cmd(req, 'open')

def loadFile(filename):
    path = os.path.dirname(os.path.abspath(__file__))+'/'+filename
    with open(path, 'r') as fd:
        return fd.read()
    return None

def render(req, filename, result):
    html = loadFile(filename+'.html')
    if result:
        html = re.sub('<!--result-->', result, html)
    req.write(html)

def renderDIR(req, d):
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])
    req.write('<h1>Index of %s</h1>\n' %(d))
    req.write('<div style="line-height:200%;font-size:20">\n')
    for dirName, subdirList, fileList in os.walk(d):
        for subdir in sorted(subdirList):
            if subdir[0] != '.':
                req.write('<li><img src="/icons/folder.gif"> <a href="view.py?d=%s/%s">%s</a>\n' %(dirName, subdir, subdir))
        for fname in sorted(fileList):
            if fname.lower().endswith(('.mkv', '.mp4', '.avi', '.flv', '.rmvb', '.rm', '.f4v', '.wmv', '.m3u', '.m3u8', '.ts')):
                req.write('<li><img src="/icons/movie.gif"> <a href="view.py?f=%s/%s">%s</a>\n' %(dirName, fname, fname))
        break
    req.write('</div>\n')
    req.write(html[1])

def load(url):
    return meta.load(url)

def addEntry(req, link, title, image=None):
    if image:
        req.write('<div class="image-wrapper">\n')
        req.write('<a href="%s">\n' %(link))
        req.write('<img src="%s" />\n' %(image))
        req.write('<h2>%s</h2>\n' %(title))
        req.write('</a>\n')
        req.write('</div>\n')
    else:
        req.write('<a href="%s">\n' %(link))
        req.write('<h2 class="entryTitle">%s</h2>\n' %(title))
        req.write('</a>\n')

def addPage(req, link, title, image=None):
    addEntry(req, 'view.py?p='+link, title, image)

def addVideo(req, link, title=None, image=None):
    if not link:
        return
    if re.search(r'^//', link):
        link = re.sub('//', 'http://', link)
    autoCluster(req)
    addEntry(req, 'view.py?v='+link, title or link, image or meta.getImage(link) or 'Movies-icon.png')

def addYouTube(req, vid, title=None):
    link = 'https://www.youtube.com/watch?v='+vid
    addVideo(req, link, title)

def addPlayList(req, playlist, title, video=None):
    link = 'https://www.youtube.com/playlist?list='+playlist
    image = None
    if video:
        image = 'http://img.youtube.com/vi/'+video+'/0.jpg'
    addPage(req, link, title, image)

def addDailyMotion(req, vid, title=None):
    link = 'http://www.dailymotion.com/video/'+vid
    addVideo(req, link, title)

def addOpenLoad(req, vid, title=None):
    link = 'https://openload.co/embed/'+vid
    addVideo(req, link, title)

def addGoogleDrive(req, vid, title=None):
    link = 'https://drive.google.com/file/d/'+vid
    addVideo(req, link, title)

def search_youtube(req, q):
    url = 'https://www.youtube.com/results?sp=CAISAiAB&q='+q
    for m in re.finditer(r'<a href="/watch\?v=(.{11})".*?>([^<]*)</a>', load(url)):
        addYouTube(req, m.group(1), m.group(2))

def search_playlist(req, q):
    url = 'https://www.youtube.com/results?sp=EgIQAw%3D%3D&q='+q
    playlist = None
    for m in re.finditer(r'href="/watch\?v=(.{11})&amp;list=([^"]*)".*?>([^<]*)</a>', load(url)):
        if playlist != m.group(2):
            video, playlist, title = m.group(1), m.group(2), m.group(3)
            addPlayList(req, playlist, title, video)

def search_bing(req, q):
    url = 'https://www.bing.com/search?count=30&q=site:drive.google.com+(mp4+OR+mkv+OR+avi+OR+flv)+'+q
    txt = re.sub('(<strong>|</strong>)', '', load(url))
    for m in re.finditer(r'<h2><a href="([^"]*)".*?>(.*?)</a></h2>', txt):
        link, title = m.group(1), m.group(2)
        vid = meta.search(r'drive.google.com/file/d/(\w*)', link)
        if vid:
            addGoogleDrive(req, vid, title)

def search_yandex(req, q):
    url = 'https://yandex.com/video/search?text=site%3Adrive.google.com%20'+q
    txt = load(url)
    for m in re.finditer(r'data-video="([^"]*)"', txt):
        unquote = re.sub('&quot;', '\"', m.group(1))
        meta.comment(req, unquote)
        title = meta.search(r'"title":"([^"]*)"', unquote)
        link  = meta.search(r'"url":"([^"]*)"', unquote)
        image = meta.search(r'"thumbUrl":"([^"]*)"', unquote)
        if title and url:
            addVideo(req, link, title, image)

def search_db(req, q):
    local = os.path.expanduser('~')+'/.voddatabase'
    for m in re.finditer(r'<a href="([^"]*)">(.*?)</a>', meta.readLocal(local), re.DOTALL|re.MULTILINE):
        link = m.group(1)
        title = meta.search(r'<h2>(.*?)</h2>', m.group(2))
        image = meta.search(r'src="([^"]*)"', m.group(2)) or 'Movies-icon.png'
        if re.search(q, title, re.IGNORECASE):
            addEntry(req, link, title, image)

def search(req, q, s):
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    s = s or 'youtube'

    q1 = re.sub(' ', '+', q)

    req.write('<img onload="loadImage()" onclick="startDictation()" src="mic-icon.png" id="ximage" class="topright" />\n')

    req.write('<h1>\n')
    req.write('<a href=view.py>Home</a>&nbsp;&nbsp;&nbsp;\n')
    req.write('<a href=view.py?s=youtube&q='+q1+'>YouTube</a>&nbsp;&nbsp;&nbsp;\n')
    req.write('<a href=view.py?s=playlist&q='+q1+'>PlayList</a>&nbsp;&nbsp;&nbsp;\n')
    req.write('</h1>\n')

    req.write('<br>\n')

    req.write('<form action="view.py" method="get" id="xform">\n')
    req.write('<input type="hidden" name="s" value="%s" class="input"\>\n' %(s))
    req.write('<input type="text" name="q" value="%s" class="input" id="xinput"\>\n' %(q))
    req.write('</form>\n')

    req.write('<br>\n')

    search_db(req, q1)

    if s == 'youtube':
        search_youtube(req, q1)
    elif s == 'playlist':
        search_playlist(req, q1)
    elif s == 'bing':
        search_bing(req, q1)
    elif s == 'yandex':
        search_yandex(req, q1)

    req.write(html[1])

def page_def(req, url):
    meta.findLink(req, url)

def page_xuite(req, url):
    if re.search(r'xuite.net/([a-zA-Z0-9]*)($)', url):
        page_xuiteDIR(req, url)
    else:
        meta.findVideo(req, url)

def page_xuiteDIR(req, url):

    m = re.search(r'xuite.net/([a-z0-9A-Z]*)($)', url)
    if not m:
        return

    user = m.group(1)

    m = re.search(r'userSn=([0-9]*)', load(url))
    if not m:
        return

    userSn = m.group(1)

    data = json.loads(load('http://vlog.xuite.net/default/media/widget?title=dir&userSn=%s' %(userSn)))
    if 'content' not in data:
        return

    for d in data['content']:
        t = d['TITLE'].encode('utf8')
        p = d['PARENT_SEQUENCE'].encode('utf8')
        l = 'http://vlog.xuite.net/%s?t=cat&p=%s&dir_num=0' %(user, p)
        addPage(req, l, t)
    return

def page_litv(req, url):
    m = re.search(r'(\?|&)id=([a-zA-Z0-9]*)', url)
    if m:
        _contentId = m.group(2)
        _url = 'https://www.litv.tv/vod/ajax/getProgramInfo?contentId='+_contentId
        headers = [('Accept', 'application/json, text/javascript, */*; q=0.01')]
        programInfo = meta.load(_url, None, headers)
        for m in re.finditer(r'{"contentId":"([^"]*)",.*?}', programInfo, re.DOTALL):
            contentId = m.group(1)
            imageLink = None
            subtitle = re.search(r'"subtitle":"([^"]*)"', m.group())
            imageFile = re.search(r'"imageFile":"([^"]*)"', m.group())
            if imageFile:
                imageLink = imageFile.group(1)
            if subtitle:
                addVideo(req, re.sub(_contentId, contentId, url), subtitle.group(1), imageLink)
    else:
        meta.findVideoLink(req, url, True, True, 'data-img')

def page_lovetv(req, url):
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    if re.search(r'special-drama-list.html$', url):
        for m in re.finditer(r'<a href="([^"]*)">([^<]*)</a>', load(url)):
            meta.comment(req, m.group())
            if re.search(r'special-drama-([0-9-]+).html$', m.group(1)):
                addPage(req, meta.absURL(domain, m.group(1)), m.group(2))
    elif re.search(r'drama-list.html$', url):
        for m in re.finditer(r'<a href="([^"]*)">([^<]*)</a>', load(url)):
            meta.comment(req, m.group())
            if re.search(r'-list.html$', m.group(1)):
                addPage(req, meta.absURL(domain, m.group(1)), m.group(2))
    elif re.search(r'-list.html$', url):
        for m in re.finditer(r'<a href="([^"]*)">([^<]*)</a>', load(url)):
            meta.comment(req, m.group())
            if re.search(r'-ep([0-9]+).html$', m.group(1)):
                addPage(req, meta.absURL(domain, m.group(1)), m.group(2))
    else:
        for m in re.finditer(r'<div id="video_div(|_s[0-9])">.*?\n</div>', load(url), re.DOTALL|re.MULTILINE):
            meta.comment(req, m.group())
            video_ids  = meta.search(r'video_ids.*?>([^<]*)</div>', m.group())
            video_type = meta.search(r'video_type.*?>([^<]*)</div>', m.group())
            if not video_type or not video_ids:
                continue
            for vid in video_ids.split(','):
                if video_type == '1':
                    addYouTube(req, vid)
                elif video_type == '2':
                    addDailyMotion(req, vid)
                elif video_type == '3':
                    addOpenLoad(req, vid)
                elif video_type == '21':
                    addGoogleDrive(req, vid)

def page_imovie(req, url):
    if url == 'http://i-movie.co/':
        for i in range(1, 5):
            data = json.loads(meta.post('http://i-movie.co/sql.php?tag=getMovie', {'page':str(i), 'type':'all', 'sort':'time'}))
            if 'json' in data:
                for d in data['json']:
                    vid, title, image  = d['id'].encode('utf8'), d['name'].encode('utf8'), d['image'].encode('utf8')
                    addPage(req, 'http://i-movie.co/view.php?id='+vid, title, image)
    else:
        vid = meta.search(r'view.php\?id=([0-9]*)', url)
        if vid:
            data = json.loads(meta.post('http://i-movie.co/sql.php?tag=getOneMovie', {'id':vid}))
            for d in data:
                url = d['url'].encode('utf8')
                src = meta.search(r'src="([^"]*)"', url) or url
                addVideo(req, src)

def page_youtube(req, url):
    if re.search(r'/playlists($)', url):
        playlist = None
        for m in re.finditer(r'href="/playlist\?list=([^"]*)"*?>([^<]*)</a>', load(url)):
            if playlist != m.group(1):
                playlist, title = m.group(1), m.group(2)
                addPlayList(req, playlist, title)
    elif re.search(r'/channels($)', url):
        for m in re.finditer(r'class="yt-uix-sessionlink yt-uix-tile-link ([^>]*)', load(url)):
                link = meta.search(r'href="([^"]*)"', m.group())
                title = meta.search(r'title="([^"]*)"', m.group())
                if link and title:
                    addPage(req, 'https://www.youtube.com'+link, title)
    elif re.search(r'playlist\?', url):
        for m in re.finditer(r'pl-video yt-uix-tile ([^>]*)', load(url)):
            vid = re.search(r'data-video-id="([^"]*)"', m.group())
            title = re.search(r'data-title="([^"]*)"', m.group())
            if vid and title:
                addYouTube(req, vid.group(1), title.group(1))
    else:
        for m in re.finditer(r'watch\?v=(.{11})">([^<]*)</a>', load(url)):
            vid = m.group(1)
            addYouTube(req, m.group(1), m.group(2))

def page(req, url):

    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    autoCluster_cmd(req, 'create')

    if re.search(r'litv', url):
        page_litv(req, url);

    elif re.search(r'lovetv', url):
        page_lovetv(req, url);

    elif re.search(r'youtube', url):
        page_youtube(req, url)

    elif re.search(r'xuite', url):
        page_xuite(req, url)

    elif re.search(r'i-movie', url):
        page_imovie(req, url)

    elif re.search('(porn|jav)',url):
        meta.findImageLink(req, url, True, False)

    else:
        page_def(req, url)

    autoCluster_cmd(req, 'destroy')

    req.write(html[1])

