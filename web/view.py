#!/usr/bin/env python

import os
import re
import subprocess
import page
import conf

from mod_python import util

def playURL(url):
    cmd = 'python -u %s \'%s\'' %(conf.vod, url)
    log = open(conf.log, 'a')
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', cmd], stdout=log)
    else:
        subprocess.Popen(cmd, shell=True, stdout=log)

def sendACT(act, val):
    cmd = 'python -u %s \'%s\' \'%s\'' %(conf.act, act, val)
    log = open(conf.log, 'a')
    subprocess.Popen(cmd, shell=True, stdout=log).communicate()

def index(req):

    req.content_type = 'text/html; charset=utf-8'

    arg  = util.FieldStorage(req)
    url  = arg.get('url', None)
    act  = arg.get('act', None)
    val  = arg.get('val', None)
    p    = arg.get('p', None)
    q    = arg.get('q', None)

    if url and url[0:4] != 'http' and url[0] != '/':
        q = url
        url = None

    if p:
        src = page.listURL(req, p)

    elif q:
        page.render(req, 'list', page.search(q))

    elif url and re.search(r'^http', url):
        if re.search(r'www.eslpod.com', url):
            page.loadWord(req, url)
        else:
            playURL(url)
            page.render(req, 'panel', 'playURL <a target=_blank href=%s>%s</a>' %(url, url))

    elif url and re.search(r'^/', url):
        if os.path.isdir(url):
            page.renderDIR(req, url)
        elif os.path.exists(url):
            playURL(url)
            page.render(req, 'panel', 'playURL '+url)

    elif act:
        sendACT(act, val)
        page.render(req, 'panel', act+','+val)

    else:
        page.render(req, 'panel', None)

    return

