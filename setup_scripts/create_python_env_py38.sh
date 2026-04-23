#!/bin/bash

cd /jwd
rm -rf python_venv_py38

module load miniforge/4.9.2-7-py38

python -m venv python_venv_py38
source ./python_venv_py38/bin/activate
python -m pip install --force-reinstall numpy==1.23.5 # pyCollier seems to be incompatible with numpy 2.0+
python -m pip install scipy pandas tqdm matplotlib iminuit uproot hist[plot] PyYAML seaborn
python -m pip install ipykernel ipywidgets
python -m pip install cmake ninja scikit-build build

export CMAKE_ARGS="-DCMAKE_POLICY_VERSION_MINIMUM=3.5" # issue with cmake and pyCollier
export CMAKE_ARGS="-DF2PY_EXECUTABLE=$(which f2py)"
export F2PY=$(which f2py)
python -m pip install --no-build-isolation --no-cache-dir --verbose pyCollier # anyBSM

cd /jwd
tar czf /cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/code/python_venv_py38.tar.gz python_venv_py38

cd /cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21
