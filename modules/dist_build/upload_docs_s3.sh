#!/bin/sh
#
#
# usage : upload_docs_s3.sh  dirname  target
#
#  ex. $ upload_docs_s3.sh target/mongo-dist/docs/html  c++
#
#

for j in `cd $1; find . -type f | sed -e "s/.\///"` 
do
   echo "Uploading : $1/$j to $2/$j"
   ~/s3curl.pl --id=xgen --put=$1/$j --contentType text/html --acl public-read --  http://api.mongodb.org.s3.amazonaws.com/$2/$j
done

