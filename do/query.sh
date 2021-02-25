/usr/bin/curl -s  "$SCYY" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%SCYYnet" $2}'
