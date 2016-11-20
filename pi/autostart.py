#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

def update():
	conf = '/var/tmp/autostart_update'
	if os.path.exists(conf):
		os.chdir('/opt/vod')
		os.system('sudo git pull')
		os.system('sudo ./install.sh')
		os.system('sudo ./sync.sh')
        	os.system('sudo rm %s' %(conf))
	return

def main():
	update()
	os.system('ifconfig')
	os.system('tail -F /tmp/view.log')
	return

if __name__ == '__main__':
	main()
