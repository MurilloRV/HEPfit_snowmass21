#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/find_WC_dependence_general_obs/"
COPY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits/SM_FCCee240_FCCee365"

# Use same number of points for all WCs
# CH_values=($(seq -10.0 1.0 10.0))
# CHbox_values=($(seq -10.0 1.0 10.0))
# CHD_values=($(seq -10.0 1.0 10.0))
# CHW_values=($(seq -10.0 1.0 10.0))
# CHB_values=($(seq -10.0 1.0 10.0))
# CHWB_values=($(seq -10.0 1.0 10.0))

CH_values=("1.0")
CHbox_values=("1.0")
CHD_values=("1.0")
CHW_values=("1.0")
CHG_values=("1.0")
CHB_values=("1.0")
CHWB_values=("1.0")
CuH_33r_values=("1.0")

echo "${CH_values[@]}"
echo "${CHbox_values[@]}"
echo "${CHD_values[@]}"
echo "${CHW_values[@]}"
echo "${CHG_values[@]}"
echo "${CHB_values[@]}"
echo "${CHWB_values[@]}"
echo "${CuH_33r_values[@]}"

mkdir -p observables_results

# Copying the configuration files 
mkdir -p $ORIGINAL_PATH/Config_Files/Globalfits/AllOps
cd $ORIGINAL_PATH/Config_Files/

cp $COPY_PATH/*.conf .
cp $COPY_PATH/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
cp $COPY_PATH/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf



for ((i=0; i<${#CH_values[@]}; i++)); do

    # Setting up the wilson coefficients
    WC_ARRAY=("CH" "CHbox" "CHD" "CHW" "CHG" "CHB" "CHWB" "CuH_33r")
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
