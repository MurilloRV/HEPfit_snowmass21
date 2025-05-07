#!/bin/bash

setupATLAS
lsetup "views LCG_105 x86_64-el9-gcc11-opt" 

export PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat/build_rocky9/bin:$PATH"
export LD_LIBRARY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat/build_rocky9/lib:$LD_LIBRARY_PATH"
export CPATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat/build_rocky9/include:$CPATH"
export PKG_CONFIG_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/bat/build_rocky9/lib/pkgconfig:$PKG_CONFIG_PATH"

# add line "#include <Math/Util.h>" to BCIntegrate.cxx