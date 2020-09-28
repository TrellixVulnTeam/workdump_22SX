#!/bin/bash
set -o nounset
cd "$1"
echo "Removing alpha channels..."
ls | grep .png | sort | xargs -I {} convert "{}" -background white -alpha remove -alpha off "{}"
echo "Merging pdf..."
(echo img2pdf\ \\ && \
 ls | grep .png | sort | sed -e 's/ /\\ /g'  | xargs -I {} echo \"{}\"\ \\ && \
 echo -o\ "$1.pdf") > merge.sh
bash merge.sh
rm merge.sh