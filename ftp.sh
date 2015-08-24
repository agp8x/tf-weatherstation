#!/bin/bash
CONFIG="ftpconfig.xml"
FTP_COMMAND="mput temp*
mput humi*
mput ambi*
mput baro*
quit
"

if [ ! -f $CONFIG ]; then
	echo "configuration file not found, exiting! (see ftpconfig.sample.xml)"
	exit 1;
fi
read DIR SFTPUSER URL SFTPPASS < <(xmlstarlet sel -t -v "//dir" -o $'\t' -v "//sftpuser" -o $'\t' -v "//url" -o $'\t' -v "//sftppass" $CONFIG)

cd $DIR || exit 1
cp records/humi* ftp/
cp records/ambi* ftp/
cp records/temp* ftp/
cp records/baro* ftp/
cd ftp


if [ -z $SFTPPASS ]; then
	#sftp-key-auth
	sftp -oBatchMode=no -b - $SFTPUSER "$FTP_COMMAND"
else
	#sftp-pass-auth
	sshpass -p $SFTPPASS sftp -oBatchMode=no -b - $SFTPUSER "$FTP_COMMAND"
fi
rm humi* ambi* temp* baro*
cd ..
wget $URL -O logs/wget_recent -q
echo "ftpupload">>logs/ftp.log
date>>logs/ftp.log
echo "finished\n\n">>logs/ftp.log
python move.py
