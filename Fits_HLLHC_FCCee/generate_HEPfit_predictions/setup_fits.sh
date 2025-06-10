#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/large_kappa_lambda_fits"


CH=($(seq -25.0 0.7 0.0))
CHBox=($(seq -2.0 0.05 0.2))

echo "${CH[@]}"
echo "${CHBox[@]}"


# mkdir -p configuration_files
# cd configuration_files

mkdir -p Globalfits/AllOps/
cp ../different_scenario_fits/SM_FCCee240_FCCee365/*.conf .
cp ../different_scenario_fits/SM_FCCee240_FCCee365/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
cp ../different_scenario_fits/SM_FCCee240_FCCee365/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf

sed -i "\/IncludeFile ..\/..\/ObservablesEW.conf.*/c # IncludeFile ..\/..\/ObservablesEW.conf" Globalfits/AllOps/model_fits.conf
sed -i "\/IncludeFile ..\/..\/ObservablesVV.conf.*/c # IncludeFile ..\/..\/ObservablesVV.conf" Globalfits/AllOps/model_fits.conf
sed -i "\/IncludeFile d6Ops_corr.conf.*/c # IncludeFile d6Ops_corr.conf" Globalfits/AllOps/model_fits.conf
sed -i "\/IncludeFile ..\/..\/EffVHcouplings_QFU12.conf.*/c # IncludeFile ..\/..\/EffVHcouplings_QFU12.conf" Globalfits/AllOps/model_fits.conf
sed -i "\/IncludeFile ..\/..\/HiggsEW_Par_Corr.conf.*/c # IncludeFile ..\/..\/HiggsEW_Par_Corr.conf" Globalfits/AllOps/model_fits.conf

mkdir -p results

output_file="results/k_ZH_240_365_central_value_results.txt"
rm -f $output_file

for ((i=0; i<${#CH[@]}; i++)); do
    for ((j=0; j<${#CHBox[@]}; j++)); do

        CH_CHBox="CH_${CH[i]}_CHBox_${CHBox[j]}"
        cp Globalfits/AllOps/model_fits.conf Globalfits/AllOps/model_fits_${CH_CHBox}.conf

        NEW_CH="ModelParameter  CH   ${CH[i]}  0.  50.0 "
        sed -i "/ModelParameter  CH  .*/c\\$NEW_CH" Globalfits/AllOps/model_fits_${CH_CHBox}.conf

        NEW_CHBox="ModelParameter  CHbox   ${CHBox[j]}  0.  50.0 "
        sed -i "/ModelParameter  CHbox  .*/c\\$NEW_CHBox" Globalfits/AllOps/model_fits_${CH_CHBox}.conf

        ../../HEPfit/build_rocky9/HEPfit/bin/analysis Globalfits/AllOps/model_fits_${CH_CHBox}.conf --noMC |& tee results/observables_${CH_CHBox}.txt


        python read_hepfit_output.py -i results/observables_${CH_CHBox}.txt -o $output_file --CH ${CH[i]} --CHBox ${CHBox[j]}
        rm results/observables_${CH_CHBox}.txt
        rm Globalfits/AllOps/model_fits_${CH_CHBox}.conf

    done
done
