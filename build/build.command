#!/bin/bash

BUILD_TARGET="../latk.py"

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

cd $DIR

rm $BUILD_TARGET
touch $BUILD_TARGET

cat "main.py" "zip.py" "rdp.py" "kmeans.py" "tilt.py" > $BUILD_TARGET

#cp $BUILD_TARGET "${HOME}/Library/Application Support/Blender/2.77/scripts/addons/"
