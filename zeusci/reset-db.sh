#!/bin/sh

rm -Rf builds
rm .database.sqlite
./manage.py syncdb --noinput
./manage.py data
