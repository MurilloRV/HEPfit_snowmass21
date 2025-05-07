#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250_350_500_1000/large_kappa_lambda_fits"


LAMBDAS=({-5..10})
CH=()

for lamb in "${LAMBDAS[@]}"; do
    CH_value=$(echo "scale=12; ($lamb - 1) * (-2.1290888208276963)" | bc)
    CH+=("$CH_value")
done

echo "${LAMBDAS[@]}"
echo "${CH[@]}"
BASE_SCENARIOS=('ILC_250_350' 'ILC_250_350_500')

for ((i=0; i<${#LAMBDAS[@]}; i++)); do

    for scenario in "${BASE_SCENARIOS[@]}"; do

        if [[ "$scenario" != "ILC_250" ]] && \
           [[ "$scenario" != "ILC_250_350" ]] && \
           [[ "$scenario" != "ILC_250_350_500" ]]; then
            echo "Error: Scenario not implemented: $scenario" >&2
            exit 1
        fi

        SCENARIO_PATH="Lambda${LAMBDAS[i]}_$scenario"

        mkdir -p "$SCENARIO_PATH/Globalfits/AllOps"
        cd "$SCENARIO_PATH"
        cp ../../Fits_HLLHC_ILC_250_350_500_1000/GIMR/*.conf .
        cp ../../Fits_HLLHC_ILC_250_350_500_1000/GIMR/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
        cp ../../Fits_HLLHC_ILC_250_350_500_1000/GIMR/Globalfits/AllOps/model.conf Globalfits/AllOps/model_fits.conf


        #####################################################################
        ######### GENERAL MODIFICATIONS TO THE CONFIGURATION FILES ##########
        #####################################################################
        # Vary CH in the fit
        NEW_CH_PRIOR="ModelParameter  CH   ${CH[i]}  0.  15.0 "
        sed -i "/ModelParameter  CH                  0.  0.  0. /c\\$NEW_CH_PRIOR" Globalfits/AllOps/model_fits.conf
        NEW_CH_OBS="Observable  CH_corr  CH  C_{H}  0.  0.  noMCMC noweight"
        sed -i "/Observable  CLL_1221_corr  CLL_1221  C_{LL}  0.  0.  noMCMC noweight/a\\$NEW_CH_OBS" Globalfits/AllOps/d6Ops_corr.conf
        sed -i "/CorrelatedObservables dim6Ops 28/c CorrelatedObservables dim6Ops 29" Globalfits/AllOps/d6Ops_corr.conf

        # Increase prior for CuH_33r to avoid cutoff
        sed -i "/ModelParameter  CuH_33r   0.  0.  4.0/c ModelParameter  CuH_33r   0.  0.  8.0" Globalfits/AllOps/model_fits.conf

        # Modify theoretical uncertainties
        sed -i "/ModelParameter  eHggint .*/c     ModelParameter  eHggint            0.  0.010   0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHggpar .*/c     ModelParameter  eHggpar            0.  0.005   0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHWWint .*/c     ModelParameter  eHWWint            0.  0.003   0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHWWpar .*/c     ModelParameter  eHWWpar            0.  0.      0.007 " Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHZZint .*/c     ModelParameter  eHZZint            0.  0.003   0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHZZpar .*/c     ModelParameter  eHZZpar            0.  0.      0.007 " Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHZgaint .*/c    ModelParameter  eHZgaint           0.  0.010   0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHZgapar .*/c    ModelParameter  eHZgapar           0.  0.      0.007 " Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHgagaint .*/c   ModelParameter  eHgagaint          0.  0.010   0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHgagapar .*/c   ModelParameter  eHgagapar          0.  0.      0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHmumuint .*/c   ModelParameter  eHmumuint          0.  0.001   0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHmumupar .*/c   ModelParameter  eHmumupar          0.  0.      0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHtautauint .*/c ModelParameter  eHtautauint        0.  0.001   0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHtautaupar .*/c ModelParameter  eHtautaupar        0.  0.      0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHccint .*/c     ModelParameter  eHccint            0.  0.002   0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHccpar .*/c     ModelParameter  eHccpar            0.  0.0101  0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHbbint .*/c     ModelParameter  eHbbint            0.  0.002   0. "    Globalfits/AllOps/model_fits.conf
        sed -i "/ModelParameter  eHbbpar .*/c     ModelParameter  eHbbpar            0.  0.0061  0. "    Globalfits/AllOps/model_fits.conf

        # Add kappa_lambda observable
        printf "\n# Trilinear Higgs coupling prediction:" >> ObservablesHiggs.conf
        printf "\nObservable deltalHHH_HLLHC    deltalHHH   #delta#lambda_{H^{3}}/#lambda_{SM} 1. -1. noMCMC noweight" >> ObservablesHiggs.conf


        if [[ "$scenario" != "ILC_250_350" ]] && \
           [[ "$scenario" != "ILC_250_350_500" ]] && \
           [[ "$scenario" != "ILC_250_350_500_1000" ]]; then
            # Remove 350 GeV observables
            sed -i "/IncludeFile ObservablesHiggs_ILC_350_SM.conf/c\# IncludeFile ObservablesHiggs_ILC_350_SM.conf" ObservablesHiggs.conf
            sed -i "/IncludeFile ObservablesVV_OO_ILC_350.conf/c\# IncludeFile ObservablesVV_OO_ILC_350.conf" ObservablesVV.conf
        fi
        if [[ "$scenario" != "ILC_250_350_500" ]] && \
           [[ "$scenario" != "ILC_250_350_500_1000" ]]; then
            # Remove 500 GeV observables
            sed -i "/IncludeFile ObservablesHiggs_ILC_500_SM.conf/c\# IncludeFile ObservablesHiggs_ILC_500_SM.conf" ObservablesHiggs.conf
            sed -i "/IncludeFile ObservablesVV_OO_ILC_500.conf/c\# IncludeFile ObservablesVV_OO_ILC_500.conf" ObservablesVV.conf
            sed -i "/IncludeFile ObservablesEW_ILC_tt.conf/c\# IncludeFile ObservablesEW_ILC_tt.conf" ObservablesEW.conf
        fi
        if [[ "$scenario" != "ILC_250_350_500_1000" ]]; then
            # Remove 1000 GeV observables
            sed -i "/IncludeFile ObservablesHiggs_ILC_1000_SM.conf/c\# IncludeFile ObservablesHiggs_ILC_1000_SM.conf" ObservablesHiggs.conf
            sed -i "/IncludeFile ObservablesVV_OO_ILC_1000.conf/c\# IncludeFile ObservablesVV_OO_ILC_1000.conf" ObservablesVV.conf
        fi


        #####################################################################
        ####################### SETUP OF REDUCED PRIORS #####################
        #####################################################################
        cp Globalfits/AllOps/model_fits.conf Globalfits/AllOps/model_fits_small_priors.conf

        sed -i "/ModelParameter  CW   0.  0. .*/c             ModelParameter  CW                     0.  0.  0.2"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHG   0.  0. .*/c            ModelParameter  CHG                    0.  0.  0.08" Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHWB   0.  0. .*/c           ModelParameter  CHWB                   0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHWHB_gaga   0.  0. .*/c     ModelParameter  CHWHB_gaga             0.  0.  0.8"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHWHB_gagaorth   0.  0. .*/c ModelParameter  CHWHB_gagaorth         0.  0.  0.8"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHD   0.  0. .*/c            ModelParameter  CHD                    0.  0.  2.0"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHbox   0.  0. .*/c          ModelParameter  CHbox                  0.  0.  4.0"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CH   0.  0. .*/c             ModelParameter  CH                     0.  0.  20."  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHL1_11   0.  0. .*/c        ModelParameter  CHL1_11                0.  0.  0.2"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHL1_22   0.  0. .*/c        ModelParameter  CHL1_22                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHL1_33   0.  0. .*/c        ModelParameter  CHL1_33                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHL3_11   0.  0. .*/c        ModelParameter  CHL3_11                0.  0.  0.2"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHL3_22   0.  0. .*/c        ModelParameter  CHL3_22                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHL3_33   0.  0. .*/c        ModelParameter  CHL3_33                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHe_11   0.  0. .*/c         ModelParameter  CHe_11                 0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHe_22   0.  0. .*/c         ModelParameter  CHe_22                 0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHe_33   0.  0. .*/c         ModelParameter  CHe_33                 0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHQ1_11   0.  0. .*/c        ModelParameter  CHQ1_11                0.  0.  0.8"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHQ1_33   0.  0. .*/c        ModelParameter  CHQ1_33                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHQ3_11   0.  0. .*/c        ModelParameter  CHQ3_11                0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHu_11   0.  0. .*/c         ModelParameter  CHu_11                 0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHd_11   0.  0. .*/c         ModelParameter  CHd_11                 0.  0.  0.3"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CHd_33   0.  0. .*/c         ModelParameter  CHd_33                 0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CeH_22r   0.  0. .*/c        ModelParameter  CeH_22r                0.  0.  0.04" Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CeH_33r   0.  0. .*/c        ModelParameter  CeH_33r                0.  0.  0.12" Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CuH_22r   0.  0. .*/c        ModelParameter  CuH_22r                0.  0.  0.16" Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CuH_33r   0.  0. .*/c        ModelParameter  CuH_33r                0.  0.  8.0"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CdH_33r   0.  0. .*/c        ModelParameter  CdH_33r                0.  0.  0.2"  Globalfits/AllOps/model_fits_small_priors.conf
        sed -i "/ModelParameter  CLL_1221   0.  0. .*/c       ModelParameter  CLL_1221               0.  0.  0.4"  Globalfits/AllOps/model_fits_small_priors.conf


        #####################################################################
        ######## SETUP OF MODIFIED MONTE CARLO CONFIGURATION FILES ##########
        #####################################################################
        sed -i "/SignificantDigits 5 /c SignificantDigits 15 " MonteCarlo.conf

        cp MonteCarlo.conf MonteCarlo_short.conf
        cp MonteCarlo.conf MonteCarlo_long.conf
        cp MonteCarlo.conf MonteCarlo_full.conf

        sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              100000 " MonteCarlo_short.conf
        sed -i "/Iterations                 1000000 /c Iterations                 50000 " MonteCarlo_short.conf
        sed -i "/RValueForConvergence    1.01 /c RValueForConvergence    1.1 " MonteCarlo_short.conf

        sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              1000000 " MonteCarlo_long.conf
        sed -i "/Iterations                 1000000 /c Iterations                 100000 " MonteCarlo_long.conf
        sed -i "/RValueForConvergence    1.01 /c RValueForConvergence    1.1 " MonteCarlo_long.conf

        sed -i "/PrerunMaxIter              10000000 /c PrerunMaxIter              5000000 " MonteCarlo_full.conf
        sed -i "/RValueForConvergence    1.01 /c RValueForConvergence    1.1 " MonteCarlo_full.conf


        cp MonteCarlo_long.conf MonteCarlo_long_initial_chain_priors.conf
        sed -i "/MCMCInitialPosition    Center /c MCMCInitialPosition    RandomPrior " MonteCarlo_long_initial_chain_priors.conf


        mkdir -p results_fits
        mkdir -p results_observables
        cd results_observables
        analysis ../Globalfits/AllOps/model_fits.conf --noMC |& tee observables.txt

        cd $ORIGINAL_PATH

    done
done

python modify_observables.py