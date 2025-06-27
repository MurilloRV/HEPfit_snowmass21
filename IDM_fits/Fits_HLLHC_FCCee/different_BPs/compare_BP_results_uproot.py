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
    "fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_small_priors_strict",
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
# colors = ["tab:blue", "tab:orange"]
colors = ["tab:red", "tab:blue"]
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
        ax.set_ylabel("Posterior distribution", fontsize=12)

        for spec, label, color, color_rgb in zip(model_specs[scenario], spec_labels, colors, colors_rgb_list):

            # Open the ROOT file
            file_path = f"{working_dir}/{BP}/{scenario}/results_{spec}/MCout.root"
            with uproot.open(file_path) as file:

                hist_lmbd_y, hist_lmbd_x = file["deltalHHH_HLLHC"].to_numpy()
                hist_lmbd_x = hist_lmbd_x + 1 
                plt.hist(hist_lmbd_x[:-1], hist_lmbd_x, weights=hist_lmbd_y, label=label, density=True, histtype="step", edgecolor=(*color_rgb, 1.0), facecolor=(*color_rgb, 0.5), linewidth=1.5, fill=True)

        plt.axvline(BP_lambda, color="black", linestyle="--", label=rf"IDM {BP_name} value"+"\n"+rf"($\kappa_{{\lambda}}$ = {BP_lambda:.2f})")
        plt.legend(fontsize=9, loc="best")
        plt.tight_layout()
        plt.savefig(f"{working_dir}/comparison_plots/results_{results_dir}/IDM_{BP}_{scenario}_final.pdf")

# plt.show()






import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
import subprocess
import os.path


plt.rcParams.update({
#   "text.usetex": True,
  'text.latex.preamble': r'\usepackage{txfonts}'+'\n'+r'\usepackage{amsmath}',
})


def observable_order(obs):
    order_dict = {
        "deltalHHH_HLLHC": 1,
    }
    if obs in order_dict:
        order = order_dict[obs]
    else:
        order = 999999

    return order

plot_pull = False

# Open the input file in read mode and output file in write mode
working_dir = "./"


# BPs = [f"BP_{i}" for i in range(8)]

num_BPOs = 2
num_BPBs = 17
BPs = [f"BPO_{i}" for i in range(num_BPOs)]
BPs = BPs + [f"BPB_{i}" for i in range(num_BPBs)]
BPs = ["BPB_2", "BPB_4", "BPB_6"]
# BPs = ["BPB_2",]
# BP_Names = ["BPB 2", "BPB 4", "BPB 6",]
BP_Names = ["BP 1", "BP 2", "BP 3"]
# BP_Names = ["BPB 2",]
print(f"BPs: {BPs}")


obs_list = ["deltalHHH_HLLHC",]
obs_tex_list = [r"$\kappa_{\lambda}$",]
true_kappas = {
    "BPB_2": 2.3867362274064843,
    "BPB_4": 3.3446699219962595,
    "BPB_6": 4.332584967850238,
}



n_BPs = len(BPs)

# scenarios = ["IDM_FCCee240_FCCee365" for i in range(n_BPs)]
scenarios = [
    # "IDM_FCCee240",
    "IDM_FCCee240_FCCee365",
    # "IDM_FCCee240_FCCee365_HLLHClambda",
]

scenario_titles = [
    # rf"FCC-ee$_{{240}}$",
    rf"FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$",
    # rf"FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$ + $\kappa_{{\lambda}}$ at HL-LHC",
]


files = {}
for BP in BPs:
    files[BP] = {}
    for scenario in scenarios:
        files[BP][scenario] = {}
        for model_spec in model_specs[scenario]:
            files[BP][scenario][model_spec] = f"{working_dir}{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"


print(f"Reading fit results")
results = {}
observables = {}
observables_tex = {}
central_values_obs = {}

for BP in BPs:

    results[BP] = {}
    observables[BP] = {}
    observables_tex[BP] = {}
    central_values_obs[BP] = {}
    for scenario in scenarios:

        results[BP][scenario] = {}
        observables[BP][scenario] = {}
        observables_tex[BP][scenario] = {}
        central_values_obs[BP][scenario] = {}
        for model_spec in model_specs[scenario]:

            file_path = files[BP][scenario][model_spec]
            observables[BP][scenario][model_spec] = obs_list
            observables_tex[BP][scenario][model_spec] = obs_tex_list
            central_values_obs[BP][scenario][model_spec] = [true_kappas[BP],]

            print(f"Reading file: {file_path}")

            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    
                    line_nrs = [np.nan for obs in observables[BP][scenario][model_spec]]
                    for n, line in enumerate(lines):
                        columns = line.split()
                        if len(columns) < 2:
                            continue
                        
                        if (columns[1] == "Observable" \
                            or columns[1] == "AsyGausObservable") \
                            and columns[2][1:-2] in observables[BP][scenario][model_spec]:

                            observable_index = observables[BP][scenario][model_spec].index(columns[2][1:-2])
                            line_nrs[observable_index] = n

                    print(f"Line numbers: {line_nrs}")

                    if any(np.isnan(line_nrs)):
                        print(f"Missing observable: {observables[BP][scenario][model_spec][line_nrs.index(np.nan)]}")
                        raise ValueError(f"Not all observables were found in the file {file_path}!")

                    results[BP][scenario][model_spec] = []
                    # print(BP)

                    for line_nr, obs in zip(line_nrs, observables[BP][scenario][model_spec]):
                    
                        columns = lines[line_nr + 1].split()
                        if obs == "deltalHHH_HLLHC":
                            results[BP][scenario][model_spec].append([float(columns[3])+1,    # Mean
                                                                    float(columns[5]),])  # Uncertainty
                        else:
                            results[BP][scenario][model_spec].append([float(columns[3]),    # Mean
                                                                float(columns[5]),])  # Uncertainty

            else:
                print(f"File not found: {file_path}")
                results[BP][scenario][model_spec] = []
                for obs in observables[BP][scenario][model_spec]:
                    results[BP][scenario][model_spec].append(np.full(2, np.nan))

            results[BP][scenario][model_spec] = np.array(results[BP][scenario][model_spec])

            # print(results[BP][scenario])

            # index = observables[BP][scenario][model_spec].index("muttHWW2l2vHL")
            # print(f"muttHWW2l2vHL results = {results[BP][scenario][model_spec][index,:]}")


# Align observables across model_specs
aligned_observables = {}
aligned_observables_tex = {}

for BP in BPs:
    aligned_observables[BP] = {}
    aligned_observables_tex[BP] = {}

    for scenario in scenarios:
        # Collect all unique observables across model_specs
        all_observables = set()
        for model_spec in model_specs[scenario]:
            all_observables.update(observables[BP][scenario][model_spec])

        aligned_observables[BP][scenario] = sorted(all_observables, key=observable_order)

        aligned_observables_tex[BP][scenario] = [np.nan for i in range(len(aligned_observables[BP][scenario]))]

        # Align central values for observables for each model_spec
        for model_spec in model_specs[scenario]:
            aligned_central_values = []
            aligned_results = []
            for aligned_idx, obs in enumerate(aligned_observables[BP][scenario]):
                if obs in observables[BP][scenario][model_spec]:
                    idx = observables[BP][scenario][model_spec].index(obs)
                    aligned_central_values.append(central_values_obs[BP][scenario][model_spec][idx])
                    aligned_results.append(results[BP][scenario][model_spec][idx])
                    aligned_observables_tex[BP][scenario][aligned_idx] = observables_tex[BP][scenario][model_spec][idx]
                else:
                    # Handle missing observables (e.g., assign NaN)
                    aligned_central_values.append(np.nan)
                    aligned_results.append([np.nan, np.nan])

            central_values_obs[BP][scenario][model_spec] = np.array(aligned_central_values)
            results[BP][scenario][model_spec] = np.array(aligned_results)

        if np.nan in aligned_observables_tex[BP][scenario]:
            print(f"Missing observable LaTeX: {aligned_observables[BP][scenario][aligned_observables_tex[BP][scenario].index(np.nan)]}")
            raise ValueError(f"Not all observables LaTeX descriptions were found in the file for {BP} in scenario: {scenario}, model spec {model_spec}!")

print(f"\n\n\n")
print(f"Aligned observables: {aligned_observables[BP][scenario]}")
print(f"Aligned observables (LaTeX): {aligned_observables_tex[BP][scenario]}")
print(f"Central values shape: {central_values_obs[BP][scenario][model_spec].shape}")
print(f"results shape: {results[BP][scenario][model_spec].shape}")
# print(f"results: {results}")



table_tex_output_file = working_dir + f'comparison_plots/results_{results_dir}/klam_results.tex'
headers = ["", "True value", "Original fit", "With new NPs"]
columns = BP_Names
# table_text = "\\hline\n" + " & ".join(headers) + "\\\\\n"
table_text = " & ".join(headers) + "\\\\\n"
table_text += "\\hline"
for idx, (column, BP) in enumerate(zip(columns, BPs)):
    table_text += "\\hline\n"
    table_text += f"{column} & {BP_lambdas[idx]:.3g}"
    for model_spec in model_specs[scenario]:
        klam = results[BP][scenario][model_spec][0,0]
        klam_err_abs = results[BP][scenario][model_spec][0,1]
        klam_err_rel = klam_err_abs / klam
        table_text += rf" & ${klam:.2f}\pm{klam_err_abs:.2f}\;[\textcolor{{violet}}{{{100*klam_err_rel:.2g}\%}}]$"
    table_text += "\\\\"

with open(table_tex_output_file, "w") as out_file:
    print("\\begin{tabular}{c||c|c|c}", file=out_file)
    print(table_text, file=out_file)
    print("\\end{tabular}", file=out_file)
    # print("\\hline\n\\end{tabular}", file=out_file)
