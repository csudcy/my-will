#!/bin/bash
pip install virtualenv

virtualenv --no-site-packages ./venv

chmod +x ./venv/bin/activate
source ./venv/bin/activate

pip install -r ./requirements.txt

python ./run_will.py