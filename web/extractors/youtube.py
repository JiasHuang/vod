#!/usr/bin/env python
# coding: utf-8

import re
import json

import xurl
from utils import *

VALID_URL = r'youtube'

def loadYouTube(url):
    txt = xurl.curl(url)
    if not re.search(r'ytInitialData', txt):
        txt = xurl.curl(url, cache=False)
    return txt

def parseYoutubeInitialDataJSON(url):
    txt = loadYouTube(url)
    m = re.search(r'ytInitialData\W*= (.*?});', txt)
    if m:
        try:
            return json.loads(m.group(1))
        except:
            log('Exception:\n'+m.group(1))
    return None

def findYouTubeNextPage(url, q):
    objs = []
    headers = [('cookie', 'PREF=f1=50000000&f6=1408&f5=30&hl=en')]
    local = xurl.genLocal(url, suffix='.old')
    txt = xurl.load(url, local, headers)
    pages = re.search(r'search-pager(.*?)</div>', txt, re.DOTALL|re.MULTILINE)
    if pages:
        for m in re.finditer(r'<(a|button) .*?</(a|button)>', pages.group(1)):
            label = re.search(r'<span.*?">(.*?)</span>', m.group())
            label = label.group(1) if label else None
            link = None
            if m.group(1) == 'a':
                href = re.search(r'href="([^"]*)"', m.group())
                link = urljoin(url, href.group(1)) if href else None
            objs.append(navObj(label, link))

    return objs

def extract_youtube_videos(url):
    data = parseYoutubeInitialDataJSON(url)
    objs = []
    if data:
        for x in findItem(data, ['gridVideoRenderer']):
            try:
                videoId = x['videoId'].encode('utf8')
                link = 'https://www.youtube.com/watch?v='+videoId
                title = x['title']['runs'][0]['text'].encode('utf8')
                image = x['thumbnail']['thumbnails'][0]['url'].encode('utf8')
                desc = None
                for timeStatus in findItem(x, ['thumbnailOverlayTimeStatusRenderer']):
                    if 'simpleText' in timeStatus['text']:
                        desc = timeStatus['text']['simpleText'].encode('utf8')
                objs.append(entryObj(link, title, image, desc))
            except:
                log('Exception:\n'+str(x))

    return objs

def extract_youtube_channels(url):
    data = parseYoutubeInitialDataJSON(url)
    objs = []
    if data:
        for x in findItem(data, ['gridChannelRenderer']):
            try:
                channelId = x['channelId'].encode('utf8')
                link = 'https://www.youtube.com/channel/'+channelId
                title = x['title']['simpleText'].encode('utf8')
                image = x['thumbnail']['thumbnails'][0]['url'].encode('utf8')
                objs.append(entryObj(link, title, image, 'Channel', False))
            except:
                log('Exception:\n'+str(x))

    return objs

def extract_youtube_playlists(url):
    data = parseYoutubeInitialDataJSON(url)
    objs = []
    if data:
        for x in findItem(data, ['gridPlaylistRenderer']):
            try:
                playlistId = x['playlistId'].encode('utf8')
                link = 'https://www.youtube.com/playlist?list='+playlistId
                title = x['title']['runs'][0]['text'].encode('utf8')
                image = x['thumbnail']['thumbnails'][0]['url'].encode('utf8')
                objs.append(entryObj(link, title, image, 'Playlist', False))
            except:
                log('Exception:\n'+str(x))

    return objs

def extract_youtube_playlistVideo(url):
    data = parseYoutubeInitialDataJSON(url)
    objs = []
    if data:
        for x in findItem(data, ['playlistVideoRenderer']):
            try:
                videoId = x['videoId'].encode('utf8')
                link = 'https://www.youtube.com/watch?v='+videoId
                title = x['title']['runs'][0]['text'].encode('utf8')
                image = 'http://img.youtube.com/vi/%s/0.jpg' %(videoId)
                desc = None
                for timeStatus in findItem(x, ['thumbnailOverlayTimeStatusRenderer']):
                    if 'simpleText' in timeStatus['text']:
                        desc = timeStatus['text']['simpleText'].encode('utf8')
                objs.append(entryObj(link, title, image, desc))
            except:
                log('Exception:\n'+str(x))

    return objs

def extract_youtube_channel(url):
    data = parseYoutubeInitialDataJSON(url)
    objs = []
    if data:
        for x in findItem(data, ['gridVideoRenderer']):
            try:
                image = x['thumbnail']['thumbnails'][0]['url'].encode('utf8')
                objs.append(entryObj(url+'/videos', 'VIDEOS', image, 'Videos', False))
                break
            except:
                log('Exception:\n'+str(x))

    objs.extend(extract_youtube_videos(url+'/videos?view=2'))
    objs.extend(extract_youtube_playlists(url+'/playlists'))

    return objs

def extract(url):
    if re.search(r'/playlists$', url):
        return extract_youtube_playlists(url)
    elif re.search(r'/channels$', url):
        return extract_youtube_channels(url)
    elif re.search(r'/channel/([^/]*)$', url):
        return extract_youtube_channel(url)
    elif re.search(r'list=', url):
        return extract_youtube_playlistVideo(url)
    else:
        return extract_youtube_videos(url)

def search_youtube(q, sp=None):
    objs = []
    url = 'https://www.youtube.com/results?q='+ xurl.quote(q)
    if sp:
        url = url+'&sp='+sp
    data = parseYoutubeInitialDataJSON(url)
    if data:
        for x in findItem(data, ['videoRenderer', 'playlistRenderer']):
            try:
                if 'videoId' in x:
                    videoId = x['videoId'].encode('utf8')
                    link = 'https://www.youtube.com/watch?v='+videoId
                    title = x['title']['runs'][0]['text'].encode('utf8')
                    if 'lengthText' in x:
                        desc = x['lengthText']['simpleText'].encode('utf8')
                    else:
                        desc = 'live'
                    image = x['thumbnail']['thumbnails'][0]['url'].encode('utf8')
                    objs.append(entryObj(link, title, image, desc))
                elif 'playlistId' in x:
                    playlistId = x['playlistId'].encode('utf8')
                    link = 'https://www.youtube.com/playlist?list='+playlistId
                    title = x['title']['simpleText'].encode('utf8')
                    image = x['thumbnails'][0]['thumbnails'][0]['url'].encode('utf8')
                    objs.append(pageObj(link, title, image, 'Playlist'))
            except:
                log('Exception:\n'+str(x))

    objs.extend(findYouTubeNextPage(url, q))

    return objs

def search_long(q, sp=None):
    return search_youtube(q, sp or 'EgIYAlAU')

def search_playlist(q, sp=None):
    return search_youtube(q, sp or 'EgIQA1AU')

def search_live(q, sp=None):
    return search_youtube(q, sp or 'EgJAAQ%3D%3D')

