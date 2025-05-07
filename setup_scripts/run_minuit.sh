#!/bin/bash

working_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/different_scenario_fits/"
model_spec="SQUARED"
cd ${working_dir}/SM_noHLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/SM_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Z2SSM_noHLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Z2SSM_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf


working_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/large_kappa_lambda_fits/"
model_spec="fits"
cd ${working_dir}/Lambda2_noHLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda2_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda3_noHLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda3_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda5_noHLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda5_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda10_noHLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda10_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf


working_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/different_scenario_fits/"
model_spec="crosscheck_1percent_k_lambda_error"
cd ${working_dir}/Z2SSM_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf




working_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits/"
model_spec="all_uncertainties_SQUARED"
cd ${working_dir}/SM_FCCee240/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_all_uncertainties.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/SM_FCCee240_FCCee365/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_all_uncertainties.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/SM_FCCee240_FCCee365_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_all_uncertainties.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Z2SSM_FCCee240/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Z2SSM_FCCee240_FCCee365/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Z2SSM_FCCee240_FCCee365_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf



working_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/large_kappa_lambda_fits/"
model_spec="fits"
cd ${working_dir}/Lambda2_FCCee240_FCCee365_noHLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda2_FCCee240_FCCee365_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda3_FCCee240_FCCee365_noHLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda3_FCCee240_FCCee365_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda5_FCCee240_FCCee365_noHLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda5_FCCee240_FCCee365_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda10_FCCee240_FCCee365_noHLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf
cd ${working_dir}/Lambda10_FCCee240_FCCee365_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf


working_dir="/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/different_scenario_fits/"
model_spec="crosscheck_1percent_k_lambda_error"
cd ${working_dir}/Z2SSM_FCCee240_FCCee365_HLLHClambda/results_${model_spec}/
../../../../HEPfit/build_rocky9/HEPfit/bin/analysis ../Globalfits/AllOps/model_${model_spec}.conf ../MonteCarlo_MinuitOnly.conf


cd /cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/