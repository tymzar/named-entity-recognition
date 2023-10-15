#!/bin/bash

main() {
    pip3.10 install -U pip setuptools wheel
    pip3.10 install -U 'spacy[transformers,lookups,apple]'
    python3.10 -m spacy download pl_core_news_lg
}

main
