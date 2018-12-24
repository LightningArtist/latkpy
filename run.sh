#!/bin/bash

DIR=$PWD
cd $DIR

INPUT=example/latk_logo.latk
OUTPUT=test.latk

python latk_viz.py -- $DIR/$INPUT $DIR/$OUTPUT