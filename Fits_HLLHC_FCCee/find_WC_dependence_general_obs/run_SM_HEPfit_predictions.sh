#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/find_WC_dependence_general_obs/"
COPY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits/SM_FCCee240_FCCee365"

mkdir -p observables_results

modify_scheme="true"

# Copying the configuration files 
mkdir -p $ORIGINAL_PATH/Config_Files/Globalfits/AllOps
cd $ORIGINAL_PATH/Config_Files/

cp $COPY_PATH/*.conf .
cp $COPY_PATH/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
cp $COPY_PATH/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf

MODEL_CONF="Globalfits/AllOps/model_fits.conf"
output_file="observables_SM.txt"
if [ "$modify_scheme" = "true" ]; then
    SM_CONF="./SMparameters.conf"
    echo "#" >> $SM_CONF
    echo "ModelFlag  Mw  NORESUM" >> $SM_CONF
    echo "ModelFlag  RhoZ  NORESUM" >> $SM_CONF
    echo "ModelFlag  KappaZ  NORESUM" >> $SM_CONF
    echo "ModelFlag  NoApproximateGammaZ  true" >> $SM_CONF

    output_file="observables_SM_OMSII.txt"

    NEW_MODEL_CONF="Globalfits/AllOps/model_fits_OMSII.conf"
    cp $MODEL_CONF $NEW_MODEL_CONF
    MODEL_CONF=$NEW_MODEL_CONF
fi



EWPO_CURRENT_CONF="./ObservablesEW_Current_SM_noLFU.conf"
echo "#" >> $EWPO_CURRENT_CONF
echo "######################################################################" >> $EWPO_CURRENT_CONF
echo "Observable  sin2thetaEff_C sin2thetaEff sin^{2}#theta_{eff}^{lept} 1. -1. noMCMC noweight" >> $EWPO_CURRENT_CONF


cd ../observables_results
analysis "../Config_Files/${MODEL_CONF}" --noMC |& tee "$output_file"

cd $ORIGINAL_PATH
