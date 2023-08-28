#!/usr/bin/env bash

for filename in *.gif; do
    echo "Converting \"$filename\" -> \"${filename%.*}.webm\""

    if test -f "${filename%.*}.webm"; then
        echo "File \"${filename%.*}.webm\" already exists, skipping."
    else
        ffmpeg -hide_banner -loglevel error -stats -i "$filename" -c:v libvpx-vp9 -pix_fmt yuva420p "${filename%.*}.webm"
        echo "Converting \"${filename%.*}.webm\" done."
    fi

    echo ""
done
