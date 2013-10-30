#!/bin/sh

DIR="source"
CMD="make html"
NOTIFY='growlnotify zeus-ci Documentation -m Recreated'


# Run command
$CMD
$NOTIFY

# Run command on .rst file change.
watchmedo shell-command --pattern "*.rst" --recursive -w -c "clear && $CMD && $NOTIFY" $DIR

