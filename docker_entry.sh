#!/bin/sh

if [ "$RESTORE" = true ]; then
  echo "Restoring grafana"
  grafana-backup restore _OUTPUT_/$ARCHIVE_FILE
else
  echo "Backing up grafana"
  grafana-backup save
fi

