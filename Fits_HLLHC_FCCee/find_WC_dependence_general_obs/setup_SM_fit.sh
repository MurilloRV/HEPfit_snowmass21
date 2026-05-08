#!/bin/bash

ORIGINAL_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/find_WC_dependence_general_obs/"
COPY_PATH="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits/SM_FCCee240_FCCee365"

# Copying the configuration files 
mkdir -p $ORIGINAL_PATH/SM_fit/Globalfits/AllOps
cd $ORIGINAL_PATH/SM_fit/

cp $COPY_PATH/*.conf .
cp $COPY_PATH/Globalfits/AllOps/d6Ops_corr.conf Globalfits/AllOps/
cp $COPY_PATH/Globalfits/AllOps/model_all_uncertainties.conf Globalfits/AllOps/model_fits.conf

MODEL_CONF_FILE="model_fits"

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



cd $ORIGINAL_PATH
