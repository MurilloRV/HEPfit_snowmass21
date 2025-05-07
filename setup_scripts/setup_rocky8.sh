#!/bin/bash

setupATLAS
lsetup "views LCG_99 x86_64-centos8-gcc10-opt" 

export PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat/build/bin:$PATH"
export LD_LIBRARY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat/build/lib:$LD_LIBRARY_PATH"
export CPATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat/build/include:$CPATH"
export PKG_CONFIG_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat/build/lib/pkgconfig:$PKG_CONFIG_PATH"