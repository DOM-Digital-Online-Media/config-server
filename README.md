# config-server
a Flask app that delivers configurations per JSON based on rules.

install

config-server may run with any python3 but is tested with 3.8 only


git clone https://github.com/DOM-Digital-Online-Media/config-server.git
cd config-server
apt install python3.8-venv
python3.8 -m venv .venv

usage

you may test your install by executing the bash script 'checkconfig'.
per default it should deliver:

{"AUTH_BACKEND": "auth2.dom.de", "COMMUNICATION_PROCESS": "new"}

configuration

check the example configs.toml

run it as a server

we use uwsgi and nginx for that purpose.