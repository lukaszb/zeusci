#!/bin/sh

DIR="source"
CMD="make html"


# Run command
$CMD

# Run command on .rst file change.
watchmedo shell-command --pattern "*.rst" --recursive -w -c "clear && $CMD" $DIR

