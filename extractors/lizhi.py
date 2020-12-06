#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

import xurl

from optparse import OptionParser

def dl(url, local, ref=None, read=True):
    if not os.path.exists(local):
        xurl.load(url, local, ref=ref)
    if read:
        return xurl.readLocal(local)
    return None

def main():

    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", action='append')
    parser.add_option("-c", "--chdir", dest="chdir")
    (options, args) = parser.parse_args()

    if options.chdir:
        os.chdir(options.chdir)

    for i in options.input:
        try:
            m = re.search(r'www.lizhi.fm/(\d*)/(\d*)', i)
            data_band, data_id = m.group(1), m.group(2)

            html_url = i
            html_local = data_id+'.html'
            html_txt = dl(html_url, html_local)

            media_url = 'http://www.lizhi.fm/media/url/'+data_id
            media_local = data_id+'.json'
            media_txt = dl(media_url, media_local)

            m = re.search(r'"url":"([^"]*)"', media_txt)
            audio_url = m.group(1)
            audio_local = data_id+'.mp3'
            dl(audio_url, audio_local, ref='http://www.lizhi.fm/box', read=False)

        except:
            print('Exception: ' + i)

    return

if __name__ == '__main__':
    main()
