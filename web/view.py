#!/usr/bin/env python

import os
import re
import subprocess

import page
import conf
import urllib

from mod_python import util

def runCmd(val):
    if not os.path.exists(conf.vod):
        return
    cmd = 'python %s %s' %(conf.cmd, val or '')
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def playURL(url):
    if not os.path.exists(conf.vod):
        return
    cmd = 'python -u %s \'%s\' | tee -a %s' %(conf.vod, url, conf.log)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True)

def sendACT(act, val):
    if not os.path.exists(conf.act):
        return
    cmd = 'python -u %s \'%s\' \'%s\' | tee -a %s' %(conf.act, act, val, conf.log)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd]).communicate()
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def getUnparsedURL(req):
    m = re.search(r'=(.*)$', req.unparsed_uri, re.DOTALL)
    if m:
        return urllib.unquote(m.group(1))
    return None

def handleCmd(cmd):
    os.system('rm -f '+conf.workdir+'vod_*')
    if cmd in ['update', 'updatedb']:
        runCmd(cmd)
    elif cmd in ['def', 'low']:
        conf.loadConf(conf.vodpath+'config/vodconf_'+cmd)
    else:
        return 'error'
    return 'success'
 
def index(req):

    req.content_type = 'text/html; charset=utf-8'

    arg  = util.FieldStorage(req)
    act  = arg.get('act', None)
    val  = arg.get('val', None)
    url  = arg.get('url', None)
    p    = arg.get('p', None)
    v    = arg.get('v', None)
    q    = arg.get('q', None)
    s    = arg.get('s', None)
    d    = arg.get('d', None)
    f    = arg.get('f', None)
    w    = arg.get('w', None)
    c    = arg.get('c', None)

    if url:
        if re.search(r'^#', url):
            c = url[1:]
        elif re.search(r'^http', url):
            v = url
        elif re.search(r'^/', url) and os.path.isdir(url):
            d = url
        elif re.search(r'^/', url) and os.path.exists(url):
            f = url
        else:
            q = url

    if p:
        p = getUnparsedURL(req) or p
        page.listURL(req, p)

    elif q:
        page.search(req, q, s)

    elif d:
        page.renderDIR(req, d)

    elif f:
        playURL(f)
        page.render(req, 'panel', '<h1>playURL %s</h1>' %(f))

    elif v:
        v = getUnparsedURL(req) or v
        playURL(v)
        page.render(req, 'panel', '<h1>playURL <a target=_blank href=%s>%s</a><h1>' %(v, v))

    elif w:
        page.loadword(req, w)

    elif act:
        sendACT(act, val)
        page.render(req, 'panel', '<h1>%s %s</h1>' %(act, val or ''))

    elif c:
        page.render(req, handleCmd(c), None)

    else:
        page.render(req, 'panel', None)

    return

