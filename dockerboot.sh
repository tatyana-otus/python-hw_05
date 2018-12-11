#!/bin/bash

cp nginx_uwsgi.conf /etc/nginx/nginx.conf      # replace nginx configuration file
mkdir /usr/local/etc/ip2w                      # create CONFIG_DIR
cp ip2w/ip2w.cfg /usr/local/etc/ip2w/ip2w.cfg  # copy ip2w configuration file to CONFIG_DIR
mkdir /var/log/ip2w                            # create LOG_DIR for ip2w log file
mkdir -p /run/uwsgi                            # create DIR for socket communication between uwsgi and nginx
uwsgi --ini ip2w/ip2w.ini &                    # run uswgi with ip2w.ini init file 
nginx                                          # run nginx