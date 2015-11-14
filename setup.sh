#!/bin/bash

function unzip_dir {
    gunzip $1/*.gz
    for dir in $1/*; do
	if [ -d $dir ] ; then
	    unzip_dir $dir
	fi
    done 
}

echo 'Downloading dataset...'

#download dataset first,
wget http://opus.lingfil.uu.se/download.php?f=OpenSubtitles/en.tar.gz

echo 'Unzipping dataset...'

#Making assumption that user hasn't put any other tar files in folder
tar -xvf *.gz

echo 'Extracting dataset...'

#extract all files.
for dir in *; do
  if [ -d $dir ] ; then
      unzip_dir $dir
  fi
done

echo 'Running python preprocessor...'

#run python pre-processor
python opensubtitleparser.py

