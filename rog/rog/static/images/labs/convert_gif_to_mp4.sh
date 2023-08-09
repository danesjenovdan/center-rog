#!/usr/bin/env bash

for filename in *.gif; do
    echo "Converting \"$filename\" -> \"${filename%.*}.mp4\""

    if test -f "${filename%.*}.mp4"; then
        echo "File \"${filename%.*}.mp4\" already exists, skipping."
    else
        ffmpeg -hide_banner -loglevel error -stats -i "$filename" -movflags +faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" "${filename%.*}.mp4"
        echo "Converting \"${filename%.*}.mp4\" done."
    fi

    echo ""
done
