#!/bin/bash

cd /jwd/HEPfit

rm -rf build
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=./HEPfit -DMPIBAT=ON -DBAT_INSTALL=OFF
make
make install

HEPfit_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21"
cd /jwd

tar czf ${HEPfit_dir}/code/HEPfit_snowmass_mod_NPs.tar.gz HEPfit

cd $HEPfit_dir