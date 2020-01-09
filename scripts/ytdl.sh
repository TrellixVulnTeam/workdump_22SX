#! bash

url=$1
[ -z "${url}" ] && read url
youtube-dl --continue --ignore-errors --extract-audio --audio-format mp3 -f bestaudio ${url}
