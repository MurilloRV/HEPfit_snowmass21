import uproot
import subprocess
import hist
from matplotlib import pyplot as plt
import matplotlib

working_dir = "."

all_scenarios = [
    # "IDM_FCCee240",
    "IDM_FCCee240_FCCee365",
    # "IDM_FCCee240_FCCee365_HLLHClambda"
]

specs = [
    # "fits_realistic_HL_LHC_WFR_kala2_input_all_small_priors_long",
    # "fits_realistic_HL_LHC_WFR_kala2_input_all_no_HLLHC_Higgs_small_priors_long",
    "fits_realistic_HL_LHC_WFR_kala2_input_all_all_EW_mods_small_priors_long",
    # "fits_realistic_HL_LHC_WFR_kala2_input_all_all_EW_mods_no_HLLHC_Higgs_small_priors_long",
    # "fits_realistic_HL_LHC_WFR_kala2_input_no_C_HG_small_priors_long",
    # "fits_realistic_HL_LHC_WFR_kala2_input_no_HLLHC_Higgs_small_priors_long",
    # "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_small_priors_long",
    # "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_no_HLLHC_Higgs_small_priors_long",
    # "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_all_EW_mods_small_priors_long",
    # "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_all_EW_mods_no_HLLHC_Higgs_small_priors_long",
    "fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_small_priors_long",
    # "fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_small_priors_strict",
    # "fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_no_HLLHC_Higgs_small_priors_long",
]

spec_labels = [
    "Original",
    "With new NPs",
    # "With new, scaled NPs",
]


model_specs = {
    # "IDM_FCCee240" : spec,
    "IDM_FCCee240_FCCee365" : specs,
    # "IDM_FCCee240_FCCee365_HLLHClambda" : spec,
}


# results_dirs = specs
# results_dirs = [ model_specs["IDM_FCCee240_FCCee365"] for spec in specs ]
results_dir = "comparison_NPs_scaled"

# num_BPs = 8
# num_BPOs = 2
# num_BPBs = 17
# BPs = [f"BP_{i}" for i in range(num_BPs)]
# BPs = [f"BPO_{i}" for i in range(num_BPOs)]
# BPs = BPs + [f"BPB_{i}" for i in range(num_BPBs)]

BPs = ["BPB_2", "BPB_4", "BPB_6", ]
BP_names = ["BP 1", "BP 2", "BP 3", ]
colors = ["tab:blue", "tab:orange"]
colors_rgb_list = [ matplotlib.colors.to_rgb(c) for c in colors ]
print(colors_rgb_list)
BP_lambdas = [        
    2.3867362274064843, # BPB_2
    3.3446699219962595, # BPB_4
    4.332584967850238, # BPB_6
]
print(BPs)

# Create the output directories
subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])


fig_num = 0
for scenario in all_scenarios:
    for BP, BP_name, BP_lambda in zip(BPs, BP_names, BP_lambdas):

        fig = plt.figure(fig_num, figsize=(4.0, 3.5), dpi=300)
        fig_num += 1
        ax = plt.gca()
        ax.set_title(rf"IDM {BP_name}, FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$")
        ax.set_xlabel(r"$\kappa_{\lambda}$", fontsize=12)

        for spec, label, color, color_rgb in zip(model_specs[scenario], spec_labels, colors, colors_rgb_list):

            # Open the ROOT file
            file_path = f"{working_dir}/{BP}/{scenario}/results_{spec}/MCout.root"
            with uproot.open(file_path) as file:
                # print(file.classnames())

                

                hist_lmbd_y, hist_lmbd_x = file["deltalHHH_HLLHC"].to_numpy()
                hist_lmbd_x = hist_lmbd_x + 1 
                plt.hist(hist_lmbd_x[:-1], hist_lmbd_x, weights=hist_lmbd_y, label=label, density=True, histtype="step", edgecolor=(*color_rgb, 1.0), facecolor=(*color_rgb, 0.5), linewidth=1.5, fill=True)
                # plt.hist(hist_lmbd_x[:-1], hist_lmbd_x, weights=hist_lmbd_y, color=color, alpha=0.5, density=True)
                # plt.stairs(hist_lmbd_y, hist_lmbd_x, label=label, fill=True, alpha=0.5)
                # print("hist_lmbd:", hist_lmbd)
                # hist_lmbd.plot()

        plt.axvline(BP_lambda, color="black", linestyle="--", label=rf"IDM {BP_name} value"+"\n"+rf"($\kappa_{{\lambda}}$ = {BP_lambda:.2f})")
        plt.legend(fontsize=9, loc="best")
        plt.tight_layout()
        plt.savefig(f"{working_dir}/comparison_plots/results_{results_dir}/IDM_{BP}_{scenario}_final.pdf")

# plt.show()