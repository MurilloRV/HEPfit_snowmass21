#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_scenario_fits"
TARGET_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_BPs"
cd $TARGET_PATH

# BP_Names=("BP_"{0..7})
BPO_Names=("BPO_"{0..1})
BPB_Names=("BPB_"{0..18})
# BP_New_Names=("BP_new_"{0..10})

no_CH_no_CHbox="true"

# BP_Names_Total=("${BP_Names[@]}" "${BPO_Names[@]}" "${BPB_Names[@]}" "${BP_New_Names[@]}")
BP_Names_Total=("${BPO_Names[@]}" "${BPB_Names[@]}")

IDM_SCENARIOS=('IDM_FCCee240' 'IDM_FCCee240_FCCee365' 'IDM_FCCee240_FCCee365_HLLHClambda')

for BP_Name in "${BP_Names_Total[@]}"; do

    mkdir -p "${BP_Name}"

    for ((j=0; j<${#IDM_SCENARIOS[@]}; j++)); do

        mkdir -p "${BP_Name}/${IDM_SCENARIOS[j]}/Globalfits/AllOps"
        cd "${BP_Name}/${IDM_SCENARIOS[j]}"
        cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/*.conf .
        cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
        cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/Globalfits/AllOps/model_fits.conf Globalfits/AllOps/model_fits_realistic_HL_LHC.conf
        # cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/Globalfits/AllOps/model_fits_test_small_priors.conf Globalfits/AllOps/model_fits_realistic_HL_LHC_test_small_priors.conf

        if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
            NEW_HIGGS_CONF="IncludeFile ../../ObservablesHiggs_scaled_realistic_HL_LHC.conf"
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_HIGGS_CONF" Globalfits/AllOps/model_fits_realistic_HL_LHC.conf
            # sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_HIGGS_CONF" Globalfits/AllOps/model_fits_realistic_HL_LHC_test_small_priors.conf
        fi


        if [ "$no_CH_no_CHbox" == "true" ]; then

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
                HIGGS_CONF="ObservablesHiggs_scaled_realistic_HL_LHC"
            else
                HIGGS_CONF="ObservablesHiggs"
            fi
            # HIGGS_CONF="${HIGGS_CONF}.conf"

            cp Globalfits/AllOps/model_fits_realistic_HL_LHC.conf Globalfits/AllOps/model_fits_realistic_HL_LHC_no_CH.conf
            cp Globalfits/AllOps/model_fits_realistic_HL_LHC.conf Globalfits/AllOps/model_fits_realistic_HL_LHC_no_CHbox.conf

            NEW_CH_LINE="ModelParameter  CH                  0.  0.  0. "
                sed -i "/ModelParameter  CH                  0.  0.  50. /c\\$NEW_CH_LINE" Globalfits/AllOps/model_fits_realistic_HL_LHC_no_CH.conf
            NEW_CHbox_LINE="ModelParameter  CHbox   0.  0.  50.0"
                sed -i "/ModelParameter  CHbox   0.  0.  4.0/c\\$NEW_CHbox_LINE" Globalfits/AllOps/model_fits_realistic_HL_LHC_no_CH.conf


            NEW_CHbox_LINE="ModelParameter  CHbox   0.  0.  0."
                sed -i "/ModelParameter  CHbox   0.  0.  4.0/c\\$NEW_CHbox_LINE" Globalfits/AllOps/model_fits_realistic_HL_LHC_no_CHbox.conf
            
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
        else
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
        fi

    done

done