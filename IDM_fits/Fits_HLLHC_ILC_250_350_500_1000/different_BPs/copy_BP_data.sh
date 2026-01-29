#!/bin/bash

# Warning! Running this scripts will overwrite the content of the BP_yaml_files/ directory!
ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HiggsTools/future_projections/scan_output/IDM_scan_output/BP_yaml_files"
TARGET_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_ILC_250_350_500_1000/different_BPs"
cd $TARGET_PATH

mkdir -p yaml_files_BPs/
cp $ORIGINAL_PATH/* yaml_files_BPs/