import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
import subprocess
import os.path

# Old script, to be implemented in new package


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

# scenarios = ["IDM_ILC250_ILC350" for i in range(n_BPs)]
scenarios = [
    # "IDM_ILC250",
    "IDM_IL_250_350",
    # "IDM_IL_250_350_HLLHClambda",
]

scenario_titles = [
    # rf"ILC-ee$_{{250}}$",
    rf"ILC$_{{250}}$ + ILC$_{{350}}$",
    # rf"ILC$_{{250}}$ + ILC$_{{350}}$ + $\kappa_{{\lambda}}$ at HL-LHC",
]




theo_errs = ["0.0010", "0.0020", "0.0050", "0.0075", "0.010", "0.015", "0.020", "0.030", "0.050", "0.100",]
# specs = [ f"fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_no_HLLHC_Higgs_err{err}_small_priors_long" for err in theo_errs]
specs = [ f"fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_err{err}_small_priors_strict" for err in theo_errs]

# spec_compare = "fits_realistic_HL_LHC_WFR_kala2_input_all_no_HLLHC_Higgs_small_priors_long"
spec_compare = "fits_realistic_HL_LHC_WFR_kala2_input_all_all_EW_mods_small_priors_long"
model_specs = {
    # "IDM_ILC250" : [spec, "fits"],
    "IDM_ILC250_ILC350" : [*specs, spec_compare],
    # "IDM_ILC250_ILC350_HLLHClambda" : [spec, "fits_realistic_HL_LHC_realistic_HL_LHC_long"],
}

labels = [r"$\epsilon^{\text{theo}}=$"+err for err in theo_errs]
model_specs_labels = {
    # "IDM_ILC250" : labels,
    "IDM_ILC250_ILC350" : [*labels, "Original"],
    # "IDM_ILC250_ILC350_HLLHClambda" : labels,
}

# results_dir = spec
results_dir = "klam_results_new_NPs_scale1.52_comparison"

# Create the output directory
subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{results_dir}"])

plot_title = {}

for i, BP in enumerate(BPs):
    plot_title[BP] = {}

    for scenario, scenario_title in zip(scenarios, scenario_titles):
        plot_title[BP][scenario] = rf"IDM ({BP_Names[i]}), {scenario_title}"


colors = [
    "tab:orange",
    "tab:blue",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:brown",
    "tab:pink",
    "tab:gray",
    "tab:olive",
    "tab:cyan",
    "black",
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


# y_shift = [-0.15, 0.15]
w = 1.7
dimw = w / 2
n_specs = len(model_specs["IDM_ILC250_ILC350"])
y_shift = np.linspace(+dimw/2, -dimw/2, n_specs) 


fig_klam_err_curves, ax_klam_err_curves = plt.subplots(figsize=(5.5,4), dpi=150)
BP_colors = [
    "tab:blue", 
    "tab:red", 
    "tab:green",
]
BP_labels = [
    r"$\kappa_\lambda=2.39$",
    r"$\kappa_\lambda=3.34$",
    r"$\kappa_\lambda=4.33$",
]

fig_num = 0
for i, BP in enumerate(BPs):

    for scenario in scenarios:


        labels = aligned_observables_tex[BP][scenario][:]
        for j, obs in enumerate(aligned_observables_tex[BP][scenario]):
            labels[j] = obs


        nvar_per_plot = 50
        param_breaks = np.arange(0, len(aligned_observables[BP][scenario]), nvar_per_plot)

        if len(param_breaks)==1 or param_breaks[-1] != len(aligned_observables[BP][scenario]):
            param_breaks = np.append(param_breaks, [len(aligned_observables[BP][scenario])])

        print(len(aligned_observables[BP][scenario]))
        print(param_breaks)

        
        for k in range(len(param_breaks) - 1):

            fig, ax = plt.subplots(figsize=(5.5,4), dpi=150)
            fig_num = fig_num + 1
            # ax = plt.gca()

            for spec_index, model_spec in enumerate(model_specs[scenario]):

                # index = aligned_observables[BP][scenario].index("muttHWW2l2vHL")
                # print(f"muttHWW2l2vHL results = {results[BP][scenario][model_spec][index,:]}")

                if plot_pull:
                    results_means  = np.copy((results[BP][scenario][model_spec][:,0] - central_values_obs[BP][scenario][model_spec]) / results[BP][scenario][model_spec][:,1] )
                    results_errors = np.copy( results[BP][scenario][model_spec][:,1] / results[BP][scenario][model_spec][:,1] )
                    plt.axvline(x=0, c='0.6', linewidth=2)
                else:
                    results_means  = np.copy( results[BP][scenario][model_spec][:,0] )
                    results_errors = np.copy( results[BP][scenario][model_spec][:,1] )
                    plt.axvline(x=central_values_obs[BP][scenario][model_spec], c='0.6', linewidth=2)

                y = np.arange(param_breaks[k],param_breaks[k+1])
            
                ax.errorbar(results_means[param_breaks[k]:param_breaks[k+1]],
                            -y-y_shift[spec_index], 
                            # -y, 
                            xerr=(results_errors[param_breaks[k]:param_breaks[k+1]],), 
                            fmt='o', 
                            linewidth=1.5, 
                            capsize=3.5, 
                            markersize=4, 
                            color=colors[spec_index],
                            label=model_specs_labels[scenario][spec_index],
                            # alpha=alphas[i],
                            )

            # ax.set_yticks(-y-y_shift)
            ax.set_yticks([])
            # ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]],fontsize=8)
            ax.set_yticklabels([])
            x_limits = [plt.xlim()[0], plt.xlim()[1]]
            y_limits = [plt.ylim()[0] +1.0, plt.ylim()[1] -1.0]
            # ax.hlines(y=-y, xmin=x_limits[0], xmax=x_limits[1], color="black", linestyle="--", linewidth=0.5)
            ax.set_xlim(*x_limits)
            ax.set_ylim(*y_limits)
            ax.tick_params(axis='x', size=10, labelsize=11)
            ax.tick_params(axis='x', which='minor', size=6)
            if plot_pull:
                ax.set_xlabel(r'$\kappa_{\lambda}$ pulls', fontsize=13)
                plot_filename = f"klam_pull_{BP}_{scenario}_compare"
            else:
                ax.set_xlabel(r'$\kappa_{\lambda}$ results', fontsize=13)
                plot_filename = f"klam_results_{BP}_{scenario}_compare"
            ax.legend(loc='best', fontsize=8, bbox_to_anchor=(1., 1.))
            ax.set_title(plot_title[BP][scenario], fontsize=11)
            plt.tight_layout()   # Makes sure labels are not cut off
            plt.savefig(working_dir + f'comparison_plots/results_{results_dir}/{plot_filename}.pdf')

            plot_theo_errs = [0.0] + [float(err) for err in theo_errs]
            plot_klam_errs = [results[BP][scenario][model_spec][0,1] for model_spec in model_specs[scenario]]
            plot_klam_errs = plot_klam_errs[-1:] + plot_klam_errs[:-1]
            ax_klam_err_curves.plot(plot_theo_errs, plot_klam_errs, label=BP_labels[i], color=BP_colors[i])
            ax_klam_err_curves.scatter(plot_theo_errs, plot_klam_errs, color=BP_colors[i])


# Generate plots with curves for the klam uncertainty as function of the new theo NP,
# one curve per BP/kappa_lambda
# fig_klam_err_curves 
# ax_klam_err_curves
ax_klam_err_curves.grid(which='major', linestyle='--', linewidth=0.5, color="black")
ax_klam_err_curves.grid(which='minor', linestyle='--', linewidth=0.5)
ax_klam_err_curves.set_xlabel(r"$\epsilon^\text{theo}$", fontsize=15)
ax_klam_err_curves.set_ylabel(r"$\kappa_{\lambda}$ absolute uncertainty", fontsize=13)
ax_klam_err_curves.set_xscale('log')
ax_klam_err_curves.legend(loc='best', fontsize=10,)
fig_klam_err_curves.tight_layout()   # Makes sure labels are not cut off
plot_filename = f"klam_error_curves_{scenario}"
fig_klam_err_curves.savefig(working_dir + f'comparison_plots/results_{results_dir}/{plot_filename}.pdf')

# plt.show()

table_tex_output_file = working_dir + f'comparison_plots/results_{results_dir}/klam_results.tex'
headers = ["Scenario", "BP 1", "BP 2", "BP 3"]
columns = [rf"$\epsilon^{{\text{{theo}}}}={err}$" for err in theo_errs] + ["Original"]
table_text = "\\hline\n" + " & ".join(headers) + "\\\\\n"
table_text += "\\hline"
for column, model_spec in zip(columns, model_specs[scenario]):
    table_text += "\\hline\n"
    table_text += f"{column} & " + " & ".join([f"${results[BP][scenario][model_spec][0,1]:.3g}$" for BP in BPs]) + "\\\\"

with open(table_tex_output_file, "w") as out_file:
    print("\\begin{tabular}{|c||c|c|c|}", file=out_file)
    print(table_text, file=out_file)
    print("\\hline\n\\end{tabular}", file=out_file)
