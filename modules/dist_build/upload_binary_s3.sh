#!/bin/bash

~/s3curl.pl --id=xgen --put=$1 --contentType application/gzip --acl public-read --  http://downloads.mongodb.org.s3.amazonaws.com/$2/$3


