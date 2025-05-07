#!/bin/bash

setupATLAS
lsetup "views LCG_105 x86_64-el9-gcc11-opt" 

cd /jwd

HEPfit_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21"

tar xvf ${HEPfit_dir}/code/bat_mod.tar.gz
# tar xvf ${HEPfit_dir}/code/gslpp.tar.gz
tar xvf ${HEPfit_dir}/code/HEPfit_snowmass_mod.tar.gz
# tar xvf ${HEPfit_dir}/code/HEPfit_snowmass.tar.gz

export PATH="/jwd/bat_mod/BAT-1.0.0/build/bin:$PATH"
export LD_LIBRARY_PATH="/jwd/bat_mod/BAT-1.0.0/build/lib:$LD_LIBRARY_PATH"
export CPATH="/jwd/bat_mod/BAT-1.0.0/build/include:$CPATH"
export PKG_CONFIG_PATH="/jwd/bat_mod/BAT-1.0.0/build/lib/pkgconfig:$PKG_CONFIG_PATH"

export PATH="/jwd/HEPfit/build/HEPfit/bin:$PATH"

cd ${HEPfit_dir}

# add line "#include <Math/Util.h>" to BCIntegrate.cxx
