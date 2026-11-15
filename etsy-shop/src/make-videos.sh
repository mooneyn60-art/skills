#!/bin/bash
# Stitch 6 scenes per ad into a ~12s 1080x1920 TikTok video: slow push-in per scene + quick crossfades.
set -e
cd "$(dirname "$0")/../tiktok"
D=2.2; X=0.25; FPS=30; N=$(python3 -c "print(int($D*$FPS))")
for ad in santa-mail-set elf-arrival nice-list 2027-planner; do
  in=""; fc=""
  for i in 1 2 3 4 5 6; do
    in="$in -i scenes/$ad-$i.png"
    z=$([ $i = 1 ] && echo 0.0016 || echo 0.0009)   # stronger punch-in on the hook
    fc="$fc[$((i-1)):v]scale=2160:3840,zoompan=z='min(zoom+$z,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$N:s=1080x1920:fps=$FPS,setsar=1,format=yuv420p[v$i];"
  done
  prev="v1"; off=0
  for i in 2 3 4 5 6; do
    off=$(python3 -c "print(round($off+$D-$X,3))")
    fc="$fc[$prev][v$i]xfade=transition=slideleft:duration=$X:offset=$off[x$i];"; prev="x$i"
  done
  ffmpeg -y -loglevel error $in -f lavfi -i anullsrc=r=44100:cl=stereo -filter_complex "${fc%;}" -map "[$prev]" -map 6:a -shortest -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -movflags +faststart "DoodleDesignAndCo-TikTok-$ad.mp4"
  echo "$ad $(ffprobe -v error -show_entries format=duration -of csv=p=0 DoodleDesignAndCo-TikTok-$ad.mp4)s"
done
