#!/bin/bash


WORKING_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Self_consistent_IDM_fits"
COPY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_BPs"

HEPfit_EXEC="/jwd/HEPfit/build/HEPfit/bin/analysis"

cd $WORKING_PATH

# BP_Names=("BP_"{0..7})
# BPO_Names=("BPO_"{0..1})
BPO_Names=()
# BPB_Names=("BPB_"{0..18})
BPB_Names=("BPB_2" "BPB_4" "BPB_6")
# BP_New_Names=("BP_new_"{0..10})
# BP_others="BP_lambda1"

# Using realistic HL-LHC observables

# Default behavior: all flags set to false
# Exclusive flag
no_1L_BSM_sqrt_s="false" # Excludes the momentum dependence of the BSM k_Zh coupling
no_1L_BSM="false" # Excludes the full BSM contribution to the k_Zh coupling
no_quad="false" # Excludes the quadratic term in the scaling of the Zh cross-section coming from the 1L BSM contribution
smeft_formula="false" # Using the HEPfit SMEFT expression for sigma_Zh, along with dkappaf
smeft_formula_sqrt="false" # Using the HEPfit SMEFT expression for sigma_Zh, including dkappaf**2 inside of the square root (not correct)
smeft_formula_no_cross="false" # Using the HEPfit SMEFT expression for sigma_Zh, removing cross terms
smeft_formula_external_leg="false" # Using the HEPfit SMEFT expression for sigma_Zh, without the external-leg correction (dkappaf)
smeft_formula_all="false" # Using the HEPfit SMEFT expression for all XS and BR, including 2*dkappaf in the square root to stand in for C_Hbox  (as "_no_cross")
WFR_kala2_input="false" # Include the WFR contribution, proportional to kappa_lambda**2, into the IDM ZH cross-section prediction
WFR_kala2_input_all="true" # Include the WFR contribution, proportional to kappa_lambda**2, into the IDM predictions for all the XS and BR

# Additional, independent flags
modify_all_ewpos="true" # Modify also the EWPO central values for *current* observables, not just future ones
LoopHd6NoSubleading="false" # Do not include the subleading corrections (resummation) in kappa_lambda NLO effects. That is, Sets dZH1 = dZH2 = dZH
noLoopH3d6Quad="false" # Do not include quadratic modifications in the SM loops in Higgs observables due to the dim 6 interactions that contribute to the trilinear Higgs coupling. That is, sets cLH3d62 = 0.0
LoopHd6noWFR="false" # Completely remove the wavefunction renormalization contribution to the kappa_lambda NLO effects. That is, sets dZH1 = dZH2 = 0.0
no_C_HG="false" # Exclude the C_HG operator from the fit
no_HLLHC_Higgs="false" # Exclude the HL-LHC Higgs observables from the fit
LoopH3d6Full="false" # Use the full expansion of the ZH cross-section in terms of C1 and dZH

use_new_NPs="false" # Use newly implementent theory nuisance parameters
# scale_NPs=$(echo "scale=20.0; scl=2.295748928898636; scl=sqrt(scl); scl" | bc)
scale_NPs="1.0"  # default

# Check if more than one exclusive flag is set to "true"
EXCLUSIVE_FLAGS=(
    "$no_1L_BSM_sqrt_s"
    "$no_1L_BSM"
    "$no_quad"
    "$smeft_formula"
    "$smeft_formula_sqrt"
    "$smeft_formula_no_cross"
    "$smeft_formula_external_leg"
    "$smeft_formula_all"
    "$WFR_kala2_input"
    "$WFR_kala2_input_all"
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


# BP_Names_Total=("${BP_Names[@]}" "${BPO_Names[@]}" "${BPB_Names[@]}" "${BP_New_Names[@]}")
BP_Names_Total=("${BPO_Names[@]}" "${BPB_Names[@]}")
# BP_Names_Total+=("$BP_others")

# IDM_SCENARIOS=('IDM_FCCee240' 'IDM_FCCee240_FCCee365' 'IDM_FCCee240_FCCee365_HLLHClambda')
IDM_SCENARIOS=('IDM_FCCee240_FCCee365')

for BP_Name in "${BP_Names_Total[@]}"; do

    

    for ((j=0; j<${#IDM_SCENARIOS[@]}; j++)); do

        MODEL_CONF_FILE="model_fits_realistic_HL_LHC"

        if [ "$use_new_NPs" == "true" ]; then 
            MODEL_CONF_FILE="${MODEL_CONF_FILE}_use_new_NPs"
            scale_NPs_formatted=$(printf "%.3g" "$scale_NPs")
            if [ "$scale_NPs_formatted" != "1" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_scale${scale_NPs_formatted}"; fi
        fi

        if [ "$no_1L_BSM_sqrt_s" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_1L_BSM_sqrt_s"; fi
        if [ "$no_1L_BSM" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_1L_BSM"; fi
        if [ "$no_quad" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_quad"; fi
        if [ "$smeft_formula" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_smeft_formula"; fi
        if [ "$smeft_formula_sqrt" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_smeft_formula_sqrt"; fi
        if [ "$smeft_formula_no_cross" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_smeft_formula_no_cross"; fi
        if [ "$smeft_formula_external_leg" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_smeft_formula_external_leg"; fi
        if [ "$smeft_formula_all" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_smeft_formula_all"; fi
        if [ "$WFR_kala2_input" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_WFR_kala2_input"; fi
        if [ "$WFR_kala2_input_all" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_WFR_kala2_input_all"; fi
        
        if [ "$modify_all_ewpos" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_all_EW_mods"; fi
        if [ "$noLoopH3d6Quad" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_noLoopH3d6Quad"; fi
        if [ "$LoopHd6NoSubleading" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopHd6NoSubleading"; fi
        if [ "$LoopHd6noWFR" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopHd6noWFR"; fi
        if [ "$no_C_HG" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_C_HG"; fi
        if [ "$no_HLLHC_Higgs" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_HLLHC_Higgs"; fi
        if [ "$LoopH3d6Full" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopH3d6Full"; fi

        SCENARIO_PATH="${WORKING_PATH}/${BP_Name}/${IDM_SCENARIOS[j]}"
        mkdir -p "$SCENARIO_PATH/Globalfits/AllOps"

        OBS_DIR="${SCENARIO_PATH}/results_${MODEL_CONF_FILE}_small_priors_observables"
        mkdir -p $OBS_DIR

        cd "${COPY_PATH}/${BP_Name}/${IDM_SCENARIOS[j]}"
        $HEPfit_EXEC ./Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf --noMC |& tee "${OBS_DIR}/observables.txt"

        cp ./Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf "$SCENARIO_PATH/Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf"
        cp ./Globalfits/AllOps/d6Ops_corr.conf "$SCENARIO_PATH/Globalfits/AllOps/d6Ops_corr.conf"

        MODEL_CONF_FILE_NP_SCALE=model_fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_small_priors
        cp ./Globalfits/AllOps/$MODEL_CONF_FILE_NP_SCALE.conf "$SCENARIO_PATH/Globalfits/AllOps/$MODEL_CONF_FILE_NP_SCALE.conf"
        cp "./FCCee_new_NPs_scale1.52.conf" "$SCENARIO_PATH/FCCee_new_NPs_scale1.52.conf"
        
        MODEL_CONF_FILE_NP=model_fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_all_EW_mods_small_priors
        cp ./Globalfits/AllOps/$MODEL_CONF_FILE_NP.conf "$SCENARIO_PATH/Globalfits/AllOps/$MODEL_CONF_FILE_NP.conf"
        cp "./FCCee_new_NPs.conf" "$SCENARIO_PATH/FCCee_new_NPs.conf"

        cp ./MonteCarlo*.conf "$SCENARIO_PATH/"

        cd $SCENARIO_PATH
        python ../../modify_observables.py \
            -s ${IDM_SCENARIOS[j]} \
            -b ${BP_Name} \
            --conf ${MODEL_CONF_FILE}_small_priors \
            --workingdir $WORKING_PATH \
            --copydir "${COPY_PATH}/${BP_Name}/${IDM_SCENARIOS[j]}"
    done
done

cd $WORKING_PATH