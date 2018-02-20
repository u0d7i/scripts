#/bin/bash
# export chromium bookmarks  to html
# quite an oldschool and reasonably hardcore


#check the gear
for gear in base64 cut date jq sed sqlite3 tr xxd
do
  command -v $gear >/dev/null 2>&1 || { echo  "err: $gear not found"; exit 1; }
done

DDIR="${HOME}/.config/chromium/Default"
TMPD=$(mktemp -d)
EMPTY="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAAE0lEQVR42mP8X8+AFzCOKhhJCgAePhfxCE5/6wAAAABJRU5ErkJggg==" # transparent 16x16 png

# make a local cpoy (to avoid locks)
for ff in ${DDIR}/{Bookmarks,Favicons}
do
  cp $ff $TMPD
done


echo "<html><head><meta charset='utf-8'></head><body>"
cd $TMPD
cat Bookmarks | jq '.roots.other.children[] | "\(.date_added) \(.url) \(.name)"' | sed -e 's/^\"//' -e 's/\"$//' | while read line
do
  # Chrome timestamp is a 64-bit value for microseconds since Jan 1, 1601 00:00 UTC.
  TS=$(date +"%F %T" -d @$(( $(echo $line | cut -d ' ' -f1) / 1000000 + $(date -u +"%s" -d "1601-01-01") )))
  URL=$(echo $line | cut -d ' ' -f2)
  TXT=$(echo $line | cut -d ' ' -f3-)
  ICO=$(echo "select quote(favicon_bitmaps.image_data) from favicon_bitmaps,icon_mapping where icon_mapping.page_url='$URL' and favicon_bitmaps.width=16 and icon_mapping.icon_id=favicon_bitmaps.icon_id;" | sqlite3 Favicons |  cut -d\' -f2 | xxd -r -p | base64 -w 0)
  [[ -z "$ICO" ]] && ICO=$EMPTY
  echo "<img src=\"data:image/png;base64,${ICO}\"><a href=\"${URL}\">${TXT}</a> ($TS)<br>"
done
echo "</body></html>"
cd
rm -rf $TMPD
