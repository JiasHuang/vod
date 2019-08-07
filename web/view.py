#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess

import page
import conf
import xurl

from mod_python import util, Cookie

def search(pattern, txt, flags=0):
    if not txt:
        return None
    m = re.search(pattern, txt, flags)
    if m:
        return m.group(1)
    return None

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
    cmd = 'python %s \'%s\' %s' %(conf.vod, url, opt or '')
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True)

def sendACT(act, num):
    if not os.path.exists(conf.act):
        return
    cmd = 'python %s \'%s\' \'%s\'' %(conf.act, act, num)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd]).communicate()
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def getCookie(req, key):
    cookies = Cookie.get_cookies(req)
    if cookies and cookies.has_key(key):
        return cookies[key].value
    return None

def getOption(req):
    fmt      = getCookie(req, 'format')
    autosub  = getCookie(req, 'autosub')
    pagelist = getCookie(req, 'pagelist')
    dlconf   = getCookie(req, 'dlconf')
    opt = []
    if fmt:
        opt.append('-f \'%s\'' %(fmt))
    if autosub:
        opt.append('--autosub %s' %(autosub))
    if pagelist:
        opt.append('--pagelist %s' %(pagelist))
    if dlconf:
        opt.append('--dlconf %s' %(dlconf))

    return ' '.join(opt)

def handleCmd(cmd):
    cmd = cmd.lower()
    if cmd in ['update', 'updatedb']:
        os.system('rm -f '+conf.workdir+'vod_*')
        runCmd(cmd)
    else:
        return 'error'
    return 'success'

def msgID(ID):
    return '<span class="message" id="%s"></span>' %(ID)

def msgLink(link):
    return '<a target=_blank href=%s>%s</a>' %(link, link)

def getPlaybackMode():
    return '<meta id="playbackMode" playbackMode="%s">' %(xurl.readLocal(conf.playbackMode))

def index(req):

    req.content_type = 'text/html; charset=utf-8'
    form = req.form or util.FieldStorage(req)

    p = search(r'view\.py\?p=(.*)$', req.unparsed_uri, re.DOTALL)
    v = search(r'view\.py\?v=(.*)$', req.unparsed_uri, re.DOTALL)

    i = form.get('i', None) # input
    a = form.get('a', None) # action
    n = form.get('n', None) # number
    q = form.get('q', None) # query
    s = form.get('s', None) # search
    d = form.get('d', None) # directory
    f = form.get('f', None) # file
    c = form.get('c', None) # command
    x = form.get('x', None) # extra

    if i:
        i = i.strip()
        if i.startswith('#'):
            c = i[1:]
        elif i.startswith('http'):
            v = i
        elif i.startswith('/') and os.path.isdir(i):
            d = i
        elif i.startswith('/') and os.path.exists(i):
            f = i
        else:
            q = re.sub('\s+', ' ', i)

    if p:
        page.page(req, p)

    elif v:
        playURL(v, getOption(req))
        result = '%s<h1>%s %s</h1>' %(getPlaybackMode(), msgID('playing'), msgLink(v))
        page.render(req, 'panel', result)

    elif q:
        url = 'search.html?q='+q
        if s:
            url += '&s='+s
        if x:
            url += '&x='+x
        util.redirect(req, url)

    elif d:
        page.renderDIR(req, d)

    elif f:
        playURL(f)
        result = '%s<h1>%s %s</h1>' %(getPlaybackMode(), msgID('playing'), f)
        page.render(req, 'panel', result)

    elif a:
        sendACT(a, n)
        req.write('<h1>%s %s</h1>' %(msgID(a), n or ''))

    elif c:
        page.render(req, 'status', '<h1>%s</h1>' %(msgID(handleCmd(c))))

    else:
        result = getPlaybackMode()
        page.render(req, 'panel', result)

    return

