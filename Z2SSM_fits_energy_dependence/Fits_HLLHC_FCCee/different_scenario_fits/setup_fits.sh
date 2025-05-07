#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits"
IDM_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_scenario_fits"

IDM_SCENARIOS=('SM_FCCee240' 'SM_FCCee240_FCCee365' 'SM_FCCee240_FCCee365_HLLHClambda' 'IDM_FCCee240' 'IDM_FCCee240_FCCee365' 'IDM_FCCee240_FCCee365_HLLHClambda')
Z2SSM_SCENARIOS=('SM_FCCee240' 'SM_FCCee240_FCCee365' 'SM_FCCee240_FCCee365_HLLHClambda' 'Z2SSM_FCCee240' 'Z2SSM_FCCee240_FCCee365' 'Z2SSM_FCCee240_FCCee365_HLLHClambda')

for ((i=0; i<${#IDM_SCENARIOS[@]}; i++)); do

    mkdir -p "${IDM_SCENARIOS[i]}/Globalfits/AllOps"
    cd "${IDM_SCENARIOS[i]}"
    cp ${ORIGINAL_PATH}/${Z2SSM_SCENARIOS[i]}/*.conf .
    cp ${ORIGINAL_PATH}/${Z2SSM_SCENARIOS[i]}/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
    cp ${ORIGINAL_PATH}/${Z2SSM_SCENARIOS[i]}/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf

    cd $IDM_PATH
done