#!/bin/bash
pip install openai beautifulsoup4
python3 scripts/hnscrape.py
python3 scripts/hnsummarize.py
python3 scripts/hngenerate.py
