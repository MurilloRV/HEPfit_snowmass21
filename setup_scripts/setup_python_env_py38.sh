#!/bin/bash

cd /jwd
rm -rf python_venv_py38

unset PYTHONHOME
unset PYTHONPATH

module load miniforge/4.9.2-7-py38

tar xf /cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/code/python_venv_py38.tar.gz
source ./python_venv_py38/bin/activate

cd /cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21