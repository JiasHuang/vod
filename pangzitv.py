#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import base64
import urllib

import xurl

def getSource(url):
    if re.search(r'vod-play-id', url):
        try:
            m = re.search(r'num-(\d+)', url)
            ep_num = m.group(1)
            txt = xurl.load2(url)
            m = re.search(r'base64decode\(\'([^\']*)', txt)
            code = m.group(1)
            decoded = urllib.unquote(base64.b64decode(code))
            for m in re.finditer(r'(\d\d).*?(http[^#$\n]*)', decoded):
                if (int(m.group(1)) == int(ep_num)):
                    return m.group(2)
        except:
            print('Exception')
    return None

