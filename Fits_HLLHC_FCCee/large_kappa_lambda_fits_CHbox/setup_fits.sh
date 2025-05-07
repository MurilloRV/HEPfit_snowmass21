#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/large_kappa_lambda_fits_CHbox"

# INDIVIDUAL_LAMBDAS=({-5..10})
INDIVIDUAL_LAMBDAS=($(seq 0.9 0.05 1.2))
LAMBDAS=()
WITH_LAMBDA=()
CHbox=()

for lamb in "${INDIVIDUAL_LAMBDAS[@]}"; do
    LAMBDAS+=("$lamb" "$lamb")
    WITH_LAMBDA+=('no' '')


    CHbox_value=$(echo "scale=12; ($lamb - 1) * (5.498361921343667)" | bc)
    # CHbox_value=$(echo "scale=12; ($lamb - 1) * (0.5498361921343667)" | bc)
    CHbox+=("$CHbox_value" "$CHbox_value")
done

echo "${LAMBDAS[@]}"
echo "${WITH_LAMBDA[@]}"
echo "${CHbox[@]}"


for ((i=0; i<${#LAMBDAS[@]}; i++)); do
    SCENARIO_PATH="Lambda${LAMBDAS[i]}_FCCee240_FCCee365_${WITH_LAMBDA[i]}HLLHClambda"

    mkdir -p "$SCENARIO_PATH/Globalfits/AllOps"
    cd "$SCENARIO_PATH"
    cp ../../different_scenario_fits/SM_FCCee240_FCCee365/*.conf .
    cp ../../different_scenario_fits/SM_FCCee240_FCCee365/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
    cp ../../different_scenario_fits/SM_FCCee240_FCCee365/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf

    NEW_CHbox="ModelParameter  CHbox   ${CHbox[i]}  0.  50.0 "
    sed -i "/ModelParameter  CHbox   0.  0.  4.0/c\\$NEW_CHbox" Globalfits/AllOps/model_fits.conf

    NEW_CH="ModelParameter  CH   0.  0.  4.0 "
    sed -i "/ModelParameter  CH                  0.  0.  25./c\\$NEW_CH" Globalfits/AllOps/model_fits.conf

    mkdir -p results_fits
    mkdir -p results_observables
    cd results_observables
    ../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_fits.conf --noMC |& tee observables.txt

    cd $ORIGINAL_PATH
done

python modify_observables.py