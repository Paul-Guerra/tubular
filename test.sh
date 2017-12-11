# /bin/bash
# python -m unittest discover -p *_test.py
coverage run --omit='.*' -m unittest discover -p *_test.py 
coverage report -m