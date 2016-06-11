#!/bin/sh

sudo mkdir -p /var/www/vod/
sudo cp -vu web/* /var/www/vod/

if [ ! -e vod.fifo ]; then
    mkfifo vod.fifo
fi

if [ ! -e vod.fifo ]; then
    mkfifo vod.bs.fifo
fi

chmod 666 *.fifo
