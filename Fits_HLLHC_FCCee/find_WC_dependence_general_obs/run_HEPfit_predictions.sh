#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/find_WC_dependence_general_obs/"
COPY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits/SM_FCCee240_FCCee365"

updated_lumi="true"
COPY_PATH_UPDATED_LUMI="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_scenario_fits/IDM_FCCee240_FCCee365"

json=$(python3 find_1sigma_WCs.py --wilson_coefficients CH CHbox CHD CHW CHG CHB CHWB CuH_33r CHe_11 CHL1_11 CHL3_11 | tail -n 1)

# Parse JSON
CH_low=$(echo "$json" | jq '.CH_low')
CH_high=$(echo "$json" | jq '.CH_high')
CHbox_low=$(echo "$json" | jq '.CHbox_low')
CHbox_high=$(echo "$json" | jq '.CHbox_high')
CHD_low=$(echo "$json" | jq '.CHD_low')
CHD_high=$(echo "$json" | jq '.CHD_high')
CHW_low=$(echo "$json" | jq '.CHW_low')
CHW_high=$(echo "$json" | jq '.CHW_high')
CHG_low=$(echo "$json" | jq '.CHG_low')
CHG_high=$(echo "$json" | jq '.CHG_high')
CHB_low=$(echo "$json" | jq '.CHB_low')
CHB_high=$(echo "$json" | jq '.CHB_high')
CHWB_low=$(echo "$json" | jq '.CHWB_low')
CHWB_high=$(echo "$json" | jq '.CHWB_high')
CuH_33r_low=$(echo "$json" | jq '.CuH_33r_low')
CuH_33r_high=$(echo "$json" | jq '.CuH_33r_high')
CHe_11_low=$(echo "$json" | jq '.CHe_11_low')
CHe_11_high=$(echo "$json" | jq '.CHe_11_high')
CHL1_11_low=$(echo "$json" | jq '.CHL1_11_low')
CHL1_11_high=$(echo "$json" | jq '.CHL1_11_high')
CHL3_11_low=$(echo "$json" | jq '.CHL3_11_low')
CHL3_11_high=$(echo "$json" | jq '.CHL3_11_high')

CH_intervals=($CH_low $CH_high)
CHbox_intervals=($CHbox_low $CHbox_high)
CHD_intervals=($CHD_low $CHD_high)
CHW_intervals=($CHW_low $CHW_high)
CHG_intervals=($CHG_low $CHG_high)
CHB_intervals=($CHB_low $CHB_high)
CHWB_intervals=($CHWB_low $CHWB_high)
CuH_33r_intervals=($CuH_33r_low $CuH_33r_high)
CHe_11_intervals=($CHe_11_low $CHe_11_high)
CHL1_11_intervals=($CHL1_11_low $CHL1_11_high)
CHL3_11_intervals=($CHL3_11_low $CHL3_11_high)

# Instead of just evaluating the predictions at the 1-sigma values, we now evaluate these also at multiples of the 1-sigma values, both in the negative and positive direction.
n_sigmas=5
get_WC_values() {
    local intervals=("$@")
    local wc_values=()
    for ((i=n_sigmas; i>0; i--)); do
        wc_values+=($(printf "%.20f" "$(echo "${intervals[0]} * $i" | bc -l)"))
    done
    for ((i=1; i<=n_sigmas; i++)); do
        wc_values+=($(printf "%.20f" "$(echo "${intervals[1]} * $i" | bc -l)"))
    done
    echo "${wc_values[@]}"
}

CH_values=($(get_WC_values "${CH_intervals[@]}"))
CHbox_values=($(get_WC_values "${CHbox_intervals[@]}"))
CHD_values=($(get_WC_values "${CHD_intervals[@]}"))
CHW_values=($(get_WC_values "${CHW_intervals[@]}"))
CHG_values=($(get_WC_values "${CHG_intervals[@]}"))
CHB_values=($(get_WC_values "${CHB_intervals[@]}"))
CHWB_values=($(get_WC_values "${CHWB_intervals[@]}"))
CuH_33r_values=($(get_WC_values "${CuH_33r_intervals[@]}"))
CHe_11_values=($(get_WC_values "${CHe_11_intervals[@]}"))
CHL1_11_values=($(get_WC_values "${CHL1_11_intervals[@]}"))
CHL3_11_values=($(get_WC_values "${CHL3_11_intervals[@]}"))


# CH_values=("0.01")
# CHbox_values=("0.01")
# CHD_values=("0.01")
# CHW_values=("0.01")
# CHG_values=("0.01")
# CHB_values=("0.01")
# CHWB_values=("0.01")
# CuH_33r_values=("0.01")
# CHe_11_values=("0.01")
# CHL1_11_values=("0.01")
# CHL3_11_values=("0.01")

echo "${CH_values[@]}"
echo "${CHbox_values[@]}"
echo "${CHD_values[@]}"
echo "${CHW_values[@]}"
echo "${CHG_values[@]}"
echo "${CHB_values[@]}"
echo "${CHWB_values[@]}"
echo "${CuH_33r_values[@]}"
echo "${CHe_11_values[@]}"
echo "${CHL1_11_values[@]}"
echo "${CHL3_11_values[@]}"

mkdir -p observables_results

# Copying the configuration files 
mkdir -p $ORIGINAL_PATH/Config_Files/Globalfits/AllOps
cd $ORIGINAL_PATH/Config_Files/

cp $COPY_PATH/*.conf .
cp $COPY_PATH/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
cp $COPY_PATH/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf


if [[ $updated_lumi == "true" ]]; then
    cp $COPY_PATH_UPDATED_LUMI/*_updated_lumi*.conf .
fi

EWPO_CURRENT_CONF="ObservablesEW_Current_SM_noLFU.conf"
echo "#" >> $EWPO_CURRENT_CONF
echo "######################################################################" >> $EWPO_CURRENT_CONF
echo "Observable  sin2thetaEff_C sin2thetaEff sin^{2}#theta_{eff}^{lept} 1. -1. noMCMC noweight" >> $EWPO_CURRENT_CONF



for ((i=0; i<${#CH_values[@]}; i++)); do

    # Setting up the wilson coefficients
    WC_ARRAY=("CH" "CHbox" "CHD" "CHW" "CHG" "CHB" "CHWB" "CuH_33r" "CHe_11" "CHL1_11" "CHL3_11")
    # WC_ARRAY=("CH" "CHbox")
    # WC_ARRAY=("CH")
    echo "WC number : $i"

    for WC in "${WC_ARRAY[@]}"; do
        MODEL_CONF="Globalfits/AllOps/model_fits_${WC}_${i}"
        cp Globalfits/AllOps/model_fits.conf ${MODEL_CONF}.conf

        WC_value="${WC}_values[i]"
        NEW_WC="ModelParameter  $WC   ${!WC_value}  0.  50.0 "
        sed -i "/ModelParameter  $WC  .*/c\\$NEW_WC" ${MODEL_CONF}.conf

        # Modifying the configuration file to rotate the CHW and CHB operators
        NEW_CHWHB_gaga="ModelParameter  CHWHB_gaga   0.  0.  0. "
        sed -i "/ModelParameter  CHWHB_gaga  .*/c\\$NEW_CHWHB_gaga" ${MODEL_CONF}.conf
        NEW_CHWHB_gagaorth="ModelParameter  CHWHB_gagaorth   0.  0.  0. "
        sed -i "/ModelParameter  CHWHB_gagaorth  .*/c\\$NEW_CHWHB_gagaorth" ${MODEL_CONF}.conf
        NEW_RotateCHWCHB_FLAG="ModelFlag       RotateCHWCHB    false"
        sed -i "/ModelFlag       RotateCHWCHB  .*/c\\$NEW_RotateCHWCHB_FLAG" ${MODEL_CONF}.conf

        HIGGS_CONF="ObservablesHiggs"
        HIGGS_240_CONF="ObservablesHiggs_FCCee_240_SM"
        HIGGS_365_CONF="ObservablesHiggs_FCCee_365"
        if [[ $updated_lumi == "true" ]]; then
            NEW_MODEL_CONF="${MODEL_CONF}_updated_lumi"
            cp ${MODEL_CONF}.conf ${NEW_MODEL_CONF}.conf
            MODEL_CONF="${NEW_MODEL_CONF}"

            NEW_HIGGS_CONF="${HIGGS_CONF}_updated_lumi"
            cp ${HIGGS_CONF}.conf ${NEW_HIGGS_CONF}.conf 
            HIGGS_CONF="${NEW_HIGGS_CONF}"
            sed -i "\/IncludeFile ..\/..\/ObservablesHiggs.*/c\\IncludeFile ..\/..\/${HIGGS_CONF}.conf" ${MODEL_CONF}.conf

            NEW_HIGGS_240_CONF="${HIGGS_240_CONF}_updated_lumi"
            sed -i "\/IncludeFile ObservablesHiggs_FCCee_240*/c\\IncludeFile ${NEW_HIGGS_240_CONF}.conf" ${HIGGS_CONF}.conf
            HIGGS_240_CONF="${NEW_HIGGS_240_CONF}"

            NEW_HIGGS_365_CONF="${HIGGS_365_CONF}_updated_lumi"
            sed -i "\/IncludeFile ObservablesHiggs_FCCee_365*/c\\IncludeFile ${NEW_HIGGS_365_CONF}.conf" ${HIGGS_CONF}.conf
            HIGGS_365_CONF="${NEW_HIGGS_365_CONF}"
        fi

        cd ../observables_results
        results_filename="observables_${WC}_${i}"
        if [[ $updated_lumi == "true" ]]; then
            results_filename="${results_filename}_updated_lumi"
        fi
        analysis "../Config_Files/${MODEL_CONF}.conf" --noMC |& tee "${results_filename}.txt"
        cd $ORIGINAL_PATH/Config_Files/
    done
done

cd $ORIGINAL_PATH
