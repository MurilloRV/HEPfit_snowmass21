import subprocess


# model_spec = "fits"
# model_spec = "fits_realistic_HL_LHC_all_EW_mods_long"
# model_spec = "fits_realistic_HL_LHC_no_1L_BSM_sqrt_s_long"

# Open the input file in read mode and output file in write mode
# working_dir = "./"
working_dir = "../../Self_consistent_IDM_fits/"


all_scenarios = [
    # "IDM_FCCee240",
    "IDM_FCCee240_FCCee365",
    # "IDM_FCCee240_FCCee365_HLLHClambda"
]

specs = [
    # "fits_realistic_HL_LHC_smeft_formula_small_priors_long",
    # "fits_realistic_HL_LHC_smeft_formula_sqrt_small_priors_long",
    # "fits_realistic_HL_LHC_smeft_formula_no_cross_small_priors_long",
    # "fits_realistic_HL_LHC_smeft_formula_all_small_priors_long",
    # "fits_realistic_HL_LHC_smeft_formula_no_cross_no_C_HG_small_priors_long",
    # "fits_realistic_HL_LHC_smeft_formula_no_cross_no_HLLHC_Higgs_small_priors_long",
    # "fits_realistic_HL_LHC_smeft_formula_external_leg_small_priors_long",
    # "fits_realistic_HL_LHC_WFR_kala2_input_small_priors_long",
    # "fits_realistic_HL_LHC_WFR_kala2_input_all_small_priors_long",
    # "fits_realistic_HL_LHC_WFR_kala2_input_all_no_HLLHC_Higgs_small_priors_long",
    "fits_realistic_HL_LHC_WFR_kala2_input_all_all_EW_mods_small_priors_long",
    # "fits_realistic_HL_LHC_WFR_kala2_input_all_all_EW_mods_no_HLLHC_Higgs_small_priors_long",
    # "fits_realistic_HL_LHC_WFR_kala2_input_no_C_HG_small_priors_long",
    # "fits_realistic_HL_LHC_WFR_kala2_input_no_HLLHC_Higgs_small_priors_long",
    # "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_small_priors_long",
    # "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_no_HLLHC_Higgs_small_priors_long",
    "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_all_EW_mods_small_priors_long",
#     "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_all_EW_mods_no_HLLHC_Higgs_small_priors_long",
    "fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_small_priors_long",
    # "fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_small_priors_strict",
#     "fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_no_HLLHC_Higgs_small_priors_long",
]


model_specs = {
    # "IDM_FCCee240" : spec,
    "IDM_FCCee240_FCCee365" : specs,
    # "IDM_FCCee240_FCCee365_HLLHClambda" : spec,
}

results_dirs = specs
# results_dirs = [ model_specs["IDM_FCCee240_FCCee365"] for spec in specs ]
# results_dirs = [ "final_mod_ranges" for spec in specs ]

# num_BPs = 8
# num_BPOs = 2
# num_BPBs = 17
# BPs = [f"BP_{i}" for i in range(num_BPs)]
# BPs = [f"BPO_{i}" for i in range(num_BPOs)]
# BPs = BPs + [f"BPB_{i}" for i in range(num_BPBs)]

BPs = ["BPB_2", "BPB_4", "BPB_6"]
# BPs = ["BP_lambda1"]
print(BPs)


# Create the output directories
for results_dir in results_dirs:
    subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{results_dir}"])

# Copy and rename plots for specific parameters/observables

# copy_obs = [
#     # "CH_corr", 
#     # "CHbox_corr", 
#     # "CHD_corr", 
#     "deltalHHH_HLLHC",
# ]

copy_obs = [
    # "CH_corr_mod", 
    # "CHbox_corr_mod", 
    # "CHD_corr_mod", 
    "deltalHHH_HLLHC_mod",
]


for scenario in all_scenarios:
    for spec, results_dir in zip(model_specs[scenario] , results_dirs):
        for BP in BPs:
            for obs in copy_obs:
                try:
                    subprocess.run(["cp", f"{working_dir}{BP}/{scenario}/results_{spec}/Observables/{obs}.pdf",
                            f"{working_dir}comparison_plots/results_{results_dir}/{obs}_{BP}_{scenario}.pdf"])
                except:
                    print(f"file not found: {working_dir}{BP}/{scenario}/results_{spec}/Observables/{obs}.pdf")