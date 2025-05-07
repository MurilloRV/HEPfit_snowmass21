#!/bin/bash

cd /jwd
rm -rf python_venv

unset PYTHONHOME
unset PYTHONPATH

module load miniforge/24.7.1-0-py312

tar xf /cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/code/python_venv.tar.gz
source ./python_venv/bin/activate

cd /cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21