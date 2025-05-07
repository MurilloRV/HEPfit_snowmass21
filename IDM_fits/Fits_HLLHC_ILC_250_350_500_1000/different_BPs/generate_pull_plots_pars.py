import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
import subprocess


def find_tex_label_par(par):
    if par =="AlsMz":             tex_label = r"$\alpha_s(M_Z)$"
    elif par == "dAle5Mz":        tex_label = r"$\Delta\alpha_{\mathrm{had}}^{(5)}(M_Z^2)$"
    elif par == "mtop":           tex_label = r"$M_t$"
    elif par == "mHl":            tex_label = r"$M_h$"
    elif par == "Mz":             tex_label = r"$M_Z$"
    elif par == "CW":             tex_label = r"$C_W$"
    elif par == "CHG":            tex_label = r"$C_{HG}$"
    elif par == "CHWB":           tex_label = r"$C_{HWB}$"
    elif par == "CHWHB_gaga":     tex_label = r"$(C_{HWHB})_{\gamma\gamma}$"
    elif par == "CHWHB_gagaorth": tex_label = r"$(C_{HWHB})_{\gamma\gamma\text{orth}}$"
    elif par == "CHW":            tex_label = r"$C_{HW}$"  # Rotated!!
    elif par == "CHB":            tex_label = r"$C_{HB}$"  # Rotated!!
    elif par == "CHD":            tex_label = r"$C_{HD}$"
    elif par == "CHbox":          tex_label = r"$C_{H\boxdot}$"
    elif par == "CH":             tex_label = r"$C_{H}$"
    elif par == "CHL1_11":        tex_label = r"$(C_{HL}^{(1)})_{11}$"
    elif par == "CHL1_22":        tex_label = r"$(C_{HL}^{(1)})_{22}$"
    elif par == "CHL1_33":        tex_label = r"$(C_{HL}^{(1)})_{33}$"
    elif par == "CHL3_11":        tex_label = r"$(C_{HL}^{(3)})_{11}$"
    elif par == "CHL3_22":        tex_label = r"$(C_{HL}^{(3)})_{22}$"
    elif par == "CHL3_33":        tex_label = r"$(C_{HL}^{(3)})_{33}$"
    elif par == "CHe_11":         tex_label = r"$(C_{He})_{11}$"
    elif par == "CHe_22":         tex_label = r"$(C_{He})_{22}$"
    elif par == "CHe_33":         tex_label = r"$(C_{He})_{33}$"
    elif par == "CHQ1_11":        tex_label = r"$(C_{HQ}^{(1)})_{11}$"
    elif par == "CHQ1_33":        tex_label = r"$(C_{HQ}^{(1)})_{33}$"
    elif par == "CHQ3_11":        tex_label = r"$(C_{HQ}^{(3)})_{11}$"
    elif par == "CHu_11":         tex_label = r"$(C_{Hu})_{11}$"
    elif par == "CHd_11":         tex_label = r"$(C_{Hd})_{11}$"
    elif par == "CHd_33":         tex_label = r"$(C_{Hd})_{33}$"
    elif par == "CeH_22r":        tex_label = r"${Re}\left[(C_{eH})_{22}\right]$"
    elif par == "CeH_33r":        tex_label = r"${Re}\left[(C_{eH})_{33}\right]$"
    elif par == "CuH_22r":        tex_label = r"${Re}\left[(C_{uH})_{22}\right]$"
    elif par == "CuH_33r":        tex_label = r"${Re}\left[(C_{uH})_{33}\right]$"
    elif par == "CdH_33r":        tex_label = r"${Re}\left[(C_{dH})_{33}\right]$"
    elif par == "CLL_1221":       tex_label = r"$(C_{LL})_{1221}$"
    elif par == "eHggint":        tex_label = r"$\varepsilon_\text{Int}(H\to gg)$"
    elif par == "eHggpar":        tex_label = r"$\varepsilon_\text{Par}(H\to gg)$"
    elif par == "eHWWint":        tex_label = r"$\varepsilon_\text{Int}(H\to WW^*)$"
    elif par == "eHWWpar":        tex_label = r"$\varepsilon_\text{Par}(H\to WW^*)$"
    elif par == "eHZZint":        tex_label = r"$\varepsilon_\text{Int}(H\to ZZ^*)$"
    elif par == "eHZZpar":        tex_label = r"$\varepsilon_\text{Par}(H\to ZZ^*)$"
    elif par == "eHZgaint":       tex_label = r"$\varepsilon_\text{Int}(H\to Z\gamma)$"
    elif par == "eHZgapar":       tex_label = r"$\varepsilon_\text{Par}(H\to Z\gamma)$"
    elif par == "eHgagaint":      tex_label = r"$\varepsilon_\text{Int}(H\to \gamma\gamma)$"
    elif par == "eHgagapar":      tex_label = r"$\varepsilon_\text{Par}(H\to \gamma\gamma)$"
    elif par == "eHmumuint":      tex_label = r"$\varepsilon_\text{Int}(H\to \mu\mu)$"
    elif par == "eHmumupar":      tex_label = r"$\varepsilon_\text{Par}(H\to \mu\mu)$"
    elif par == "eHtautauint":    tex_label = r"$\varepsilon_\text{Int}(H\to \tau\tau)$"
    elif par == "eHtautaupar":    tex_label = r"$\varepsilon_\text{Par}(H\to \tau\tau)$"
    elif par == "eHccint":        tex_label = r"$\varepsilon_\text{Int}(H\to cc)$"
    elif par == "eHccpar":        tex_label = r"$\varepsilon_\text{Par}(H\to cc)$"
    elif par == "eHbbint":        tex_label = r"$\varepsilon_\text{Int}(H\to bb)$"
    elif par == "eHbbpar":        tex_label = r"$\varepsilon_\text{Par}(H\to bb)$"
    else: raise KeyError(f"Latex label for parameter {par} not found!")
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


# model_spec = "fits"
# model_spec = "fits_realistic_HL_LHC_all_EW_mods_long"

# model_spec = {}

# Open the input file in read mode and output file in write mode
working_dir = "./"


# BPs = [f"BP_{i}" for i in range(8)]

num_BPOs = 2
num_BPBs = 17
BPs = [f"BPO_{i}" for i in range(num_BPOs)]
BPs = BPs + [f"BPB_{i}" for i in range(num_BPBs)]
BPs = ["BPB_2", "BPB_4", "BPB_6"]
# BP_Names = ["BPB 2", "BPB 4", "BPB 6"]
BP_Names = ["BP 1", "BP 2", "BP 3"]
print(BPs)


# plot_labels = [f"BP {i}" for i in range(8)]

plot_labels = [f"BPO {i}" for i in range(num_BPOs)]
plot_labels = plot_labels + [f"BPB {i}" for i in range(num_BPBs)]

n_BPs = len(BPs)

# plot_title = [rf"IDM Central values ({BP}), FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$" for BP in BPs]
# plot_title = [rf"IDM ({BP}), FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$" for BP in BP_Names]

# scenarios = ["IDM_FCCee240_FCCee365" for i in range(num_BPOs + num_BPBs)]

scenarios = [
    "IDM_FCCee240",
    "IDM_FCCee240_FCCee365",
    "IDM_FCCee240_FCCee365_HLLHClambda",
]

model_spec = {
    "IDM_FCCee240" : "fits",
    "IDM_FCCee240_FCCee365" : "fits",
    "IDM_FCCee240_FCCee365_HLLHClambda" : "fits_realistic_HL_LHC_realistic_HL_LHC_long",
}

# model_spec = {
#     "IDM_FCCee240" : "fits_realistic_HL_LHC_all_EW_mods_long",
#     "IDM_FCCee240_FCCee365" : "fits_realistic_HL_LHC_all_EW_mods_long",
#     "IDM_FCCee240_FCCee365_HLLHClambda" : "fits_realistic_HL_LHC_all_EW_mods_long",
# }

results_dir = "final"
# results_dir = model_spec["IDM_FCCee240"]

scenario_titles = [
    rf"FCC-ee$_{{240}}$",
    rf"FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$",
    rf"FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$ + $\kappa_{{\lambda}}$ at HL-LHC",
]

plot_title = {}

for i, BP in enumerate(BPs):
    plot_title[BP] = {}

    for scenario, scenario_title in zip(scenarios, scenario_titles):
        plot_title[BP][scenario] = rf"IDM ({BP_Names[i]}), {scenario_title}"


# colors = ["tab:blue",
#           "tab:blue",
#           "tab:orange",
#           "tab:orange",
#           "tab:green",
#           "tab:green",
#           "tab:red",
#           "tab:red",
#           ]

# alphas = [1, 0.5, 1, 0.5, 1, 0.5, 1, 0.5,]


# files = [f"{working_dir}{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt" for scenario, BP in zip(scenarios, BPs)]
files = {}
for BP in BPs:
    files[BP] = {}
    for scenario in scenarios:
        files[BP][scenario] = f"{working_dir}{BP}/{scenario}/results_{model_spec[scenario]}/Observables/Statistics.txt"

# files = [f"{working_dir}BP_0/{scenario}/results_{model_spec}/Observables/Statistics.txt" for scenario, BP in zip(scenarios, BPs)]

# BP_2 = BP_3
# BP_4 = BP_5
# files[3] = files[2]
# files[5] = files[4]


subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{results_dir}"])



results = {}
parameters = {}
parameters_tex = {}

for BP in BPs:

    results[BP] = {}
    parameters[BP] = {}
    parameters_tex[BP] = {}
    for scenario in scenarios:

        file_path = files[BP][scenario]
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            line_nrs = []
            parameters[BP][scenario] = []
            parameters_tex[BP][scenario] = []
            for n, line in enumerate(lines):
                columns = line.split()
                if len(columns) < 2:
                    continue
                
                if columns[1] == "Observable" and \
                columns[2].startswith("\"C") and \
                columns[2].endswith("corr\":"):
                    parameter = columns[2][1:-7]
                    parameters[BP][scenario].append(parameter)
                    parameter_tex_label = find_tex_label_par(parameter)
                    parameters_tex[BP][scenario].append(parameter_tex_label)
                    line_nrs.append(n)

            nobs = len(parameters[BP][scenario])

            results[BP][scenario] = []
            print(BP)
            for line_nr, par in zip(line_nrs, parameters[BP][scenario]):
            
                columns = lines[line_nr + 1].split()
                means_uncertainties = [float(columns[3]),    # Mean
                                       float(columns[5]),]  # Uncertainty
                means_uncertainties[0] = means_uncertainties[0]/means_uncertainties[1]
                means_uncertainties[1] = means_uncertainties[1]/means_uncertainties[1]

                results[BP][scenario].append(means_uncertainties)

        results[BP][scenario] = np.array(results[BP][scenario])

print(parameters)

# parameters_tex = [find_tex_label_par(par) for par in parameters]
print(parameters_tex)

w = 1.0
dimw = w / 2
y_shift = np.linspace(0, -dimw, n_BPs) 


# results_plot = results
results_plot = results

# labels = parameters_tex[:]
# for i, par in enumerate(parameters_tex):
#         labels[i] = par



#print(param_breaks)
num_fig = 0
for i, BP in enumerate(BPs):
    for scenario in scenarios:

        nvar_per_plot = 1_000_000
        param_breaks = np.arange(0, len(parameters[BP][scenario]), nvar_per_plot)
        # param_breaks = np.array([0,5,10,15,20,25,29,33,37,41,46])
        if len(param_breaks)==1 or param_breaks[-1] != len(parameters[BP][scenario]):
            param_breaks = np.append(param_breaks, [len(parameters[BP][scenario])])

        print(len(parameters[BP][scenario]))
        print(param_breaks)

        labels = parameters_tex[BP][scenario][:]
        for j, par in enumerate(parameters_tex[BP][scenario]):
            labels[j] = par

        fig= plt.figure(num_fig, figsize=(4,6), dpi=150)
        num_fig = num_fig + 1
        ax = plt.gca()

        for k in range(len(param_breaks) - 1):
            y = np.arange(param_breaks[k],param_breaks[k+1])
            
            plt.axvline(x=0, c='0.6', linewidth=2)
        
            results = np.copy(results_plot[BP][scenario])
            ax.errorbar(results[param_breaks[k]:param_breaks[k+1], 0],
                        # -y+y_shift[i], 
                        -y, 
                        xerr=(results[param_breaks[k]:param_breaks[k+1], 1],), 
                        fmt='o', 
                        linewidth=1.5, 
                        capsize=3.5, 
                        markersize=4, 
                        label=plot_labels[i],
                        # color=colors[i],
                        # alpha=alphas[i],
                        )

        # ax.set_yticks(-y-dimw/2.)
        ax.set_yticks(-y)
        ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]],fontsize=7.5)
        x_limits = [plt.xlim()[0], plt.xlim()[1]]
        ax.hlines(y=-y, xmin=x_limits[0], xmax=x_limits[1], color="black", linestyle="--", linewidth=0.5)
        ax.set_xlim(*x_limits)
        ax.tick_params(axis='x', size=10, labelsize=11)
        ax.tick_params(axis='x', which='minor', size=6)
        ax.set_xlabel(r'Pulls', fontsize=15)
        # ax.legend(loc='best', fontsize=8)
        ax.set_title(plot_title[BP][scenario], fontsize=9)
        plt.tight_layout()   # Makes sure labels are not cut off
        plt.savefig(working_dir + f'comparison_plots/results_{results_dir}/pull_pars_{BP}_{scenario}_{k}.pdf')

# plt.show()


# # Copy and rename plots for specific parameters/observables

# copy_obs = ["CH_corr", 
#             "CHbox_corr", 
#             "CHD_corr", 
#             "deltalHHH_HLLHC",]

# all_scenarios = ["IDM_FCCee240",
#                  "IDM_FCCee240_FCCee365",
#                  "IDM_FCCee240_FCCee365_HLLHClambda"]

# for scenario in all_scenarios:
#     for BP in BPs:
#         for obs in copy_obs:

#             # if BP == "BP_3": BP_data = "BP_2"
#             # elif BP == "BP_5": BP_data = "BP_4"
#             # else: BP_data = BP
#             # BP_data = "BP_0"

#             BP_data = BP

#             try:
#                 subprocess.run(["cp", f"{working_dir}{BP_data}/{scenario}/results_{model_spec}/Observables/{obs}.pdf",
#                         f"{working_dir}comparison_plots/results_{model_spec}/{obs}_{BP}_{scenario}.pdf"])
#             except:
#                 print(f"file not found: {working_dir}{BP_data}/{scenario}/results_{model_spec}/Observables/{obs}.pdf")