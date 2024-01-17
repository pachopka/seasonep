#!/usr/bin/bash

CSV_FILENAME=dataset/results.csv

if [ -f $CSV_FILENAME ]; then

    tail -n +2 "$CSV_FILENAME" | while IFS=, read -r col1 col2 col3 col4 col5
    do
        ORIGINAL_FILENAME=dataset/video/$col2.mkv
        SEASON=dataset/video/$col3
        NEW_FILENAME=${SEASON}/${col4}.mkv
        if [ ! -d $SEASON ]; then
            mkdir $SEASON
        fi
        mv "${ORIGINAL_FILENAME}" "${NEW_FILENAME}"
        echo "$ORIGINAL_FILENAME was moved and renamed"
    done
else
    echo "No results file at $PWD/$CSV_FILENAME"
fi
