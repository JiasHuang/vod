# VOD (Video-On-Demand)

- Play online streaming videos on RaspberryPi.
- Control playback on your mobile phone or tablet.

# Requirement

- apache2+mod-python: Web Interface
- youtubedl: Extract video URLs

# Install VOD on RaspberryPi

- Install apache2, libapache2-mod-python, nodejs, xterm
```
sudo apt-get install apache2 libapache2-mod-python nodejs xterm
```

- Enable apache2 mod-python
``` 
sudo vi /etc/apache2/apache2.conf

<Directory /var/www/>
    AddHandler mod_python .py
    PythonHandler mod_python.publisher
    PythonDebug On
</Directory>
```

- Edit apache2 environment variables
```
sudo vi /etc/apache2/envvars

export APACHE_RUN_USER=pi
export APACHE_RUN_GROUP=pi
```

- Restart apache2
``` 
sudo service apache2 restart
```

- Download source codes
```
git clone http://gitbub.com/jiashuang/vod
cd vod
```

- Download latest youtubedl
``` 
sudo ./sync.sh
```

- Install Web Interface
```
sudo ./install.sh
```

- Play it
```
go to http://192.168.1.145/vod or 
go to http://raspberrypi.local/vod (if you had iPhone/iPad that supported mDNS)
(192.168.1.145 is my RPI's local IP)
```

