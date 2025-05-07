import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
import subprocess


def find_tex_label_var(var):
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


def find_tex_label_obs(obs):
    ### FCC-ee_240
    if obs == "eeZH_FCCee240":         tex_label = r"$\sigma_{ZH}$(FCC-ee$_{240}$)"
    elif obs == "eeZHbb_FCCee240":     tex_label = r"$\mu_{ZH,bb}$(FCC-ee$_{240}$)"
    elif obs == "eeHvvbb_FCCee240":    tex_label = r"$\mu_{\nu\nu H,bb}$(FCC-ee$_{240}$)"
    elif obs == "eeZHcc_FCCee240":     tex_label = r"$\mu_{ZH,cc}$(FCC-ee$_{240}$)"
    elif obs == "eeZHgg_FCCee240":     tex_label = r"$\mu_{ZH,gg}$(FCC-ee$_{240}$)"
    elif obs == "eeZHWW_FCCee240":     tex_label = r"$\mu_{ZH,WW}$(FCC-ee$_{240}$)"
    elif obs == "eeZHZZ_FCCee240":     tex_label = r"$\mu_{ZH,ZZ}$(FCC-ee$_{240}$)"
    elif obs == "eeZHtautau_FCCee240": tex_label = r"$\mu_{ZH,\tau\tau}$(FCC-ee$_{240}$)"
    elif obs == "eeZHgaga_FCCee240":   tex_label = r"$\mu_{ZH,\gamma\gamma}$(FCC-ee$_{240}$)"
    elif obs == "eeZHmumu_FCCee240":   tex_label = r"$\mu_{ZH,\mu\mu}$(FCC-ee$_{240}$)"
    elif obs == "eeZHZga_FCCee240":    tex_label = r"$\mu_{ZH,Z\gamma}$(FCC-ee$_{240}$)"

    ### FCC-ee_365
    elif obs == "eeZH_FCCee365":        tex_label = r"$\sigma_{ZH}$(FCC-ee$_{365}$)"
    elif obs == "eeZHbb_FCCee365":      tex_label = r"$\mu_{ZH,bb}$(FCC-ee$_{365}$)"
    elif obs == "eeHvvbb_FCCee365":     tex_label = r"$\mu_{\nu\nu H,bb}$(FCC-ee$_{365}$)"
    elif obs == "eeZHcc_FCCee365":      tex_label = r"$\mu_{ZH,cc}$(FCC-ee$_{365}$)"
    elif obs == "eeHvvcc_FCCee365":     tex_label = r"$\mu_{\nu\nu H,cc}$(FCC-ee$_{365}$)"
    elif obs == "eeZHgg_FCCee365":      tex_label = r"$\mu_{ZH,gg}$(FCC-ee$_{365}$)"
    elif obs == "eeHvvgg_FCCee365":     tex_label = r"$\mu_{\nu\nu H,gg}$(FCC-ee$_{365}$)"
    elif obs == "eeZHWW_FCCee365":      tex_label = r"$\mu_{ZH,WW}$(FCC-ee$_{365}$)"
    elif obs == "eeHvvWW_FCCee365":     tex_label = r"$\mu_{\nu\nu H,WW}$(FCC-ee$_{365}$)"
    elif obs == "eeZHZZ_FCCee365":      tex_label = r"$\mu_{ZH,ZZ}$(FCC-ee$_{365}$)"
    elif obs == "eeHvvZZ_FCCee365":     tex_label = r"$\mu_{\nu\nu H,ZZ}$(FCC-ee$_{365}$)"
    elif obs == "eeZHtautau_FCCee365":  tex_label = r"$\mu_{ZH,\tau\tau}$(FCC-ee$_{365}$)"
    elif obs == "eeHvvtautau_FCCee365": tex_label = r"$\mu_{\nu\nu H,\tau\tau}$(FCC-ee$_{365}$)"
    elif obs == "eeZHgaga_FCCee365":    tex_label = r"$\mu_{ZH,\gamma\gamma}$(FCC-ee$_{365}$)"
    elif obs == "eeHvvgaga_FCCee365":   tex_label = r"$\mu_{\nu\nu H,\gamma\gamma}$(FCC-ee$_{365}$)"
    elif obs == "eeZHmumu_FCCee365":    tex_label = r"$\mu_{ZH,\mu\mu}$(FCC-ee$_{365}$)"
    # elif obs == "eeHvvmumu_FCCee365":   tex_label = r"$\mu_{\nu\nu H,\mu\mu}$(FCC-ee$_{365}$)"



    ### HL-LHC
    elif obs == "muggHgagaHL":     tex_label = r"$\mu_{ggH}^{\gamma\gamma}$(HL-LHC)"
    elif obs == "muggHZZ4lHL":     tex_label = r"$\mu_{ggH}^{ZZ,4\ell}$(HL-LHC)"
    elif obs == "muggHWW2l2vHL":   tex_label = r"$\mu_{ggH}^{WW,2\ell 2\nu}$(HL-LHC)"
    elif obs == "muggHtautauHL":   tex_label = r"$\mu_{ggH}^{\tau\tau}$(HL-LHC)"
    elif obs == "muggHbbHL":       tex_label = r"$\mu_{ggH}^{bb}$(HL-LHC)"
    elif obs == "muggHmumuHL":     tex_label = r"$\mu_{ggH}^{\mu\mu}$(HL-LHC)"
    elif obs == "muggHZgaHL":      tex_label = r"$\mu_{ggH}^{Z\gamma}$(HL-LHC)"

    elif obs == "muVBFgagaHL":     tex_label = r"$\mu_{VBF}^{\gamma\gamma}$(HL-LHC)"
    elif obs == "muVBFZZ4lHL":     tex_label = r"$\mu_{VBF}^{ZZ,4\ell}$(HL-LHC)"
    elif obs == "muVBFWW2l2vHL":   tex_label = r"$\mu_{VBF}^{WW,2\ell 2\nu}$(HL-LHC)"
    elif obs == "muVBFtautauHL":   tex_label = r"$\mu_{VBF}^{\tau\tau}$(HL-LHC)"
    elif obs == "muVBFmumuHL":     tex_label = r"$\mu_{VBF}^{\mu\mu}$(HL-LHC)"
    elif obs == "muVBFZgaHL":      tex_label = r"$\mu_{VBF}^{Z\gamma}$(HL-LHC)"

    elif obs == "muWHgagaHL":     tex_label = r"$\mu_{WH}^{\gamma\gamma}$(HL-LHC)"
    elif obs == "muWHZZ4lHL":     tex_label = r"$\mu_{WH}^{ZZ,4\ell}$(HL-LHC)"
    elif obs == "muWHWW2l2vHL":   tex_label = r"$\mu_{WH}^{WW,2\ell 2\nu}$(HL-LHC)"
    elif obs == "muWHbbHL":       tex_label = r"$\mu_{WH}^{bb}$(HL-LHC)"

    elif obs == "muZHgagaHL":     tex_label = r"$\mu_{ZH}^{\gamma\gamma}$(HL-LHC)"
    elif obs == "muZHZZ4lHL":     tex_label = r"$\mu_{ZH}^{ZZ,4\ell}$(HL-LHC)"
    elif obs == "muZHWW2l2vHL":   tex_label = r"$\mu_{ZH}^{WW,2\ell 2\nu}$(HL-LHC)"
    elif obs == "muZHbbHL":       tex_label = r"$\mu_{ZH}^{bb}$(HL-LHC)"

    elif obs == "muttHgagaHL":     tex_label = r"$\mu_{ttH}^{\gamma\gamma}$(HL-LHC)"
    elif obs == "muttHZZ4lHL":     tex_label = r"$\mu_{ttH}^{ZZ,4\ell}$(HL-LHC)"
    elif obs == "muttHWW2l2vHL":   tex_label = r"$\mu_{ttH}^{WW,2\ell 2\nu}$(HL-LHC)"
    elif obs == "muttHtautauHL":   tex_label = r"$\mu_{ttH}^{\tau\tau}$(HL-LHC)"
    elif obs == "muttHbbHL":       tex_label = r"$\mu_{ttH}^{bb}$(HL-LHC)"

    #else: raise KeyError(f"Latex label for parameter {obs} not found!")
    else: tex_label = "test"
    return tex_label

plt.rcParams.update({
#   "text.usetex": True,
  'text.latex.preamble': r'\usepackage{txfonts}',
})


# model_spec_UVmodel = "all_uncertainties_SQUARED"
model_spec = "fits"

# Open the input file in read mode and output file in write mode
# working_dir_UVmodel = "../different_scenario_fits/"
working_dir = "./"

lambdas = list(range(-5, 11))
# lambdas = [2, 3, 5, 6, 7, 8, 9, 10]

# scenarios = [# "Z2SSM_FCCee240_FCCee365",
#              "Lambda2_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda3_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda5_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda6_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda7_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda8_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda9_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda10_FCCee240_FCCee365_noHLLHClambda",
#             ]

scenarios = [f"Lambda{lamb}_FCCee240_FCCee365_noHLLHClambda" for lamb in lambdas]

# plot_titles = [# r"Z2SSM Central values, no HL-LHC $\lambda_{hhh}$ constraint",
#                r"$\kappa_\lambda=2$ cross-check, no HL-LHC $\kappa_\lambda$ constraint",
#                r"$\kappa_\lambda=3$ cross-check, no HL-LHC $\kappa_\lambda$ constraint",
#                r"$\kappa_\lambda=5$ cross-check, no HL-LHC $\kappa_\lambda$ constraint",
#                r"$\kappa_\lambda=6$ cross-check, no HL-LHC $\kappa_\lambda$ constraint",
#                r"$\kappa_\lambda=7$ cross-check, no HL-LHC $\kappa_\lambda$ constraint",
#                r"$\kappa_\lambda=8$ cross-check, no HL-LHC $\kappa_\lambda$ constraint",
#                r"$\kappa_\lambda=9$ cross-check, no HL-LHC $\kappa_\lambda$ constraint",
#                r"$\kappa_\lambda=10$ cross-check, no HL-LHC $\kappa_\lambda$ constraint",
#               ]

plot_titles = [fr"$\kappa_\lambda={lamb}$ cross-check, no HL-LHC $\kappa_\lambda$ constraint" for lamb in lambdas]

# plot_labels = [# r"$\mathbb{Z}_{2}$SSM, no $\kappa_\lambda$",
#                r"$\kappa_\lambda=2$ cross-check",
#                r"$\kappa_\lambda=3$ cross-check",
#                r"$\kappa_\lambda=5$ cross-check",
#                r"$\kappa_\lambda=6$ cross-check",
#                r"$\kappa_\lambda=7$ cross-check",
#                r"$\kappa_\lambda=8$ cross-check",
#                r"$\kappa_\lambda=9$ cross-check",
#                r"$\kappa_\lambda=10$ cross-check",
#               ]

plot_labels = [rf"$\kappa_\lambda={lamb}$ cross-check" for lamb in lambdas]
n_scenarios = len(scenarios)

files = [working_dir + file_dir + f"/results_{model_spec}/Observables/Statistics.txt" for file_dir in scenarios]
# files = [working_dir_UVmodel + scenarios[0] + f"/results_{model_spec_UVmodel}/Observables/Statistics.txt",
#          working_dir + scenarios[1] + f"/results_{model_spec}/Observables/Statistics.txt",
#          working_dir + scenarios[2] + f"/results_{model_spec}/Observables/Statistics.txt",
#          working_dir + scenarios[3] + f"/results_{model_spec}/Observables/Statistics.txt",
#          working_dir + scenarios[4] + f"/results_{model_spec}/Observables/Statistics.txt",
# ]

# Create the output directory
subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{model_spec}"])


results = {}
kappa_lambda_results = {}


for file_path, scenario in zip(files, scenarios):

    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        line_nrs = []
        observables = []
        for n, line in enumerate(lines):
            columns = line.split()
            if len(columns) < 2:
                continue
            
            if columns[1] == "Observable" and \
                (columns[2].startswith("\"ee") or columns[2].startswith("\"mu")):
                observables.append(columns[2][1:-2])
                line_nrs.append(n)

            if columns[1] == "Observable" and columns[2].startswith("\"deltalHHH_HLLHC"):
                line_kappa_lambda = n
                

        nobs = len(observables)

        results[scenario] = []
        for line_nr, obs in zip(line_nrs, observables):
        
            columns = lines[line_nr + 1].split()
            results[scenario].append([float(columns[3]),    # Mean
                                      float(columns[5]),])  # Uncertainty

        columns_kappa_lambda = lines[line_kappa_lambda + 1].split()
        kappa_lambda_results[scenario] = [float(columns_kappa_lambda[3]),    # Mean
                                          float(columns_kappa_lambda[5]),]   # Uncertainty

    results[scenario] = np.array(results[scenario])





obs_240_365 = [False for i, obs in enumerate(observables)]  # boolean list, determining whether an 240 GeV observable has an equivalent 365 GeV one
observables_reordered = []
for i, obs in enumerate(observables):
    if obs.endswith("240") and (obs[:-3] + "365" in observables):
        obs_240_365[i] = True
        observables_reordered.append(obs)
        observables_reordered.append(obs[:-3] + "365")

    elif obs.endswith("365") and (obs[:-3] + "240" in observables):
        obs_240_365[i] = True

for i, obs in enumerate(observables):
    if obs_240_365[i] == False:
        observables_reordered.append(obs)

if not len(observables_reordered) == len(observables):
    raise ValueError("The reordered list of observables has a different length as the original list!")

print(observables_reordered)

results_reordered = {}
for scenario in scenarios:
    results_reordered[scenario] = []

    for obs in observables_reordered:
        index = observables.index(obs)
        results_reordered[scenario].append(results[scenario][index])


observables_tex = [find_tex_label_obs(obs) for obs in observables]

#print(results)


### Means and standard deviations

w = 1.0
dimw = w / 2
y_shift = np.linspace(0, -dimw, n_scenarios) 


# results_plot = results
results_plot = results_reordered

labels = observables_tex[:]
for i, obs in enumerate(observables_tex):
        labels[i] = obs


def plot_obs(scenarios,
             means,
             errors, 
             y,
             scenario_labels,
             obs_labels,
             file_name,
             ):
    fig= plt.figure(k,dpi=150)
    ax = plt.gca()
    y = np.arange(param_breaks[k],param_breaks[k+1])
    
    for i, scenario in enumerate(scenarios):
        ax.errorbar(means[scenario], -y+y_shift[i], xerr=(errors[scenario],), 
                    fmt='o', linewidth=1.5, capsize=3.5, markersize=4, label = scenario_labels[i])

    plt.axvline(x=1, c='0.6', linewidth=2)
    ax.set_yticks(-y-dimw/2.)
    ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]],fontsize=16)
    ax.tick_params(axis='x', size=10, labelsize=12)
    ax.tick_params(axis='x', which='minor', size=6)
    ax.set_xlabel(r'Means and standard deviations', fontsize=15)
    ax.legend(loc='best', fontsize=7)
    plt.tight_layout()   # Makes sure labels are not cut off
    plt.savefig(file_name)



nvar_per_plot = 2
param_breaks = np.arange(0, len(observables), nvar_per_plot)
if param_breaks[-1] != len(observables):
    param_breaks = np.append(param_breaks, [len(observables)])

#print(param_breaks)
for k in range(len(param_breaks) - 1):
    y = np.arange(param_breaks[k],param_breaks[k+1])
    
    # for i, scenario in enumerate(scenarios):
    #     results = np.copy(results_plot[scenario])
    #     ax.errorbar(results[param_breaks[k]:param_breaks[k+1], 0],
    #                 -y+y_shift[i], xerr=(results[param_breaks[k]:param_breaks[k+1], 1],), 
    #                 fmt='o', linewidth=1.5, capsize=3.5, markersize=4, label = plot_labels[i])

    means = {scenario : np.copy(results_plot[scenario])[param_breaks[k]:param_breaks[k+1], 0] for scenario in scenarios}
    errors = {scenario : np.copy(results_plot[scenario])[param_breaks[k]:param_breaks[k+1], 1] for scenario in scenarios}

    plot_obs(scenarios=scenarios,
             means=means,
             errors=errors,
             y=y,
             scenario_labels=plot_labels,
             obs_labels=labels[param_breaks[k]:param_breaks[k+1]],
             file_name=working_dir + f'comparison_plots/results_{model_spec}/mean_stddev_{k}.pdf',)

# plt.show()


# Copy and rename plots for specific parameters/observables

# copy_obs = ["CH_corr_mod", 
#             "CHbox_corr_mod", 
#             "CHD_corr_mod", 
#             "deltalHHH_HLLHC_mod",]

copy_obs = ["CH_corr", 
            "CHbox_corr", 
            "CHD_corr", 
            "deltalHHH_HLLHC",]

# scenarios = ["Lambda2_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda3_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda5_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda10_FCCee240_FCCee365_noHLLHClambda",
#              "Lambda2_FCCee240_FCCee365_HLLHClambda",
#              "Lambda3_FCCee240_FCCee365_HLLHClambda",
#              "Lambda5_FCCee240_FCCee365_HLLHClambda",
#              "Lambda10_FCCee240_FCCee365_HLLHClambda",
#             ]


# to generate useful plots later:
with open(f"comparison_plots/results_{model_spec}/kappa_lambda_means_std_dev.txt", "w") as kappa_lambda_output:

    for scenario in scenarios:
        for obs in copy_obs:
            subprocess.run(["cp", f"{working_dir}{scenario}/results_{model_spec}/Observables/{obs}.pdf",
                        f"{working_dir}comparison_plots/results_{model_spec}/{obs}_{scenario}.pdf"])

        text_kala = f"{scenario} " + \
                    "deltalHHH_HLLHC " + \
                    f"{kappa_lambda_results[scenario][0]} " + \
                    f"{kappa_lambda_results[scenario][1]} "
        print(text_kala, file=kappa_lambda_output)

        # for obs in ['eeZH_FCCee240', 'eeZH_FCCee365',]:

        #     index = observables_reordered.index(obs)

        #     text = f"{scenario} " + \
        #            f"{obs} " + \
        #            f"{results_reordered[scenario][index][0]} " + \
        #            f"{results_reordered[scenario][index][1]} "
        #     print(text, file=kappa_lambda_output)


