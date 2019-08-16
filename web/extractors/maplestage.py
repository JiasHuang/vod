#!/usr/bin/env python
# coding: utf-8

import re
import json

from .utils import *

VALID_URL = r'maplestage'

def extract(url):
    objs = []
    if re.search(r'/drama/', url):
        pageProps = re.search(r'var pageProps = (.*?});', load(url))
        if pageProps:
            data = json.loads(pageProps.group(1))
            try:
                for show in sorted(data['shows'], key=lambda x : x['updatedAt'], reverse=True):
                    slug, cover = darg(show, 'slug', 'cover')
                    link = 'http://maplestage.com/show/' + slug
                    objs.append(entryObj(link, slug, video=False))
            except:
                print('Exception:\n'+str(data))
    elif re.search(r'/show/', url):
        pageData = re.search(r'var pageData = (.*?});', load(url));
        if pageData:
            data = json.loads(pageData.group(1))
            try:
                for ep in data['props'][0]['value']['episodes']:
                    shortId, slug, thumb, numStr = darg(ep, 'shortId', 'slug', 'thumb', 'numStr')
                    link = 'http://maplestage.com/episode/'+shortId+'/'+numStr # FIXME
                    title = slug+'('+numStr+')'
                    if 'topic' in ep:
                        title += darg(ep, 'topic')
                    objs.append(entryObj(link, title, video=False))
            except:
                print('Exception:\n'+str(data))
    elif re.search(r'/episode/', url):
        pageData = re.search(r'var pageData = (.*?});', load(url));
        if pageData:
            data =  json.loads(pageData.group(1))
            for prop in data['props']:
                if 'value' in prop and 'videoSources' in prop['value']:
                    try:
                        for videoSrc in prop['value']['videoSources']:
                            vcnt = len(videoSrc['videos'])
                            for videoIndex, video in enumerate(videoSrc['videos'], 1):
                                vtype, vid = darg(video, 'type', 'id')
                                if vtype in ['youtube', 'dailymotion']:
                                    link = getLink(vtype, vid)
                                    title = getTitle(vtype, videoIndex, vcnt)
                                    image = getImage(vtype, vid)
                                    objs.append(entryObj(link, title, image))
                                if vtype == 'html':
                                    vsrc = re.search(r'src="([^"]*)"', vid)
                                    if vsrc:
                                        objs.append(entryObj(vsrc.group(1)))
                    except:
                        print('Exception:\n'+str(prop))

    return objs
