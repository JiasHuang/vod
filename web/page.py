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

def addEntry(req, link, title, image=None, desc=None):
    global entryCnt
    entryCnt = entryCnt + 1
    entryEven = None
    if (entryCnt & 1 == 0):
        entryEven = 'entryEven'
    req.write('<!--Entry%s-->\n' %(entryCnt))
    req.write('<!-- link="%s" title="%s" image="%s" desc="%s" -->\n' %(link, title, image or '', desc or ''))
    if re.search('view.py\?v=', link):
        anchor = 'href="%s" target="playVideo"' %(link)
    else:
        anchor = 'href="%s"' %(link)
    if image:
        req.write('<div class="imageWrapper">\n')
        req.write('<div class="imageContainer">\n')
        req.write('<a %s><img src="%s" /></a>\n' %(anchor, image))
        if desc:
            req.write('<p>%s</p>\n' %(desc))
        req.write('</div>\n')
        req.write('<h2><a %s>%s</a></h2>\n' %(anchor, title))
        req.write('</div>\n')
    else:
        req.write('<h2 class="entryTitle %s"><a %s>%s</a></h2>\n' %(entryEven or '', anchor, title))

def addPage(req, link, title, image=None, desc=None):
    if not link:
        return
    addEntry(req, 'view.py?p='+link, title, image, desc)

def addVideo(req, link, title=None, image=None, desc=None):
    if not link:
        return
    if re.search(r'^//', link):
        link = re.sub('//', 'http://', link)
    addEntry(req, 'view.py?v='+link, title or link, image or meta.getImage(link) or 'Movies-icon.png', desc)

def addYouTube(req, vid, title=None, desc=None):
    link = 'https://www.youtube.com/watch?v='+vid
    addVideo(req, link, title, None, desc)

def addPlayList(req, playlist, title, vid=None, desc=None):
    link = 'https://www.youtube.com/playlist?list='+playlist
    image = None
    if vid:
        image = 'http://img.youtube.com/vi/'+vid+'/0.jpg'
        if not desc:
            # Some playlist URLs don't actually serve a playlist
            link = 'https://www.youtube.com/watch?v=%s&list=%s' %(vid, playlist)
            desc = 'Playlist'
    addPage(req, link, title, image, desc)

def addDailyMotion(req, vid, title=None):
    link = 'http://www.dailymotion.com/video/'+vid
    addVideo(req, link, title)

def addOpenLoad(req, vid, title=None):
    link = 'https://openload.co/embed/'+vid
    addVideo(req, link, title)

def addGoogleDrive(req, vid, title=None):
    link = 'https://drive.google.com/file/d/'+vid
    addVideo(req, link, title)

def getDuration(desc):
    return meta.search(r'(\d[^<。]*)', desc)

def getDescription(attributes, txt):
    desc_id = meta.search(r'description-id-([^"]*)', attributes)
    if desc_id:
        desc = meta.search(r'description-id-'+re.escape(desc_id)+'">([^<]*)</span>', txt)
        return getDuration(desc) or desc
    return None

def addNextPages(req, q, txt):
    prefix = 'view.py?q='+q
    req.write('<table class="pages"><tr>\n')
    for m in re.finditer(r'<a href="/results.*?</a>', txt):
        sp = meta.search(r'sp=([^"&]*)', m.group())
        if not sp:
            continue
        pageno = meta.search(r'>(\d+)</span>', m.group())
        if pageno:
            req.write('<td class="pageno"><a href="%s">%s</a></td>\n' %(prefix+'&x='+sp, pageno))
            continue
        if re.search(r'«', m.group()):
            req.write('<td class="pageno"><a href="%s">«Prev</a></td>\n' %(prefix+'&x='+sp))
            continue
        if re.search(r'»', m.group()):
            req.write('<td class="pageno"><a href="%s">Next»</a></td>\n' %(prefix+'&x='+sp))
            continue
    req.write('</tr></table>\n')
    return

def search_youtube(req, q, sp=None):
    url = 'https://www.youtube.com/results?q='+q
    if sp:
        url = url+'&sp='+sp
    txt = load(url)
    playlists = []
    for m in re.finditer(r'href="/watch\?v=(.{11})([^"]*)".*?>([^<]*)</a>', txt):
        vid, args, title = m.group(1), m.group(2), m.group(3)
        playlist = meta.search(r'list=([^"]*)', args)
        if playlist:
            if playlist not in playlists:
                playlists.append(playlist)
                desc = meta.search(r'<a href="/playlist\?list='+re.escape(playlist)+'" .*?\((.*?)\)</a>', txt)
                addPlayList(req, playlist, title, vid, desc)
        else:
            addYouTube(req, vid, title, getDescription(m.group(), txt))
    addNextPages(req, q, txt)

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

def search(req, q, s=None, x=None):
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    s = s or 'youtube'

    q1 = re.sub(' ', '+', q)

    req.write('<img onload="loadImage()" onclick="startDictation()" src="mic-icon.png" id="ximage" class="topright" />\n')

    engines = ['YouTube', 'HD', 'Long', 'Playlist']

    req.write('<div class="searchbar">\n')
    req.write('<table><tr>\n')
    for engin in engines:
        css = 'center'
        if engin.lower() == s:
            css += ' highlight'
        req.write('<td class="%s"><a href=view.py?s=%s&q=%s>%s</a></td>\n' %(css, engin.lower(), q1, engin))
    req.write('</tr></table>\n')

    req.write('<form class="form" action="view.py" method="get" id="xform">\n')
    req.write('<input type="hidden" name="s" value="%s" class="input"\>\n' %(s))
    req.write('<input type="text" name="q" value="%s" class="input" id="xinput"\>\n' %(q))
    req.write('</form>\n')
    req.write('</div>\n')

    req.write('<div class="space"></div>\n')

    if s == 'youtube':
        search_youtube(req, q1, x)
    elif s == 'hd':
        search_youtube(req, q1, x or 'EgIgAQ%3D%3D')
    elif s == 'long':
        search_youtube(req, q1, x or 'EgIYAg%3D%3D')
    elif s == 'playlist':
        search_youtube(req, q1, x or 'EgIQAw%3D%3D')
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

    user = meta.search(r'xuite.net/([a-z0-9A-Z]*)($)', url)
    if not user:
        return

    userSn = meta.search(r'userSn=([0-9]*)', load(url))
    if not userSn:
        return

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
            subtitle = meta.search(r'"subtitle":"([^"]*)"', m.group())
            imageFile = meta.search(r'"imageFile":"([^"]*)"', m.group())
            if subtitle:
                addVideo(req, re.sub(_contentId, contentId, url), subtitle, imageFile)
    else:
        meta.findVideoLink(req, url, True, True, 'data-img')

def page_iqiyi(req, url):
    if re.search(r'list.', url):
        pages = []
        pages.append(url)
        parsed_uri = urlparse.urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        for m in re.finditer(r'<a data-key.*? href="([^"]*)"', load(url), re.DOTALL):
            page = meta.absURL(domain, m.group(1))
            if page not in pages:
                pages.append(page)
        for page in pages[0:5]:
            objs = meta.findImageLink(None, page, True)
            for obj in objs:
                basename = os.path.basename(obj.url)
                if re.search(r'^a_', basename):
                    addPage(req, obj.url, obj.title, obj.image)
                elif re.search(r'^v_', basename):
                    addVideo(req, obj.url, obj.title, obj.image)
    else:
        albumId = meta.search(r'albumId:\s*(\d+)', load(url))
        if albumId:
            avlist = load('http://cache.video.qiyi.com/jp/avlist/%s/' %(albumId))
            avlist = re.sub('var tvInfoJs=', '', avlist)
            data = json.loads(avlist)
            if 'data' in data:
                if 'vlist' in data['data']:
                    for d in data['data']['vlist']:
                        if 'vurl' in d and 'vn' in d and 'vpic' in d:
                            addVideo(req, d['vurl'].encode('utf8'), d['vn'].encode('utf8'), d['vpic'].encode('utf8'))

def page_letv(req, url):
    pages = []
    pages.append(url)
    if re.search(r'list.', url):
        nextpage = re.search(r'<div class="next-page">.*?</div>', load(url), re.DOTALL|re.MULTILINE)
        if nextpage:
            for m in re.finditer(r'href="([^"]*)"', nextpage.group()):
                if m.group(1) not in pages:
                    pages.append(m.group(1))
    for page in pages[0:5]:
        objs = meta.findImageLink(None, page, True)
        for obj in objs:
            if re.search(r'/tv/', obj.url):
                addPage(req, obj.url, obj.title, obj.image)
            elif re.search(r'/vplay/', obj.url):
                addVideo(req, obj.url, obj.title, obj.image)

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
    txt = load(url)
    if re.search(r'/playlists$', url):
        playlists = []
        for m in re.finditer(r'href="/playlist\?list=([^"]*)"*?>([^<]*)</a>', txt):
            playlist, title = m.group(1), m.group(2)
            if playlist not in playlists:
                playlists.append(playlist)
                addPlayList(req, playlist, title)
    elif re.search(r'/channels$', url):
        for m in re.finditer(r'class="yt-uix-sessionlink yt-uix-tile-link ([^>]*)', txt):
                link = meta.search(r'href="([^"]*)"', m.group())
                title = meta.search(r'title="([^"]*)"', m.group())
                if link and title:
                    addPage(req, 'https://www.youtube.com'+link+'/playlists', title+'/playlists')
                    addPage(req, 'https://www.youtube.com'+link+'/videos', title+'/videos')
    elif re.search(r'playlist\?', url):
        for m in re.finditer(r'<tr (.*?)</tr>', txt, re.DOTALL|re.MULTILINE):
            vid = meta.search(r'data-video-id="([^"]*)"', m.group())
            title = meta.search(r'data-title="([^"]*)"', m.group())
            if vid and title:
                desc = meta.search(r'<span aria-label=".*?">(.*?)</span>', m.group())
                addYouTube(req, vid, title, getDuration(desc) or desc)
    elif re.search(r'list=', url):
        for m in re.finditer(r'<li ([^>]*)>', txt):
            vid = meta.search(r'data-video-id="([^"]*)"', m.group())
            title = meta.search(r'data-video-title="([^"]*)"', m.group())
            if vid and title:
                addYouTube(req, vid, title)
    else:
        for m in re.finditer(r'<a (.*?)</a>', txt, re.DOTALL|re.MULTILINE):
            vid = meta.search(r'href="/watch\?v=(.{11})', m.group())
            title = meta.search(r'title="([^"]*)"', m.group())
            if vid and title:
                desc = getDescription(m.group(), txt)
                addYouTube(req, vid, title, desc)

def onPageEnd(req):
    global entryCnt
    if entryCnt == 0:
        req.write('<h2>Oops! Not Found</h2>\n')
    req.write('<!--EntryEnd-->\n')

def page(req, url):

    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    req.write('<div class="bxslider">\n')

    if re.search(r'litv', url):
        page_litv(req, url);

    elif re.search(r'iqiyi', url):
        page_iqiyi(req, url)

    elif re.search(r'(le.com|letv)', url):
        page_letv(req, url)

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

