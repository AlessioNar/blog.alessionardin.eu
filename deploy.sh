#!/bin/bash

USER=alessio
DIR=/home/alessio/blog.alessionardin.eu  
DIR_VIRTUALENV=/home/alessio/blog
APP_NAME=blog

cd $DIR

git pull

source $DIR_VIRTUALENV/bin/activate && python manage.py makemigrations && python manage.py migrate

sudo supervisorctl restart $APP_NAME
sudo systemctl restart nginx

exit 0