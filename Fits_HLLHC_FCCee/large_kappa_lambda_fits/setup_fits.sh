#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/large_kappa_lambda_fits"

# LAMBDAS=('2' 
#          '2' 
#          '3' 
#          '3' 
#          '5' 
#          '5' 
#          '6' 
#          '6' 
#          '7' 
#          '7' 
#          '8' 
#          '8' 
#          '9' 
#          '9' 
#          '10' 
#          '10')

INDIVIDUAL_LAMBDAS=({-5..10})
LAMBDAS=()
WITH_LAMBDA=()
CH=()

for lamb in "${INDIVIDUAL_LAMBDAS[@]}"; do
    LAMBDAS+=("$lamb" "$lamb")
    WITH_LAMBDA+=('no' '')


    CH_value=$(echo "scale=12; ($lamb - 1) * (-2.1332885478)" | bc)
    CH+=("$CH_value" "$CH_value")
done

echo "${LAMBDAS[@]}"
echo "${WITH_LAMBDA[@]}"
echo "${CH[@]}"



for ((i=0; i<${#LAMBDAS[@]}; i++)); do
    SCENARIO_PATH="Lambda${LAMBDAS[i]}_FCCee240_FCCee365_${WITH_LAMBDA[i]}HLLHClambda"

    mkdir -p "$SCENARIO_PATH/Globalfits/AllOps"
    cd "$SCENARIO_PATH"
    cp ../../different_scenario_fits/SM_FCCee240_FCCee365/*.conf .
    cp ../../different_scenario_fits/SM_FCCee240_FCCee365/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
    cp ../../different_scenario_fits/SM_FCCee240_FCCee365/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf

    NEW_CH="ModelParameter  CH   ${CH[i]}  0.  50.0 "
    sed -i "/ModelParameter  CH                  0.  0.  25./c\\$NEW_CH" Globalfits/AllOps/model_fits.conf

    mkdir -p results_fits
    mkdir -p results_observables
    cd results_observables
    ../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_fits.conf --noMC |& tee observables.txt

    cd $ORIGINAL_PATH
done

python modify_observables.py