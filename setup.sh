#!/bin/bash
set -e
pipenv run python -m spacy download en_core_web_trf

pipenv run python script.py
