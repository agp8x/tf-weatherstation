#!/bin/bash
DIR="/home/USER/weather"
SFTPPASS="PASS OR REPLACE WITH KEY"
SFTPUSER="USER@DOMAIN.TLD"
URL="DOMAIN.TLD/PATH/FILE.EXT"

cd $DIR
cp records/humi* ftp/
cp records/ambi* ftp/
cp records/temp* ftp/
cp records/baro* ftp/
cd ftp
# Using a plain password here is evil, but in my context sadly needed
# better use key-authentication, and switch the commented lines
#sftp -oBatchMode=no -b - $SFTPUSER <<EOF
sshpass -p $SFTPPASS sftp -oBatchMode=no -b - $SFTPUSER <<EOF
mput temp*
mput humi*
mput ambi*
mput baro*
quit
EOF
rm humi* ambi* temp* baro*
cd ..
wget $URL -O logs/wget_recent -q
echo "ftpupload">>logs/ftp.log
date>>logs/ftp.log
echo "finished\n\n">>logs/ftp.log
python move.py
