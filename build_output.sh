#$1 is video_id, $2 is fps, $3 is filetype
ffmpeg -framerate "$2" -start_number 0 -i videos/"$1"/frames/frame%04d.bmp -vcodec mpeg4 -preset ultrafast videos/"$1"/output."$3"
rm -r videos/"$1"/frames
