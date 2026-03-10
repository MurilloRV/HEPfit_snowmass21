#!/bin/bash

ORIGINAL_PATH="$BUDDY/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250_350_500_1000/Fits_HLLHC_ILC_250_350_500_1000/GIMR"
TARGET_PATH="$BUDDY/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_ILC_250_350_500_1000/different_BPs"
cd $TARGET_PATH

# Defining the names of the benchmark points to be considered
BP_Names=()
# BP_Names=("BP_"{0..7})

BPO_Names=()
# BPO_Names=("BPO_"{0..1})

BPB_Names=("BPB_2" "BPB_4" "BPB_6")
# BPB_Names=("BPB_"{0..18})

BP_New_Names=()
# BP_New_Names=("BP_new_"{0..10})

BP_others=("BP_lambda1")

BP_Names_Total=("${BP_Names[@]}" "${BPO_Names[@]}" "${BPB_Names[@]}" "${BP_New_Names[@]}" "${BP_others[@]}")


# Using realistic HL-LHC observabless

# Default behavior: all flags set to false
# Exclusive flag
no_1L_BSM_sqrt_s="false" # Excludes the momentum dependence of the BSM k_Zh coupling
no_1L_BSM="false" # Excludes the full BSM contribution to the k_Zh coupling
pure_1L_BSM="false" # Only includes strictly 1L BSM contributions, no SM-like diagrams with insertions of kappa_lambda
no_quad="false" # Excludes the quadratic term in the scaling of the Zh cross-section coming from the 1L BSM contribution
smeft_formula="false" # Using the HEPfit SMEFT expression for sigma_Zh, along with dkappaf
smeft_formula_sqrt="false" # Using the HEPfit SMEFT expression for sigma_Zh, including dkappaf**2 inside of the square root (not correct)
smeft_formula_no_cross="false" # Using the HEPfit SMEFT expression for sigma_Zh, removing cross terms
smeft_formula_external_leg="false" # Using the HEPfit SMEFT expression for sigma_Zh, without the external-leg correction (dkappaf)
smeft_formula_all="false" # Using the HEPfit SMEFT expression for all XS and BR, including 2*dkappaf in the square root to stand in for C_Hbox  (as "_no_cross")
WFR_kala2_input="false" # Include the WFR contribution, proportional to kappa_lambda**2, into the IDM ZH cross-section prediction
WFR_kala2_input_all="false" # Include the WFR contribution, proportional to kappa_lambda**2, into the IDM predictions for all the XS and BR
use_HEPfit_C1_values_WFR_kala2_input_all="false" # Use the HEPfit C1 values, instead of the IDM values. Activates WFR_kala2_input_all as well
use_HEPfit_C1_values_decayrates_WFR_kala2_input_all="true" # Use the HEPfit C1 values, also for the Higgs decay rates, instead of the Z2SSM values. Activates WFR_kala2_input_all as well
use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all="false" # Includes higher-order contributions to the ZZh vertex, beyond the 1L BSM contribution

# Additional, independent flags
modify_all_ewpos="true" # Modify also the EWPO central values for *current* observables, not just future ones
LoopHd6NoSubleading="false" # Do not include the subleading corrections (resummation) in kappa_lambda NLO effects. That is, Sets dZH1 = dZH2 = dZH
noLoopH3d6Quad="false" # Do not include quadratic modifications in the SM loops in Higgs observables due to the dim 6 interactions that contribute to the trilinear Higgs coupling. That is, sets cLH3d62 = 0.0
LoopHd6noWFR="false" # Completely remove the wavefunction renormalization contribution to the kappa_lambda NLO effects. That is, sets dZH1 = dZH2 = 0.0
no_C_HG="false" # Exclude the C_HG operator from the fit
no_HLLHC_Higgs="false" # Exclude the HL-LHC Higgs observables from the fit
LoopH3d6Full="false" # Use the full expansion of the ZH cross-section in terms of C1 and dZH

# TODO: implement new nuisance parameters for ILC!
# use_new_NPs="false" # Use newly implementent theory nuisance parameters
# # theoerr_FCCee240_input="0.001074700180397359" # smaller ellipses
# theoerr_FCCee240_input="0.01148860653191953"  # including blue curve (only 1/Lambda^2)
# # theoerr_FCCee240_input="DEFAULT"

# # theoerr_FCCee365_input="0.0010540963454747359" # smaller ellipses
# theoerr_FCCee365_input="0.011380169070804323"  # including blue curve (only 1/Lambda^2)
# # theoerr_FCCee365_input="DEFAULT"

# NPmismatch_FCCee240_input="0.0"
# # NPmismatch_FCCee240_input="DEFAULT"
# NPmismatch_FCCee365_input="0.0"
# # NPmismatch_FCCee365_input="DEFAULT"

# set_nuisance_parameter() {
#     local input="$1"
#     local default="$2"
#     local scale="$3"
#     if [ "$input" != "DEFAULT" ]; then
#         printf "%.20f" "$(echo "$scale * $input" | bc)"
#     else
#         printf "%.20f" "$(echo "$scale * $default" | bc)"
#     fi
# }

# scale_NPs=$(echo "scale=20.0; scl=2.295748928898636; scl=sqrt(scl); scl" | bc)
# # scale_NPs="1.0"  # default


# Check if more than one exclusive flag is set to "true"
EXCLUSIVE_FLAGS=(
    "$no_1L_BSM_sqrt_s"
    "$no_1L_BSM"
    "$pure_1L_BSM"
    "$no_quad"
    "$smeft_formula"
    "$smeft_formula_sqrt"
    "$smeft_formula_no_cross"
    "$smeft_formula_external_leg"
    "$smeft_formula_all"
    "$WFR_kala2_input"
    "$WFR_kala2_input_all"
    "$use_HEPfit_C1_values_WFR_kala2_input_all"
    "$use_HEPfit_C1_values_decayrates_WFR_kala2_input_all"
    "$use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all"
)

# Count how many flags are set to "true"
true_count=0
for flag in "${EXCLUSIVE_FLAGS[@]}"; do
    if [ "$flag" == "true" ]; then
        ((true_count++))
    fi
done

# Check if more than one flag is "true"
if [ "$true_count" -gt 1 ]; then
    echo "Error: More than one exclusive flag is set to true. Only one such flag can be true at a time."
    return 1
fi


# IDM_SCENARIOS=('IDM_ILC_250_350' 'IDM_ILC_250_350_500' 'IDM_ILC_250_350_500_1000')
IDM_SCENARIOS=('IDM_ILC_250_350' 'IDM_ILC_250_350_500')

for BP_Name in "${BP_Names_Total[@]}"; do

    mkdir -p "${BP_Name}"

    for ((j=0; j<${#IDM_SCENARIOS[@]}; j++)); do

        MODEL_CONF_FILE="model_fits_realistic_HL_LHC"

        # TODO: implement new nuisance parameters for ILC!
        # if [ "$use_new_NPs" == "true" ]; then 
        #     MODEL_CONF_FILE="${MODEL_CONF_FILE}_use_new_NPs"
        #     scale_NPs_formatted=$(printf "%.3g" "$scale_NPs")
        #     if [ "$scale_NPs_formatted" != "1" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_scale${scale_NPs_formatted}"; fi

        #     if [[ "$theoerr_FCCee240_input" != "DEFAULT" || "$theoerr_FCCee365_input" != "DEFAULT" ]]; then
        #         theoerr_FCCee240_path=$(printf "%.3g" "$(echo "$theoerr_FCCee240_input" | bc)" )
        #         theoerr_FCCee365_path=$(printf "%.3g" "$(echo "$theoerr_FCCee365_input" | bc)" )
        #         MODEL_CONF_FILE="${MODEL_CONF_FILE}_theoerr240_${theoerr_FCCee240_path}_theoerr365_${theoerr_FCCee365_path}"
        #     fi

        #     if [[ "$NPmismatch_FCCee240_input" != "DEFAULT" || "$NPmismatch_FCCee365_input" != "DEFAULT" ]]; then
        #         NPmismatch_FCCee240_path=$(printf "%.3g" "$(echo "$NPmismatch_FCCee240_input" | bc)" )
        #         NPmismatch_FCCee365_path=$(printf "%.3g" "$(echo "$NPmismatch_FCCee365_input" | bc)" )
        #         MODEL_CONF_FILE="${MODEL_CONF_FILE}_NPmismatch240_${NPmismatch_FCCee240_path}_NPmismatch365_${NPmismatch_FCCee365_path}"
        #     fi
        # fi

        if [ "$no_1L_BSM_sqrt_s" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_1L_BSM_sqrt_s"; fi
        if [ "$no_1L_BSM" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_1L_BSM"; fi
        if [ "$pure_1L_BSM" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_pure_1L_BSM"; fi
        if [ "$no_quad" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_quad"; fi
        if [ "$smeft_formula" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_smeft_formula"; fi
        if [ "$smeft_formula_sqrt" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_smeft_formula_sqrt"; fi
        if [ "$smeft_formula_no_cross" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_smeft_formula_no_cross"; fi
        if [ "$smeft_formula_external_leg" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_smeft_formula_external_leg"; fi
        if [ "$smeft_formula_all" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_smeft_formula_all"; fi
        if [ "$WFR_kala2_input" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_WFR_kala2_input"; fi
        if [ "$WFR_kala2_input_all" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_WFR_kala2_input_all"; fi
        if [ "$use_HEPfit_C1_values_WFR_kala2_input_all" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_use_HEPfit_C1_values_WFR_kala2_input_all"; fi
        if [ "$use_HEPfit_C1_values_decayrates_WFR_kala2_input_all" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_use_HEPfit_C1_values_decayrates_WFR_kala2_input_all"; fi
        if [ "$use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all"; fi

        if [ "$modify_all_ewpos" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_all_EW_mods"; fi
        if [ "$noLoopH3d6Quad" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_noLoopH3d6Quad"; fi
        if [ "$LoopHd6NoSubleading" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopHd6NoSubleading"; fi
        if [ "$LoopHd6noWFR" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopHd6noWFR"; fi
        if [ "$no_C_HG" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_C_HG"; fi
        if [ "$no_HLLHC_Higgs" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_HLLHC_Higgs"; fi
        if [ "$LoopH3d6Full" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopH3d6Full"; fi

        mkdir -p "${BP_Name}/${IDM_SCENARIOS[j]}/Globalfits/AllOps"
        cd "${BP_Name}/${IDM_SCENARIOS[j]}"
        # cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/*.conf .
        cp ${ORIGINAL_PATH}/*.conf .
        cp ${ORIGINAL_PATH}/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
        cp ${ORIGINAL_PATH}/Globalfits/AllOps/model.conf Globalfits/AllOps/${MODEL_CONF_FILE}.conf

        sed -i "\/IncludeFile ObservablesEW_ILC_250_SM.conf/c\\IncludeFile ObservablesEW_ILC_250_IDM.conf" ObservablesEW_all_mods.conf
        sed -i "\/IncludeFile ObservablesEW_ILC_tt.conf/c\\IncludeFile ObservablesEW_ILC_tt_IDM.conf" ObservablesEW_all_mods.conf
        sed -i "\/IncludeFile ObservablesEW_HLLHC.conf/c\\IncludeFile ObservablesEW_HLLHC_IDM.conf" ObservablesEW_all_mods.conf

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

        # Increase prior for CuH_33r to avoid cutoff
        sed -i "/ModelParameter  CuH_33r   0.  0. .*/c ModelParameter  CuH_33r   0.  0.  8.0" Globalfits/AllOps/${MODEL_CONF_FILE}.conf

        #####################################################################
        ####################### SETUP OF REDUCED PRIORS #####################
        #####################################################################
        cp Globalfits/AllOps/${MODEL_CONF_FILE}.conf Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

        sed -i "/ModelParameter  CW   0.  0. .*/c             ModelParameter  CW                     0.  0.  0.2"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHG   0.  0. .*/c            ModelParameter  CHG                    0.  0.  0.08" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHWB   0.  0. .*/c           ModelParameter  CHWB                   0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHWHB_gaga   0.  0. .*/c     ModelParameter  CHWHB_gaga             0.  0.  0.8"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHWHB_gagaorth   0.  0. .*/c ModelParameter  CHWHB_gagaorth         0.  0.  0.8"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHD   0.  0. .*/c            ModelParameter  CHD                    0.  0.  2.0"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHbox   0.  0. .*/c          ModelParameter  CHbox                  0.  0.  4.0"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CH   0.  0. .*/c             ModelParameter  CH                     0.  0.  20."  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHL1_11   0.  0. .*/c        ModelParameter  CHL1_11                0.  0.  0.2"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHL1_22   0.  0. .*/c        ModelParameter  CHL1_22                0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHL1_33   0.  0. .*/c        ModelParameter  CHL1_33                0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHL3_11   0.  0. .*/c        ModelParameter  CHL3_11                0.  0.  0.2"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHL3_22   0.  0. .*/c        ModelParameter  CHL3_22                0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHL3_33   0.  0. .*/c        ModelParameter  CHL3_33                0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHe_11   0.  0. .*/c         ModelParameter  CHe_11                 0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHe_22   0.  0. .*/c         ModelParameter  CHe_22                 0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHe_33   0.  0. .*/c         ModelParameter  CHe_33                 0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHQ1_11   0.  0. .*/c        ModelParameter  CHQ1_11                0.  0.  0.8"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHQ1_33   0.  0. .*/c        ModelParameter  CHQ1_33                0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHQ3_11   0.  0. .*/c        ModelParameter  CHQ3_11                0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHu_11   0.  0. .*/c         ModelParameter  CHu_11                 0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHd_11   0.  0. .*/c         ModelParameter  CHd_11                 0.  0.  0.3"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CHd_33   0.  0. .*/c         ModelParameter  CHd_33                 0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CeH_22r   0.  0. .*/c        ModelParameter  CeH_22r                0.  0.  0.04" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CeH_33r   0.  0. .*/c        ModelParameter  CeH_33r                0.  0.  0.12" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CuH_22r   0.  0. .*/c        ModelParameter  CuH_22r                0.  0.  0.16" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CuH_33r   0.  0. .*/c        ModelParameter  CuH_33r                0.  0.  8.0"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CdH_33r   0.  0. .*/c        ModelParameter  CdH_33r                0.  0.  0.2"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        sed -i "/ModelParameter  CLL_1221   0.  0. .*/c       ModelParameter  CLL_1221               0.  0.  0.4"  Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf


        #####################################################################
        ######## SETUP OF MODIFIED MONTE CARLO CONFIGURATION FILES ##########
        #####################################################################
        sed -i "/SignificantDigits 5 /c SignificantDigits 15 " MonteCarlo.conf

        cp MonteCarlo.conf MonteCarlo_short.conf
        cp MonteCarlo.conf MonteCarlo_long.conf
        cp MonteCarlo.conf MonteCarlo_full.conf
        cp MonteCarlo.conf MonteCarlo_strict.conf

        sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              100000 " MonteCarlo_short.conf
        sed -i "/Iterations                 1000000 /c Iterations                 50000 " MonteCarlo_short.conf
        sed -i "/RValueForConvergence  .*/c RValueForConvergence    1.1 " MonteCarlo_short.conf

        sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              1000000 " MonteCarlo_long.conf
        sed -i "/Iterations                 1000000 /c Iterations                 100000 " MonteCarlo_long.conf
        sed -i "/RValueForConvergence  .*/c RValueForConvergence    1.1 " MonteCarlo_long.conf

        sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              5000000 " MonteCarlo_full.conf
        sed -i "/RValueForConvergence  .*/c RValueForConvergence    1.1 " MonteCarlo_full.conf

        sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              2000000 " MonteCarlo_strict.conf
        sed -i "/RValueForConvergence  .*/c RValueForConvergence    1.01 " MonteCarlo_strict.conf


        # TODO: implement new nuisance parameters for ILC!
        # ####################################################################################
        # ################### SETUP CONFIG FILES FOR NEW NUISANCE PARAMETERS #################
        # ####################################################################################
        # if [[ "$use_new_NPs" == "true" ]]; then
        #     NEW_NP_CONF="FCCee_new_NPs"
        #     if [ "$scale_NPs_formatted" != "1" ]; then NEW_NP_CONF="${NEW_NP_CONF}_scale${scale_NPs_formatted}"; fi

        #     if [[ "$theoerr_FCCee240_input" != "DEFAULT" || "$theoerr_FCCee365_input" != "DEFAULT" ]]; then
        #         theoerr_FCCee240_path=$(printf "%.3g" "$(echo "$theoerr_FCCee240_input" | bc)" )
        #         theoerr_FCCee365_path=$(printf "%.3g" "$(echo "$theoerr_FCCee365_input" | bc)" )
        #         NEW_NP_CONF="${NEW_NP_CONF}_theoerr240_${theoerr_FCCee240_path}_theoerr365_${theoerr_FCCee365_path}"
        #     fi

        #     if [[ "$NPmismatch_FCCee240_input" != "DEFAULT" || "$NPmismatch_FCCee365_input" != "DEFAULT" ]]; then
        #         NPmismatch_FCCee240_path=$(printf "%.3g" "$(echo "$NPmismatch_FCCee240_input" | bc)" )
        #         NPmismatch_FCCee365_path=$(printf "%.3g" "$(echo "$NPmismatch_FCCee365_input" | bc)" )
        #         NEW_NP_CONF="${NEW_NP_CONF}_NPmismatch240_${NPmismatch_FCCee240_path}_NPmismatch365_${NPmismatch_FCCee365_path}"
        #     fi

        #     NEW_NP_CONF="${NEW_NP_CONF}.conf"

        #     NEW_NP_CONF_INCLUDE="IncludeFile ../../${NEW_NP_CONF}"
        #     sed -i "\%IncludeFile ../../HiggsEW_Par_Corr.conf.*%a #\n$NEW_NP_CONF_INCLUDE" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        #     sed -i "\%IncludeFile ../../HiggsEW_Par_Corr.conf.*%a #\n$NEW_NP_CONF_INCLUDE" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

        #     theoerr_FCCee240=$(set_nuisance_parameter "$theoerr_FCCee240_input" "0.0023295620053664676" "$scale_NPs")
        #     theoerr_FCCee365=$(set_nuisance_parameter "$theoerr_FCCee365_input" "0.0022585758048204183" "$scale_NPs")
        #     NPmismatch_FCCee240=$(set_nuisance_parameter "$NPmismatch_FCCee240_input" "0.006856788995512071" "$scale_NPs")
        #     NPmismatch_FCCee365=$(set_nuisance_parameter "$NPmismatch_FCCee365_input" "0.0034632124670086065" "$scale_NPs")

        #     echo "######################################################################" > $NEW_NP_CONF
        #     echo "# New theory nuisance parameters for FCCee Higgs production" >> $NEW_NP_CONF
        #     echo "# cross-sections" >> $NEW_NP_CONF
        #     echo "######################################################################" >> $NEW_NP_CONF
        #     echo "#" >> $NEW_NP_CONF
        #     echo "ModelParameter  theoerr_FCCee240        0.  ${theoerr_FCCee240}  0." >> $NEW_NP_CONF
        #     echo "ModelParameter  theoerr_FCCee365        0.  ${theoerr_FCCee365}  0." >> $NEW_NP_CONF
            
        #     echo "ModelParameter  NPmismatch_FCCee240        0.  ${NPmismatch_FCCee240}  0." >> $NEW_NP_CONF
        #     echo "ModelParameter  NPmismatch_FCCee365        0.  ${NPmismatch_FCCee365}  0." >> $NEW_NP_CONF
        #     echo "#" >> $NEW_NP_CONF

        # fi


        if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000_HLLHClambda" ]]; then
            MODEL_HIGGS="IncludeFile ../../ObservablesHiggs_scaled_realistic_HL_LHC.conf"
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            HIGGS_CONF="ObservablesHiggs_scaled_realistic_HL_LHC"
            cp ObservablesHiggs.conf ${HIGGS_CONF}.conf
        else
            HIGGS_CONF="ObservablesHiggs"
        fi

        if [ "$noLoopH3d6Quad" == "true" ]; then
            NEW_FlagLoopH3d6Quad="ModelFlag       LoopH3d6Quad    false"
            sed -i "/ModelFlag       LoopH3d6Quad    true/c\\$NEW_FlagLoopH3d6Quad" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "/ModelFlag       LoopH3d6Quad    true/c\\$NEW_FlagLoopH3d6Quad" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        fi

        if [ "$LoopHd6NoSubleading" == "true" ]; then
            NEW_FlagLoopHd6NoSubleading="ModelFlag       LoopHd6NoSubleading    true"
            sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopHd6NoSubleading" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopHd6NoSubleading" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        fi

        if [ "$LoopHd6noWFR" == "true" ]; then
            NEW_FlagLoopHd6noWFR="ModelFlag       LoopHd6noWFR    true"
            sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopHd6noWFR" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopHd6noWFR" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        fi

        if [ "$no_C_HG" == "true" ]; then
            sed -i "/ModelParameter  CHG  .*/c            ModelParameter  CHG                    0.  0.  0." Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "/ModelParameter  CHG  .*/c            ModelParameter  CHG                    0.  0.  0." Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            NEW_d6Ops_CONF="d6Ops_corr_no_C_HG"
            cp Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/${NEW_d6Ops_CONF}.conf
            sed -i "/CorrelatedObservables dim6Ops .*/c CorrelatedObservables dim6Ops 28" Globalfits/AllOps/${NEW_d6Ops_CONF}.conf
            sed -i "/Observable  CHG_corr  CHG  C_{HG}  0.  0.  noMCMC noweight/d" Globalfits/AllOps/${NEW_d6Ops_CONF}.conf
        
            sed -i "/IncludeFile d6Ops_corr.conf/c IncludeFile ${NEW_d6Ops_CONF}.conf" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "/IncludeFile d6Ops_corr.conf/c IncludeFile ${NEW_d6Ops_CONF}.conf" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        fi

        if [ "$no_HLLHC_Higgs" == "true" ]; then
            NEW_HIGGS_CONF="${HIGGS_CONF}_no_HLLHC"
            cp ${HIGGS_CONF}.conf ${NEW_HIGGS_CONF}.conf
            HIGGS_CONF="${NEW_HIGGS_CONF}"

            NEW_HIGGS_HLLHC="# IncludeFile ObservablesHiggs_HLLHC_SM_IDM.conf"
            sed -i "\/ObservablesHiggs_HLLHC_SM_IDM.*/c\\$NEW_HIGGS_HLLHC" ${HIGGS_CONF}.conf

            NEW_MODEL_HIGGS="IncludeFile ../../${HIGGS_CONF}.conf "
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.*/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.*/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            # Increase prior for CuH_33r, CHG, to avoid cutoff. Lack of HL-LHC Higgs observables means that CuH_33r is not constrained by the fit
            sed -i "/ModelParameter  CuH_33r  .*/c ModelParameter  CuH_33r   0.  0.  50.0" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "/ModelParameter  CuH_33r  .*/c ModelParameter  CuH_33r                0.  0.  50.0" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
            sed -i "/ModelParameter  CHG  .*/c ModelParameter  CHG   0.  0.  2.0" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "/ModelParameter  CHG  .*/c ModelParameter  CHG                    0.  0.  2.0" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        fi

        if [ "$LoopH3d6Full" == "true" ]; then
            NEW_FlagLoopH3d6Full="ModelFlag       LoopH3d6Full    true"
            sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopH3d6Full" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagLoopH3d6Full" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
        fi

        if [ "$modify_all_ewpos" == "true" ]; then
            cp ObservablesEW.conf ObservablesEW_all_mods.conf
            NEW_EW_CURRENT="IncludeFile ObservablesEW_Current_SM_noLFU_IDM.conf"
            sed -i "\/IncludeFile ObservablesEW_Current_SM_noLFU.conf/c\\$NEW_EW_CURRENT" ObservablesEW_all_mods.conf

            NEW_MODEL_EWS="IncludeFile ../../ObservablesEW_all_mods.conf "
            sed -i "\/IncludeFile ..\/..\/ObservablesEW.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "\/IncludeFile ..\/..\/ObservablesEW.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            sed -i "\/IncludeFile ObservablesEW_ILC_250_SM.conf/c\\IncludeFile ObservablesEW_ILC_250_IDM.conf" ObservablesEW_all_mods.conf
            sed -i "\/IncludeFile ObservablesEW_HLLHC.conf/c\\IncludeFile ObservablesEW_HLLHC_IDM.conf" ObservablesEW_all_mods.conf
            
             if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500" ]] || \
                [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
                sed -i "\/IncludeFile ObservablesEW_ILC_tt.conf/c\\IncludeFile ObservablesEW_ILC_tt_IDM.conf" ObservablesEW_all_mods.conf
            fi

            EWPO_FLAG="--ewpos_all"
        else
            EWPO_FLAG=""
        fi


        if [[ "$no_1L_BSM_sqrt_s" == "true" || 
              "$no_1L_BSM" == "true" || 
              "$pure_1L_BSM" == "true" || 
              "$no_quad" == "true" || 
              "$smeft_formula" == "true" || 
              "$smeft_formula_sqrt" == "true" || 
              "$smeft_formula_no_cross" == "true" || 
              "$smeft_formula_external_leg" == "true" || 
              "$smeft_formula_all" == "true" || 
              "$WFR_kala2_input" == "true" ||
              "$WFR_kala2_input_all" == "true" ||
              "$use_HEPfit_C1_values_WFR_kala2_input_all" == "true" ||
              "$use_HEPfit_C1_values_decayrates_WFR_kala2_input_all" == "true" ||
              "$use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all" == "true" ]]; then

            FLAG_ARRAY=("no_1L_BSM_sqrt_s" 
                        "no_1L_BSM" 
                        "pure_1L_BSM" 
                        "no_quad" 
                        "smeft_formula" 
                        "smeft_formula_sqrt" 
                        "smeft_formula_no_cross" 
                        "smeft_formula_external_leg" 
                        "smeft_formula_all" 
                        "WFR_kala2_input"
                        "WFR_kala2_input_all"
                        "use_HEPfit_C1_values_WFR_kala2_input_all"
                        "use_HEPfit_C1_values_decayrates_WFR_kala2_input_all"
                        "use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all"
                       )

            for FLAG in "${FLAG_ARRAY[@]}"; do
                if [ "${!FLAG}" == "true" ]; then
                    NEW_HIGGS_CONF="${HIGGS_CONF}_${FLAG}"
                    cp ${HIGGS_CONF}.conf ${NEW_HIGGS_CONF}.conf 
                    HIGGS_CONF="${NEW_HIGGS_CONF}"

                    NEW_HIGGS_250="IncludeFile ObservablesHiggs_ILC_250_IDM_${FLAG}.conf"
                    sed -i "\/ObservablesHiggs_ILC_250_SM.conf/c\\$NEW_HIGGS_250" ${HIGGS_CONF}.conf
                    if [[ "${IDM_SCENARIOS[j]}" != "IDM_ILC_250" ]]; then
                        NEW_HIGGS_350="IncludeFile ObservablesHiggs_ILC_350_IDM_${FLAG}.conf"
                        sed -i "\/ObservablesHiggs_ILC_350_SM.conf/c\\$NEW_HIGGS_350" ${HIGGS_CONF}.conf
                    fi

                    if [[ "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500" || 
                          "${IDM_SCENARIOS[j]}" == "IDM_ILC_250_350_500_1000" ]]; then
                        NEW_HIGGS_500="IncludeFile ObservablesHiggs_ILC_500_IDM_${FLAG}.conf"
                        sed -i "\/ObservablesHiggs_ILC_500_SM.conf/c\\$NEW_HIGGS_500" ${HIGGS_CONF}.conf
                    fi
                    if [[ "$no_HLLHC_Higgs" != "true" ]]; then
                        NEW_HIGGS_HLLHC="IncludeFile ObservablesHiggs_HLLHC_IDM_${FLAG}.conf"
                        sed -i "\/ObservablesHiggs_HLLHC_SM.conf/c\\$NEW_HIGGS_HLLHC" ${HIGGS_CONF}.conf
                    fi

                    NEW_MODEL_HIGGS="IncludeFile ../../${HIGGS_CONF}.conf "

                    sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.*/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
                    sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.*/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
                    

                    PYTHON_ARG="--${FLAG}"

                    cd $TARGET_PATH
                    python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
                    python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
                    python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic ${PYTHON_ARG} --higgsconf ${HIGGS_CONF} ${EWPO_FLAG}
                    # Running the script also without the flag, so that the main fits (i.e. the ones with the flag set to false) are also set up properly

                fi
            done

            
                
        else
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic  --higgsconf ${HIGGS_CONF} ${EWPO_FLAG}
        fi

    done

done