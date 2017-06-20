#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import base64
import hashlib

import xurl
import jsunpack
import jwplayer

def checkURL(url):
    site = xurl.findSite(url)
    return re.compile('(jav)').search(site)

def checkVideoURL(url):
    site = xurl.findSite(url)
    return re.compile('(openload|drive.google|bitporno)').search(site)

def load(url, local=None, options=None):
    return xurl.load2(url, local, options)

def decryptJSCode(url):
    txt = load(url)
    if re.search(r'<script src="https://jqd.cdn-qdnetwork.com', txt):
        jsonurl = re.sub('/embed/', '/stream/v6/', url)
        jsontxt = load(jsonurl)
        if jsontxt != '':
            token = 'avcms.co'
            dirname = os.path.dirname(os.path.realpath(__file__))
            jscode = xurl.readLocal(dirname+'/cryptoJSAESJson.js') + '\n'
            jscode += 'console.log(CryptoJSAESdecrypt(\'%s\', \'%s\'));' %(jsontxt, token)
            output = jsunpack.executeJSCode(jscode)
            return jwplayer.parseSetup(output)
    return None

def getSource(url):
    links = xurl.getIFrame(url)
    for link in links:
        if checkVideoURL(link):
            return link
    for link in links:
        dec = decryptJSCode(link)
        if dec:
            return dec
    dec = decryptJSCode(url)
    if dec:
        return dec
    return None

