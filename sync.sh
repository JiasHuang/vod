#!/bin/sh

cd /opt/

if [ -d "youtube-dl" ]
then
	cd youtube-dl
	sudo git pull
else
	sudo git clone https://github.com/ytdl-org/youtube-dl.git
	sudo ln -sfn /opt/youtube-dl/youtube_dl/__main__.py /usr/local/bin/youtube-dl
fi
