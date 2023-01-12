#!/bin/bash

# Set up the Secret key used by Beaker and Flask
# This can be overriden using a CKAN___BEAKER__SESSION__SECRET env var
if grep -E "beaker.session.secret ?= ?$" ckan.ini
then
    echo "Setting beaker.session.secret in ini file"
    paster --plugin=ckan config-tool $CKAN_INI "beaker.session.secret=$(python -c 'import secrets; print(secrets.token_urlsafe())')"
fi

# Run the prerun script to init CKAN and create the default admin user
sudo -u ckan -EH python prerun.py

# Run any startup scripts provided by images extending this one
if [[ -d "/docker-entrypoint.d" ]]
then
    for f in /docker-entrypoint.d/*; do
        case "$f" in
            *.sh)     echo "$0: Running init file $f"; . "$f" ;;
            *.py)     echo "$0: Running init file $f"; python "$f"; echo ;;
            *)        echo "$0: Ignoring $f (not an sh or py file)" ;;
        esac
        echo
    done
fi

# Set the common uwsgi options
UWSGI_OPTS="--socket /tmp/uwsgi.sock --uid 92 --gid 92 --http :5000 --master --enable-threads --paste config:/srv/app/production.ini --paste-logger --lazy-apps -p 2 -L -b 32768"

if [ $? -eq 0 ]
then
    # Start supervisord
    supervisord --configuration /etc/supervisord.conf &
    # Start uwsgi
    sudo -u ckan -EH uwsgi $UWSGI_OPTS
fi
