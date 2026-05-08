#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/find_WC_dependence_general_obs/"
COPY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits/SM_FCCee240_FCCee365"



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

CH_values=($CH_low $CH_high)
CHbox_values=($CHbox_low $CHbox_high)
CHD_values=($CHD_low $CHD_high)
CHW_values=($CHW_low $CHW_high)
CHG_values=($CHG_low $CHG_high)
CHB_values=($CHB_low $CHB_high)
CHWB_values=($CHWB_low $CHWB_high)
CuH_33r_values=($CuH_33r_low $CuH_33r_high)
CHe_11_values=($CHe_11_low $CHe_11_high)
CHL1_11_values=($CHL1_11_low $CHL1_11_high)
CHL3_11_values=($CHL3_11_low $CHL3_11_high)

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



for ((i=0; i<${#CH_values[@]}; i++)); do

    # Setting up the wilson coefficients
    WC_ARRAY=("CH" "CHbox" "CHD" "CHW" "CHG" "CHB" "CHWB" "CuH_33r" "CHe_11" "CHL1_11" "CHL3_11")
    echo "WC number : $i"

    for WC in "${WC_ARRAY[@]}"; do
        MODEL_CONF="Globalfits/AllOps/model_fits_${WC}_${i}.conf"
        cp Globalfits/AllOps/model_fits.conf $MODEL_CONF

        WC_value="${WC}_values[i]"
        NEW_WC="ModelParameter  $WC   ${!WC_value}  0.  50.0 "
        sed -i "/ModelParameter  $WC  .*/c\\$NEW_WC" $MODEL_CONF

        # Modifying the configuration file to rotate the CHW and CHB operators
        NEW_CHWHB_gaga="ModelParameter  CHWHB_gaga   0.  0.  0. "
        sed -i "/ModelParameter  CHWHB_gaga  .*/c\\$NEW_CHWHB_gaga" $MODEL_CONF
        NEW_CHWHB_gagaorth="ModelParameter  CHWHB_gagaorth   0.  0.  0. "
        sed -i "/ModelParameter  CHWHB_gagaorth  .*/c\\$NEW_CHWHB_gagaorth" $MODEL_CONF
        NEW_RotateCHWCHB_FLAG="ModelFlag       RotateCHWCHB    false"
        sed -i "/ModelFlag       RotateCHWCHB  .*/c\\$NEW_RotateCHWCHB_FLAG" $MODEL_CONF

        cd ../observables_results
        analysis "../Config_Files/${MODEL_CONF}" --noMC |& tee "observables_${WC}_${i}.txt"
        cd $ORIGINAL_PATH/Config_Files/
    done
done

cd $ORIGINAL_PATH
