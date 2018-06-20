#$1 is video_id, $2 is original input file, $3 is filetype
mkdir videos/"$1"
mkdir videos/"$1"/frames
cp "$2" videos/"$1"/input."$3"
