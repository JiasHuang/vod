#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json

import xurl

def str2int(s):
    m = re.search(r'(\d+)', s)
    if m:
        return int(m.group(1))
    return None

def parseSetup(txt):
    try:
        results = json.loads(txt)
        best_file = None
        best_label = 0
        for r in results:
            if 'file' not in r:
                continue
            if 'label' in r:
                label = str2int(r['label'])
                if label and label > best_label:
                    best_file = r['file']
                    best_label = label
            if best_file == None:
                best_file = r['file']
        print('file (%d) :\n\t%s' %(best_label, best_file or 'N/A'))
        return best_file
    except:
        print('parseSetup Error')
    return None


def getSource(dataLink):
    url = 'http://play.wtutor.net/wp-admin/admin-ajax.php?action=ts-ajax&p=%s&n=1' %dataLink
    txt = xurl.load(url)
    videos = re.findall('file\s*:\s*[\"\']([^\"\']+).+?label\s*:\s*[\"\'](\d+)p[^\}]', txt)
    if videos:
        return videos[0][0]
    return None

