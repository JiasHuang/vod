#!/bin/sh

cd $(dirname $(readlink -f $0))

sudo mkdir -p /var/www/html/vod/db/
sudo mkdir -p /var/www/html/vod/images/
sudo cp -vuL web/* /var/www/html/vod/
sudo cp -vu web/db/* /var/www/html/vod/db/
sudo cp -vu web/images/* /var/www/html/vod/images/

sudo mkdir -p /opt/vod/
sudo cp -vu * /opt/vod/

if [ ! -e /opt/vod/vod.fifo ]; then
    sudo mkfifo /opt/vod/vod.fifo
fi

sudo chmod 666 /opt/vod/*.fifo
