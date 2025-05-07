#!/bin/bash

cd /jwd/HEPfit

rm -rf build
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=./HEPfit -DMPIBAT=ON -DBAT_INSTALL=OFF
# cmake .. -DCMAKE_INSTALL_PREFIX=./HEPfit -DBAT_INSTALL=OFF
make
make install

HEPfit_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21"
cd /jwd

tar czf ${HEPfit_dir}/code/HEPfit_snowmass_mod.tar.gz HEPfit
# tar czf ${HEPfit_dir}/code/HEPfit_snowmass.tar.gz HEPfit

cd $HEPfit_dir