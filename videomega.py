#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import jsunpack

def getSource(url):

    media_id = re.search(r'ref=([0-9a-zA-Z]+)', url).group(1)
    ref = 'http://videomega.tv/cdn.php?ref=%s' %(media_id)

    print '\n[videomega][ref]\n\n\t%s' %(ref)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0',
        'Referer': ref
    }

    r = requests.get(ref, headers=headers)
    txt = r.text.encode('utf8')

    stream_url = None
    unpacked = None

    packed = re.search('(eval\(function\(p,a,c,k,e,d\)\{.+\))', txt)
    if packed:
        # change radix before trying to unpack, 58-61 seen in testing, 62 worked for all
        packed = re.sub(r"(.+}\('.*', *)\d+(, *\d+, *'.*?'\.split\('\|'\))", "\g<01>62\g<02>", packed.group(1))
        unpacked = jsunpack.unpack(packed)

    if unpacked:
        print '\n[videomega][unpacked]\n\n\t%s' %(unpacked)
        r = re.search(r'http://([^"]+)', unpacked)
        if r:
            stream_url = r.group()

    if stream_url:
        print '\n[videomega][src]\n\n\t%s' %(stream_url)
        return stream_url

    return ''

def search(txt):

    m = re.search(r'http://videomega.tv/([^"]*)', txt)
    if m:
        return m.group()

    return

