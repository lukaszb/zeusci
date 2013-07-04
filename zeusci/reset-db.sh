#!/bin/sh

rm -Rf ../var/builds
rm .database.sqlite
./manage.py syncdb --noinput
./manage.py data
