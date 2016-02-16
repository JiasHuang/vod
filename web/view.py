#!/usr/bin/env python

import os
import subprocess
import page
import json
import conf

from mod_python import util

def loadHTML(req, path):
  f = open(path, 'r')
  req.write(f.read())
  f.close()

def listDIR(req, d):
  req.write('<h1>Index of %s</h1>' %(d))
  req.write('<div style="line-height:200%;font-size:20">')
  req.write('<ul>')
  for dirName, subdirList, fileList in os.walk(d):
    for subdir in sorted(subdirList):
      if subdir[0] != '.':
        req.write('<li><img src="/icons/folder.gif"> <a href="view.py?url=%s/%s">%s</a>' %(dirName, subdir, subdir))
    for fname in sorted(fileList):
      if fname.lower().endswith(('.mkv', '.mp4', '.avi', '.flv', '.rmvb', '.rm', 'f4v', '.m3u', '.m3u8')):
        req.write('<li><img src="/icons/movie.gif"> <a href="view.py?url=%s/%s">%s</a>' %(dirName, fname, fname))
    break
  req.write('</ul>')
  req.write('</div>')

def loadURL(req, url):
    loadHTML(req, '/var/www/html/action.html')
    req.write('<br>playURL <a target="_blank" href="%s">%s</a>' %(url, url))
    cmd = 'python -u %s \'%s\' | tee -a %s' %(conf.vod, url, conf.log)
    subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', cmd])
    req.write("<br>Sent")

def sendAct(act):
    cmd = '%s \'%s\'' %(conf.act, act)
    subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', cmd]).communicate()

def index(req):

  req.content_type = 'text/html; charset=utf-8'

  #env = os.environ.copy()
  #env['DISPLAY'] = ':0'

  arg  = util.FieldStorage(req)
  url  = arg.get('url', None)
  act  = arg.get('act', None)
  val  = arg.get('val', None)
  p    = arg.get('p', None)
  q    = arg.get('q', None)

  if act == 'load':
    loadHTML(req, '/var/www/html/'+val+'.html')
    return

  loadHTML(req, '/var/www/html/head.html')

  if p:
    src = page.listURL(req, p)
    if src != None and src != '':
        loadURL(req, src)

  elif q:
    page.search(req, q)

  elif url:
    if url[0:4] == 'http':
        loadURL(req, url)
    elif url[0] == '/' and os.path.isdir(url):
        listDIR(req, url)
    elif url[0] == '/' and os.path.exists(url):
        loadURL(req, url)
    else:
        page.search(req, url)

  elif act:
    if act == 'forward' and val:
        sendAct('seek %s' %val)
    elif act == 'backward' and val:
        sendAct('seek -%s' %val)
    elif act == 'percent' and val:
        sendAct('seek %s absolute-percent' %val)
    elif act in ['osd', 'mute', 'pause', 'stop', 'playlist_next', 'playlist_prev']:
        sendAct(act)
    loadHTML(req, '/var/www/html/action.html')

  else:
    loadHTML(req, '/var/www/html/action.html')

  loadHTML(req, '/var/www/html/tail.html')

  return

