#!/usr/bin/env bash
set -x
alias ffmpeg_exe="C:/Users/guzma/Downloads/PortableInstallations/ffmpeg-20190604-d3f236b-win64-static/ffmpeg-20190604-d3f236b-win64-static/bin/ffmpeg.exe"
dump_path="C:/Users/guzma/Music"
mode=${1:-$(read in && echo ${in})}

if [ "${mode}" == "gen" ]; then
    ffmpeg_exe \
        -i "${dump_path}/Frames/framedump0.avi" \
        -i "${dump_path}/Audio/dspdump.wav" \
        -c copy \
        "${dump_path}/dump.avi"
    echo "Dump file: ${dump_path}/dump.avi"
elif [ "${mode}" == "clip" ]; then
    echo "Start time: " && read t1
    echo "End time: " && read t2
    echo "Filename suffix: " && read suff
    ffmpeg_exe \
        -i "${dump_path}\dump.avi" \
        -ss ${t1} \
        -to ${t2} \
        -c copy \
        "${dump_path}/dump_${suff}.avi"
    echo "Clip file: ${dump_path}/dump_${suff}.avi"
elif [ "${mode}" == "sync" ]; then
    echo "Audio offset time: " && read ast
    ffmpeg_exe \
        -i "${dump_path}\dump.avi" \
        -itsoffset ${ast} \
        -i "${dump_path}\dump.avi" \
        -map 1:v \
        -map 0:a \
        -c copy \
        "${dump_path}\dump_ast_${ast}.avi"
    echo "Sync file: ${dump_path}\dump_ast_${ast}.avi"
elif [ "${mode}" == "split" ]; then
    echo "Segment time (format in hh:mm:ss): " && read seg
    ffmpeg_exe \
        -i "${dump_path}\dump.avi" \
        -c copy \
        -map 0 \
        -segment_time ${seg} \
        -f segment \
        -reset_timestamps 1 \
        "${dump_path}\dump_split_%03d.avi"
    echo "Split files: ${dump_path}\dump_split_%03d.avi"
else
    echo "Try adding an available parameter (gen|clip|sync|split)"
fi
echo "Press enter to continue..." && read


