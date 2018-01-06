#!/bin/sh

cd $(dirname $(readlink -f $0))

sudo mkdir -p /var/www/html/vod/db/
sudo mkdir -p /var/www/html/vod/images/
sudo cp -vL web/* /var/www/html/vod/
sudo cp -v web/db/* /var/www/html/vod/db/
sudo cp -v web/images/* /var/www/html/vod/images/

sudo mkdir -p /opt/vod/
sudo cp -v * /opt/vod/

if [ ! -e /opt/vod/vod.fifo ]; then
    sudo mkfifo /opt/vod/vod.fifo
fi

sudo chmod 666 /opt/vod/*.fifo
