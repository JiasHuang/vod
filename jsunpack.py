#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import xurl

def unpackURL(url):
    txt = xurl.load2(url)
    return unpack(txt)

def unpackFILE(local):
    txt = xurl.readLocal(local)
    return unpack(txt)

def unpack(txt):
    m = re.search('(eval\(function\(p,a,c,k,e,d\)\{.+\))', txt)
    if m :
        packed = m.group()
        output = xurl.post('http://jsunpack.jeek.org/?', {'urlin':packed})
        output = re.sub('\\\\\\\\/', '/', output)
        print('\n----------------------------------------------------- [packed] -------------------------------------------------------------\n\n')
        print(packed)
        print('\n----------------------------------------------------- [unpack] -------------------------------------------------------------\n\n')
        print(output)
        print('\n----------------------------------------------------------------------------------------------------------------------------\n\n')
        return output
    return None

