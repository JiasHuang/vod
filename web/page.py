#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
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

def addEntry(req, link, title, image=None, desc=None, password=None):
    global entryCnt
    entryCnt = entryCnt + 1
    entryEven = None
    if (entryCnt & 1 == 0):
        entryEven = 'entryEven'
    req.write('<!--Entry%s-->\n' %(entryCnt))
    req.write('<!-- link="%s" title="%s" image="%s" desc="%s" -->\n' %(link, title, image or '', desc or ''))
    if re.search('view.py\?v=', link):
        if password:
            password = '&ytdl_password='+password
        anchor = 'href="%s%s" target="playVideo"' %(link, password or '')
    else:
        anchor = 'href="%s"' %(link)
    if image:
        req.write('<div class="imageWrapper">\n')
        req.write('<div class="imageContainer">\n')
        req.write('<a %s><img src="%s" onerror=\'this.onerror=null; this.src="Movies-icon.png"\' /></a>\n' %(anchor, image))
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
    if re.search(r'^//', link):
        link = re.sub('//', 'http://', link)
    addEntry(req, 'view.py?p='+link, title, image, desc)

def addVideo(req, link, title=None, image=None, desc=None, password=None):
    if not link:
        return
    if re.search(r'^//', link):
        link = re.sub('//', 'http://', link)
    addEntry(req, 'view.py?v='+link, title or link, image or meta.getImage(link) or 'Movies-icon.png', desc, password)

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

def addDailyMotion(req, vid, password=None):
    link = 'http://www.dailymotion.com/video/'+vid
    addVideo(req, link, password=password)

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

def addNextPage(req, q, txt, engine='youtube'):
    req.write('<!--NextPage-->\n')
    if engine == 'youtube':
        prefix = 'view.py?q='+q
        for m in re.finditer(r'<a href="/results.*?</a>', txt):
            sp = meta.search(r'sp=([^"&]*)', m.group())
            if sp:
                pageno = meta.search(r'>(\d+)</span>', m.group()) or meta.search(r'(«|»)', m.group())
                if pageno:
                    pageno = re.sub('«','prev', pageno)
                    pageno = re.sub('»','next', pageno)
                    req.write('<div id="div_page_%s" title="%s" value="%s"></div>\n' %(pageno, pageno, prefix+'&x='+sp))
    elif engine == 'google':
        prefix = 'view.py?s=google&q='+q
        navcnt = meta.search(r'<div id="navcnt">(.*?)</div>', txt, re.DOTALL|re.MULTILINE)
        if navcnt:
            for m in re.finditer(r'<a .*?</a>', navcnt):
                link = meta.search(r'href="([^"]*)"', m.group())
                label = meta.search(r'aria-label="Page (\d+)"', m.group()) or meta.search(r'id="pn([^"]*)"', m.group()) or ''
                start = meta.search(r'start=(\d+)', link)
                if start:
                    req.write('<div id="div_page_%s" title="%s" value="%s"></div>\n' %(label, label, prefix+'&x='+start))
    req.write('<!--NextPageEnd-->\n')
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
    addNextPage(req, q, txt)

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
        if title and url:
            addVideo(req, link, title)

def search_google(req, q, start=None):
    url = 'http://www.google.com/search?hl=en&q=site%3Adrive.google.com%20'+q
    if start:
        url = url+'&start='+start
    txt = load(url)
    for m in re.finditer(r'<h3 class="r"><a href="([^"]*)" .*?>(.*?)</a>', txt):
        link, title = m.group(1), m.group(2)
        title = re.sub('- Google Drive', '', title)
        addVideo(req, link, title)
    addNextPage(req, q, txt, engine='google')

def search_db(req, q):
    local = os.path.expanduser('~')+'/.voddatabase'
    for m in re.finditer(r'<!-- link="([^"]*)" title="([^"]*)" image="([^"]*)" -->', meta.readLocal(local)):
        link, title, image = m.group(1), m.group(2), m.group(3)
        if len(image) == 0:
            image = 'Movies-icon.png'
        if re.search(q, title, re.IGNORECASE):
            addEntry(req, link, title, image)

def search_xuite(req, q):
    for i in range(3):
        url = 'http://m.xuite.net/rpc/search?method=vlog&kw='+q+'&offset='+str(i*10+1)
        data = meta.parseJSON(load(url))
        if 'rsp' not in data or 'items' not in data['rsp']:
            return
        for d in data['rsp']['items']:
            try:
                vlog_id = d['vlog_id'].encode('utf8')
                thumb = d['thumb'].encode('utf8')
                title = d['title'].encode('utf8')
                duration = d['duration'].encode('utf8')
                addVideo(req, 'http://vlog.xuite.net/play/'+vlog_id, title, thumb, duration)
            except:
                continue
    return

def search(req, q, s=None, x=None):
    html = re.split('<!--result-->', loadFile('list_search.html'))
    req.write(html[0])

    s = (s or 'youtube').lower()

    q1 = re.sub(' ', '+', q)

    engines = ['YouTube', 'HD', 'Long', 'Playlist']
    enginez = ['Google', 'Bing', 'Yandex', 'Xuite', 'Live', 'CC', 'Latest']

    req.write('<!--SearchEngine-->\n')

    for e in engines:
        req.write('<div id="div_engines_%s" value="%s"></div>\n' %(e, e))

    for e in enginez:
        req.write('<div id="div_enginez_%s" value="%s"></div>\n' %(e, e))

    req.write('<div id="div_search_s" value="%s"></div>\n' %(s))
    req.write('<div id="div_search_q" value="%s"></div>\n' %(q1))

    req.write('<!--SearchEngineEnd-->\n')

    if s == 'youtube':
        search_youtube(req, q1, x)
    elif s == 'hd':
        search_youtube(req, q1, x or 'EgIgAQ%3D%3D')
    elif s == 'long':
        search_youtube(req, q1, x or 'EgIYAg%3D%3D')
    elif s == 'playlist':
        search_youtube(req, q1, x or 'EgIQAw%3D%3D')
    elif s == 'live':
        search_youtube(req, q1, x or 'EgJAAQ%3D%3D')
    elif s == 'cc':
        search_youtube(req, q1, x or 'EgIoAQ%3D%3D')
    elif s == 'latest':
        search_youtube(req, q1, x or 'CAI%3D')
    elif s == 'google':
        search_google(req, q1, x)
    elif s == 'bing':
        search_bing(req, q1)
    elif s == 'yandex':
        search_yandex(req, q1)
    elif s == 'xuite':
        search_xuite(req, q1)

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

    data = meta.parseJSON(load('http://vlog.xuite.net/default/media/widget?title=dir&userSn=%s' %(userSn)))
    if 'content' not in data:
        return

    for d in data['content']:
        t = d['TITLE'].encode('utf8')
        p = d['PARENT_SEQUENCE'].encode('utf8')
        l = 'http://vlog.xuite.net/%s?t=cat&p=%s&dir_num=0' %(user, p)
        addPage(req, l, t)
    return

def page_litv(req, url):
    if re.search(r'/movie/', url):
        for m in re.finditer(r'<div class="movie_poster play_by_content_id" (.*?)>', load(url)):
            contentId = meta.search(r'data-content-id="(.*?)"', m.group())
            title = meta.search(r'title="(.*?)"', m.group())
            image = meta.search(r'background-image:url\((.*?)\)', m.group())
            if contentId and title and image:
                addVideo(req, 'https://www.litv.tv/vod/movie/content.do?id='+contentId, title, image)
        return
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
            data = meta.parseJSON(avlist)
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

def page_youku(req, url):
    global entryCnt
    if re.search(r'/v_show/', url):
        txt = load(url)
        if re.search(r'tvlist', txt):
            pattern = r'name="tvlist"(.*?)</div>'
        else:
            pattern = r'<div class="program(.*?)</div>'
        for m in re.finditer(pattern, txt):
            url = meta.search(r'href="([^"]*)"', m.group())
            title = meta.search(r'title="([^"]*)"', m.group())
            if url and title:
                addVideo(req, url, title)
    else:
        for m in re.finditer(r'<div class="p-thumb">(.*?)</div>', load(url)):
            url = meta.search(r'href="([^"]*)"', m.group())
            title = meta.search(r'title="([^"]*)"', m.group())
            image = meta.search(r'src="([^"]*)"', m.group())
            addPage(req, url, title, image)
    return

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
        txt = load(url)
        password = meta.search(r'密碼：(\w+)', txt)
        for m in re.finditer(r'<div id="video_div(|_s[0-9])">.*?\n</div>', txt, re.DOTALL|re.MULTILINE):
            meta.comment(req, m.group())
            video_ids  = meta.search(r'video_ids.*?>([^<]*)</div>', m.group())
            video_type = meta.search(r'video_type.*?>([^<]*)</div>', m.group())
            if not video_type or not video_ids:
                continue
            for vid in video_ids.split(','):
                if video_type == '1':
                    addYouTube(req, vid)
                elif video_type == '2':
                    addDailyMotion(req, vid, password=password)
                elif video_type == '3':
                    addOpenLoad(req, vid)
                elif video_type == '21':
                    addGoogleDrive(req, vid)

def page_imovie(req, url):
    if url == 'http://i-movie.co/':
        for i in range(1, 5):
            data = meta.parseJSON(meta.post('http://i-movie.co/sql.php?tag=getMovie', {'page':str(i), 'type':'all', 'sort':'time'}))
            if 'json' in data:
                for d in data['json']:
                    vid, title, image  = d['id'].encode('utf8'), d['name'].encode('utf8'), d['image'].encode('utf8')
                    addPage(req, 'http://i-movie.co/view.php?id='+vid, title, image)
    else:
        vid = meta.search(r'view.php\?id=([0-9]*)', url)
        if vid:
            data = meta.parseJSON(meta.post('http://i-movie.co/sql.php?tag=getOneMovie', {'id':vid}))
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
                    addPage(req, 'https://www.youtube.com'+link, title)
    elif re.search(r'/channel/([^/]*)$', url):
        addPage(req, url+'/videos', 'videos')
        playlists = []
        for m in re.finditer(r'href="/playlist\?list=([^"]*)"*?>([^<]*)</a>', load(url+'/playlists')):
            playlist, title = m.group(1), m.group(2)
            if playlist not in playlists:
                playlists.append(playlist)
                addPlayList(req, playlist, title)
    elif re.search(r'playlist\?', url):
        addVideo(req, url, 'PLAY ALL')
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

    elif re.search(r'youku', url):
        page_youku(req, url)

    elif re.search(r'i-movie', url):
        page_imovie(req, url)

    else:
        page_def(req, url)

    req.write('</div>\n')

    onPageEnd(req)
    req.write(html[1])

