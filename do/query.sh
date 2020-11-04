echo '[root@s200 libvirt]# cd qe'
/usr/bin/curl -s  "$sh" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%snet"}'
#/usr/bin/curl -s  "$cmzy" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%cmzymem"}' ;
/usr/bin/curl -s  "$xyzq" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%xyzqnet"}'
/usr/bin/curl -s  "$gyyh" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%gyyhnet"}'
/usr/bin/curl -s  "$gtja" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%gtja"}'
/usr/bin/curl -s  "$bggf" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%bg"}';
/usr/bin/curl -s  "$flzy" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%flzy"}'
/usr/bin/curl -s  "$gonghang" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%gsyhnet"}'
/usr/bin/curl -s  "$wcdl" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%wcdlnet"}'
/usr/bin/curl -s  "$slkj" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%slkfnet"}'
/usr/bin/curl -s  "$zgsh" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%zgshnet"}'
/usr/bin/curl -s  "$lggf" |/bin/awk -F , '{print  $4  "test2" "----"  $11/1000 "----" $21/1000 "%lggfnet"}'
echo 'root@s200 qemu]# ^C'
