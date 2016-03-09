#!/bin/bash
cat wet_file_paths | while read f; 
do
  	if [ -f "$f" ]
	then
	    continue
	fi
  mkdir -p `dirname $f`
  echo "Downloading `basename $f` ..."
  echo "---"
  curl https://aws-publicdatasets.s3.amazonaws.com/$f -o `$f`
done

