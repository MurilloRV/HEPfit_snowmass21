import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
import subprocess

def find_tex_label(var):
    if var =="AlsMz":             tex_label = r"$\alpha_s(M_Z)$"
    elif var == "dAle5Mz":        tex_label = r"$\Delta\alpha_{\mathrm{had}}^{(5)}(M_Z^2)$"
    elif var == "mtop":           tex_label = r"$M_t$"
    elif var == "mHl":            tex_label = r"$M_h$"
    elif var == "Mz":             tex_label = r"$M_Z$"
    elif var == "CW":             tex_label = r"$C_W$"
    elif var == "CHG":            tex_label = r"$C_{HG}$"
    elif var == "CHWB":           tex_label = r"$C_{HWB}$"
    elif var == "CHWHB_gaga":     tex_label = r"$(C_{HWHB})_{\gamma\gamma}$"
    elif var == "CHWHB_gagaorth": tex_label = r"$(C_{HWHB})_{\gamma\gamma\text{orth}}$"
    elif var == "CHD":            tex_label = r"$C_{HD}$"
    elif var == "CHbox":          tex_label = r"$C_{H\boxdot}$"
    elif var == "CH":             tex_label = r"$C_{H}$"
    elif var == "CHL1_11":        tex_label = r"$(C_{HL}^{(1)})_{11}$"
    elif var == "CHL1_22":        tex_label = r"$(C_{HL}^{(1)})_{22}$"
    elif var == "CHL1_33":        tex_label = r"$(C_{HL}^{(1)})_{33}$"
    elif var == "CHL3_11":        tex_label = r"$(C_{HL}^{(3)})_{11}$"
    elif var == "CHL3_22":        tex_label = r"$(C_{HL}^{(3)})_{22}$"
    elif var == "CHL3_33":        tex_label = r"$(C_{HL}^{(3)})_{33}$"
    elif var == "CHe_11":         tex_label = r"$(C_{He})_{11}$"
    elif var == "CHe_22":         tex_label = r"$(C_{He})_{22}$"
    elif var == "CHe_33":         tex_label = r"$(C_{He})_{33}$"
    elif var == "CHQ1_11":        tex_label = r"$(C_{HQ}^{(1)})_{11}$"
    elif var == "CHQ1_33":        tex_label = r"$(C_{HQ}^{(1)})_{33}$"
    elif var == "CHQ3_11":        tex_label = r"$(C_{HQ}^{(3)})_{11}$"
    elif var == "CHu_11":         tex_label = r"$(C_{Hu})_{11}$"
    elif var == "CHd_11":         tex_label = r"$(C_{Hd})_{11}$"
    elif var == "CHd_33":         tex_label = r"$(C_{Hd})_{33}$"
    elif var == "CeH_22r":        tex_label = r"${Re}\left[(C_{eH})_{22}\right]$"
    elif var == "CeH_33r":        tex_label = r"${Re}\left[(C_{eH})_{33}\right]$"
    elif var == "CuH_22r":        tex_label = r"${Re}\left[(C_{uH})_{22}\right]$"
    elif var == "CuH_33r":        tex_label = r"${Re}\left[(C_{uH})_{33}\right]$"
    elif var == "CdH_33r":        tex_label = r"${Re}\left[(C_{dH})_{33}\right]$"
    elif var == "CLL_1221":       tex_label = r"$(C_{LL})_{1221}$"
    elif var == "eHggint":        tex_label = r"$\varepsilon_\text{Int}(H\to gg)$"
    elif var == "eHggpar":        tex_label = r"$\varepsilon_\text{Par}(H\to gg)$"
    elif var == "eHWWint":        tex_label = r"$\varepsilon_\text{Int}(H\to WW^*)$"
    elif var == "eHWWpar":        tex_label = r"$\varepsilon_\text{Par}(H\to WW^*)$"
    elif var == "eHZZint":        tex_label = r"$\varepsilon_\text{Int}(H\to ZZ^*)$"
    elif var == "eHZZpar":        tex_label = r"$\varepsilon_\text{Par}(H\to ZZ^*)$"
    elif var == "eHZgaint":       tex_label = r"$\varepsilon_\text{Int}(H\to Z\gamma)$"
    elif var == "eHZgapar":       tex_label = r"$\varepsilon_\text{Par}(H\to Z\gamma)$"
    elif var == "eHgagaint":      tex_label = r"$\varepsilon_\text{Int}(H\to \gamma\gamma)$"
    elif var == "eHgagapar":      tex_label = r"$\varepsilon_\text{Par}(H\to \gamma\gamma)$"
    elif var == "eHmumuint":      tex_label = r"$\varepsilon_\text{Int}(H\to \mu\mu)$"
    elif var == "eHmumupar":      tex_label = r"$\varepsilon_\text{Par}(H\to \mu\mu)$"
    elif var == "eHtautauint":    tex_label = r"$\varepsilon_\text{Int}(H\to \tau\tau)$"
    elif var == "eHtautaupar":    tex_label = r"$\varepsilon_\text{Par}(H\to \tau\tau)$"
    elif var == "eHccint":        tex_label = r"$\varepsilon_\text{Int}(H\to cc)$"
    elif var == "eHccpar":        tex_label = r"$\varepsilon_\text{Par}(H\to cc)$"
    elif var == "eHbbint":        tex_label = r"$\varepsilon_\text{Int}(H\to bb)$"
    elif var == "eHbbpar":        tex_label = r"$\varepsilon_\text{Par}(H\to bb)$"
    else: raise KeyError(f"Latex label for parameter {var} not found!")
    return tex_label

plt.rcParams.update({
#   "text.usetex": True,
  'text.latex.preamble': r'\usepackage{txfonts}',
})

# Short script to compare the results

model_spec = "fits"

# Open the input file in read mode and output file in write mode
working_dir = "./"
scenarios = ["SM_FCCee240",
             "SM_FCCee240_FCCee365",
             "SM_FCCee240_FCCee365_HLLHClambda",
             "IDM_FCCee240",
             "IDM_FCCee240_FCCee365",
             "IDM_FCCee240_FCCee365_HLLHClambda"
             ]

plot_titles = [r"SM Central values, FCC-ee$_{240}$",
               r"SM Central values, FCC-ee$_{240}$ + FCC-ee$_{365}$",
               r"SM Central values, FCC-ee$_{240}$ + FCC-ee$_{365}$ + $\kappa_\lambda$ constraint",
               r"IDM Central values, FCC-ee$_{240}$",
               r"IDM Central values, FCC-ee$_{240}$ + FCC-ee$_{365}$",
               r"IDM Central values, FCC-ee$_{240}$ + FCC-ee$_{365}$ + $\kappa_\lambda$ constraint",
          ]

# plot_labels = [r"SM, FCC-ee$_{240}$",
#                r"SM, FCC-ee$_{240}$ + FCC-ee$_{365}$",
#                r"SM, FCC-ee$_{240}$ + FCC-ee$_{365}$ + $\kappa_\lambda$",
#                r"IDM, FCC-ee$_{240}$",
#                r"IDM, FCC-ee$_{240}$ + FCC-ee$_{365}$",
#                r"IDM, FCC-ee$_{240}$ + FCC-ee$_{365}$ + $\kappa_\lambda$",
#           ]

plot_labels = [r"SM, FCC-ee$_{240}$",
               r"SM, FCC-ee$_{240+365}$",
               r"SM, FCC-ee$_{240+365}$ + $\kappa_\lambda$",
               r"IDM, FCC-ee$_{240}$",
               r"IDM, FCC-ee$_{240+365}$",
               r"IDM, FCC-ee$_{240+365}$ + $\kappa_\lambda$",
          ]

n_scenarios = len(scenarios)

files = [working_dir + file_dir + f"/results_{model_spec}/MonteCarlo_results.txt" for file_dir in scenarios]

# Create the output directory
subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{model_spec}"])


results = {}
parameters = []


for file_path, scenario in zip(files, scenarios):
    found_results = False
    results[scenario] = []
    with open(file_path, 'r') as file:
        for line in file:
            if not found_results:
                if line.startswith(" Global mode:"):
                    found_results = True
                continue

            # Reached end of the relevant data
            if line in ['\n', '\r\n']:
                break

            # Split the line into columns by whitespace
            columns = line.split()

            if scenario == scenarios[0]:
                parameters.append(columns[2].strip("\""))
                
            results[scenario].append([float(columns[4]), float(columns[6])])

    results[scenario] = np.array(results[scenario])

parameters_tex = [find_tex_label(par) for par in parameters]

print(parameters)
print(results)


w = 1.0
dimw = w / 2
y_shift = np.linspace(0, -dimw, n_scenarios) 

parameter_order = [math.ceil(np.log10(par)) for par in results[scenarios[0]][:, 1]]
parameter_order = np.array(parameter_order)

results_plot = results
for scenario in scenarios:
    # results_plot[scenario][:,0] = results_plot[scenario][:,0] - results_plot[scenarios[0]][:,0]
    results_plot[scenario] = [par/10.**parameter_order[i] for i, par in enumerate(results[scenario])]
    results_plot[scenario] = np.array(results_plot[scenario])
print(results_plot)

labels = parameters_tex
for i, par in enumerate(parameters_tex):
    if round(parameter_order[i]) < 0 :
        labels[i] = f"{10**(-parameter_order[i])}"+r"$\cdot$"+par
    elif round(parameter_order[i]) > 0 :
        labels[i] = f"{10.**(-parameter_order[i])}"+r"$\cdot$"+par
    # if round(parameter_order[i]) == 0:
    #     labels[i] = par


nvar_per_plot = 5
param_breaks = np.arange(0, len(parameters), nvar_per_plot)
if param_breaks[-1] != len(parameters):
    param_breaks = np.append(param_breaks, [len(parameters)])

print(param_breaks)
for k in range(len(param_breaks) - 1):
    fig= plt.figure(k,dpi=150)
    ax = plt.gca()
    #fig, ax = plt.subplots(1,1,figsize=(7,5))
    y = np.arange(param_breaks[k],param_breaks[k+1])
    
    for i, scenario in enumerate(scenarios):
        results = np.copy(results_plot[scenario])
        results[:, 0] = results[:, 0] - results_plot[scenarios[0]][:, 0]
        ax.errorbar(results[param_breaks[k]:param_breaks[k+1], 0],
                    -y+y_shift[i], xerr=(results[param_breaks[k]:param_breaks[k+1], 1],), 
                    fmt='o', linewidth=1.5, capsize=3.5, markersize=4, label = plot_labels[i])


    plt.axvline(c='0.6', linewidth=2)
    ax.set_xlim([-1.1, 1.1])
    #ax.set_yticks(-x - dimw / 2)
    ax.set_yticks(-y-dimw/2.)
    ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]],fontsize=16)
    ax.tick_params(axis='x', size=10, labelsize=12)
    ax.tick_params(axis='x', which='minor', size=6)
    ax.set_xlabel(r'Global mode with uncertainty', fontsize=15)
    ax.legend(loc='best', fontsize=8)
    plt.tight_layout()   # Makes sure labels are not cut off
    plt.savefig(working_dir + f'comparison_plots/results_{model_spec}/pull_plots_{k}.pdf')

# plt.show()

# Copy and rename plots for specific parameters/observables

print("flag")

copy_obs = ["CH_corr_mod", 
            "CHbox_corr_mod", 
            "CHD_corr_mod", 
            "deltalHHH_HLLHC_mod",]
for scenario in scenarios:
    for obs in copy_obs:
        subprocess.run(["cp", f"{working_dir}{scenario}/results_{model_spec}/Observables/{obs}.pdf",
                    f"{working_dir}comparison_plots/results_{model_spec}/{obs}_{scenario}.pdf"])