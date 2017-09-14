#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import urlparse

import meta

entryCnt = 0
entryVideos = []

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
                req.write('<li><img src="/icons/folder.gif"> <a href="view.py?d=%s/%s">%s</a>\n' \
                    %(dirName, subdir, subdir))
        for fname in sorted(fileList):
            suffix = ('.mkv', '.mp4', '.avi', '.flv', '.rmvb', '.rm', '.f4v', '.wmv', '.m3u', '.m3u8', '.ts')
            if fname.lower().endswith(suffix):
                req.write('<li><img src="/icons/movie.gif"> <a href="view.py?f=%s/%s">%s</a>\n' \
                    %(dirName, fname, fname))
        break
    req.write('</div>\n')
    req.write(html[1])

def load(url):
    return meta.load2(url)

# FIXME
def loadYouTube(url):
    txt = load(url)
    if not re.search(r'ytInitialData', txt):
        txt = meta.load2(url, cache=False)
    return txt

def darg(d, *arg):
    if len(arg) == 1:
        return d[arg[0]].encode('utf8')
    return [d[a].encode('utf8') for a in arg]

def addEntry(req, link, title, image=None, desc=None, password=None):
    global entryCnt, entryVideos
    entryCnt = entryCnt + 1
    entryEven = None
    if (entryCnt & 1 == 0):
        entryEven = 'entryEven'
    req.write('<!--Entry%s-->\n' %(entryCnt))
    req.write('<!-- link="%s" title="%s" image="%s" desc="%s" -->\n' %(link, title, image or '', desc or ''))
    if re.search('view.py\?v=', link):
        if password:
            password = '&ytdl_password='+password
        source = '%s%s' %(link, password or '')
        anchor = 'href="%s" target="playVideo"' %(source)
        entryVideos.append(source[10:])
    else:
        anchor = 'href="%s" onclick="onPageClick.call(this);" title="%s"' %(link, title)
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

def getLink(site, vid):
    if site == 'youtube':
        return 'https://www.youtube.com/watch?v='+vid
    if site == 'dailymotion':
        return 'http://www.dailymotion.com/video/'+vid
    if site == 'openload':
        return 'https://openload.co/embed/'+vid
    if site == 'googledrive':
        return 'https://drive.google.com/file/d/'+vid
    return None

def getTitle(site, index, cnt):
    title = site.title()
    if cnt > 1:
        title += ' Part %d/%d' %(index, cnt)
    return title

def getDuration(desc):
    return meta.search(r'(\d[^<。]*)', desc)

def getDescription(attributes, txt):
    desc_id = meta.search(r'description-id-([^"]*)', attributes)
    if desc_id:
        desc = meta.search(r'description-id-'+re.escape(desc_id)+'">([^<]*)</span>', txt)
        return getDuration(desc) or desc
    return None

def addGoogleNextPage(req, q, txt):
    req.write('<!--NextPage-->\n')
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
    txt = loadYouTube(url)
    ytInitialData = meta.search(r'window\["ytInitialData"\] = (.*?});', txt)
    if ytInitialData:
        data = meta.parseJSON(ytInitialData)
        for x in meta.findItem(data, ['videoRenderer', 'playlistRenderer']):
            try:
                if 'videoId' in x:
                    vid = x['videoId'].encode('utf8')
                    title = x['title']['simpleText'].encode('utf8')
                    desc = x['lengthText']['simpleText'].encode('utf8')
                    addVideo(req, getLink('youtube', vid), title, desc=desc)
                elif 'playlistId' in x:
                    playlistId = x['playlistId'].encode('utf8')
                    title = x['title']['simpleText'].encode('utf8')
                    image = x['thumbnails'][0]['thumbnails'][0]['url'].encode('utf8')
                    addPage(req, 'https://www.youtube.com/playlist?list='+playlistId, title, image, 'Playlist')
            except:
                meta.comment(req, str(x))

def search_google(req, q, start=None):
    url = 'http://www.google.com/search?num=30&hl=en&q=site%3Adrive.google.com%20video%20'+q
    if start:
        url = url+'&start='+start
    txt = load(url)
    for m in re.finditer(r'<h3 class="r"><a href="([^"]*)" .*?>(.*?)</a>', txt):
        link, title = m.group(1), m.group(2)
        link = re.sub('preview', 'view', link)
        title = re.sub('- Google Drive', '', title)
        q1 = re.sub('\*', '+', q)
        for x in re.split('\+', q1):
            if not re.search(re.escape(x), title, re.IGNORECASE):
                link = title = None
                break
        if link and title:
            addVideo(req, link, title)
    addGoogleNextPage(req, q, txt)

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
                prefix = 'http://vlog.xuite.net/play/'
                vid, title, image, desc = darg(d, 'vlog_id', 'title', 'thumb', 'duration')
                addVideo(req, prefix+vid, title, image, desc)
            except:
                continue
    return

def search_dailymotion(req, q):
    url = 'https://api.dailymotion.com/videos/?search="'+q+'"&limit=100'
    data = meta.parseJSON(load(url))
    if 'list' not in data:
        return
    for d in data['list']:
        try:
            prefix = 'http://www.dailymotion.com/video/'
            vid, title = darg(d, 'id', 'title')
            addVideo(req, prefix+vid, title)
        except:
            continue
    return

def search(req, q, s=None, x=None):
    html = re.split('<!--result-->', loadFile('list_search.html'))
    req.write(html[0])

    s = (s or 'youtube').lower()

    q1 = re.sub(' ', '+', q)

    engines = ['YouTube', 'Long', 'Playlist', 'Google', 'Xuite', 'DailyMotion']

    req.write('<!--SearchEngine-->\n')

    for e in engines:
        req.write('<div id="div_engine_%s" value="%s"></div>\n' %(e, e))

    req.write('<div id="div_search_s" value="%s"></div>\n' %(s))
    req.write('<div id="div_search_q" value="%s"></div>\n' %(q1))

    req.write('<!--SearchEngineEnd-->\n')

    if s == 'youtube':
        search_youtube(req, q1, x)
    elif s == 'long':
        search_youtube(req, q1, x or 'EgIYAlAU')
    elif s == 'playlist':
        search_youtube(req, q1, x or 'EgIQA1AU')
    elif s == 'google':
        search_google(req, q1, x)
    elif s == 'xuite':
        search_xuite(req, q1)
    elif s == 'dailymotion':
        search_dailymotion(req, q1)

    onPageEnd(req)
    req.write(html[1])

def page_def(req, url):
    meta.findLink(req, url)
    meta.findImageLink(req, url, True, False)

def page_xuite(req, url):
    if re.search(r'xuite.net/([a-zA-Z0-9]*)($)', url):
        page_xuiteDIR(req, url)
    else:
        meta.findVideo(req, url)
        next_page_links = meta.search(r'<!-- Numbered page links -->(.*?)<!-- Next page link -->', \
            load(url), re.DOTALL|re.MULTILINE)
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

    json = 'http://vlog.xuite.net/default/media/widget?title=dir&userSn='+userSn
    data = meta.parseJSON(load(json))
    if 'content' not in data:
        return

    if (len(data['content']) <= 3):
        json = 'http://vlog.xuite.net/default/media/widget?title=media&type=latest&userSn='+userSn
        data = meta.parseJSON(load(json))
        if 'content' not in data:
            return
        for d in data['content']:
            title, vid, image = darg(d, 'TITLE', 'FILE_NAME', 'THUMBNAIL')
            link = 'http://vlog.xuite.net/play/'+vid
            addVideo(req, link, title, image)
        return

    for d in data['content']:
        title, parent = darg(d, 'TITLE', 'PARENT_SEQUENCE')
        link = 'http://vlog.xuite.net/%s?t=cat&p=%s&dir_num=0' %(user, parent)
        addPage(req, link, title)

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
        dataURL = 'https://www.litv.tv/vod/ajax/getProgramInfo?contentId='+_contentId
        data = load(dataURL)
        seriesId = meta.search(r'"seriesId":"(.*?)"', load(dataURL))
        if seriesId:
            dataURL = 'https://www.litv.tv/vod/ajax/getSeriesTree?seriesId='+seriesId
            data = load(dataURL)
        meta.comment(req, dataURL)
        meta.comment(req, data)
        for m in re.finditer(r'{"contentId":"([^"]*)",.*?}', data, re.DOTALL):
            contentId = m.group(1)
            subtitle = meta.search(r'"subtitle":"([^"]*)"', m.group()) or meta.search(r'"episode":"([^"]*)"', m.group())
            imageFile = meta.search(r'"videoImage":"([^"]*)"', m.group())
            addVideo(req, re.sub(_contentId, contentId, url), subtitle, imageFile)
    else:
        meta.findVideoLink(req, url, True, True, ImagePattern=r'\"([^ ]*jpg)\"')

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
            meta.comment(req, avlist)
            data = meta.parseJSON(avlist)
            if 'data' in data and 'vlist' in data['data'] and len(data['data']['vlist']) > 0:
                for d in data['data']['vlist']:
                    if 'vurl' in d and 'vn' in d and 'vpic' in d:
                        link, title, image = darg(d, 'vurl', 'vn', 'vpic')
                        addVideo(req, link, title, image)
            else:
                meta.findImageLink(req, url, True, False)

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
    elif re.search(r'(drama-list.html|/)$', url):
        for m in re.finditer(r'<a href=[\'|"]([^\'"]*)[\'|"]>([^<]*)</a>', load(url)):
            meta.comment(req, m.group())
            if re.search(r'-list', m.group(1)):
                addPage(req, meta.absURL(domain, m.group(1)), m.group(2))
    elif re.search(r'-list', url):
        for m in re.finditer(r'<a href="([^"]*)">([^<]*)</a>', load(url)):
            meta.comment(req, m.group())
            if re.search(r'-ep([0-9]+).html$', m.group(1)):
                addPage(req, meta.absURL(domain, m.group(1)), m.group(2))
    else:
        video_types = {'1':'youtube', '2':'dailymotion', '3':'openload', '21':'googledrive'}
        txt = load(url)
        password = meta.search(r'密碼：(\w+)', txt)
        for m in re.finditer(r'<div id="video_div(|_s[0-9])">.*?</div>\n*</div>', txt, re.DOTALL|re.MULTILINE):
            meta.comment(req, m.group())
            video_ids  = meta.search(r'video_ids.*?>([^<]*)</div>', m.group())
            video_type = meta.search(r'video_type.*?>([^<]*)</div>', m.group())
            if not video_type or not video_ids or video_type not in video_types:
                continue
            videos = video_ids.split(',')
            vcnt = len(videos)
            for videoIndex, video in enumerate(videos, 1):
                site = video_types[video_type]
                title = getTitle(site, videoIndex, vcnt)
                addVideo(req, getLink(site, video), title, password=password)

def page_maplestage(req, url):
    if re.search(r'/drama/', url):
        pageProps = meta.search(r'var pageProps = (.*?});', load(url))
        if pageProps:
            data = meta.parseJSON(pageProps)
            meta.comment(req, str(data))
            prefix = ['熱門戲劇 : ', '最新戲劇 : ', '']
            for index, category in enumerate(['hotShows', 'latestShows', 'shows']):
                try:
                    for show in data[category]:
                        meta.comment(req, str(show))
                        slug, cover = darg(show, 'slug', 'cover')
                        link = 'http://maplestage.com/show/' + slug
                        addPage(req, link, prefix[index]+slug)
                except:
                    meta.comment(req, 'Exception: '+category)
    elif re.search(r'/show/', url):
        pageData = meta.search(r'var pageData = (.*?});', load(url));
        if pageData:
            data = meta.parseJSON(pageData)
            meta.comment(req, str(data))
            try:
                for ep in data['props'][0]['value']['episodes']:
                    meta.comment(req, str(ep))
                    shortId, slug, thumb, numStr = darg(ep, 'shortId', 'slug', 'thumb', 'numStr')
                    link = 'http://maplestage.com/episode/'+shortId+'/'+numStr # FIXME
                    addPage(req, link, slug+'('+numStr+')', thumb)
            except:
                meta.comment(req, 'Exception')
    elif re.search(r'/episode/', url):
        pageData = meta.search(r'var pageData = (.*?});', load(url));
        if pageData:
            data =  meta.parseJSON(pageData)
            meta.comment(req, str(data))
            for prop in data['props']:
                if 'value' in prop and 'videoSources' in prop['value']:
                    try:
                        for videoSrc in prop['value']['videoSources']:
                            meta.comment(req, str(videoSrc))
                            vcnt = len(videoSrc['videos'])
                            for videoIndex, video in enumerate(videoSrc['videos'], 1):
                                vtype, vid = darg(video, 'type', 'id')
                                if vtype in ['youtube', 'dailymotion']:
                                    title = getTitle(vtype, videoIndex, vcnt)
                                    addVideo(req, getLink(vtype, vid), title)
                    except:
                        meta.comment(req, 'Exception')

def page_youtube_videos(req, url):
    txt = loadYouTube(url)
    ytInitialData = meta.search(r'window\["ytInitialData"\] = (.*?});', txt)
    if ytInitialData:
        data = meta.parseJSON(ytInitialData)
        for x in meta.findItem(data, ['gridVideoRenderer']):
            try:
                vid = x['videoId'].encode('utf8')
                title = x['title']['simpleText'].encode('utf8')
                desc = None
                for timeStatus in meta.findItem(x, ['thumbnailOverlayTimeStatusRenderer']):
                    desc = timeStatus['text']['simpleText'].encode('utf8')
                addVideo(req, getLink('youtube', vid), title, desc)
            except:
                meta.comment(req, 'Exception:\n'+str(x))

def page_youtube_channels(req, url):
    txt = loadYouTube(url)
    ytInitialData = meta.search(r'window\["ytInitialData"\] = (.*?});', txt)
    if ytInitialData:
        data = meta.parseJSON(ytInitialData)
        for x in meta.findItem(data, ['gridChannelRenderer']):
            try:
                channelId = x['channelId'].encode('utf8')
                title = x['title']['simpleText'].encode('utf8')
                image = x['thumbnail']['thumbnails'][0]['url'].encode('utf8')
                addPage(req, 'https://www.youtube.com/channel/'+channelId, title, image, 'Channel')
            except:
                meta.comment(req, 'Exception:\n'+str(x))

def page_youtube_playlists(req, url):
    txt = loadYouTube(url)
    ytInitialData = meta.search(r'window\["ytInitialData"\] = (.*?});', txt)
    if ytInitialData:
        data = meta.parseJSON(ytInitialData)
        for x in meta.findItem(data, ['gridPlaylistRenderer']):
            try:
                playlistId = x['playlistId'].encode('utf8')
                title = x['title']['simpleText'].encode('utf8')
                image = x['thumbnail']['thumbnails'][0]['url'].encode('utf8')
                addPage(req, 'https://www.youtube.com/playlist?list='+playlistId, title, image, 'Playlist')
            except:
                meta.comment(req, 'Exception:\n'+str(x))

def page_youtube_playlistVideo(req, url):
    txt = loadYouTube(url)
    ytInitialData = meta.search(r'window\["ytInitialData"\] = (.*?});', txt)
    if ytInitialData:
        data = meta.parseJSON(ytInitialData)
        for x in meta.findItem(data, ['playlistVideoRenderer']):
            try:
                videoId = x['videoId'].encode('utf8')
                title = x['title']['simpleText'].encode('utf8')
                desc = None
                for timeStatus in meta.findItem(x, ['thumbnailOverlayTimeStatusRenderer']):
                    desc = timeStatus['text']['simpleText'].encode('utf8')
                addVideo(req, getLink('youtube', videoId), title, desc=desc)
            except:
                meta.comment(req, 'Exception:\n'+str(x))

def page_youtube_channel(req, url):
    txt = loadYouTube(url+'/videos')
    ytInitialData = meta.search(r'window\["ytInitialData"\] = (.*?});', txt)
    if ytInitialData:
        data = meta.parseJSON(ytInitialData)
        for x in meta.findItem(data, ['gridVideoRenderer']):
            try:
                vid = x['videoId'].encode('utf8')
                title = x['title']['simpleText'].encode('utf8')
                image = x['thumbnail']['thumbnails'][0]['url'].encode('utf8')
                addPage(req, url+'/videos', 'VIDEOS', image, 'Videos')
                break
            except:
                meta.comment(req, 'Exception:\n'+str(x))
    page_youtube_playlists(req, url+'/playlists')

def page_youtube(req, url):
    if re.search(r'/playlists$', url):
        page_youtube_playlists(req, url)
    elif re.search(r'/channels$', url):
        page_youtube_channels(req, url)
    elif re.search(r'/channel/([^/]*)$', url):
        page_youtube_channel(req, url)
    elif re.search(r'list=', url):
        page_youtube_playlistVideo(req, url)
    else:
        page_youtube_videos(req, url)

def page_dailymotion(req, url):
    meta.findImageLink(req, url, True, False)

def page_gdrive(req, url):
    txt = load(url)
    drive_ivd = re.search(r'window\[\'_DRIVE_ivd\'\] = \'(.*?)\'', txt, re.DOTALL|re.MULTILINE)
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
                    if mimeType.endswith('folder'):
                        addPage(req, 'https://drive.google.com/drive/folders/'+vid, title, 'folder-video-icon.png')
        except:
            meta.comment(req, 'exception in page_gdrive')
            return

def savePageList():
    global entryVideos
    local = '/tmp/vod_list_pagelist_%s' %(str(os.getpid() % 100))
    fd = open(local, 'w')
    for v in entryVideos:
        fd.write(v+'\n')
    fd.close()
    return local

def onPageEnd(req):
    global entryCnt
    if entryCnt == 0:
        req.write('<h1><span class="message" id="NotFound"></span></h1>\n')
    req.write('<!--EntryEnd-->\n')
    req.write('<div id="pageinfo" pagelist="%s"></div>' %(savePageList()))
    meta.showDebugLog(req)

def page(req, url):

    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    req.write('<div class="bxslider">\n')

    if re.search(r'litv', url):
        page_litv(req, url);

    elif re.search(r'iqiyi', url):
        page_iqiyi(req, url)

    elif re.search(r'(\.le.com|letv)', url):
        page_letv(req, url)

    elif re.search(r'lovetv', url):
        page_lovetv(req, url);

    elif re.search(r'maplestage', url):
        page_maplestage(req, url);

    elif re.search(r'youtube', url):
        page_youtube(req, url)

    elif re.search(r'dailymotion', url):
        page_dailymotion(req, url)

    elif re.search(r'xuite', url):
        page_xuite(req, url)

    elif re.search(r'youku', url):
        page_youku(req, url)

    elif re.search(r'drive\.google\.com', url):
        page_gdrive(req, url)

    else:
        page_def(req, url)

    req.write('</div>\n')

    onPageEnd(req)
    req.write(html[1])

