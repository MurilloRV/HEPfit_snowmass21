#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/large_kappa_lambda_fits_kappa_framework"


INDIVIDUAL_LAMBDAS=({-5..10})
LAMBDAS=()
WITH_LAMBDA=()
CH=()

for lamb in "${INDIVIDUAL_LAMBDAS[@]}"; do
    LAMBDAS+=("$lamb" "$lamb")
    WITH_LAMBDA+=('no' '')

    CH_value=$(echo "scale=12; ($lamb - 1) * (-2.1290888208276963)" | bc)
    CH+=("$CH_value" "$CH_value")
done

echo "${LAMBDAS[@]}"
echo "${WITH_LAMBDA[@]}"
echo "${CH[@]}"



for ((i=0; i<${#LAMBDAS[@]}; i++)); do
    SCENARIO_PATH="Lambda${LAMBDAS[i]}_FCCee240_FCCee365_${WITH_LAMBDA[i]}HLLHClambda"

    #####################################################################
    ######### GENERAL MODIFICATIONS TO THE CONFIGURATION FILES ##########
    #####################################################################

    mkdir -p "$SCENARIO_PATH/Globalfits/AllOps"
    cd "$SCENARIO_PATH"
    cp ../../different_scenario_fits/SM_FCCee240_FCCee365/*.conf .
    cp ../../different_scenario_fits/SM_FCCee240_FCCee365/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
    cp ../../different_scenario_fits/SM_FCCee240_FCCee365/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf

    NEW_CH="ModelParameter  CH   ${CH[i]}  0.  50.0 "
    sed -i "/ModelParameter  CH                  0.  0.  25./c\\$NEW_CH" Globalfits/AllOps/model_fits.conf

    # Increase prior for CuH_33r to avoid cutoff
    sed -i "/ModelParameter  CuH_33r   0.  0.  4.0/c ModelParameter  CuH_33r   0.  0.  8.0" Globalfits/AllOps/model_fits.conf

    HIGGS_CONF="ObservablesHiggs"
    sed -i "/IncludeFile ObservablesHiggs_FCCee_240_SM.conf/c IncludeFile ObservablesHiggs_FCCee_240_SM_kappa_scaled.conf" ${HIGGS_CONF}.conf
    sed -i "/IncludeFile ObservablesHiggs_FCCee_365.conf/c IncludeFile ObservablesHiggs_FCCee_365_kappa_scaled.conf" ${HIGGS_CONF}.conf
    sed -i "/IncludeFile ObservablesHiggs_HLLHC_SM.conf/c IncludeFile ObservablesHiggs_HLLHC_SM_kappa_scaled.conf" ${HIGGS_CONF}.conf

    EWPO_CONF="ObservablesEW"
    sed -i "/IncludeFile ObservablesEW_FCCee_WW_SM.conf/c IncludeFile ObservablesEW_FCCee_WW_SM_kappa_scaled.conf" ${EWPO_CONF}.conf
    sed -i "/IncludeFile ObservablesEW_FCCee_Zpole_SM.conf/c IncludeFile ObservablesEW_FCCee_Zpole_SM_kappa_scaled.conf" ${EWPO_CONF}.conf
    sed -i "/IncludeFile ObservablesEW_HLLHC.conf/c IncludeFile ObservablesEW_HLLHC_kappa_scaled.conf" ${EWPO_CONF}.conf



    #####################################################################
    ####################### SETUP OF REDUCED PRIORS #####################
    #####################################################################
    cp Globalfits/AllOps/model_fits.conf Globalfits/AllOps/model_fits_small_priors.conf

    sed -i "/ModelParameter  CW   0.  0. .*/c             ModelParameter  CW                     0.  0.  0.2"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHG   0.  0. .*/c            ModelParameter  CHG                    0.  0.  0.08" Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHWB   0.  0. .*/c           ModelParameter  CHWB                   0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHWHB_gaga   0.  0. .*/c     ModelParameter  CHWHB_gaga             0.  0.  0.8"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHWHB_gagaorth   0.  0. .*/c ModelParameter  CHWHB_gagaorth         0.  0.  0.8"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHD   0.  0. .*/c            ModelParameter  CHD                    0.  0.  2.0"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHbox   0.  0. .*/c          ModelParameter  CHbox                  0.  0.  4.0"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CH   0.  0. .*/c             ModelParameter  CH                     0.  0.  20."  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHL1_11   0.  0. .*/c        ModelParameter  CHL1_11                0.  0.  0.2"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHL1_22   0.  0. .*/c        ModelParameter  CHL1_22                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHL1_33   0.  0. .*/c        ModelParameter  CHL1_33                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHL3_11   0.  0. .*/c        ModelParameter  CHL3_11                0.  0.  0.2"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHL3_22   0.  0. .*/c        ModelParameter  CHL3_22                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHL3_33   0.  0. .*/c        ModelParameter  CHL3_33                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHe_11   0.  0. .*/c         ModelParameter  CHe_11                 0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHe_22   0.  0. .*/c         ModelParameter  CHe_22                 0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHe_33   0.  0. .*/c         ModelParameter  CHe_33                 0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHQ1_11   0.  0. .*/c        ModelParameter  CHQ1_11                0.  0.  0.8"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHQ1_33   0.  0. .*/c        ModelParameter  CHQ1_33                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHQ3_11   0.  0. .*/c        ModelParameter  CHQ3_11                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHu_11   0.  0. .*/c         ModelParameter  CHu_11                 0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHd_11   0.  0. .*/c         ModelParameter  CHd_11                 0.  0.  0.3"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CHd_33   0.  0. .*/c         ModelParameter  CHd_33                 0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CeH_22r   0.  0. .*/c        ModelParameter  CeH_22r                0.  0.  0.04" Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CeH_33r   0.  0. .*/c        ModelParameter  CeH_33r                0.  0.  0.12" Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CuH_22r   0.  0. .*/c        ModelParameter  CuH_22r                0.  0.  0.16" Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CuH_33r   0.  0. .*/c        ModelParameter  CuH_33r                0.  0.  8.0"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CdH_33r   0.  0. .*/c        ModelParameter  CdH_33r                0.  0.  0.2"  Globalfits/AllOps/model_fits_small_priors.conf
    sed -i "/ModelParameter  CLL_1221   0.  0. .*/c       ModelParameter  CLL_1221               0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf


    #####################################################################
    ######## SETUP OF MODIFIED MONTE CARLO CONFIGURATION FILES ##########
    #####################################################################
    sed -i "/SignificantDigits 5 /c SignificantDigits 15 " MonteCarlo.conf

    cp MonteCarlo.conf MonteCarlo_short.conf
    cp MonteCarlo.conf MonteCarlo_long.conf
    cp MonteCarlo.conf MonteCarlo_full.conf

    sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              100000 " MonteCarlo_short.conf
    sed -i "/Iterations                 1000000 /c Iterations                 50000 " MonteCarlo_short.conf
    sed -i "/RValueForConvergence  .*/c RValueForConvergence    1.05 " MonteCarlo_short.conf

    sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              1000000 " MonteCarlo_long.conf
    sed -i "/Iterations                 1000000 /c Iterations                 100000 " MonteCarlo_long.conf
    sed -i "/RValueForConvergence  .*/c RValueForConvergence    1.05 " MonteCarlo_long.conf

    sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              5000000 " MonteCarlo_full.conf
    sed -i "/RValueForConvergence  .*/c RValueForConvergence    1.05 " MonteCarlo_full.conf


    mkdir -p results_fits
    mkdir -p results_observables
    cd results_observables
    analysis ../Globalfits/AllOps/model_fits.conf --noMC |& tee observables.txt

    cd $ORIGINAL_PATH
done

python modify_observables.py