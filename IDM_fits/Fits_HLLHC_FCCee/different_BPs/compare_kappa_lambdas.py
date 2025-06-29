import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import math
import subprocess

plt.rcParams.update({
#   "text.usetex": True,
  'text.latex.preamble': r'\usepackage{txfonts}',
})

working_dir = "./"

scenarios = [
    # "IDM_FCCee240",
    "IDM_FCCee240_FCCee365",
    # "IDM_FCCee240_FCCee365_HLLHClambda"
]

spec = "fits_realistic_HL_LHC_smeft_formula_all_small_priors_long"

model_specs = {
    # "IDM_FCCee240" : spec,
    "IDM_FCCee240_FCCee365" : [spec],
    # "IDM_FCCee240_FCCee365_HLLHClambda" : spec,
}

# results_dir = "fits_realistic_HL_LHC_no_1L_BSM_small_priors_long"
results_dir = spec

BPs = ["BPB_2", "BPB_4", "BPB_6"]
# plot_labels = ["BP 1", "BP 2", "BP 3"]
plot_labels = [
    r"BP 1 $(\kappa_\lambda=2.39)$",
    r"BP 2 $(\kappa_\lambda=3.34)$",
    r"BP 3 $(\kappa_\lambda=4.33)$",
]
n_BPs = len(BPs)

lambdas = [
    2.3867362274064843,
    3.3446699219962595,
    4.332584967850238,
]


# files = [working_dir + file_dir + f"/results_{model_specs}/Observables/Statistics.txt" for file_dir in scenarios]
files = {}
for BP in BPs:
    files[BP] = {}
    for scenario in scenarios:
        files[BP][scenario] = {}
        for model_spec in model_specs[scenario]:
            files[BP][scenario][model_spec] = f"{working_dir}{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"


# Create the output directory
subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{results_dir}"])



kappa_lambda_results = {}
for BP in BPs:

    kappa_lambda_results[BP] = {}
    for scenario in scenarios:

        kappa_lambda_results[BP][scenario] = {}
        for model_spec in model_specs[scenario]:

            file_path = files[BP][scenario][model_spec]
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
                for n, line in enumerate(lines):
                    columns = line.split()
                    if len(columns) < 2:
                        continue
                    
                    if columns[1] == "Observable" and columns[2].startswith("\"deltalHHH_HLLHC"):
                        line_kappa_lambda = n
                        
                columns_kappa_lambda = lines[line_kappa_lambda + 1].split()
                kappa_lambda_results[BP][scenario][model_spec] = [float(columns_kappa_lambda[3])+1,  # Mean
                                                                  float(columns_kappa_lambda[5]),]   # Uncertainty
                
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(3.5, 4), height_ratios=[0.7, 0.3], dpi=300, gridspec_kw=dict(hspace=0.))
colors = [
    "tab:blue",
    "tab:orange",
    "tab:green",
]

means  = {BP : kappa_lambda_results[BP][scenario][model_spec][0] for BP in BPs}
errors = {BP : kappa_lambda_results[BP][scenario][model_spec][1] for BP in BPs}
for i, BP in enumerate(BPs):
    ax1.errorbar(x=lambdas[i],
                 y=means[BP],
                 yerr=(errors[BP],), 
                 fmt='o', 
                 linewidth=1.5, 
                 capsize=3.5, 
                 markersize=4, 
                 label=plot_labels[i],
                 color=colors[i])
    
    ax2.errorbar(x=lambdas[i],
                 y=means[BP] - lambdas[i],
                 yerr=(errors[BP],), 
                 fmt='o', 
                 linewidth=1.5, 
                 capsize=3.5, 
                 markersize=4, 
                 color=colors[i])
    
plt.axhline(y=0, c='0.6', linewidth=1)

# ax2.tick_params(axis='x', size=10, labelsize=12)
# ax2.tick_params(axis='x', which='minor', size=6)

# ax1.set_yticks(lambdas)
# ax2.set_xticks(lambdas)
# ax2.set_xticklabels(lambdas,fontsize=16)
ax1.set_xlim(2.0, 5.0)
ax2.set_ylim(-0.9, 0.9)
    
ax1.set_ylabel(r'$\kappa_{\lambda}^\text{fit}$', fontsize=15)
ax2.set_ylabel(r'$\kappa_{\lambda}^\text{fit} - \kappa_{\lambda}^\text{true}$', fontsize=15)

ax2.set_xlabel(r'$\kappa_{\lambda}^\text{true}$', fontsize=15)

ax1.grid(which='both', linestyle='--', linewidth=0.5)
ax2.grid(which='both', linestyle='--', linewidth=0.5)
ax1.legend(loc='best', fontsize=9)
plt.tight_layout()   # Makes sure labels are not cut off

plt.savefig(working_dir + f'comparison_plots/results_{results_dir}/kappa_lambda_results.pdf')

# plt.show()
