#!/bin/bash

python_interpreter=""
cfn=${PWD##*//}

sudo ufw allow 22
sudo ufw allow enable

read -p "Python interpreter: " python_interpreter
`$python_interpreter -m venv venv`
source venv/bin/activate
pip install -U pip
pip install -r deps.txt

sudo ln -s /home/$cfn/presets/nginx/nginx.conf /etc/nginx/nginx.conf
sudo ln -s /home/$cfn/presets/nginx/backend.conf /etc/nginx/conf.d/backend.conf

sudo ln -s /home/$cfn/presets/gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service
sudo ln -s /home/$cfn/presets/gunicorn/gunicorn.socket /etc/systemd/system/gunicorn.socket

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo service nginx restart