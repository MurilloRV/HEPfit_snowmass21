#!/bin/bash

# Use the SM hepfit model, instead of the SMEFT one, as  a test of the dependence of the EWPOs on the renormalization scheme.

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/find_WC_dependence_general_obs/"
COPY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits/SM_FCCee240_FCCee365"

mkdir -p observables_results

modify_scheme="MIX"
# modify_scheme="false"

# Copying the configuration files 
mkdir -p $ORIGINAL_PATH/Config_Files_SM_model/Globalfits/AllOps
cd $ORIGINAL_PATH/Config_Files_SM_model/

cp $COPY_PATH/*.conf .
cp $COPY_PATH/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
cp $COPY_PATH/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf

MODEL_CONF="Globalfits/AllOps/model_fits.conf"


sed -i '14,671d' $MODEL_CONF
sed -i "/NPSMEFTd6.*/c\\StandardModel" $MODEL_CONF
sed -i "/IncludeFile d6Ops_corr.conf.*/d" $MODEL_CONF
sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf.*/d" $MODEL_CONF
sed -i "\/IncludeFile ..\/..\/ObservablesVV.conf.*/d" $MODEL_CONF
sed -i "\/IncludeFile ..\/..\/EffVHcouplings_QFU12.conf.*/d" $MODEL_CONF
sed -i "\/IncludeFile ..\/..\/HiggsEW_Par_Corr.conf.*/d" $MODEL_CONF


output_file="observables_SM_model"
if [ "$modify_scheme" != "false" ]; then

    if [ "$modify_scheme" != "MIX" ]; then
        sed -i "12a\#" $MODEL_CONF
        sed -i "12a\ModelFlag  KappaZ  $modify_scheme" $MODEL_CONF
        sed -i "12a\#" $MODEL_CONF
        sed -i "12a\ModelFlag  RhoZ  $modify_scheme" $MODEL_CONF
        sed -i "12a\#" $MODEL_CONF
        sed -i "12a\ModelFlag  Mw  $modify_scheme" $MODEL_CONF
        # sed -i "12a\#" $MODEL_CONF
        # sed -i "12a\ModelFlag  NoApproximateGammaZ  true" $MODEL_CONF
    else 
        # sed -i "12a\#" $MODEL_CONF
        # sed -i "12a\ModelFlag  KappaZ  OMSI" $MODEL_CONF
        # sed -i "12a\#" $MODEL_CONF
        # sed -i "12a\ModelFlag  RhoZ  OMSII" $MODEL_CONF
        # sed -i "12a\#" $MODEL_CONF
        # sed -i "12a\ModelFlag  Mw  OMSII" $MODEL_CONF
        sed -i "12a\#" $MODEL_CONF
        sed -i "12a\ModelFlag  NoApproximateGammaZ  true" $MODEL_CONF
    fi

    output_file="${output_file}_${modify_scheme}"

    NEW_MODEL_CONF="Globalfits/AllOps/model_fits_${modify_scheme}.conf"
    cp $MODEL_CONF $NEW_MODEL_CONF
    MODEL_CONF=$NEW_MODEL_CONF
fi



EWPO_CURRENT_CONF="./ObservablesEW_Current_SM_noLFU.conf"
echo "#" >> $EWPO_CURRENT_CONF
echo "######################################################################" >> $EWPO_CURRENT_CONF
echo "Observable  sin2thetaEff_C sin2thetaEff sin^{2}#theta_{eff}^{lept} 1. -1. noMCMC noweight" >> $EWPO_CURRENT_CONF

EWPO_CONF="./ObservablesEW.conf"
echo "#" >> $EWPO_CONF
echo "######################################################################" >> $EWPO_CONF
echo "# Add observable below to obtain HEPfit prediction for Gamma_{Z,had} (not used in the fit)" >> $EWPO_CONF
echo "Observable GammaZhad        GammaZhad         #Gamma_{Z,had} 1. -1.  noMCMC noweight" >> $EWPO_CONF

cd ../observables_results
analysis "../Config_Files_SM_model/${MODEL_CONF}" --noMC |& tee "${output_file}.txt"

cd $ORIGINAL_PATH
