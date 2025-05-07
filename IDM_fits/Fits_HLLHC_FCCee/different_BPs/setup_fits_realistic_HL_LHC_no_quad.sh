#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_scenario_fits"
TARGET_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_BPs"
cd $TARGET_PATH

# BP_Names=("BP_"{0..7})
BPO_Names=("BPO_"{0..1})
BPB_Names=("BPB_"{0..18})
# BP_New_Names=("BP_new_"{0..10})

modify_all_ewpos="false"
LoopHd6NoSubleading="false"
noLoopH3d6Quad="false"
LoopHd6noWFR="true"
no_1L_BSM_sqrt_s="false"
no_1L_BSM="false"
no_quad="false"

# BP_Names_Total=("${BP_Names[@]}" "${BPO_Names[@]}" "${BPB_Names[@]}" "${BP_New_Names[@]}")
BP_Names_Total=("${BPO_Names[@]}" "${BPB_Names[@]}")

IDM_SCENARIOS=('IDM_FCCee240' 'IDM_FCCee240_FCCee365' 'IDM_FCCee240_FCCee365_HLLHClambda')

for BP_Name in "${BP_Names_Total[@]}"; do

    mkdir -p "${BP_Name}"

    for ((j=0; j<${#IDM_SCENARIOS[@]}; j++)); do

        MODEL_CONF_FILE="model_fits_realistic_HL_LHC"
        if [ "$noLoopH3d6Quad" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_noLoopH3d6Quad"; fi
        if [ "$LoopHd6NoSubleading" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopHd6NoSubleading"; fi
        if [ "$LoopHd6noWFR" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopHd6noWFR"; fi
        if [ "$modify_all_ewpos" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_all_EW_mods"; fi
        if [ "$no_1L_BSM_sqrt_s" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_1L_BSM_sqrt_s"; fi
        if [ "$no_1L_BSM" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_1L_BSM"; fi
        if [ "$no_quad" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_quad"; fi

        mkdir -p "${BP_Name}/${IDM_SCENARIOS[j]}/Globalfits/AllOps"
        cd "${BP_Name}/${IDM_SCENARIOS[j]}"
        cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/*.conf .
        cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
        cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/Globalfits/AllOps/model_fits.conf Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        # cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/Globalfits/AllOps/model_fits_test_small_priors.conf Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf



        if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
            NEW_HIGGS_CONF="IncludeFile ../../ObservablesHiggs_scaled_realistic_HL_LHC.conf"
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_HIGGS_CONF" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            # sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_HIGGS_CONF" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf
        fi

        if [ "$noLoopH3d6Quad" == "true" ]; then
            NEW_FlagLoopH3d6Quad="ModelFlag       LoopH3d6Quad    false"
            sed -i "/ModelFlag       LoopH3d6Quad    true/c\\$NEW_FlagLoopH3d6Quad" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            # sed -i "/ModelFlag       LoopH3d6Quad    true/c\\$NEW_FlagLoopH3d6Quad" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf
        fi

        if [ "$LoopHd6NoSubleading" == "true" ]; then
            NEW_FlagLoopHd6NoSubleading="ModelFlag       LoopHd6NoSubleading    true"
            sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopHd6NoSubleading" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            # sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopHd6NoSubleading" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf
        fi

        if [ "$LoopHd6noWFR" == "true" ]; then
            NEW_FlagLoopHd6noWFR="ModelFlag       LoopHd6noWFR    true"
            sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopHd6noWFR" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            # sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopHd6noWFR" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf
        fi

        if [ "$modify_all_ewpos" == "true" ]; then
            cp ObservablesEW.conf ObservablesEW_all_mods.conf
            NEW_EW_CURRENT="IncludeFile ObservablesEW_Current_SM_noLFU_kappa_scaled.conf"
            sed -i "\/IncludeFile ObservablesEW_Current_SM_noLFU.conf/c\\$NEW_EW_CURRENT" ObservablesEW_all_mods.conf

            NEW_MODEL_EWS="IncludeFile ../../ObservablesEW_all_mods.conf "
            sed -i "\/IncludeFile ..\/..\/ObservablesEW.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "\/IncludeFile ..\/..\/ObservablesEW.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf

            cd $TARGET_PATH

            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic --ewpos_all

        # Excludes the momentum dependence of the BSM k_Zh coupling
        elif [ "$no_1L_BSM_sqrt_s" == "true" ]; then

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
                HIGGS_CONF="ObservablesHiggs_scaled_realistic_HL_LHC"
            else
                HIGGS_CONF="ObservablesHiggs"
            fi

            cp ${HIGGS_CONF}.conf ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf 
            NEW_HIGGS_240="IncludeFile ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_1L_BSM_sqrt_s.conf"
            sed -i "\/ObservablesHiggs_FCCee_240_SM_kappa_scaled.conf/c\\$NEW_HIGGS_240" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf
            if [[ "${IDM_SCENARIOS[j]}" != "IDM_FCCee240" ]]; then
                NEW_HIGGS_365="IncludeFile ObservablesHiggs_FCCee_365_kappa_scaled_no_1L_BSM_sqrt_s.conf"
                sed -i "\/ObservablesHiggs_FCCee_365_kappa_scaled.conf/c\\$NEW_HIGGS_365" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf
            fi
            NEW_HIGGS_HLLHC="IncludeFile ObservablesHiggs_HLLHC_SM_kappa_scaled_no_1L_BSM_sqrt_s.conf"
            sed -i "\/ObservablesHiggs_HLLHC_SM_kappa_scaled.conf/c\\$NEW_HIGGS_HLLHC" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf


            NEW_MODEL_HIGGS="IncludeFile ../../${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf "

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs_scaled_realistic_HL_LHC.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs_scaled_realistic_HL_LHC.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf
            else
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf
            fi
            
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic --no_1L_BSM_sqrt_s


        # Excluding the full BSM contribution to the k_Zh coupling
        elif [ "$no_1L_BSM" == "true" ]; then

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
                HIGGS_CONF="ObservablesHiggs_scaled_realistic_HL_LHC"
            else
                HIGGS_CONF="ObservablesHiggs"
            fi

            cp ${HIGGS_CONF}.conf ${HIGGS_CONF}_no_1L_BSM.conf 
            NEW_HIGGS_240="IncludeFile ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_1L_BSM.conf"
            sed -i "\/ObservablesHiggs_FCCee_240_SM_kappa_scaled.conf/c\\$NEW_HIGGS_240" ${HIGGS_CONF}_no_1L_BSM.conf
            if [[ "${IDM_SCENARIOS[j]}" != "IDM_FCCee240" ]]; then
                NEW_HIGGS_365="IncludeFile ObservablesHiggs_FCCee_365_kappa_scaled_no_1L_BSM.conf"
                sed -i "\/ObservablesHiggs_FCCee_365_kappa_scaled.conf/c\\$NEW_HIGGS_365" ${HIGGS_CONF}_no_1L_BSM.conf
            fi
            NEW_HIGGS_HLLHC="IncludeFile ObservablesHiggs_HLLHC_SM_kappa_scaled_no_1L_BSM.conf"
            sed -i "\/ObservablesHiggs_HLLHC_SM_kappa_scaled.conf/c\\$NEW_HIGGS_HLLHC" ${HIGGS_CONF}_no_1L_BSM.conf

            NEW_MODEL_HIGGS="IncludeFile ../../${HIGGS_CONF}_no_1L_BSM.conf "

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs_scaled_realistic_HL_LHC.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs_scaled_realistic_HL_LHC.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf
            else
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf
            fi
            
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic --no_1L_BSM



        elif [ "$no_quad" == "true" ]; then

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
                HIGGS_CONF="ObservablesHiggs_scaled_realistic_HL_LHC"
            else
                HIGGS_CONF="ObservablesHiggs"
            fi

            cp ${HIGGS_CONF}.conf ${HIGGS_CONF}_no_quad.conf 
            NEW_HIGGS_240="IncludeFile ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_quad.conf"
            sed -i "\/ObservablesHiggs_FCCee_240_SM_kappa_scaled.conf/c\\$NEW_HIGGS_240" ${HIGGS_CONF}_no_quad.conf
            if [[ "${IDM_SCENARIOS[j]}" != "IDM_FCCee240" ]]; then
                NEW_HIGGS_365="IncludeFile ObservablesHiggs_FCCee_365_kappa_scaled_no_quad.conf"
                sed -i "\/ObservablesHiggs_FCCee_365_kappa_scaled.conf/c\\$NEW_HIGGS_365" ${HIGGS_CONF}_no_quad.conf
            fi
            NEW_HIGGS_HLLHC="IncludeFile ObservablesHiggs_HLLHC_SM_kappa_scaled_no_quad.conf"
            sed -i "\/ObservablesHiggs_HLLHC_SM_kappa_scaled.conf/c\\$NEW_HIGGS_HLLHC" ${HIGGS_CONF}_no_quad.conf

            # cp Globalfits/AllOps/model_fits_realistic_HL_LHC.conf Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            # cp Globalfits/AllOps/model_fits_realistic_HL_LHC_test_small_priors.conf Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf

            NEW_MODEL_HIGGS="IncludeFile ../../${HIGGS_CONF}_no_quad.conf "

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs_scaled_realistic_HL_LHC.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
                # sed -i "\/IncludeFile ..\/..\/ObservablesHiggs_scaled_realistic_HL_LHC.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf
            else
                sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
                # sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_test_small_priors.conf
            fi
            
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic --no_quad

        else
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
        fi

    done

done