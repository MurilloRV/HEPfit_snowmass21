#!/bin/bash

cd /jwd
rm -rf python_venv

unset PYTHONHOME
unset PYTHONPATH

module load miniforge/24.7.1-0-py312

python -m venv python_venv
source ./python_venv/bin/activate
python -m pip install numpy scipy tqdm matplotlib ipykernel

cd /jwd
tar czf /cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/python_venv.tar.gz python_venv

cd /cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21