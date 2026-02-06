#!/bin/bash

# MODEL="IDM"
MODEL="Z2SSM"
ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/large_kappa_lambda_fits"
ORIGINAL_PATH="${ORIGINAL_PATH}/General_lambdas"
mkdir -p "$ORIGINAL_PATH"
cd "$ORIGINAL_PATH"

# INDIVIDUAL_LAMBDAS=({-5..10})

if [ "$MODEL" == "IDM" ]; then
    INDIVIDUAL_LAMBDAS=(
        1.1209067864736006 # BPB_0
        2.3867362274064843 # BPB_2
        3.3446699219962595 # BPB_4
        4.332584967850238  # BPB_6
        5.390968560325193  # BPB_8
        6.370034303736775  # BPB_10
        7.515862276796717  # BPB_12
        8.611459058586306  # BPB_14
        9.319513844125106  # BPB_16
        11.2535829810942   # BPB_18
    )
elif [ "$MODEL" == "Z2SSM" ]; then
    INDIVIDUAL_LAMBDAS=(
        1.0643594459030925 # BPBnew_0
        2.068362744578383  # BPBnew_1
        3.41660475844658   # BPBnew_2
        4.996504503173265  # BPBnew_4
        6.114019817191308  # BPBnew_6
        7.24831645311373   # BPBnew_8
        8.535635929341407  # BPBnew_10
        9.584476423981522  # BPBnew_12
        10.34814810189343  # BPBnew_13
    )
else 
    echo "Unknown model: $MODEL"
    return 1
fi

LAMBDAS=()
WITH_LAMBDA=()
CH=()

for lamb in "${INDIVIDUAL_LAMBDAS[@]}"; do
    LAMBDAS+=("$lamb" "$lamb")
    WITH_LAMBDA+=('no' '')


    CH_value=$(echo "scale=12; ($lamb - 1) * (-2.1332885478)" | bc)
    CH+=("$CH_value" "$CH_value")
done

echo "${LAMBDAS[@]}"
echo "${WITH_LAMBDA[@]}"
echo "${CH[@]}"



for ((i=0; i<${#LAMBDAS[@]}; i++)); do
    SCENARIO_PATH="Lambda${LAMBDAS[i]}_FCCee240_FCCee365_${WITH_LAMBDA[i]}HLLHClambda"

    mkdir -p "$SCENARIO_PATH/Globalfits/AllOps"
    cd "$SCENARIO_PATH"
    cp ../../../different_scenario_fits/SM_FCCee240_FCCee365/*.conf .
    cp ../../../different_scenario_fits/SM_FCCee240_FCCee365/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
    cp ../../../different_scenario_fits/SM_FCCee240_FCCee365/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf

    NEW_CH="ModelParameter  CH   ${CH[i]}  0.  50.0 "
    sed -i "/ModelParameter  CH                  0.  0.  25./c\\$NEW_CH" Globalfits/AllOps/model_fits.conf

    mkdir -p results_fits
    mkdir -p results_observables
    cd results_observables
    ../../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_fits.conf --noMC |& tee observables.txt

    cd $ORIGINAL_PATH
done

cd ..
python modify_observables_general_lambdas.py -m "$MODEL"