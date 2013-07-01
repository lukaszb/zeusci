#!/bin/bash
clear
cmd="./manage.py test zeus"
$cmd
TESTING=YES watchmedo shell-command -w -R -p "*.py" -c "clear && $cmd" .

