#!/bin/bash

mkdir /opt/startseite/data
chown www-data /opt/startseite/data
cp /opt/startseite/upstart/* /etc/init/
