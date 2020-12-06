#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import json

import xurl

path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(path))

import extractors

class dir_entry_obj:
    def __init__(self, path, is_file):
        self.path = path
        self.is_file = is_file

class page_obj:
    def __init__(self):
        self.type = 'page'
        self.entry = []
        self.nav = []
        self.meta = None

class dir_obj:
    def __init__(self, d):
        self.type = 'dir'
        self.dir = d
        self.entry = []

def getDIRJSON(d):
    obj = dir_obj(d)
    for dirName, subdirList, fileList in os.walk(d):
        for subdir in sorted(subdirList):
            if subdir[0] != '.':
                path = os.path.join(dirName, subdir)
                obj.entry.append(dir_entry_obj(path, False).__dict__)
        for fname in sorted(fileList):
            suffix = ('.mkv', '.mp4', '.avi', '.flv', '.rmvb', '.rm', '.f4v', '.wmv', '.m3u', '.m3u8', '.ts')
            if fname.lower().endswith(suffix):
                path = os.path.join(dirName, fname)
                obj.entry.append(dir_entry_obj(path, True).__dict__)
        break
    return json.dumps(obj.__dict__)

def getExtractorResultJSON(results):
    obj = page_obj()
    local = '/var/tmp/vod_list_pagelist_%s' %(str(os.getpid() % 100))
    links = []
    for res in results:
        if isinstance(res, extractors.entryObj):
            obj.entry.append(res.__dict__)
            links.append(res.link)
        elif isinstance(res, extractors.navObj):
            obj.nav.append(res.__dict__)
    xurl.saveLocal(local, '\n'.join(links))
    obj.meta = local
    return json.dumps(obj.__dict__)

def getSearchJSON(q, s=None, x=None):
    s = (s or 'youtube').lower()
    q1 = re.sub(' ', '+', q)
    results = extractors.search(q1, s, x)
    return getExtractorResultJSON(results)

def getPageJSON(url):
    results = extractors.extract(url)
    return getExtractorResultJSON(results)


