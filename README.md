startseite
==========

Infoserver/Startseite-Server

installing
==========

```
sudo easy_install wheezy.template
sudo apt-get install python-lxml
cd /tmp
git clone https://github.com/redyeti/startseite.git startseite
sudo mv /tmp/startseite /opt/startseite startseite
cd /opt/startseite
sudo install.sh

```

server
======
You can set the port for the server in server.py line 94.
