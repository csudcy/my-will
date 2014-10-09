#!/bin/bash
pip install virtualenv
pip install virtualenvwrapper

virtualenv --no-site-packages ./venv

cp ./postactivate ./venv/bin/postactivate
chmod +x ./venv/bin/activate
source ./venv/bin/activate

pip install -r ./requirements.txt

python ./run_will.py