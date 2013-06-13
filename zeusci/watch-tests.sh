#!/bin/bash
clear
cmd="./manage.py test zeus"
$cmd
TESTING=YES watchmedo shell-command -R -p "*.py" -c "clear && $cmd" .

