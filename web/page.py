#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import json
import urlparse

import meta

entryCnt = 0

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

def addEntry(req, link, title, image=None, option=None):
    global entryCnt
    entryCnt = entryCnt + 1
    entryEven = None
    if (entryCnt & 1 == 0):
        entryEven = 'entryEven'
    req.write('<!--Entry%s-->\n' %(entryCnt))
    req.write('<!-- link="%s" title="%s" image="%s" -->\n' %(link, title, image or ''))
    if image:
        req.write('<div class="imageWrapper">\n')
        req.write('<div class="imageContainer"><a href="%s" %s><img src="%s" /></a></div>\n' %(link, option or '', image))
        req.write('<h2><a href="%s" %s>%s</a></h2>\n' %(link, option or '', title))
        req.write('</div>\n')
    else:
        req.write('<h2 class="entryTitle %s"><a href="%s" %s>%s</a></h2>\n' %(entryEven or '', link, option or '', title))

def addPage(req, link, title, image=None):
    addEntry(req, 'view.py?p='+link, title, image)

def addVideo(req, link, title=None, image=None):
    if not link:
        return
    if re.search(r'^//', link):
        link = re.sub('//', 'http://', link)
    addEntry(req, 'view.py?v='+link, title or link, image or meta.getImage(link) or 'Movies-icon.png', 'target="playVideo"')

def addYouTube(req, vid, title=None):
    link = 'https://www.youtube.com/watch?v='+vid
    addVideo(req, link, title)

def addPlayList(req, playlist, title, vid=None):
    link = 'https://www.youtube.com/playlist?list='+playlist
    image = None
    if vid:
        link = 'https://www.youtube.com/watch?v=%s&list=%s' %(vid, playlist)
        image = 'http://img.youtube.com/vi/'+vid+'/0.jpg'
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

def search_youtube(req, q, args=None):
    url = 'https://www.youtube.com/results?q=%s%s' %(q, args or '')
    for m in re.finditer(r'href="/watch\?v=(.{11})([^"]*)".*?>([^<]*)</a>', load(url)):
        vid, args, title = m.group(1), m.group(2), m.group(3)
        playlist = meta.search(r'list=([^"]*)', args)
        if playlist:
            addPlayList(req, playlist, 'Playlist/'+title, vid)
        else:
            desc_id = meta.search(r'description-id-([^"]*)', m.group())
            if desc_id:
                desc = meta.search(r'description-id-'+re.escape(desc_id)+'">([^<]*)</span>', load(url))
                title += desc or ''
            addYouTube(req, vid, title)

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
    for m in re.finditer(r'<!-- link="([^"]*)" title="([^"]*)" image="([^"]*)" -->', meta.readLocal(local)):
        link, title, image = m.group(1), m.group(2), m.group(3)
        if len(image) == 0:
            image = 'Movies-icon.png'
        if re.search(q, title, re.IGNORECASE):
            addEntry(req, link, title, image)

def search(req, q, s):
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    s = s or 'youtube'

    q1 = re.sub(' ', '+', q)

    req.write('<img onload="loadImage()" onclick="startDictation()" src="mic-icon.png" id="ximage" class="topright" />\n')

    engines = ['YouTube', 'HD', 'Long', 'Subtitle', 'Playlist']

    req.write('<table><tr>\n')
    for x in engines:
        css = 'center'
        if x.lower() == s:
            css += ' highlight'
        req.write('<td class="%s"><a href=view.py?s=%s&q=%s>%s</a></td>\n' %(css, x.lower(), q1, x))
    req.write('</tr></table>\n')

    req.write('<form class="form" action="view.py" method="get" id="xform">\n')
    req.write('<input type="hidden" name="s" value="%s" class="input"\>\n' %(s))
    req.write('<input type="text" name="q" value="%s" class="input" id="xinput"\>\n' %(q))
    req.write('</form>\n')

    if s == 'youtube':
        search_youtube(req, q1)
    elif s == 'hd':
        search_youtube(req, q1, '&sp=EgIgAQ%3D%3D')
    elif s == 'long':
        search_youtube(req, q1, '&sp=EgIYAg%3D%3D')
    elif s == 'subtitle':
        search_youtube(req, q1, '&sp=EgIoAQ%3D%3D')
    elif s == 'playlist':
        search_youtube(req, q1, '&sp=EgIQAw%3D%3D')
    elif s == 'bing':
        search_bing(req, q1)
    elif s == 'yandex':
        search_yandex(req, q1)

    onPageEnd(req)
    req.write(html[1])

def page_def(req, url):
    global entryCnt
    meta.findLink(req, url)
    if entryCnt == 0:
        meta.findImageLink(req, url, True, False)

def page_xuite(req, url):
    if re.search(r'xuite.net/([a-zA-Z0-9]*)($)', url):
        page_xuiteDIR(req, url)
    else:
        meta.findVideo(req, url)
        next_page_links = meta.search(r'<!-- Numbered page links -->(.*?)<!-- Next page link -->', load(url), re.DOTALL|re.MULTILINE)
        if next_page_links:
            parsed_uri = urlparse.urlparse(url)
            domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            for m in re.finditer('href="([^"]*)">', next_page_links):
                meta.findVideo(req, meta.absURL(domain, m.group(1)))

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

def page_iqiyi(req, url):
    meta.findImageLink(req, url, True, False)

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
                    addPage(req, 'https://www.youtube.com'+link+'/playlists', title+'/playlists')
                    addPage(req, 'https://www.youtube.com'+link+'/videos', title+'/videos')
    elif re.search(r'playlist\?', url):
        for m in re.finditer(r'pl-video yt-uix-tile ([^>]*)', load(url)):
            vid = meta.search(r'data-video-id="([^"]*)"', m.group())
            title = meta.search(r'data-title="([^"]*)"', m.group())
            if vid and title:
                addYouTube(req, vid, title)
    elif re.search(r'list=', url):
        for m in re.finditer(r'<li ([^>]*)>', load(url)):
            vid = meta.search(r'data-video-id="([^"]*)"', m.group())
            title = meta.search(r'data-video-title="([^"]*)"', m.group())
            if vid and title:
                addYouTube(req, vid, title)
    else:
        for m in re.finditer(r'watch\?v=(.{11})">([^<]*)</a>', load(url)):
            vid = m.group(1)
            addYouTube(req, m.group(1), m.group(2))

def onPageEnd(req):
    global entryCnt
    if entryCnt == 0:
        req.write('<h2>Oops! Not Found</h2>')
    req.write('<!--EntryEnd-->')

def page(req, url):

    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    req.write('<div class="bxslider">\n')

    if re.search(r'litv', url):
        page_litv(req, url);

    elif re.search(r'iqiyi', url):
        page_iqiyi(req, url)

    elif re.search(r'lovetv', url):
        page_lovetv(req, url);

    elif re.search(r'youtube', url):
        page_youtube(req, url)

    elif re.search(r'xuite', url):
        page_xuite(req, url)

    elif re.search(r'i-movie', url):
        page_imovie(req, url)

    else:
        page_def(req, url)

    req.write('</div>\n')

    onPageEnd(req)
    req.write(html[1])

