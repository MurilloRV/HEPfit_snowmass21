#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Z2SSM_fits_energy_dependence/Fits_HLLHC_FCCee/different_scenario_fits"
TARGET_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Z2SSM_fits_energy_dependence/Fits_HLLHC_FCCee/different_BPs"
cd $TARGET_PATH

BP_Names=("BP_"{0..7})
BPO_Names=("BPO_"{0..4})
BPB_Names=("BPB_"{0..12})

BP_Names_Total=("${BP_Names[@]}" "${BPO_Names[@]}" "${BPB_Names[@]}")

Z2SSM_SCENARIOS=('Z2SSM_FCCee240' 'Z2SSM_FCCee240_FCCee365' 'Z2SSM_FCCee240_FCCee365_HLLHClambda')

for BP_Name in "${BP_Names_Total[@]}"; do

    mkdir -p "${BP_Name}"

    for ((j=0; j<${#Z2SSM_SCENARIOS[@]}; j++)); do

        mkdir -p "${BP_Name}/${Z2SSM_SCENARIOS[j]}/Globalfits/AllOps"
        cd "${BP_Name}/${Z2SSM_SCENARIOS[j]}"
        cp ${ORIGINAL_PATH}/${Z2SSM_SCENARIOS[j]}/*.conf .
        cp ${ORIGINAL_PATH}/${Z2SSM_SCENARIOS[j]}/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
        cp ${ORIGINAL_PATH}/${Z2SSM_SCENARIOS[j]}/Globalfits/AllOps/model_fits.conf Globalfits/AllOps/model_fits.conf

        cd $TARGET_PATH

        python scale_observables_kappas.py --scenario ${Z2SSM_SCENARIOS[j]} --bp ${BP_Name} --fast
    done

done