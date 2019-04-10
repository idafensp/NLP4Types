#!/bin/bash

set -x

python app.py --log ./log_flask_class.log --classifier /home/isantana/nlp4types/data/results/10Kl_classifier.p --vect /home/isantana/nlp4types/data/results/10Kl_vectorizer.p --ner --sw --model 10KL --collection feedoeg10k
