#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/large_kappa_lambda_fits"

LAMBDAS=('2' '2' '3' '3' '5' '5' '10' '10')
CH=('-2.1332885478' '-2.1332885478' '-4.2665770957' '-4.2665770957' '-8.5331541914' '-8.5331541914' '-19.1995969306' '-19.1995969306')
# CH=('-4.2665770957' '-4.2665770957' '-6.3998656435' '-6.3998656435' '-10.6664427392' '-10.6664427392' '-21.3328854784' '-21.3328854784')
WITH_LAMBDA=('no' '' 'no' '' 'no' '' 'no' '')


for ((i=0; i<${#LAMBDAS[@]}; i++)); do
    SCENARIO_PATH="Lambda${LAMBDAS[i]}_${WITH_LAMBDA[i]}HLLHClambda"

    mkdir -p "$SCENARIO_PATH/Globalfits/AllOps"
    cd "$SCENARIO_PATH"
    cp ../../different_scenario_fits/SM_noHLLHClambda/*.conf .
    cp ../../different_scenario_fits/SM_noHLLHClambda/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
    cp ../../different_scenario_fits/SM_noHLLHClambda/Globalfits/AllOps/model.conf Globalfits/AllOps/model_fits.conf

    NEW_CH="ModelParameter  CH   ${CH[i]}  0.  50.0 "
    sed -i "/ModelParameter  CH   0.  0.  25.0 /c\\$NEW_CH" Globalfits/AllOps/model_fits.conf

    mkdir -p results_fits
    mkdir -p results_observables
    cd results_observables
    ../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_fits.conf --noMC |& tee observables.txt

    cd $ORIGINAL_PATH

    # mkdir -p "Lambda${LAMBDA}_HLLHClambda"
done

python modify_observables.py