#!/bin/sh

cd /opt/

sudo curl -L https://github.com/rg3/youtube-dl/archive/master.zip -o youtube-dl-master.zip
sudo unzip -o youtube-dl-master.zip
sudo ln -sfn /opt/youtube-dl-master/youtube_dl/__main__.py /usr/local/bin/youtube-dl
sudo python -m compileall /opt/youtube-dl-master

if [ ! -f phantomjs-2.1.1-linux-x86_64.tar.bz2 ]; then
    sudo curl -L https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 -o phantomjs-2.1.1-linux-x86_64.tar.bz2
    sudo tar jxf phantomjs-2.1.1-linux-x86_64.tar.bz2
    sudo ln -sfn /opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs
fi
