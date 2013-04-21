#!/bin/bash
cd /home/XXX/temp/python
cp records/humi* ftp/
cp records/ambi* ftp/
cp records/temp* ftp/
cp records/baro* ftp/
cd ftp
sshpass -p 'XXXXXXXXXX' sftp -oBatchMode=no -b - XXXX@YYYYY.ZZZ <<EOF
mput temp*
mput humi*
mput ambi*
mput baro*
quit
EOF
rm humi* ambi* temp* baro*
cd ..
wget YYYYY.ZZZ/temp/new/update.php -O logs/wget_recent -q
echo "ftpupload">>logs/ftp.log
date>>logs/ftp.log
echo "finished\n\n">>logs/ftp.log
python move.py
