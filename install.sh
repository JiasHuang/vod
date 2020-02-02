#!/bin/sh

cd $(dirname $(readlink -f $0))

sudo mkdir -p /var/www/html/vod/
sudo cp -vLr web/* /var/www/html/vod/

sudo mkdir -p /opt/vod/extractors
sudo cp -vL * /opt/vod/
sudo cp -vL extractors/* /opt/vod/extractors/

if [ ! -e /opt/vod/vod.fifo ]; then
    sudo mkfifo /opt/vod/vod.fifo
fi

sudo chmod 666 /opt/vod/*.fifo
