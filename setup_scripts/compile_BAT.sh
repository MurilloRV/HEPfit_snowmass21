#!/bin/bash

cd /jwd/bat_mod/BAT-1.0.0

HEPfit_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21"

cp ${HEPfit_dir}/HEPfit/BATv1.0.0_parallel-dev/src-dev/* src/
cp ${HEPfit_dir}/HEPfit/BATv1.0.0_parallel-dev/BAT-dev/* BAT/

rm -rf build
mkdir build
./configure --prefix="/jwd/bat_mod/BAT-1.0.0/build" CXX=mpic++
make
make install

cd /jwd

tar czf ${HEPfit_dir}/code/bat_mod.tar.gz bat_mod

cd $HEPfit_dir

# add line "#include <Math/Util.h>" to BCIntegrate.cxx