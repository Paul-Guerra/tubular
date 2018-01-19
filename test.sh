# /bin/bash
# python tests/episode_test.py
# python -m unittest discover -p *_test.py

# If this gets more complicated we can move this to a .coveragerc config file
# coverage run \
#   --omit='.venv/*' \
#   --source=. \
#   -m unittest discover -p *_test.py 
# coverage report -m

# run coverage but only test one file
coverage run tests/utils/files_test.py
coverage report -m