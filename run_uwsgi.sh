#!/bin/sh
touch ./uwsgi.touch
$VIRTUAL_ENV/bin/uwsgi --module=app --callable=app --socket=:3000 --touch-reload=./uwsgi.touch --daemonize ./uwsgi.log -H $VIRTUAL_ENV