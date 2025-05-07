import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import math
import subprocess

plt.rcParams.update({
#   "text.usetex": True,
  'text.latex.preamble': r'\usepackage{txfonts}',
})

short_range = True


model_specs = "fits_small_priors_long"
working_dir = "./"

if short_range:
    lambdas = list(range(0, 7))
else:
    lambdas = list(range(-5, 11))

scenarios = [f"Lambda{lamb}_FCCee240_FCCee365_noHLLHClambda" for lamb in lambdas]

# plot_title = "Comparison of the kappa-lambda fits"

plot_labels = [rf"$\kappa_\lambda={lamb}$" for lamb in lambdas]
n_scenarios = len(scenarios)

files = [working_dir + file_dir + f"/results_{model_specs}/Observables/Statistics.txt" for file_dir in scenarios]

# Create the output directory
subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{model_specs}"])


# def plot_obs(fig,
#              ax,
#              scenarios,
#              means,
#              errors, 
#              y,
#              colors,
#              scenario_labels,
#              obs_labels,
#              file_name,
#              not_first_plot,
#              ):
    
#     y = np.arange(param_breaks[k],param_breaks[k+1])
    
#     for i, scenario in enumerate(scenarios):
#         ax.errorbar(means[scenario], -y+y_shift[i], xerr=(errors[scenario],), 
#                     fmt='o', linewidth=1.5, capsize=3.5, markersize=4, label = scenario_labels[i], color=colors[i])
        
#     x_limits = ax.get_xlim()
#     # print(x_limits)
    
#     if not_first_plot:
#         for i, scenario in enumerate(scenarios):
#             ax.hlines(y=-y+y_shift[i], xmin=x_limits[0], xmax=x_limits[1], color="black", linestyle="--", linewidth=0.1)
        
#         ax.set_xlim(*x_limits)

#     plt.axvline(x=1, c='0.6', linewidth=2)
#     ax.set_yticks(-y-dimw/2.)
#     ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]],fontsize=16)
#     ax.tick_params(axis='x', size=10, labelsize=12)
#     ax.tick_params(axis='x', which='minor', size=6)
#     ax.set_xlabel(r'Means and standard deviations', fontsize=15)
#     if not not_first_plot: ax.legend(loc='best', fontsize=7, ncol=2)
#     plt.tight_layout()   # Makes sure labels are not cut off
#     # plt.savefig(file_name)


kappa_lambda_results = {}
for file_path, scenario in zip(files, scenarios):

    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for n, line in enumerate(lines):
            columns = line.split()
            if len(columns) < 2:
                continue
            
            if columns[1] == "Observable" and columns[2].startswith("\"deltalHHH_HLLHC"):
                line_kappa_lambda = n
                
        columns_kappa_lambda = lines[line_kappa_lambda + 1].split()
        kappa_lambda_results[scenario] = [float(columns_kappa_lambda[3])+1,  # Mean
                                          float(columns_kappa_lambda[5]),]   # Uncertainty
        
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(4.5, 5), height_ratios=[0.7, 0.3], dpi=300, gridspec_kw=dict(hspace=0.))
# fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(4.5, 5), height_ratios=[0.7, 0.3], dpi=300)
# Remove horizontal space between axes
# fig.subplots_adjust(hspace=0)

# colors = mpl.colormaps['hsv']
# colors = list(colors(np.linspace(0.001, 0.9, len(lambdas))[::-1]))

colors = "tab:blue"

means  = {scenario : kappa_lambda_results[scenario][0] for scenario in scenarios}
errors = {scenario : kappa_lambda_results[scenario][1] for scenario in scenarios}
for i, scenario in enumerate(scenarios):
    ax1.errorbar(x=lambdas[i],
                 y=means[scenario],
                 yerr=(errors[scenario],), 
                 fmt='o', 
                 linewidth=1.5, 
                 capsize=3.5, 
                 markersize=4, 
                 color=colors)
    
    ax2.errorbar(x=lambdas[i],
                 y=means[scenario] - lambdas[i],
                 yerr=(errors[scenario],), 
                 fmt='o', 
                 linewidth=1.5, 
                 capsize=3.5, 
                 markersize=4, 
                 color=colors)
    
plt.axhline(y=0, c='0.6', linewidth=1)

# ax2.tick_params(axis='x', size=10, labelsize=12)
# ax2.tick_params(axis='x', which='minor', size=6)

ax1.set_yticks(lambdas)

ax2.set_xticks(lambdas)
# ax2.set_xticklabels(lambdas,fontsize=16)
ax2.set_ylim(-0.9, 0.9)
    
ax1.set_ylabel(r'$\kappa_{\lambda}^\text{fit}$', fontsize=15)
ax2.set_ylabel(r'$\kappa_{\lambda}^\text{fit} - \kappa_{\lambda}^\text{true}$', fontsize=15)

ax2.set_xlabel(r'$\kappa_{\lambda}^\text{true}$', fontsize=15)

ax1.grid(which='both', linestyle='--', linewidth=0.5)
ax2.grid(which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()   # Makes sure labels are not cut off

if short_range:
    plt.savefig(working_dir + f'comparison_plots/results_{model_specs}/kappa_lambda_results_short_range.pdf')
else:
    plt.savefig(working_dir + f'comparison_plots/results_{model_specs}/kappa_lambda_results.pdf')

# plt.show()
