#!/bin/sh

cd /opt/

sudo curl -L https://github.com/rg3/youtube-dl/archive/master.zip -o youtube-dl-master.zip
sudo unzip -o youtube-dl-master.zip
sudo ln -sfn /opt/youtube-dl-master/youtube_dl/__main__.py /usr/local/bin/youtube-dl
sudo python -m compileall /opt/youtube-dl-master
