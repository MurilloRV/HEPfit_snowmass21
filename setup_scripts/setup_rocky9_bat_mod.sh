#!/bin/bash

setupATLAS
lsetup "views LCG_105 x86_64-el9-gcc11-opt" 

HEPfit_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21"
cd ${HEPfit_dir}

tar xvf ${HEPfit_dir}/bat_mod.tar.gz
tar xvf ${HEPfit_dir}/gslpp.tar.gz
tar xvf ${HEPfit_dir}/HEPfit.tar.gz

export PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat_mod/BAT-1.0.0/build/bin:$PATH"
export LD_LIBRARY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat_mod/BAT-1.0.0/build/lib:$LD_LIBRARY_PATH"
export CPATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat_mod/BAT-1.0.0/build/include:$CPATH"
export PKG_CONFIG_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat_mod/BAT-1.0.0/build/lib/pkgconfig:$PKG_CONFIG_PATH"

# add line "#include <Math/Util.h>" to BCIntegrate.cxx
