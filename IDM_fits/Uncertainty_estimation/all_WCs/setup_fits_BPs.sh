#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Uncertainty_estimation/all_WCs"
COPY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits/SM_FCCee240_FCCee365"

# INDIVIDUAL_LAMBDAS=({-5..10})
# LAMBDAS=()
# WITH_LAMBDA=()
# CH=()

# for lamb in "${INDIVIDUAL_LAMBDAS[@]}"; do
#     LAMBDAS+=("$lamb" "$lamb")
#     WITH_LAMBDA+=('no' '')

#     CH_value=$(echo "scale=12; ($lamb - 1) * (-2.1290888208276963)" | bc)
#     CH+=("$CH_value" "$CH_value")
# done

CH_values=()
CHbox_values=()
CHD_values=()
CHW_values=()
CHB_values=()
CHWB_values=()
# while IFS=, read BP CH CHbox CHD CHW CHB CHWB ; do
while IFS=, read BP CH CHbox CHD CHW CHB CHWB ; do
    CH_values+=("$CH")
    CHbox_values+=("$CHbox")
    CHD_values+=("$CHD")
    CHW_values+=("$CHW")
    CHB_values+=("$CHB")
    CHWB_values+=("$CHWB")
done < <(tail -n +2 "WC_results.txt")

echo "${CH_values[@]}"
echo "${CHbox_values[@]}"
echo "${CHD_values[@]}"
echo "${CHW_values[@]}"
echo "${CHB_values[@]}"
echo "${CHWB_values[@]}"



for ((i=0; i<${#CH_values[@]}; i++)); do
    # SCENARIO_PATH="Lambda${LAMBDAS[i]}_FCCee240_FCCee365_${WITH_LAMBDA[i]}HLLHClambda"
    # SCENARIO_PATH="CH${CH_values[i]}_CHbox${CHbox_values[i]}_FCCee240_FCCee365"
    SCENARIO_PATH="WCs_BPs_${i}_FCCee240_FCCee365"

    # Copying the configuration files 
    mkdir -p "$SCENARIO_PATH/Globalfits/AllOps"
    cd $SCENARIO_PATH
    cp $COPY_PATH/*.conf .
    cp $COPY_PATH/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
    cp $COPY_PATH/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf

    # Setting up the wilson coefficients
    NEW_CH="ModelParameter  CH   ${CH_values[i]}  0.  50.0 "
    sed -i "/ModelParameter  CH  .*/c\\$NEW_CH" Globalfits/AllOps/model_fits.conf

    NEW_CHbox="ModelParameter  CHbox   ${CHbox_values[i]}  0.  50.0 "
    sed -i "/ModelParameter  CHbox  .*/c\\$NEW_CHbox" Globalfits/AllOps/model_fits.conf

    NEW_CHD="ModelParameter  CHD   ${CHD_values[i]}  0.  2.0 "
    sed -i "/ModelParameter  CHD  .*/c\\$NEW_CHD" Globalfits/AllOps/model_fits.conf

    NEW_CHW="ModelParameter  CHW   ${CHW_values[i]}  0.  2.0 "
    sed -i "/ModelParameter  CHW  .*/c\\$NEW_CHW" Globalfits/AllOps/model_fits.conf

    NEW_CHB="ModelParameter  CHB   ${CHB_values[i]}  0.  2.0 "
    sed -i "/ModelParameter  CHB  .*/c\\$NEW_CHB" Globalfits/AllOps/model_fits.conf

    NEW_CHWB="ModelParameter  CHWB   ${CHWB_values[i]}  0.  2.0 "
    sed -i "/ModelParameter  CHWB  .*/c\\$NEW_CHWB" Globalfits/AllOps/model_fits.conf


    # Modifying the configuration file to rotate the CHW and CHB operators
    NEW_CHWHB_gaga="ModelParameter  CHWHB_gaga   0.  0.  0. "
    sed -i "/ModelParameter  CHWHB_gaga  .*/c\\$NEW_CHWHB_gaga" Globalfits/AllOps/model_fits.conf
    NEW_CHWHB_gagaorth="ModelParameter  CHWHB_gagaorth   0.  0.  0. "
    sed -i "/ModelParameter  CHWHB_gagaorth  .*/c\\$NEW_CHWHB_gagaorth" Globalfits/AllOps/model_fits.conf
    NEW_RotateCHWCHB_FLAG="ModelFlag       RotateCHWCHB    false"
    sed -i "/ModelFlag       RotateCHWCHB  .*/c\\$NEW_RotateCHWCHB_FLAG" Globalfits/AllOps/model_fits.conf


    # Setting up the existing flag
    EXISTING_FLAG="LoopH3d6Quad"
    NEW_MODEL_CONF="Globalfits/AllOps/model_fits_no${EXISTING_FLAG}.conf"
    cp Globalfits/AllOps/model_fits.conf $NEW_MODEL_CONF

    NEW_FLAG_LINE="ModelFlag       LoopH3d6Quad    false"
    sed -i "/ModelFlag       LoopH3d6Quad  .*/c\\$NEW_FLAG_LINE" $NEW_MODEL_CONF

    # Setting up the new flags
    NEW_FLAG_ARRAY=("LoopHd6NoSubleading"
                    "LoopH3d6Quad_C1term"
                    "LoopH3d6Cubi"
                    "LoopH3d6Full"
    )

    for FLAG in "${NEW_FLAG_ARRAY[@]}"; do
        NEW_MODEL_CONF="Globalfits/AllOps/model_fits_${FLAG}.conf"
        cp Globalfits/AllOps/model_fits.conf $NEW_MODEL_CONF

        NEW_FLAG_LINE="ModelFlag       ${FLAG}    true"
        sed -i "/ModelFlag       LoopH3d6Quad  .*/a #\n\\$NEW_FLAG_LINE" $NEW_MODEL_CONF
    done

    mkdir -p results_observables
    # FLAG_ARRAY+=("no${EXISTING_FLAG}")
    FLAG_ARRAY=(${NEW_FLAG_ARRAY[@]} "no${EXISTING_FLAG}")
    for FLAG in "${FLAG_ARRAY[@]}"; do
        mkdir -p results_fits_$FLAG
        cd results_observables
        analysis "../Globalfits/AllOps/model_fits_${FLAG}.conf" --noMC |& tee "observables_${FLAG}.txt"
        cd ..
    done

    mkdir -p results_fits
    cd results_observables
    analysis "../Globalfits/AllOps/model_fits.conf" --noMC |& tee "observables.txt"
    cd ..


    cd $ORIGINAL_PATH
done

python modify_observables_BPs.py