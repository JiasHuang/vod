#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import urllib

import page
import conf
import meta

from mod_python import util, Cookie

def runCmd(cmd):
    if not os.path.exists(conf.vod):
        return
    cmd = 'python %s %s' %(conf.cmd, cmd or '')
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def playURL(url, opt=None):
    if not os.path.exists(conf.vod):
        return
    cmd = 'python -u %s \'%s\' %s | tee -a %s' %(conf.vod, url, opt or '', conf.log)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True)

def sendACT(act, num):
    if not os.path.exists(conf.act):
        return
    cmd = 'python -u %s \'%s\' \'%s\' | tee -a %s' %(conf.act, act, num, conf.log)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd]).communicate()
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def getUnparsedURL(req):
    m = re.search(r'=(.*)$', req.unparsed_uri, re.DOTALL)
    if m:
        return urllib.unquote(m.group(1))
    return None

def getCookie(req, key):
    cookies = Cookie.get_cookies(req)
    if cookies and cookies.has_key(key):
        return cookies[key].value
    return None

def getOption(req):
    fmt      = getCookie(req, 'format')
    autosub  = getCookie(req, 'autosub')
    pagelist = getCookie(req, 'pagelist')
    opt = ''
    if fmt:
        opt += '-f \'%s\' ' %(fmt)
    if autosub:
        opt += '--autosub %s ' %(autosub)
    if pagelist:
        opt += '--pagelist %s ' %(pagelist)
    return opt

def metadata(name, value=None):
    local = None
    if name == 'playbackMode':
        local = conf.playbackMode
    if not local:
        return ''
    if value and len(value) > 0:
        meta.saveLocal(local, value, 0)
    else:
        value = meta.readLocal(local, 0)
    return value

def handleCmd(cmd):
    os.system('rm -f '+conf.workdir+'vod_*')
    if cmd in ['update', 'updatedb']:
        runCmd(cmd)
    else:
        return 'error'
    return 'success'

def msgID(ID):
    return '<span class="message" id="%s"></span>' %(ID)

def msgLink(link):
    return '<a target=_blank href=%s>%s</a>' %(link, link)

def index(req):

    req.content_type = 'text/html; charset=utf-8'
    form = req.form or util.FieldStorage(req)

    a = form.get('a', None) # action
    n = form.get('n', None) # number
    i = form.get('i', None) # input
    p = form.get('p', None) # page
    v = form.get('v', None) # video
    q = form.get('q', None) # query
    s = form.get('s', None) # search
    d = form.get('d', None) # directory
    f = form.get('f', None) # file
    c = form.get('c', None) # command
    x = form.get('x', None) # extra
    m = form.get('m', None) # metadata

    if not os.path.exists(conf.playbackMode):
        metadata('playbackMode', getCookie(req, 'playbackMode'))

    if i:
        i = i.strip()
        if re.search(r'^#', i):
            c = i[1:]
        elif re.search(r'^http', i):
            v = i
        elif re.search(r'^/', i) and os.path.isdir(i):
            d = i
        elif re.search(r'^/', i) and os.path.exists(i):
            f = i
        else:
            q = re.sub('\s+', ' ', i)

    if p:
        p = getUnparsedURL(req) or p
        page.page(req, p)

    elif q:
        s = s or getCookie(req, 'engine')
        page.search(req, q, s, x)

    elif d:
        page.renderDIR(req, d)

    elif f:
        playURL(f)
        page.render(req, 'panel', '<h1>%s %s</h1>' %(msgID('playing'), f))

    elif v:
        v = getUnparsedURL(req) or v
        playURL(v, getOption(req))
        page.render(req, 'panel', '<h1>%s %s</h1>' %(msgID('playing'), msgLink(v)))

    elif a:
        sendACT(a, n)
        req.write('<h1>%s %s</h1>' %(msgID(a), n or ''))

    elif c:
        page.render(req, 'status', '<h1>%s</h1>' %(msgID(handleCmd(c))))

    elif m:
        if m == 'sync':
            metadata('playbackMode', getCookie(req, 'playbackMode'))
            page.render(req, 'panel', None)
        else:
            req.write('<div id="div_%s" value="%s"></div>' %(m, metadata(m)))

    else:
        page.render(req, 'panel', None)

    return

