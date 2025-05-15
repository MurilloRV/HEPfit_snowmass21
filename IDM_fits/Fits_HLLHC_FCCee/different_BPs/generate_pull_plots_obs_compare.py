import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
import subprocess

def fix_obs_tex(obs_tex, obs):
    obs_tex_corrected = obs_tex.replace("lamdba", "lambda")
    obs_tex_corrected = obs_tex_corrected.replace("#", "\\")
    obs_tex_corrected = "$" + obs_tex_corrected + "$"
    if obs.endswith("_C"):
        obs_tex_corrected = obs_tex_corrected + " (Current)"
    if obs.endswith("_FCCee"):
        obs_tex_corrected = obs_tex_corrected + " (FCC-ee)"
    if obs.endswith("_FCCee161"):
        obs_tex_corrected = obs_tex_corrected + r" (FCC-ee$_{161}$)"
    if obs.endswith("_FCCee240"):
        obs_tex_corrected = obs_tex_corrected + r" (FCC-ee$_{240}$)"
    if obs.endswith("_FCCee365"):
        obs_tex_corrected = obs_tex_corrected + r" (FCC-ee$_{365}$)"
    if obs.endswith("_HLLHC") or obs.endswith("_HLLHC_OO"):
        obs_tex_corrected = obs_tex_corrected + " (HL-LHC)"
        
    return obs_tex_corrected

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

    else: raise KeyError(f"Latex label for parameter {obs} not found!")
    # else: tex_label = "test"
    return tex_label

plt.rcParams.update({
#   "text.usetex": True,
  'text.latex.preamble': r'\usepackage{txfonts}',
})





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
print(BPs)


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



# spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_small_priors_long"
spec = "fits_realistic_HL_LHC_WFR_kala2_input_small_priors_long"

model_specs = {
    # "IDM_FCCee240" : [spec, "fits"],
    "IDM_FCCee240_FCCee365" : [spec, "fits"],
    # "IDM_FCCee240_FCCee365_HLLHClambda" : [spec, "fits_realistic_HL_LHC_realistic_HL_LHC_long"],
}

# labels = ["HEPfit formula", "Original"]
labels = ["w/ h External-leg", "Original"]
model_specs_labels = {
    # "IDM_FCCee240" : labels,
    "IDM_FCCee240_FCCee365" : labels,
    # "IDM_FCCee240_FCCee365_HLLHClambda" : labels,
}

results_dir = spec


# Do not plot the following observables
skip_obs = ["Mw_C", "GammaZ_C"]

# plot_title = [rf"IDM Central values ({BP}), FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$" for BP in BPs]
# plot_title = [rf"IDM ({BP}), FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$" for BP in BP_Names]

plot_title = {}

for i, BP in enumerate(BPs):
    plot_title[BP] = {}

    for scenario, scenario_title in zip(scenarios, scenario_titles):
        plot_title[BP][scenario] = rf"IDM ({BP_Names[i]}), {scenario_title}"


colors = [
    "tab:orange",
    "tab:blue",
]


files = {}
for BP in BPs:
    files[BP] = {}
    for scenario in scenarios:
        files[BP][scenario] = {}
        for model_spec in model_specs[scenario]:
            files[BP][scenario][model_spec] = f"{working_dir}{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"



# Create the output directory
subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{results_dir}"])

conf_files = {}

for scenario in scenarios:

    conf_files[scenario] = {}
    for model_spec in model_specs[scenario]:


        conf_files[scenario][model_spec] = [
            "ObservablesEW",
            "ObservablesEW_Current_SM_noLFU",
            "ObservablesEW_FCCee_Zpole_SM_kappa_scaled",
            "ObservablesEW_FCCee_WW_SM_kappa_scaled",
            "ObservablesEW_HLLHC_kappa_scaled",
            "ObservablesHiggs",
            "ObservablesHiggs_FCCee_240_SM_kappa_scaled",
            "ObservablesHiggs_HLLHC_SM_kappa_scaled",
            "ObservablesVV",
            "aTGC_observables_Current",
            "aTGC_observables_HLLHC_Full",
            "ObservablesVV_OO_FCCee_161",
            "ObservablesVV_OO_FCCee_240",
            "EffVHcouplings_QFU12",
            "HiggsEW_Par_Corr",
        ]


        if scenario == "IDM_FCCee240_FCCee365" or scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
            conf_files[scenario][model_spec].append("ObservablesHiggs_FCCee_365_kappa_scaled")
            conf_files[scenario][model_spec].append("ObservablesVV_OO_FCCee_365")

        if scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs")] = f"ObservablesHiggs_scaled_realistic_HL_LHC"


        if model_spec == "fits_realistic_HL_LHC_all_EW_mods_long":
            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesEW")] = "ObservablesEW_all_mods"
            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesEW_Current_SM_noLFU")] = "ObservablesEW_Current_SM_noLFU_kappa_scaled"


        # if model_spec[scenario] ==  "fits_realistic_HL_LHC_no_1L_BSM_sqrt_s_long" :
        #     if scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
        #         conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs")] = "ObservablesHiggs_scaled_realistic_HL_LHC"
            
        flag_list = [
            "no_quad",
            "no_1L_BSM",
            "no_1L_BSM_sqrt_s",
            "smeft_formula", 
            "smeft_formula_sqrt", 
            "smeft_formula_no_cross", 
            "smeft_formula_external_leg", 
            "WFR_kala2_input"
        ]
        for flag in flag_list:
            if model_spec == f"fits_realistic_HL_LHC_{flag}_full"  or \
               model_spec == f"fits_realistic_HL_LHC_{flag}_long"  or \
               model_spec == f"fits_realistic_HL_LHC_{flag}_short" or \
               model_spec == f"fits_realistic_HL_LHC_{flag}_small_priors_full"  or \
               model_spec == f"fits_realistic_HL_LHC_{flag}_small_priors_long"  or \
               model_spec == f"fits_realistic_HL_LHC_{flag}_small_priors_short" or \
               model_spec == f"fits_realistic_HL_LHC_{flag}_test_small_priors_full"  or \
               model_spec == f"fits_realistic_HL_LHC_{flag}_test_small_priors_long"  or \
               model_spec == f"fits_realistic_HL_LHC_{flag}_test_small_priors_short":
                print(f"{flag}")
                print(f"{conf_files[scenario][model_spec]}")
                conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_HLLHC_SM_kappa_scaled")] = f"ObservablesHiggs_HLLHC_SM_kappa_scaled_{flag}"
                conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_FCCee_240_SM_kappa_scaled")] = f"ObservablesHiggs_FCCee_240_SM_kappa_scaled_{flag}"
                if scenario == "IDM_FCCee240_FCCee365" or scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
                    conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_FCCee_365_kappa_scaled")] = f"ObservablesHiggs_FCCee_365_kappa_scaled_{flag}"
                if scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
                    conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_scaled_realistic_HL_LHC")] = f"ObservablesHiggs_scaled_realistic_HL_LHC_{flag}"



        for i, file in enumerate(conf_files[scenario][model_spec]):
            conf_files[scenario][model_spec][i] = file + ".conf"


    


observables = {}
observables_tex = {}
central_values_obs = {}

for BP in BPs:
    observables[BP] = {}
    observables_tex[BP] = {}
    central_values_obs[BP] = {}

    for scenario in scenarios:
        observables[BP][scenario] = {}
        observables_tex[BP][scenario] = {} 
        central_values_obs[BP][scenario] = {}

        for model_spec in model_specs[scenario]:
            observables[BP][scenario][model_spec] = []
            observables_tex[BP][scenario][model_spec] = []
            central_values_obs[BP][scenario][model_spec] = []

            for conf_file in conf_files[scenario][model_spec]:

                file_name = f"{working_dir}{BP}/{scenario}/{conf_file}"
                print(f"Reading configuration file {file_name}")

                with open(file_name, "r") as infile:
                    
                    for line in infile:
                        columns = line.split()

                        if (line.startswith("Observable ") \
                            or line.startswith("AsyGausObservable ")) \
                            and columns[6]=="MCMC" and columns[7]=="weight":

                            observable = columns[1]

                            if skip_obs is not None and observable in skip_obs:
                                continue
                            observables[BP][scenario][model_spec].append(observable)

                            try:
                                observable_tex_label = find_tex_label_obs(observable)
                            except KeyError:
                                # print(observable)
                                observable_tex_label = fix_obs_tex(columns[3], observable)
                                # print(observable_tex_label)
                            observables_tex[BP][scenario][model_spec].append(observable_tex_label)
                            central_values_obs[BP][scenario][model_spec].append(float(columns[8]))
                            
            print(len(observables[BP][scenario][model_spec]))

            if not observables[BP][scenario][model_spec] == observables[BP][scenario][model_specs[scenario][0]]:
                raise ValueError(f"Observable list for {BP} in {scenario} is not the same for all model specifications!")
            if not observables_tex[BP][scenario][model_spec] == observables_tex[BP][scenario][model_specs[scenario][0]]:
                raise ValueError(f"Observable latex label list for {BP} in {scenario} is not the same for all model specifications!")

# print(observables)
# print(central_values_obs)









results = {}

for BP in BPs:

    results[BP] = {}
    for scenario in scenarios:

        results[BP][scenario] = {}
        for model_spec in model_specs[scenario]:

            file_path = files[BP][scenario][model_spec]
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

                # print(line_nrs)

                results[BP][scenario][model_spec] = []
                # print(BP)

                for line_nr, obs in zip(line_nrs, observables[BP][scenario][model_spec]):
                
                    # print(line_nr, obs)
                    columns = lines[line_nr + 1].split()
                    results[BP][scenario][model_spec].append([float(columns[3]),    # Mean
                                                              float(columns[5]),])  # Uncertainty

            results[BP][scenario][model_spec] = np.array(results[BP][scenario][model_spec])

            # print(results[BP][scenario])

            print(len(results[BP][scenario][model_spec][:, 0]), len(central_values_obs[BP][scenario][model_spec]))

# print(results)
results_reordered = results
observables_reordered = observables
observables_tex_reordered = observables_tex
central_values_obs_reordered = central_values_obs

# results_reordered = {}
# observables_reordered = {}
# observables_tex_reordered = {}
# central_values_obs_reordered = {}
# for BP in BPs:
#     obs_240_365 = [False for obs in observables[BP]]  # boolean list, determining whether an 240 GeV observable has an equivalent 365 GeV one
#     observables_reordered[BP] = []
#     for i, obs in enumerate(observables[BP]):
#         if obs.endswith("240") and (obs[:-3] + "365" in observables[BP]):
#             obs_240_365[i] = True
#             observables_reordered[BP].append(obs)
#             observables_reordered[BP].append(obs[:-3] + "365")

#         elif obs.endswith("365") and (obs[:-3] + "240" in observables[BP]):
#             obs_240_365[i] = True

#     for i, obs in enumerate(observables[BP]):
#         if obs_240_365[i] == False:
#             observables_reordered[BP].append(obs)

#     if not len(observables_reordered[BP]) == len(observables[BP]):
#         raise ValueError("The reordered list of observables has a different length as the original list!")

#     print(observables_reordered[BP])

#     results_reordered[BP] = []
#     central_values_obs_reordered[BP] = []
#     observables_tex_reordered[BP] = []

#     for obs in observables_reordered[BP]:
#         index = observables[BP].index(obs)
#         results_reordered[BP].append(results[BP][index])
#         central_values_obs_reordered[BP].append(central_values_obs[BP][index])
#         observables_tex_reordered[BP].append(observables_tex[BP][index])

#     results_reordered[BP] = np.array(results_reordered[BP])
#     central_values_obs_reordered[BP] = np.array(central_values_obs_reordered[BP])

# print(results_reordered[BP])



# observables_tex = [find_tex_label_obs(obs) for obs in observables]
# observables_tex = [find_tex_label_obs(obs) for obs in observables_reordered]
# print(observables_tex)

# w = 1.0
# dimw = w / 2
# y_shift = np.linspace(0, -dimw, n_BPs) 

y_shift = [-0.15, 0.15]


# results_plot = results
results_plot = results_reordered
# print (results_plot)



#print(param_breaks)
fig_num = 0
for i, BP in enumerate(BPs):

    for scenario in scenarios:


        labels = observables_tex_reordered[BP][scenario][model_spec][:]
        for j, par in enumerate(observables_tex_reordered[BP][scenario][model_spec]):
            labels[j] = par


        nvar_per_plot = 50
        param_breaks = np.arange(0, len(observables[BP][scenario][model_spec]), nvar_per_plot)
        # param_breaks = np.array([0,5,10,15,20,25,29,33,37,41,46])
        if len(param_breaks)==1 or param_breaks[-1] != len(observables[BP][scenario][model_spec]):
            param_breaks = np.append(param_breaks, [len(observables[BP][scenario][model_spec])])

        print(len(observables[BP][scenario][model_spec]))
        print(param_breaks)

        
        for k in range(len(param_breaks) - 1):

            fig= plt.figure(fig_num, figsize=(4,10), dpi=150)
            fig_num = fig_num + 1
            ax = plt.gca()

            for spec_index, model_spec in enumerate(model_specs[scenario]):

                results_means  = np.copy((results_plot[BP][scenario][model_spec][:,0] - central_values_obs[BP][scenario][model_spec]) / results_plot[BP][scenario][model_spec][:,1] )
                results_errors = np.copy( results_plot[BP][scenario][model_spec][:,1] / results_plot[BP][scenario][model_spec][:,1] )

                y = np.arange(param_breaks[k],param_breaks[k+1])
                
                plt.axvline(x=0, c='0.6', linewidth=2)
            
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

            # ax.set_yticks(-y-dimw/2.)
            ax.set_yticks(-y)
            ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]],fontsize=8)
            x_limits = [plt.xlim()[0], plt.xlim()[1]]
            y_limits = [plt.ylim()[0] +1.0, plt.ylim()[1] -1.0]
            ax.hlines(y=-y, xmin=x_limits[0], xmax=x_limits[1], color="black", linestyle="--", linewidth=0.5)
            ax.set_xlim(*x_limits)
            ax.set_ylim(*y_limits)
            ax.tick_params(axis='x', size=10, labelsize=11)
            ax.tick_params(axis='x', which='minor', size=6)
            ax.set_xlabel(r'Pulls', fontsize=15)
            ax.legend(loc='best', fontsize=8)
            ax.set_title(plot_title[BP][scenario], fontsize=9)
            plt.tight_layout()   # Makes sure labels are not cut off
            plt.savefig(working_dir + f'comparison_plots/results_{results_dir}/pull_obs_{BP}_{scenario}_compare_{k}.pdf')

# plt.show()
