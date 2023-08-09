#!/usr/bin/env bash

for filename in *.gif; do
    echo "Converting \"$filename\" -> \"${filename%.*}.webm\""

    if test -f "${filename%.*}.webm"; then
        echo "File \"${filename%.*}.webm\" already exists, skipping."
    else
        ffmpeg -hide_banner -loglevel error -stats -i "$filename" -c vp9 -b:v 0 -crf 40 "${filename%.*}.webm"
        echo "Converting \"${filename%.*}.webm\" done."
    fi

    echo ""
done
