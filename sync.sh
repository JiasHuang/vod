#!/bin/sh

cd /opt/
sudo rm -rf /usr/local/bin/youtube-dl youtube-dl youtube_dl
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o youtube-dl
sudo unzip youtube-dl
sudo ln -sfn /opt/youtube_dl/__main__.py /usr/local/bin/youtube-dl
sudo python -m compileall /opt/youtube_dl
