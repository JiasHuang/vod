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
      if fname.lower().endswith(('.mkv', '.mp4', '.avi', '.flv', '.rmvb', '.rm', 'f4v', '.m3u')):
        req.write('<li><img src="/icons/movie.gif"> <a href="view.py?url=%s/%s">%s</a>' %(dirName, fname, fname))
    break
  req.write('</ul>')
  req.write('</div>')

def loadFILE(req, url):
    loadHTML(req, '/var/www/html/action.html')
    req.write('<br>playURL <a target="_blank" href="%s">%s</a>' %(url, url))
    subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', '%s %s' %(conf.vod, url)])
    req.write("<br>Sent")

def loadURL(req, url):

    loadHTML(req, '/var/www/html/action.html')
    req.write('<br>[URL] <a target="_blank" href="%s">%s</a>' %(url, url))

    cmd = '%s -j %s -u \'%s\' | tee -a %s' %(conf.src, conf.json, url, conf.log)
    subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', cmd]).communicate()
    with open(conf.json, 'r') as fd:
        data = json.load(fd)
        src = data['src']
        ref = data['ref']

    if src == '':
        req.write('<br>Fail')
        return

    if src != url:
        cmd = '%s -s \'%s\' -r \'%s\' | tee -a %s' %(conf.run, src, ref, conf.log)
        subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', cmd])
        req.write('<br>[SRC] <a target="_blank" href="%s">%s</a>' %(src, src))
        req.write('<br>Sent')
        return

    if url != '':
        cmd = '%s \'%s\' | tee -a %s' %(conf.vod, url, conf.log)
        subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', cmd])
        req.write('<br>Sent')

def index(req):

  req.content_type = 'text/html; charset=utf-8'

  loadHTML(req, '/var/www/html/head.html')

  #env = os.environ.copy()
  #env['DISPLAY'] = ':0'

  arg  = util.FieldStorage(req)
  url  = arg.get('url', None)
  act  = arg.get('act', None)
  val  = arg.get('val', None)
  p    = arg.get('p', None)
  q    = arg.get('q', None)

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
        loadFILE(req, url)
    else:
        page.search(req, url)

  elif act:
    if act == 'osd':
    	os.system('echo osd > %s' %(conf.fifo))
    elif act == 'forward' and val:
    	os.system('echo seek %s > %s' %(val, conf.fifo))
    elif act == 'backward' and val:
    	os.system('echo seek -%s > %s' %(val, conf.fifo))
    elif act == 'percent' and val:
    	os.system('echo seek %s absolute-percent > %s' %(val, conf.fifo))
    elif act == 'pause':
    	os.system('echo pause > %s' %(conf.fifo))
    elif act == 'stop':
    	os.system('echo stop > %s' %(conf.fifo))
    elif act == 'mute':
    	os.system('echo mute > %s' %(conf.fifo))
    elif act == 'volL':
        os.system('echo volume -5 > %s' %(conf.fifo))
    elif act == 'volH':
        os.system('echo volume +5 > %s' %(conf.fifo))
    elif act == 'next':
        os.system('echo playlist_next > %s' %(conf.fifo))
    elif act == 'prev':
        os.system('echo playlist_prev > %s' %(conf.fifo))

    loadHTML(req, '/var/www/html/action.html')

  else:
    loadHTML(req, '/var/www/html/action.html')
  return

