#!/bin/sh

cd /opt/

sudo wget https://youtube-dl.org/downloads/latest/youtube-dl-2020.11.12.tar.gz
sudo tar zxf youtube-dl-2020.11.12.tar.gz
sudo ln -sfn /opt/youtube-dl/youtube_dl/__main__.py /usr/local/bin/youtube-dl
