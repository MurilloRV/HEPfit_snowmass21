#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_scenario_fits"
TARGET_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_BPs"
cd $TARGET_PATH

# BP_Names=("BP_"{0..7})
# BPO_Names=("BPO_"{0..1})
BPO_Names=()
# BPB_Names=("BPB_"{0..18})
BPB_Names=("BPB_2" "BPB_4" "BPB_6")
# BP_New_Names=("BP_new_"{0..10})
BP_others="BP_lambda1"

# Using realistic HL-LHC observables

updated_lumi="true" # Use updated luminosity values for the FCC-ee based on the latest projections (DOI:10.17181/n78xk-qcv56)

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
with_Af="true" # Use BSM predictions for sin2theta_eff to evaluate A_f and A_FB_f asymmetries and use these in the fit inputs
EWPO_2L="false" # Use 2-loop IDM predictions for EWPO, instead of 1-loop ones
shifted_sin2thetaEff="true" # Shift the sin2thetaEff value using the HEPfit prediction for the SM
LoopHd6NoSubleading="false" # Do not include the subleading corrections (resummation) in kappa_lambda NLO effects. That is, Sets dZH1 = dZH2 = dZH
noLoopH3d6Quad="false" # Do not include quadratic modifications in the SM loops in Higgs observables due to the dim 6 interactions that contribute to the trilinear Higgs coupling. That is, sets cLH3d62 = 0.0
LoopHd6noWFR="false" # Completely remove the wavefunction renormalization contribution to the kappa_lambda NLO effects. That is, sets dZH1 = dZH2 = 0.0
no_C_HG="false" # Exclude the C_HG operator from the fit
no_HLLHC_Higgs="false" # Exclude the HL-LHC Higgs observables from the fit
LoopH3d6Full="false" # Use the full expansion of the ZH cross-section in terms of C1 and dZH

use_new_NPs="false" # Use newly implementent theory nuisance parameters
UseKlamDependentUncertainties="true" # A boolean flag that is true if using klam-dependent theoretical uncertainties in the ee->Zh cross-section predictions.

# Changed default values to 1.0!
# theoerr_FCCee240_input="1.0"
# theoerr_FCCee240_input="0.001074700180397359" # smaller ellipses
# theoerr_FCCee240_input="0.01148860653191953"  # including blue curve (only 1/Lambda^2)
theoerr_FCCee240_input="DEFAULT"

# theoerr_FCCee365_input="1.0"
# theoerr_FCCee365_input="0.0010540963454747359" # smaller ellipses
# theoerr_FCCee365_input="0.011380169070804323"  # including blue curve (only 1/Lambda^2)
theoerr_FCCee365_input="DEFAULT"

# Changed default values to 0.0!
# NPmismatch_FCCee240_input="0.0"
NPmismatch_FCCee240_input="DEFAULT"
# NPmismatch_FCCee365_input="0.0"
NPmismatch_FCCee365_input="DEFAULT"


# Estimates EXCLUDING the O(1/Lambda_NP^2) curve
# theoerr_FCCee240_function_x2_coef_input="0.00000841930087633563"
# theoerr_FCCee240_function_x1_coef_input="0.00006932472446483649"
# theoerr_FCCee240_function_x0_coef_input="0.00012365304251529146"
# theoerr_FCCee365_function_x2_coef_input="0.00001992550937285446"
# theoerr_FCCee365_function_x1_coef_input="-0.00002663878133908424"
# theoerr_FCCee365_function_x0_coef_input="0.00031254668713761978"

# # Estimates INCLUDING the O(1/Lambda_NP^2) curve
theoerr_FCCee240_function_x2_coef_input="0.00076325757128542970"
theoerr_FCCee240_function_x1_coef_input="-0.00151726083157403824"
theoerr_FCCee240_function_x0_coef_input="0.00076121051962415318"
theoerr_FCCee365_function_x2_coef_input="0.00079217047454317366"
theoerr_FCCee365_function_x1_coef_input="-0.00161839280277012226"
theoerr_FCCee365_function_x0_coef_input="0.00083463246355167890"


set_nuisance_parameter() {
    local input="$1"
    local default="$2"
    local scale="$3"
    if [ "$input" != "DEFAULT" ]; then
        printf "%.20f" "$(echo "$scale * $input" | bc)"
    else
        printf "%.20f" "$(echo "$scale * $default" | bc)"
    fi
}


# scale_NPs=$(echo "scale=20.0; scl=2.295748928898636; scl=sqrt(scl); scl" | bc)
scale_NPs="1.0"  # default

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


# BP_Names_Total=("${BP_Names[@]}" "${BPO_Names[@]}" "${BPB_Names[@]}" "${BP_New_Names[@]}")
BP_Names_Total=("${BPO_Names[@]}" "${BPB_Names[@]}")
BP_Names_Total+=("$BP_others")

# IDM_SCENARIOS=('IDM_FCCee240' 'IDM_FCCee240_FCCee365' 'IDM_FCCee240_FCCee365_HLLHClambda')
# IDM_SCENARIOS=('IDM_FCCee240' 'IDM_FCCee240_FCCee365')
IDM_SCENARIOS=('IDM_FCCee240_FCCee365')

for BP_Name in "${BP_Names_Total[@]}"; do

    mkdir -p "${BP_Name}"

    for ((j=0; j<${#IDM_SCENARIOS[@]}; j++)); do

        MODEL_CONF_FILE="model_fits_realistic_HL_LHC"

        
        if [ "$use_new_NPs" == "true" ]; then 
            MODEL_CONF_FILE="${MODEL_CONF_FILE}_use_new_NPs"
            scale_NPs_formatted=$(printf "%.3g" "$scale_NPs")
            if [ "$scale_NPs_formatted" != "1" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_scale${scale_NPs_formatted}"; fi

            if [[ "$theoerr_FCCee240_input" != "DEFAULT" ]]; then
                theoerr_FCCee240_path=$(printf "%.3g" "$(echo "$theoerr_FCCee240_input" | bc)" )
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_theoerr240_${theoerr_FCCee240_path}"
            fi

            if [[ "$theoerr_FCCee365_input" != "DEFAULT" ]]; then
                theoerr_FCCee365_path=$(printf "%.3g" "$(echo "$theoerr_FCCee365_input" | bc)" )
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_theoerr365_${theoerr_FCCee365_path}"
            fi

            if [[ "$UseKlamDependentUncertainties" == "true" ]]; then
                if [[ "$theoerr_FCCee240_input" != "DEFAULT" || "$theoerr_FCCee365_input" != "DEFAULT" ]]; then
                    echo "Warning: using kappa_lambda dependent uncertainties, but theoerr_FCCee240_input and theoerr_FCCee365_input are not set to DEFAULT (1.0)."
                fi
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_klam_dependent"
                theoerr_FCCee240_function_x2_coef_path=$(printf "%.3g" "$(echo "$theoerr_FCCee240_function_x2_coef_input" | bc)" )
                theoerr_FCCee240_function_x1_coef_path=$(printf "%.3g" "$(echo "$theoerr_FCCee240_function_x1_coef_input" | bc)" )
                theoerr_FCCee240_function_x0_coef_path=$(printf "%.3g" "$(echo "$theoerr_FCCee240_function_x0_coef_input" | bc)" )
                theoerr_FCCee365_function_x2_coef_path=$(printf "%.3g" "$(echo "$theoerr_FCCee365_function_x2_coef_input" | bc)" )
                theoerr_FCCee365_function_x1_coef_path=$(printf "%.3g" "$(echo "$theoerr_FCCee365_function_x1_coef_input" | bc)" )
                theoerr_FCCee365_function_x0_coef_path=$(printf "%.3g" "$(echo "$theoerr_FCCee365_function_x0_coef_input" | bc)" )
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_a240_${theoerr_FCCee240_function_x2_coef_path}"
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_b240_${theoerr_FCCee240_function_x1_coef_path}"
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_c240_${theoerr_FCCee240_function_x0_coef_path}"
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_a365_${theoerr_FCCee365_function_x2_coef_path}"
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_b365_${theoerr_FCCee365_function_x1_coef_path}"
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_c365_${theoerr_FCCee365_function_x0_coef_path}"
            fi

            if [[ "$NPmismatch_FCCee240_input" != "DEFAULT" ]]; then
                NPmismatch_FCCee240_path=$(printf "%.3g" "$(echo "$NPmismatch_FCCee240_input" | bc)" )
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_NPmismatch240_${NPmismatch_FCCee240_path}"
            fi

            if [[ "$NPmismatch_FCCee365_input" != "DEFAULT" ]]; then
                NPmismatch_FCCee365_path=$(printf "%.3g" "$(echo "$NPmismatch_FCCee365_input" | bc)" )
                MODEL_CONF_FILE="${MODEL_CONF_FILE}_NPmismatch365_${NPmismatch_FCCee365_path}"
            fi
        fi

        if [ "$updated_lumi" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_updated_lumi"; fi

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
        if [ "$with_Af" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_with_Af"; fi
        if [ "$EWPO_2L" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_EWPO_2L"; fi
        if [ "$shifted_sin2thetaEff" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_shifted_sin2thetaEff"; fi
        if [ "$noLoopH3d6Quad" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_noLoopH3d6Quad"; fi
        if [ "$LoopHd6NoSubleading" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopHd6NoSubleading"; fi
        if [ "$LoopHd6noWFR" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopHd6noWFR"; fi
        if [ "$no_C_HG" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_C_HG"; fi
        if [ "$no_HLLHC_Higgs" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_no_HLLHC_Higgs"; fi
        if [ "$LoopH3d6Full" == "true" ]; then MODEL_CONF_FILE="${MODEL_CONF_FILE}_LoopH3d6Full"; fi

        mkdir -p "${BP_Name}/${IDM_SCENARIOS[j]}/Globalfits/AllOps"
        cd "${BP_Name}/${IDM_SCENARIOS[j]}"
        cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/*.conf .
        cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
        cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/Globalfits/AllOps/model_fits.conf Globalfits/AllOps/${MODEL_CONF_FILE}.conf
        # cp ${ORIGINAL_PATH}/${IDM_SCENARIOS[j]}/Globalfits/AllOps/model_fits_small_priors.conf Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

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


        ####################################################################################
        ################### SETUP CONFIG FILES FOR NEW NUISANCE PARAMETERS #################
        ####################################################################################
        if [[ "$use_new_NPs" == "true" ]]; then
            NEW_NP_CONF="FCCee_new_NPs"
            if [ "$scale_NPs_formatted" != "1" ]; then NEW_NP_CONF="${NEW_NP_CONF}_scale${scale_NPs_formatted}"; fi

            if [[ "$theoerr_FCCee240_input" != "DEFAULT" ]]; then
                theoerr_FCCee240_path=$(printf "%.3g" "$(echo "$theoerr_FCCee240_input" | bc)" )
                NEW_NP_CONF="${NEW_NP_CONF}_theoerr240_${theoerr_FCCee240_path}"
            fi

            if [[ "$theoerr_FCCee365_input" != "DEFAULT" ]]; then
                theoerr_FCCee365_path=$(printf "%.3g" "$(echo "$theoerr_FCCee365_input" | bc)" )
                NEW_NP_CONF="${NEW_NP_CONF}_theoerr365_${theoerr_FCCee365_path}"
            fi

            if [[ "$UseKlamDependentUncertainties" == "true" ]]; then
                NEW_NP_CONF="${NEW_NP_CONF}_klam_dependent"
                NEW_NP_CONF="${NEW_NP_CONF}_a240_${theoerr_FCCee240_function_x2_coef_path}"
                NEW_NP_CONF="${NEW_NP_CONF}_b240_${theoerr_FCCee240_function_x1_coef_path}"
                NEW_NP_CONF="${NEW_NP_CONF}_c240_${theoerr_FCCee240_function_x0_coef_path}"
                NEW_NP_CONF="${NEW_NP_CONF}_a365_${theoerr_FCCee365_function_x2_coef_path}"
                NEW_NP_CONF="${NEW_NP_CONF}_b365_${theoerr_FCCee365_function_x1_coef_path}"
                NEW_NP_CONF="${NEW_NP_CONF}_c365_${theoerr_FCCee365_function_x0_coef_path}"

                theoerr_FCCee240_function_x2_coef=$theoerr_FCCee240_function_x2_coef_input
                theoerr_FCCee240_function_x1_coef=$theoerr_FCCee240_function_x1_coef_input
                theoerr_FCCee240_function_x0_coef=$theoerr_FCCee240_function_x0_coef_input
                theoerr_FCCee365_function_x2_coef=$theoerr_FCCee365_function_x2_coef_input
                theoerr_FCCee365_function_x1_coef=$theoerr_FCCee365_function_x1_coef_input
                theoerr_FCCee365_function_x0_coef=$theoerr_FCCee365_function_x0_coef_input

                NEW_FlagUseKlamDependentUncertainties="ModelFlag       UseKlamDependentUncertainties    true"
                sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagUseKlamDependentUncertainties" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
                sed -i "/ModelFlag       LoopH3d6Quad    true/a #\n\\$NEW_FlagUseKlamDependentUncertainties" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            else
                theoerr_FCCee240_function_x2_coef="0.0"
                theoerr_FCCee240_function_x1_coef="0.0"
                theoerr_FCCee240_function_x0_coef="0.0"
                theoerr_FCCee365_function_x2_coef="0.0"
                theoerr_FCCee365_function_x1_coef="0.0"
                theoerr_FCCee365_function_x0_coef="0.0"

                if [[ "$theoerr_FCCee240_function_x2_coef_path" != "0.0" || 
                      "$theoerr_FCCee240_function_x1_coef_path" != "0.0" || 
                      "$theoerr_FCCee240_function_x0_coef_path" != "0.0" || 
                      "$theoerr_FCCee365_function_x2_coef_path" != "0.0" || 
                      "$theoerr_FCCee365_function_x1_coef_path" != "0.0" || 
                      "$theoerr_FCCee365_function_x0_coef_path" != "0.0" ]]; then
                    echo "Warning: using nonzero values for the coefficients of the klam-dependent uncertainties, but UseKlamDependentUncertainties is not set to true. These coefficients will be ignored."
                fi
            fi

            if [[ "$NPmismatch_FCCee240_input" != "DEFAULT" ]]; then
                NPmismatch_FCCee240_path=$(printf "%.3g" "$(echo "$NPmismatch_FCCee240_input" | bc)" )
                NEW_NP_CONF="${NEW_NP_CONF}_NPmismatch240_${NPmismatch_FCCee240_path}"
            fi

            if [[ "$NPmismatch_FCCee365_input" != "DEFAULT" ]]; then
                NPmismatch_FCCee365_path=$(printf "%.3g" "$(echo "$NPmismatch_FCCee365_input" | bc)" )
                NEW_NP_CONF="${NEW_NP_CONF}_NPmismatch365_${NPmismatch_FCCee365_path}"
            fi

            NEW_NP_CONF="${NEW_NP_CONF}.conf"

            NEW_NP_CONF_INCLUDE="IncludeFile ../../${NEW_NP_CONF}"
            sed -i "\%IncludeFile ../../HiggsEW_Par_Corr.conf.*%a #\n$NEW_NP_CONF_INCLUDE" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "\%IncludeFile ../../HiggsEW_Par_Corr.conf.*%a #\n$NEW_NP_CONF_INCLUDE" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            # Old default values
            # theoerr_FCCee240=$(set_nuisance_parameter "$theoerr_FCCee240_input" "0.0023295620053664676" "$scale_NPs")
            # theoerr_FCCee365=$(set_nuisance_parameter "$theoerr_FCCee365_input" "0.0022585758048204183" "$scale_NPs")
            # NPmismatch_FCCee240=$(set_nuisance_parameter "$NPmismatch_FCCee240_input" "0.006856788995512071" "$scale_NPs")
            # NPmismatch_FCCee365=$(set_nuisance_parameter "$NPmismatch_FCCee365_input" "0.0034632124670086065" "$scale_NPs")

            theoerr_FCCee240=$(set_nuisance_parameter "$theoerr_FCCee240_input" "1.0" "$scale_NPs")
            theoerr_FCCee365=$(set_nuisance_parameter "$theoerr_FCCee365_input" "1.0" "$scale_NPs")
            NPmismatch_FCCee240=$(set_nuisance_parameter "$NPmismatch_FCCee240_input" "0.0" "$scale_NPs")
            NPmismatch_FCCee365=$(set_nuisance_parameter "$NPmismatch_FCCee365_input" "0.0" "$scale_NPs")

            echo "######################################################################" > $NEW_NP_CONF
            echo "# New theory nuisance parameters for FCCee Higgs production" >> $NEW_NP_CONF
            echo "# cross-sections" >> $NEW_NP_CONF
            echo "######################################################################" >> $NEW_NP_CONF
            echo "#" >> $NEW_NP_CONF
            echo "ModelParameter  theoerr_FCCee240        0.  ${theoerr_FCCee240}  0." >> $NEW_NP_CONF
            echo "ModelParameter  theoerr_FCCee365        0.  ${theoerr_FCCee365}  0." >> $NEW_NP_CONF
            
            echo "ModelParameter  NPmismatch_FCCee240        0.  ${NPmismatch_FCCee240}  0." >> $NEW_NP_CONF
            echo "ModelParameter  NPmismatch_FCCee365        0.  ${NPmismatch_FCCee365}  0." >> $NEW_NP_CONF

            echo "ModelParameter  theoerr_FCCee240_function_x2_coef        ${theoerr_FCCee240_function_x2_coef}  0.  0." >> $NEW_NP_CONF
            echo "ModelParameter  theoerr_FCCee240_function_x1_coef        ${theoerr_FCCee240_function_x1_coef}  0.  0." >> $NEW_NP_CONF
            echo "ModelParameter  theoerr_FCCee240_function_x0_coef        ${theoerr_FCCee240_function_x0_coef}  0.  0." >> $NEW_NP_CONF
            echo "ModelParameter  theoerr_FCCee365_function_x2_coef        ${theoerr_FCCee365_function_x2_coef}  0.  0." >> $NEW_NP_CONF
            echo "ModelParameter  theoerr_FCCee365_function_x1_coef        ${theoerr_FCCee365_function_x1_coef}  0.  0." >> $NEW_NP_CONF
            echo "ModelParameter  theoerr_FCCee365_function_x0_coef        ${theoerr_FCCee365_function_x0_coef}  0.  0." >> $NEW_NP_CONF
            echo "#" >> $NEW_NP_CONF

        fi


        if [[ "${IDM_SCENARIOS[j]}" == "IDM_FCCee240_FCCee365_HLLHClambda" ]]; then
            MODEL_HIGGS="IncludeFile ../../ObservablesHiggs_scaled_realistic_HL_LHC.conf"
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.conf/c\\$MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            HIGGS_CONF="ObservablesHiggs_scaled_realistic_HL_LHC"
            cp ObservablesHiggs.conf ${HIGGS_CONF}.conf
        else
            HIGGS_CONF="ObservablesHiggs"
        fi

        HIGGS_240_CONF="ObservablesHiggs_FCCee_240_SM"
        HIGGS_365_CONF="ObservablesHiggs_FCCee_365"
        HIGGS_PYTHON_ARG=""
        if [ "$updated_lumi" == "true" ]; then
            NEW_HIGGS_CONF="${HIGGS_CONF}_updated_lumi"
            cp ${HIGGS_CONF}.conf ${NEW_HIGGS_CONF}.conf
            HIGGS_CONF="${NEW_HIGGS_CONF}"

            NEW_HIGGS_240_CONF="ObservablesHiggs_FCCee_240_SM_updated_lumi"
            cp ${NEW_HIGGS_240_CONF}.conf ${NEW_HIGGS_240_CONF}_kappa_scaled.conf
            
            NEW_HIGGS_365_CONF="ObservablesHiggs_FCCee_365_updated_lumi"
            cp ${NEW_HIGGS_365_CONF}.conf ${NEW_HIGGS_365_CONF}_kappa_scaled.conf


            NEW_HIGGS_240="IncludeFile ${NEW_HIGGS_240_CONF}_kappa_scaled.conf"
            sed -i "\/${HIGGS_240_CONF}_kappa_scaled.conf/c\\$NEW_HIGGS_240" ${HIGGS_CONF}.conf
            if [[ "${IDM_SCENARIOS[j]}" != "IDM_FCCee240" ]]; then
                NEW_HIGGS_365="IncludeFile ${NEW_HIGGS_365_CONF}_kappa_scaled.conf"
                sed -i "\/${HIGGS_365_CONF}_kappa_scaled.conf/c\\$NEW_HIGGS_365" ${HIGGS_CONF}.conf
            fi

            HIGGS_240_CONF="${NEW_HIGGS_240_CONF}"
            HIGGS_365_CONF="${NEW_HIGGS_365_CONF}"
            HIGGS_PYTHON_ARG="--updated_lumi"
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

            NEW_HIGGS_HLLHC="# IncludeFile ObservablesHiggs_HLLHC_SM_kappa_scaled.conf"
            sed -i "\/ObservablesHiggs_HLLHC_SM_kappa_scaled.*/c\\$NEW_HIGGS_HLLHC" ${HIGGS_CONF}.conf

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

        EWPO_PYTHON_ARG=""
        EWPO_CONF_FILE="ObservablesEW"
        EWPO_CONF_FILE_CURRENT="ObservablesEW_Current_SM_noLFU"
        EWPO_CONF_FILE_HLLHC="ObservablesEW_HLLHC_kappa_scaled"
        EWPO_CONF_FILE_FCCee_Zpole="ObservablesEW_FCCee_Zpole_SM_kappa_scaled"
        EWPO_CONF_FILE_FCCee_WW="ObservablesEW_FCCee_WW_SM_kappa_scaled"

        if [ "$updated_lumi" == "true" ]; then
            NEW_EWPO_CONF_FILE="${EWPO_CONF_FILE}_updated_lumi"
            cp ${EWPO_CONF_FILE}.conf ${NEW_EWPO_CONF_FILE}.conf

            NEW_EWPO_CONF_FILE_FCCee_Zpole="ObservablesEW_FCCee_Zpole_SM_updated_lumi"
            cp ${NEW_EWPO_CONF_FILE_FCCee_Zpole}.conf ${NEW_EWPO_CONF_FILE_FCCee_Zpole}_kappa_scaled.conf
            sed -i "\/IncludeFile ${EWPO_CONF_FILE_FCCee_Zpole}.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_FCCee_Zpole}_kappa_scaled.conf" ${NEW_EWPO_CONF_FILE}.conf

            NEW_EWPO_CONF_FILE_FCCee_WW="ObservablesEW_FCCee_WW_SM_updated_lumi"
            cp ${NEW_EWPO_CONF_FILE_FCCee_WW}.conf ${NEW_EWPO_CONF_FILE_FCCee_WW}_kappa_scaled.conf
            sed -i "\/IncludeFile ${EWPO_CONF_FILE_FCCee_WW}.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_FCCee_WW}_kappa_scaled.conf" ${NEW_EWPO_CONF_FILE}.conf


            NEW_MODEL_EWS="IncludeFile ../../${NEW_EWPO_CONF_FILE}.conf "
            sed -i "\/IncludeFile ..\/..\/${EWPO_CONF_FILE}.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "\/IncludeFile ..\/..\/${EWPO_CONF_FILE}.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            EWPO_CONF_FILE_FCCee_Zpole="${NEW_EWPO_CONF_FILE_FCCee_Zpole}_kappa_scaled"
            EWPO_CONF_FILE_FCCee_WW="${NEW_EWPO_CONF_FILE_FCCee_WW}_kappa_scaled"
            EWPO_CONF_FILE="${NEW_EWPO_CONF_FILE}"
        fi

        if [ "$modify_all_ewpos" == "true" ]; then
            NEW_EWPO_CONF_FILE="${EWPO_CONF_FILE}_all_mods"
            cp ${EWPO_CONF_FILE}.conf ${NEW_EWPO_CONF_FILE}.conf

            NEW_EWPO_CONF_FILE_CURRENT="${EWPO_CONF_FILE_CURRENT}_kappa_scaled"
            sed -i "\/IncludeFile ${EWPO_CONF_FILE_CURRENT}.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_CURRENT}.conf" ${NEW_EWPO_CONF_FILE}.conf

            NEW_MODEL_EWS="IncludeFile ../../${NEW_EWPO_CONF_FILE}.conf "
            sed -i "\/IncludeFile ..\/..\/${EWPO_CONF_FILE}.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "\/IncludeFile ..\/..\/${EWPO_CONF_FILE}.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            EWPO_PYTHON_ARG="${EWPO_PYTHON_ARG} --ewpos_all"
            EWPO_CONF_FILE="${NEW_EWPO_CONF_FILE}"
            EWPO_CONF_FILE_CURRENT="${NEW_EWPO_CONF_FILE_CURRENT}"
        fi

        if [ "$with_Af" == "true" ]; then
            NEW_EWPO_CONF_FILE="${EWPO_CONF_FILE}_with_Af"
            if [ "$shifted_sin2thetaEff" == "true" ]; then NEW_EWPO_CONF_FILE="${NEW_EWPO_CONF_FILE}_shifted_sin2thetaEff"; fi
            cp ${EWPO_CONF_FILE}.conf ${NEW_EWPO_CONF_FILE}.conf
            
            if [ "$modify_all_ewpos" == "true" ]; then
                NEW_EWPO_CONF_FILE_CURRENT="${EWPO_CONF_FILE_CURRENT}_with_Af"
                if [ "$shifted_sin2thetaEff" == "true" ]; then NEW_EWPO_CONF_FILE_CURRENT="${NEW_EWPO_CONF_FILE_CURRENT}_shifted_sin2thetaEff"; fi
                sed -i "\/IncludeFile ${EWPO_CONF_FILE_CURRENT}.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_CURRENT}.conf" ${NEW_EWPO_CONF_FILE}.conf
            fi

            # No A_f/A_FB_f obs for HL-LHC
            # NEW_EWPO_CONF_FILE_HLLHC="${EWPO_CONF_FILE_HLLHC}_with_Af"
            # sed -i "\/IncludeFile ObservablesEW_HLLHC_kappa_scaled.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_HLLHC}.conf" ${NEW_EWPO_CONF_FILE}.conf

            NEW_EWPO_CONF_FILE_FCCee_Zpole="${EWPO_CONF_FILE_FCCee_Zpole}_with_Af"
            if [ "$shifted_sin2thetaEff" == "true" ]; then NEW_EWPO_CONF_FILE_FCCee_Zpole="${NEW_EWPO_CONF_FILE_FCCee_Zpole}_shifted_sin2thetaEff"; fi
            sed -i "\/IncludeFile ${EWPO_CONF_FILE_FCCee_Zpole}.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_FCCee_Zpole}.conf" ${NEW_EWPO_CONF_FILE}.conf

            # No A_f/A_FB_f obs for FCC_ee_WW
            # NEW_EWPO_CONF_FILE_FCCee_WW="${EWPO_CONF_FILE_FCCee_WW}_with_Af"
            # sed -i "\/IncludeFile ObservablesEW_FCCee_WW_SM_kappa_scaled.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_FCCee_WW}.conf" ${NEW_EWPO_CONF_FILE}.conf

            NEW_MODEL_EWS="IncludeFile ../../${NEW_EWPO_CONF_FILE}.conf "
            sed -i "\/IncludeFile ..\/..\/${EWPO_CONF_FILE}.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "\/IncludeFile ..\/..\/${EWPO_CONF_FILE}.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            EWPO_PYTHON_ARG="${EWPO_PYTHON_ARG} --with_Af"
             if [ "$shifted_sin2thetaEff" == "true" ]; then EWPO_PYTHON_ARG="${EWPO_PYTHON_ARG} --shifted_sin2thetaEff"; fi
            EWPO_CONF_FILE="${NEW_EWPO_CONF_FILE}"

            EWPO_CONF_FILE_CURRENT="${NEW_EWPO_CONF_FILE_CURRENT}"
            # EWPO_CONF_FILE_HLLHC="${NEW_EWPO_CONF_FILE_HLLHC}"
            EWPO_CONF_FILE_FCCee_Zpole="${NEW_EWPO_CONF_FILE_FCCee_Zpole}"
            # EWPO_CONF_FILE_FCCee_WW="${NEW_EWPO_CONF_FILE_FCCee_WW}"

        fi

        if [ "$EWPO_2L" == "true" ]; then
            NEW_EWPO_CONF_FILE="${EWPO_CONF_FILE}_EWPO_2L"
            cp ${EWPO_CONF_FILE}.conf ${NEW_EWPO_CONF_FILE}.conf
            
            if [ "$modify_all_ewpos" == "true" ]; then
                NEW_EWPO_CONF_FILE_CURRENT="${EWPO_CONF_FILE_CURRENT}_EWPO_2L"
                sed -i "\/IncludeFile ${EWPO_CONF_FILE_CURRENT}.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_CURRENT}.conf" ${NEW_EWPO_CONF_FILE}.conf
            fi

            NEW_EWPO_CONF_FILE_HLLHC="${EWPO_CONF_FILE_HLLHC}_EWPO_2L"
            sed -i "\/IncludeFile ${EWPO_CONF_FILE_HLLHC}.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_HLLHC}.conf" ${NEW_EWPO_CONF_FILE}.conf

            NEW_EWPO_CONF_FILE_FCCee_Zpole="${EWPO_CONF_FILE_FCCee_Zpole}_EWPO_2L"
            sed -i "\/IncludeFile ${EWPO_CONF_FILE_FCCee_Zpole}.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_FCCee_Zpole}.conf" ${NEW_EWPO_CONF_FILE}.conf

            NEW_EWPO_CONF_FILE_FCCee_WW="${EWPO_CONF_FILE_FCCee_WW}_EWPO_2L"
            sed -i "\/IncludeFile ${EWPO_CONF_FILE_FCCee_WW}.conf/c\\IncludeFile ${NEW_EWPO_CONF_FILE_FCCee_WW}.conf" ${NEW_EWPO_CONF_FILE}.conf

            NEW_MODEL_EWS="IncludeFile ../../${NEW_EWPO_CONF_FILE}.conf "
            sed -i "\/IncludeFile ..\/..\/${EWPO_CONF_FILE}.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
            sed -i "\/IncludeFile ..\/..\/${EWPO_CONF_FILE}.conf /c\\$NEW_MODEL_EWS" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf

            EWPO_PYTHON_ARG="${EWPO_PYTHON_ARG} --EWPO_2L"
            EWPO_CONF_FILE="${NEW_EWPO_CONF_FILE}"

            EWPO_CONF_FILE_CURRENT="${NEW_EWPO_CONF_FILE_CURRENT}"
            EWPO_CONF_FILE_HLLHC="${NEW_EWPO_CONF_FILE_HLLHC}"
            EWPO_CONF_FILE_FCCee_Zpole="${NEW_EWPO_CONF_FILE_FCCee_Zpole}"
            EWPO_CONF_FILE_FCCee_WW="${NEW_EWPO_CONF_FILE_FCCee_WW}"
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

                    NEW_HIGGS_240="IncludeFile ${HIGGS_240_CONF}_kappa_scaled_${FLAG}.conf"
                    sed -i "\/${HIGGS_240_CONF}_kappa_scaled.conf/c\\$NEW_HIGGS_240" ${HIGGS_CONF}.conf
                    if [[ "${IDM_SCENARIOS[j]}" != "IDM_FCCee240" ]]; then
                        NEW_HIGGS_365="IncludeFile ${HIGGS_365_CONF}_kappa_scaled_${FLAG}.conf"
                        sed -i "\/${HIGGS_365_CONF}_kappa_scaled.conf/c\\$NEW_HIGGS_365" ${HIGGS_CONF}.conf
                    fi
                    if [[ "$no_HLLHC_Higgs" != "true" ]]; then
                        NEW_HIGGS_HLLHC="IncludeFile ObservablesHiggs_HLLHC_SM_kappa_scaled_${FLAG}.conf"
                        sed -i "\/ObservablesHiggs_HLLHC_SM_kappa_scaled.conf/c\\$NEW_HIGGS_HLLHC" ${HIGGS_CONF}.conf
                    fi

                    NEW_MODEL_HIGGS="IncludeFile ../../${HIGGS_CONF}.conf "

                    sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.*/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}.conf
                    sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.*/c\\$NEW_MODEL_HIGGS" Globalfits/AllOps/${MODEL_CONF_FILE}_small_priors.conf
                    

                    HIGGS_PYTHON_ARG="${HIGGS_PYTHON_ARG} --${FLAG}"

                    cd $TARGET_PATH
                    python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
                    python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
                    python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic ${HIGGS_PYTHON_ARG} --higgsconf ${HIGGS_CONF} ${EWPO_PYTHON_ARG}
                    # Running the script also without the flag, so that the main fits (i.e. the ones with the flag set to false) are also set up properly

                fi
            done

            
                
        else
            cd $TARGET_PATH
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name}
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic
            python scale_observables_kappas.py --scenario ${IDM_SCENARIOS[j]} --bp ${BP_Name} --realistic  --higgsconf ${HIGGS_CONF} ${EWPO_PYTHON_ARG}
        fi

    done

done