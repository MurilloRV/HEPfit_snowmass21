#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/smeft_matching_inputs/"
COPY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits/SM_FCCee240_FCCee365"

json=$(python3 find_matched_WCs.py --wilson_coefficients CH CHbox CHD CHW CHB CHWB | tail -n 1)

echo "$json"
# Parse JSON
readarray -t CH_values < <(echo "$json" | jq '.CH[]')
readarray -t CHbox_values < <(echo "$json" | jq '.CHbox[]')
readarray -t CHD_values < <(echo "$json" | jq '.CHD[]')
readarray -t CHW_values < <(echo "$json" | jq '.CHW[]')
readarray -t CHB_values < <(echo "$json" | jq '.CHB[]')
readarray -t CHWB_values < <(echo "$json" | jq '.CHWB[]')

WC_ARRAY=("CH" "CHbox" "CHD" "CHW" "CHB" "CHWB")

echo "${CH_values[@]}"
echo "${CHbox_values[@]}"
echo "${CHD_values[@]}"
echo "${CHW_values[@]}"
echo "${CHB_values[@]}"
echo "${CHWB_values[@]}"

mkdir -p observables_results

# Copying the configuration files 
mkdir -p $ORIGINAL_PATH/Config_Files/Globalfits/AllOps
cd $ORIGINAL_PATH/Config_Files/

cp $COPY_PATH/*.conf .
cp $COPY_PATH/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
cp $COPY_PATH/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf



for ((i=0; i<${#CH_values[@]}; i++)); do

    # Setting up the wilson coefficients
    WC_ARRAY=("CH" "CHbox" "CHD" "CHW" "CHB" "CHWB")
    echo "WC number : $i"

    MODEL_CONF="Globalfits/AllOps/model_fits_${i}.conf"
    cp Globalfits/AllOps/model_fits.conf $MODEL_CONF

    for WC in "${WC_ARRAY[@]}"; do
        WC_value="${WC}_values[${i}]"
        NEW_WC="ModelParameter  $WC   ${!WC_value}  0.  50.0 "
        sed -i "/ModelParameter  $WC  .*/c\\$NEW_WC" $MODEL_CONF
    done

    # Modifying the configuration file to rotate the CHW and CHB operators
    NEW_CHWHB_gaga="ModelParameter  CHWHB_gaga   0.  0.  0. "
    sed -i "/ModelParameter  CHWHB_gaga  .*/c\\$NEW_CHWHB_gaga" $MODEL_CONF
    NEW_CHWHB_gagaorth="ModelParameter  CHWHB_gagaorth   0.  0.  0. "
    sed -i "/ModelParameter  CHWHB_gagaorth  .*/c\\$NEW_CHWHB_gagaorth" $MODEL_CONF
    NEW_RotateCHWCHB_FLAG="ModelFlag       RotateCHWCHB    false"
    sed -i "/ModelFlag       RotateCHWCHB  .*/c\\$NEW_RotateCHWCHB_FLAG" $MODEL_CONF

    # sed -i "12a\#" $MODEL_CONF
    # sed -i "12a\ModelFlag  NoApproximateGammaZ  true" $MODEL_CONF

    cd ../observables_results
    analysis "../Config_Files/${MODEL_CONF}" --noMC |& tee "observables_BP${i}.txt"
    cd $ORIGINAL_PATH/Config_Files/
done

cd $ORIGINAL_PATH
