#!/bin/bash

cd /jwd
rm -rf python_venv_py38

unset PYTHONHOME
unset PYTHONPATH

module load miniforge/4.9.2-7-py38

HEPfit_dir="$BUDDY/HEPfit/HEPfit_snowmass21"

tar xf ${HEPfit_dir}/code/python_venv_py38.tar.gz
source ./python_venv_py38/bin/activate

cd $HEPfit_dir