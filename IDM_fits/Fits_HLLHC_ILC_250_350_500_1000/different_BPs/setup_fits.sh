#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250_350_500_1000/Fits_HLLHC_ILC_250_350_500_1000/GIMR"
TARGET_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_ILC_250_350_500_1000/different_BPs"
cd $TARGET_PATH

# BP_Names=("BP_"{0..7})
# BPO_Names=("BPO_"{0..1})
# BPB_Names=("BPB_"{0..18})
# BP_New_Names=("BP_new_"{0..10})

BPB_Names=("BPB_2" "BPB_4" "BPB_6")

LoopHd6NoSubleading="false"
noLoopH3d6Quad="false"
LoopHd6noWFR="false"

modify_all_ewpos="false"
no_1L_BSM_sqrt_s="false"
no_quad="false"

# BP_Names_Total=("${BP_Names[@]}" "${BPO_Names[@]}" "${BPB_Names[@]}" "${BP_New_Names[@]}")
BP_Names_Total=("${BPB_Names[@]}")

# IDM_SCENARIOS=('IDM_ILC_250_350' 'IDM_ILC_250_350_500' 'IDM_ILC_250_350_500_1000')
IDM_SCENARIOS=('IDM_ILC_250_350' 'IDM_ILC_250_350_500')

for BP_Name in "${BP_Names_Total[@]}"; do

    mkdir -p "${BP_Name}"

    for ((j=0; j<${#IDM_SCENARIOS[@]}; j++)); do

        if [[ "${IDM_SCENARIOS[j]}" != "IDM_ILC_250" ]] && \
           [[ "${IDM_SCENARIOS[j]}" != "IDM_ILC_250_350" ]] && \
           [[ "${IDM_SCENARIOS[j]}" != "IDM_ILC_250_350_500" ]]; then
            echo "Error: Scenario not implemented: ${IDM_SCENARIOS[j]}" >&2
            exit 1
        fi

        MODEL_CONF_FILE="model_fits"
        if [ "$noLoopH3d6Quad" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_noLoopH3d6Quad"; fi
        if [ "$LoopHd6NoSubleading" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopHd6NoSubleading"; fi
        if [ "$LoopHd6noWFR" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopHd6noWFR"; fi
        if [ "$modify_all_ewpos" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_all_EW_mods"; fi
        if [ "$no_1L_BSM_sqrt_s" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_1L_BSM_sqrt_s"; fi
        if [ "$no_quad" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_quad"; fi


        mkdir -p "${BP_Name}/${IDM_SCENARIOS[j]}/Globalfits/AllOps"
        cd "${BP_Name}/${IDM_SCENARIOS[j]}"
        cp ${ORIGINAL_PATH}/*.conf .
        cp ${ORIGINAL_PATH}/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
        cp ${ORIGINAL_PATH}/Globalfits/AllOps/model.conf Globalfits/AllOps/${MODEL_CONF_FILE}.conf



        #####################################################################
        ######### GENERAL MODIFICATIONS TO THE CONFIGURATION FILES ##########
        #####################################################################
        # Vary CH in the fit
        NEW_CH_PRIOR="ModelParameter  CH   0.  0.  50.0 "
        sed -i "/ModelParameter  CH                  0.  0.  0. /c\\$NEW_CH_PRIOR" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        NEW_CH_OBS="Observable  CH_corr  CH  C_{H}  0.  0.  noMCMC noweight"
        sed -i "/Observable  CLL_1221_corr  CLL_1221  C_{LL}  0.  0.  noMCMC noweight/a\\$NEW_CH_OBS" Globalfits/AllOps/d6Ops_corr.conf
        sed -i "/CorrelatedObservables dim6Ops 28/c CorrelatedObservables dim6Ops 29" Globalfits/AllOps/d6Ops_corr.conf

        # Increase prior for CuH_33r to avoid cutoff
        sed -i "/ModelParameter  CuH_33r   0.  0.  4.0/c ModelParameter  CuH_33r   0.  0.  8.0" Globalfits/AllOps/${MODEL_CONF_FILE}.conf

        # Modify theoretical uncertainties
        sed -i "/ModelParameter  eHggint .*/c     ModelParameter  eHggint            0.  0.010   0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHggpar .*/c     ModelParameter  eHggpar            0.  0.005   0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHWWint .*/c     ModelParameter  eHWWint            0.  0.003   0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHWWpar .*/c     ModelParameter  eHWWpar            0.  0.      0.007 " Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHZZint .*/c     ModelParameter  eHZZint            0.  0.003   0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHZZpar .*/c     ModelParameter  eHZZpar            0.  0.      0.007 " Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHZgaint .*/c    ModelParameter  eHZgaint           0.  0.010   0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHZgapar .*/c    ModelParameter  eHZgapar           0.  0.      0.007 " Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHgagaint .*/c   ModelParameter  eHgagaint          0.  0.010   0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHgagapar .*/c   ModelParameter  eHgagapar          0.  0.      0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHmumuint .*/c   ModelParameter  eHmumuint          0.  0.001   0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHmumupar .*/c   ModelParameter  eHmumupar          0.  0.      0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHtautauint .*/c ModelParameter  eHtautauint        0.  0.001   0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHtautaupar .*/c ModelParameter  eHtautaupar        0.  0.      0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHccint .*/c     ModelParameter  eHccint            0.  0.002   0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHccpar .*/c     ModelParameter  eHccpar            0.  0.0101  0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHbbint .*/c     ModelParameter  eHbbint            0.  0.002   0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        sed -i "/ModelParameter  eHbbpar .*/c     ModelParameter  eHbbpar            0.  0.0061  0. "    Globalfits/AllOps/${MODEL_CONF_FILE}.conf

        # Add kappa_lambda observable
        printf "\n# Trilinear Higgs coupling prediction:" >> ObservablesHiggs.conf
        printf "\nObservable deltalHHH_HLLHC    deltalHHH   #delta#lambda_{H^{3}}/#lambda_{SM} 1. -1. noMCMC noweight" >> ObservablesHiggs.conf

        if [[ "${IDM_SCENARIOS[j]}" != "IDM_ILC_250_350" ]] && \
           [[ "${IDM_SCENARIOS[j]}" != "IDM_ILC_250_350_500" ]] && \
           [[ "${IDM_SCENARIOS[j]}" != "IDM_ILC_250_350_500_1000" ]]; then
            # Remove 350 GeV observables
            sed -i "/IncludeFile ObservablesHiggs_ILC_350_SM.conf/c\# IncludeFile ObservablesHiggs_ILC_350_SM.conf" ObservablesHiggs.conf
            sed -i "/IncludeFile ObservablesVV_OO_ILC_350.conf/c\# IncludeFile ObservablesVV_OO_ILC_350.conf" ObservablesVV.conf
        fi
        if [[ "${IDM_SCENARIOS[j]}" != "IDM_ILC_250_350_500" ]] && \
           [[ "${IDM_SCENARIOS[j]}" != "IDM_ILC_250_350_500_1000" ]]; then
            # Remove 500 GeV observables
            sed -i "/IncludeFile ObservablesHiggs_ILC_500_SM.conf/c\# IncludeFile ObservablesHiggs_ILC_500_SM.conf" ObservablesHiggs.conf
            sed -i "/IncludeFile ObservablesVV_OO_ILC_500.conf/c\# IncludeFile ObservablesVV_OO_ILC_500.conf" ObservablesVV.conf
            sed -i "/IncludeFile ObservablesEW_ILC_tt.conf/c\# IncludeFile ObservablesEW_ILC_tt.conf" ObservablesEW.conf
        fi
        if [[ "${IDM_SCENARIOS[j]}" != "IDM_ILC_250_350_500_1000" ]]; then
            # Remove 1000 GeV observables
            sed -i "/IncludeFile ObservablesHiggs_ILC_1000_SM.conf/c\# IncludeFile ObservablesHiggs_ILC_1000_SM.conf" ObservablesHiggs.conf
            sed -i "/IncludeFile ObservablesVV_OO_ILC_1000.conf/c\# IncludeFile ObservablesVV_OO_ILC_1000.conf" ObservablesVV.conf
        fi

        #####################################################################
        ############ SETUP OF THE BSM INPUT CONFIGURATION FILES #############
        #####################################################################
        HIGGS_CONF="ObservablesHiggs_IDM"
        cp ObservablesHiggs.conf ${HIGGS_CONF}.conf
        sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c IncludeFile ..\/..\/${HIGGS_CONF}.conf" Globalfits/AllOps/${MODEL_CONF_FILE}.conf

        cp ObservablesHiggs_HLLHC_SM.conf ObservablesHiggs_HLLHC_IDM.conf
        cp ObservablesHiggs_ILC_250_SM.conf ObservablesHiggs_ILC_250_IDM.conf

        sed -i "/IncludeFile ObservablesHiggs_HLLHC_SM.conf/c IncludeFile ObservablesHiggs_HLLHC_IDM.conf" ${HIGGS_CONF}.conf
        sed -i "/IncludeFile ObservablesHiggs_ILC_250_SM.conf/c IncludeFile ObservablesHiggs_ILC_250_IDM.conf" ${HIGGS_CONF}.conf

        EWPO_CONF="ObservablesEW_IDM"
        cp ObservablesEW.conf ${EWPO_CONF}.conf
        sed -i "\/IncludeFile ..\/..\/ObservablesEW.conf /c IncludeFile ..\/..\/${EWPO_CONF}.conf " Globalfits/AllOps/${MODEL_CONF_FILE}.conf

        cp ObservablesEW_ILC_250_SM.conf ObservablesEW_ILC_250_IDM.conf
        cp ObservablesEW_HLLHC.conf ObservablesEW_HLLHC_IDM.conf
        cp ObservablesEW_Current_SM_noLFU.conf ObservablesEW_ILC_Current_SM_noLFU_IDM.conf

        sed -i "/IncludeFile ObservablesEW_ILC_250_SM.conf/c IncludeFile ObservablesEW_ILC_250_IDM.conf" ${EWPO_CONF}.conf
        sed -i "/IncludeFile ObservablesEW_HLLHC.conf/c IncludeFile ObservablesEW_HLLHC_IDM.conf" ${EWPO_CONF}.conf
        sed -i "/IncludeFile ObservablesEW_ILC_Current_SM_noLFU.conf/c IncludeFile ObservablesEW_ILC_Current_SM_noLFU_IDM.conf" ${EWPO_CONF}.conf

        if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350" ]] || \
           [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500" ]] || \
           [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
            cp ObservablesHiggs_ILC_350_SM.conf ObservablesHiggs_ILC_350_IDM.conf
            sed -i "/IncludeFile ObservablesHiggs_ILC_350_SM.conf/c IncludeFile ObservablesHiggs_ILC_350_IDM.conf" ${HIGGS_CONF}.conf
        fi

        if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500" ]] || \
           [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
            cp ObservablesHiggs_ILC_500_SM.conf ObservablesHiggs_ILC_500_IDM.conf
            sed -i "/IncludeFile ObservablesHiggs_ILC_500_SM.conf/c IncludeFile ObservablesHiggs_ILC_500_IDM.conf" ${HIGGS_CONF}.conf

            cp ObservablesEW_ILC_tt.conf ObservablesEW_ILC_tt_IDM.conf
            sed -i "/IncludeFile ObservablesEW_ILC_tt.conf/c IncludeFile ObservablesEW_ILC_tt_IDM.conf" ${EWPO_CONF}.conf
        fi

        if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
            cp ObservablesHiggs_ILC_1000_SM.conf ObservablesHiggs_ILC_1000_IDM.conf
            sed -i "/IncludeFile ObservablesHiggs_ILC_1000_SM.conf/c IncludeFile ObservablesHiggs_ILC_1000_IDM.conf" ${HIGGS_CONF}.conf
        fi

        #####################################################################
        ######## SETUP OF MODIFIED MONTE CARLO CONFIGURATION FILES ##########
        #####################################################################
        cp MonteCarlo.conf MonteCarlo_short.conf
        cp MonteCarlo.conf MonteCarlo_long.conf
        cp MonteCarlo.conf MonteCarlo_full.conf

        sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              100000 " MonteCarlo_short.conf
        sed -i "/Iterations                 1000000 /c Iterations                 50000 " MonteCarlo_short.conf
        sed -i "/RValueForConvergence    1.01 /c RValueForConvergence    1.1 " MonteCarlo_short.conf

        sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              1000000 " MonteCarlo_long.conf
        sed -i "/Iterations                 1000000 /c Iterations                 100000 " MonteCarlo_long.conf
        sed -i "/RValueForConvergence    1.01 /c RValueForConvergence    1.1 " MonteCarlo_long.conf

        sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              5000000 " MonteCarlo_full.conf
        sed -i "/RValueForConvergence    1.01 /c RValueForConvergence    1.1 " MonteCarlo_full.conf



        #####################################################################
        #################### IMPLEMENTATION OF FLAGS ########################
        #####################################################################
        # A boolean flag that is true if including quadratic modifications in the SM loops in Higgs observables due to the dim 6 interactions that contribute to the trilinear Higgs coupling.
        if [ "$noLoopH3d6Quad" == "true" ]; then
            NEW_FlagLoopH3d6Quad="ModelFlag       LoopH3d6Quad    false"
            sed -i "/ModelFlag       LoopH3d6Quad    true/c\\$NEW_FlagLoopH3d6Quad" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        fi

        # A boolean flag that is true if not including subleading corrections in self-coupling NLO effects
        if [ "$LoopHd6NoSubleading" == "true" ]; then
            NEW_FlagLoopHd6NoSubleading="ModelFlag       LoopHd6NoSubleading    true"
            sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopHd6NoSubleading" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        fi

        # A boolean flag that is true if not including self-coupling NLO effects from wave function renormalization terms
        if [ "$LoopHd6noWFR" == "true" ]; then
            NEW_FlagLoopHd6noWFR="ModelFlag       LoopHd6noWFR    true"
            sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopHd6noWFR" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        fi

        # If set to true, current EWPOs are also modified according to the BSM UV predictions 
        if [ "$modify_all_ewpos" == "true" ]; then

            cp ${EWPO_CONF}.conf ${EWPO_CONF}_all_mods.conf

            # cp ObservablesEW_Current_SM_noLFU.conf ObservablesEW_Current_SM_noLFU_IDM.conf
            NEW_EW_CURRENT="IncludeFile ObservablesEW_Current_SM_noLFU_IDM.conf"
            sed -i "\/IncludeFile ObservablesEW_Current_SM_noLFU.conf/c\\$NEW_EW_CURRENT" ${EWPO_CONF}_all_mods.conf

            NEW_MODEL_EWS="IncludeFile ../../${EWPO_CONF}_all_mods.conf "
            sed -i "\/IncludeFile ..\/..\/${EWPO_CONF}.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf

            cd $TARGET_PATH

            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --ewpos_all

        # If set to true, energy-dependent 1L BSM corrections are not included in the inputs to the ee->ZH cross-sections  
        elif [ "$no_1L_BSM_sqrt_s" == "true" ]; then

            cp ${HIGGS_CONF}.conf ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf 

            NEW_HIGGS_250="IncludeFile ObservablesHiggs_ILC_250_IDM_no_1L_BSM_sqrt_s.conf"
            sed -i "\/ObservablesHiggs_ILC_250_IDM.conf/c\\$NEW_HIGGS_250" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350" ]] || \
               [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500" ]] || \
               [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
                NEW_HIGGS_350="IncludeFile ObservablesHiggs_ILC_350_IDM_no_1L_BSM_sqrt_s.conf"
                sed -i "\/ObservablesHiggs_ILC_350_IDM.conf/c\\$NEW_HIGGS_350" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf
            fi
            if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500" ]] || \
               [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
                NEW_HIGGS_500="IncludeFile ObservablesHiggs_ILC_500_IDM_no_1L_BSM_sqrt_s.conf"
                sed -i "\/ObservablesHiggs_ILC_500_IDM.conf/c\\$NEW_HIGGS_500" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf
            fi
            if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
                NEW_HIGGS_1000="IncludeFile ObservablesHiggs_ILC_1000_IDM_no_1L_BSM_sqrt_s.conf"
                sed -i "\/ObservablesHiggs_ILC_1000_IDM.conf/c\\$NEW_HIGGS_1000" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf
            fi

            NEW_HIGGS_HLLHC="IncludeFile ObservablesHiggs_HLLHC_IDM_no_1L_BSM_sqrt_s.conf"
            sed -i "\/ObservablesHiggs_HLLHC_IDM.conf/c\\$NEW_HIGGS_HLLHC" ${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf

            NEW_MODEL_HIGGS="IncludeFile ../../${HIGGS_CONF}_no_1L_BSM_sqrt_s.conf "
            sed -i "\/IncludeFile ..\/..\/${HIGGS_CONF}.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --no_1L_BSM_sqrt_s

        # If set to true, the cross-sections at ILC are not scaled according to (1 + dk)**2, but according to 1 + 2*dk (i.e. no quadratic correction is included)
        elif [ "$no_quad" == "true" ]; then

            cp ${HIGGS_CONF}.conf ${HIGGS_CONF}_no_quad.conf 

            NEW_HIGGS_250="IncludeFile ObservablesHiggs_ILC_250_IDM_no_quad.conf"
            sed -i "\/ObservablesHiggs_ILC_250_IDM.conf/c\\$NEW_HIGGS_250" ${HIGGS_CONF}_no_quad.conf

            if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350" ]] || \
               [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500" ]] || \
               [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
                NEW_HIGGS_350="IncludeFile ObservablesHiggs_ILC_350_IDM_no_quad.conf"
                sed -i "\/ObservablesHiggs_ILC_350_IDM.conf/c\\$NEW_HIGGS_350" ${HIGGS_CONF}_no_quad.conf
            fi
            if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500" ]] || \
               [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
                NEW_HIGGS_500="IncludeFile ObservablesHiggs_ILC_500_IDM_no_quad.conf"
                sed -i "\/ObservablesHiggs_ILC_500_IDM.conf/c\\$NEW_HIGGS_500" ${HIGGS_CONF}_no_quad.conf
            fi
            if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
                NEW_HIGGS_1000="IncludeFile ObservablesHiggs_ILC_1000_IDM_no_quad.conf"
                sed -i "\/ObservablesHiggs_ILC_1000_IDM.conf/c\\$NEW_HIGGS_1000" ${HIGGS_CONF}_no_quad.conf
            fi

            NEW_HIGGS_HLLHC="IncludeFile ObservablesHiggs_HLLHC_IDM_no_quad.conf"
            sed -i "\/ObservablesHiggs_HLLHC_IDM.conf/c\\$NEW_HIGGS_HLLHC" ${HIGGS_CONF}_no_quad.conf

            NEW_MODEL_HIGGS="IncludeFile ../../${HIGGS_CONF}_no_quad.conf "
            sed -i "\/IncludeFile ..\/..\/${HIGGS_CONF}.conf/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --no_quad

        else
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
        fi

    done

done