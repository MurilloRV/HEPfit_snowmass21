#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_scenario_fits"
TARGET_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_BPs"
cd $TARGET_PATH

# BP_Names=("BP_"{0..7})
BPO_Names=("BPO_"{0..1})
BPB_Names=("BPB_"{0..18})
# BP_New_Names=("BP_new_"{0..10})

modify_all_ewpos="false"
no_1L_BSM_sqrt_s="true"

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
        cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/Globalfits/AllOps/model_fits_test_small_priors.conf Globalfits/AllOps/model_fits_realistic_HL_LHC_test_small_priors.conf

        if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
            NEW_HIGGS_CONF="IncludeFile ../../ObservablesHiggs_scaled_realistic_HL_LHC.conf"
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_HIGGS_CONF" Globalfits/AllOps/model_fits_realistic_HL_LHC.conf
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_HIGGS_CONF" Globalfits/AllOps/model_fits_realistic_HL_LHC_test_small_priors.conf
        fi

        if [ "$modify_all_ewpos" == "true" ]; then
            cp ObservablesEW.conf ObservablesEW_all_mods.conf
            NEW_EW_CURRENT="IncludeFile ObservablesEW_Current_SM_noLFU_kappa_scaled.conf"
            sed -i "\/IncludeFile ObservablesEW_Current_SM_noLFU.conf/c\\$NEW_EW_CURRENT" ObservablesEW_all_mods.conf

            cp Globalfits/AllOps/model_fits_realistic_HL_LHC.conf Globalfits/AllOps/model_fits_realistic_HL_LHC_all_EW_mods.conf
            cp Globalfits/AllOps/model_fits_realistic_HL_LHC_test_small_priors.conf Globalfits/AllOps/model_fits_realistic_HL_LHC_all_EW_mods_test_small_priors.conf

            NEW_MODEL_EWS="IncludeFile ../../ObservablesEW_all_mods.conf "
            sed -i "\/IncludeFile ..\/..\/ObservablesEW.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/model_fits_realistic_HL_LHC_all_EW_mods.conf
            sed -i "\/IncludeFile ..\/..\/ObservablesEW.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/model_fits_realistic_HL_LHC_all_EW_mods_test_small_priors.conf

            cd $TARGET_PATH

            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic --ewpos_all

        elif [ "$no_1L_BSM_sqrt_s" == "true" ]; then

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
                HIGGS_CONF="ObservablesHiggs_scaled_realistic_HL_LHC"
            else
                HIGGS_CONF="ObservablesHiggs"
            fi
            # HIGGS_CONF="${HIGGS_CONF}.conf"

            cp ${HIGGS_CONF}.conf ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf 
            NEW_HIGGS_240="IncludeFile ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_1L_BSM_sqrt_s.conf"
            sed -i "\/ObservablesHiggs_FCCee_240_SM_kappa_scaled.conf/c\\$NEW_HIGGS_240" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf
            if [[ "${IDM_SCENARIOS[j]}" != "IDM_FCCee240" ]]; then
                NEW_HIGGS_365="IncludeFile ObservablesHiggs_FCCee_365_kappa_scaled_no_1L_BSM_sqrt_s.conf"
                sed -i "\/ObservablesHiggs_FCCee_365_kappa_scaled.conf/c\\$NEW_HIGGS_365" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf
            fi
            NEW_HIGGS_HLLHC="IncludeFile ObservablesHiggs_HLLHC_SM_kappa_scaled_no_1L_BSM_sqrt_s.conf"
            sed -i "\/ObservablesHiggs_HLLHC_SM_kappa_scaled.conf/c\\$NEW_HIGGS_HLLHC" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf

            cp Globalfits/AllOps/model_fits_realistic_HL_LHC.conf Globalfits/AllOps/model_fits_realistic_HL_LHC_no_1L_BSM_sqrt_s.conf
            cp Globalfits/AllOps/model_fits_realistic_HL_LHC_test_small_priors.conf Globalfits/AllOps/model_fits_realistic_HL_LHC_no_1L_BSM_sqrt_s_test_small_priors.conf

            NEW_MODEL_HIGGS="IncludeFile ../../${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf "

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs_scaled_realistic_HL_LHC.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/model_fits_realistic_HL_LHC_no_1L_BSM_sqrt_s.conf
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs_scaled_realistic_HL_LHC.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/model_fits_realistic_HL_LHC_no_1L_BSM_sqrt_s_test_small_priors.conf
            else
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/model_fits_realistic_HL_LHC_no_1L_BSM_sqrt_s.conf
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/model_fits_realistic_HL_LHC_no_1L_BSM_sqrt_s_test_small_priors.conf
            fi
            
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic --no_1L_BSM_sqrt_s
        else
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
        fi

    done

done