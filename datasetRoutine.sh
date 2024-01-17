#!/usr/bin/bash

VIDEO_EXT=.mkv
AUDIO_EXT=.mp3

echo 'Creation of Sound Fragments from video files has been started'

VIDEO_ARGS=()
for f in dataset/video/*${VIDEO_EXT}; do
   VIDEO_ARGS+=("${f##*/}")
done
VIDEO_ARGS_ELEMENTS=${#VIDEO_ARGS[@]}

mkdir dataset/audio

for ((i=0;i<$VIDEO_ARGS_ELEMENTS;i++)); do 
    ffmpeg -ss 00:01:30 -t 30 -i dataset/video/${VIDEO_ARGS[${i}]} dataset/audio/${VIDEO_ARGS[${i}]%%.*}${AUDIO_EXT}
done
echo 'Sound Fragments have been created'

echo 'Transcription based on sound fragments has been started'

AUDIO_ARGS=()
for f in dataset/audio/*${AUDIO_EXT}; do
   AUDIO_ARGS+=("${f##*/}")
done
AUDIO_ARGS_ELEMENTS=${#AUDIO_ARGS[@]}

mkdir dataset/transcripted

for ((i=0;i<$AUDIO_ARGS_ELEMENTS;i++)); do

    whisper --language=en --model=base --output_format txt --output_dir dataset/transcripted dataset/audio/${AUDIO_ARGS[${i}]}
done
echo 'Transcriptions have been created'
