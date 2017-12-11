# /bin/bash
# python -m unittest discover -p *_test.py

# If this geta more complicated we can move this to a .coveragerc config file
coverage run \
  --omit='.python_environment/*' \
  --source=. \
  -m unittest discover -p *_test.py 
coverage report -m