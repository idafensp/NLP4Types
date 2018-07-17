#!/bin/bash

set -x

python main.py --log ./log_nlp4types_1M_20180622.log --fstep 0 --lstep 10 --prefix 1Ml --abstract --ner --dbonly --ibase /home/isantana/nlp4types/data/ --obase /home/isantana/nlp4types/data/results/ > err_nlp4types.txt 2>&1
