#!/usr/bin/env bash

# for mp4 use this
# ffmpeg -i file.gif -movflags +faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" file.mp4

# for webm use this
# ffmpeg -i file.gif -c vp9 -b:v 0 -crf 40 file.webm

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
