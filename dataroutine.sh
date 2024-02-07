#!/usr/bin/bash

VIDEO_EXT=.mkv
AUDIO_EXT=.mp3

echo "$(tput setaf 7)$(tput setab 5)Step 1:$(tput sgr 0)$(tput setaf 7)$(tput setab 4) Creation of Sound Fragments from video files has been started$(tput sgr 0)"

VIDEO_ARGS=()
for f in dataset/video/*${VIDEO_EXT}; do
   VIDEO_ARGS+=("${f##*/}")
done
VIDEO_ARGS_ELEMENTS=${#VIDEO_ARGS[@]}

mkdir dataset/audio

for ((i=0;i<$VIDEO_ARGS_ELEMENTS;i++)); do 
    ffmpeg -hide_banner -loglevel error -ss 00:01:30 -t 30 -i dataset/video/${VIDEO_ARGS[${i}]} dataset/audio/${VIDEO_ARGS[${i}]%%.*}${AUDIO_EXT}
done
echo "$(tput setaf 7)$(tput setab 2)Sound Fragments have been created$(tput sgr 0)"

echo "$(tput setaf 7)$(tput setab 5)Step 2:$(tput sgr 0)$(tput setaf 7)$(tput setab 4) Transcription based on sound fragments has been started$(tput sgr 0)"

AUDIO_ARGS=()
for f in dataset/audio/*${AUDIO_EXT}; do
   AUDIO_ARGS+=("${f##*/}")
done
AUDIO_ARGS_ELEMENTS=${#AUDIO_ARGS[@]}

mkdir dataset/transcripted

for ((i=0;i<$AUDIO_ARGS_ELEMENTS;i++)); do
    tput dim
    whisper --language=en --model=base.en --output_format txt --output_dir dataset/transcripted dataset/audio/${AUDIO_ARGS[${i}]}
    tput sgr 0
done
echo "$(tput setaf 7)$(tput setab 2)Transcriptions have been created$(tput sgr 0)"