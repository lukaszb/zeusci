#!/bin/bash
clear
cmd="./manage.py test zeus"
$cmd
watchmedo shell-command -R -p "*.py" -c "clear && $cmd" .

