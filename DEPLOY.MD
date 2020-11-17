# NITRIX. Deploy instruction
This instruction for deploy Flask application.

**Prerequisites:**
* OS: Ubuntu 20.*
* Web Server: Nginx
* Python3
* [uWSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface)


## Deploy from github

Choice folder for deploy. E.g. : ~/NITRIX/
For user **inv** it will be folder /home/inv/NITRIX
Create folder:
```
mkdir ~/NITRIX
```
Project NITRIX placed in GitHub repository [here](https://github.com/simple2b/NITRIX).
Let's download the project from GitHub:
```
cd ~/NITRIX
git clone https://github.com/Simple2B/NITRIX.git .
```

## Prepare environment
Update and upgrade security software:
```
apt update && apt upgrade
```
Create `cbapi` user. Enter password and optional information about the user:
```
adduser cbapi
```
Add `cbapi` user to sudo group:
```
adduser cbapi sudo
```
Log out from the system and log in using `cbapi` user:
```
ssh cbapi@<hostname>
```
Setup necessaries packages:
```
sudo apt-get install nginx python3-pip virtualenv
```
Project CorbotAPI is placed in GitHub repository [here](https://github.com/Simple2B/corbot.api).
Clone the project from GitHub:
```
git clone https://github.com/Simple2B/corbot.api
```
Now, create python virtual environment:
```
cd corbot.api
virtualenv -p python3 .venv
pip install -r requirements.txt
```


## Configure WSGI

We use uWSGI service from python virtual environment.
Activate virtual environment and setup actual packages:
```
sudo apt-get install python3-dev build-essential
source .venv/bin/activate
pip install uwsgi
```
Verify **uwsgi.ini** file (WSGI configuration) in project folder:
```ini
[uwsgi]
# Module and app name which uWSGI starts
module = wsgi:app

master = true
# Num of uWSGI processes
processes = 5

# Path to socket file
socket = /tmp/cbapi.sock
# Defining group and user for socket file
chmod-socket = 660
chown-socket = cbapi:www-data

# Defining group and user starting the uWSGI process
uid = cbapi
gid = www-data

logto = /tmp/uwsgi.log

# Clean up uWSGI temp files on service shutdown
vacuum = true
# Exit process on terminal close
# Required for proper startup using systemd
die-on-term = true
```

Line `uid = inv` must contain correct user name.

## Create Linux Service

Create file `/etc/systemd/system/cbapi.service` with follow content:
```ini
[Unit]
Description=uWSGI instance to serve CorbotAPI project
After=network.target

[Service]
User=cbapi
Group=www-data
WorkingDirectory=/home/cbapi/corbot.api
Environment="PATH=/home/cbapi/corbot.api/.venv/bin"
ExecStart=/home/cbapi/corbot.api/.venv/bin/uwsgi --ini uwsgi.ini

[Install]
WantedBy=multi-user.target
```

Run service:
```
sudo systemctl start cbapi
```
Make sure everything is working fine:
```
sudo systemctl status cbapi
```
Activate service
```
sudo systemctl enable cbapi
```

## Nginx configuration

Create file `/etc/nginx/sites-available/cbapi.conf` with following content:
```
upstream cbapi_upstream {
    server unix:/tmp/cbapi.sock;
}

server {
    listen 80;
    server_tokens off;
    server_name api1.corbot.us;

    location / {
        include uwsgi_params;
        uwsgi_pass cbapi_upstream;
    }

    location /static {
        root /home/cbapi/corbot.api/app;
    }
}
```


Activate this Nginx configuration:
```
sudo ln -s /etc/nginx/sites-available/cbapi.conf /etc/nginx/sites-enabled/
```
Check if our configuration file is OK:
```
sudo nginx -t
```
Reload Nginx configuration:
```
sudo systemctl reload nginx
```