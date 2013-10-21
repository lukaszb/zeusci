#!/bin/sh

# NOTE: This is purely for development

rm -Rf ../var/builds
rm .database.sqlite
./manage.py syncdb --noinput
./manage.py zeusci_sample_data
