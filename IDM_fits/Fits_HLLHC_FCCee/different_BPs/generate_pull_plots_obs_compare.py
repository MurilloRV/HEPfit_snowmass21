import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
import subprocess
import copy


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

def observable_order(obs):
    order_dict = {
        "eeZH_FCCee240":       1,
        "eeZHbb_FCCee240":     2,
        "eeHvvbb_FCCee240":    3,
        "eeZHcc_FCCee240":     4,
        "eeZHgg_FCCee240":     5,
        "eeZHWW_FCCee240":     6,
        "eeZHZZ_FCCee240":     7,
        "eeZHtautau_FCCee240": 8,
        "eeZHgaga_FCCee240":   9,
        "eeZHmumu_FCCee240":   10,
        "eeZHZga_FCCee240":    11,

        ### FCC-ee_365
        "eeZH_FCCee365":        12,
        "eeZHbb_FCCee365":      13,
        "eeHvvbb_FCCee365":     14,
        "eeZHcc_FCCee365":      15,
        "eeHvvcc_FCCee365":     16,
        "eeZHgg_FCCee365":      17,
        "eeHvvgg_FCCee365":     18,
        "eeZHWW_FCCee365":      19,
        "eeHvvWW_FCCee365":     20,
        "eeZHZZ_FCCee365":      21,
        "eeHvvZZ_FCCee365":     22,
        "eeZHtautau_FCCee365":  23,
        "eeHvvtautau_FCCee365": 24,
        "eeZHgaga_FCCee365":    25,
        "eeHvvgaga_FCCee365":   26,
        "eeZHmumu_FCCee365":    27,
        # "eeHvvmumu_FCCee365":   28,

        ### HL-LHC
        "muggHgagaHL":    28,
        "muggHZZ4lHL":    29,
        "muggHWW2l2vHL":  30,
        "muggHtautauHL":  31,
        "muggHbbHL":      32,
        "muggHmumuHL":    33,
        "muggHZgaHL":     34,

        "muVBFgagaHL":    35,
        "muVBFZZ4lHL":    36,
        "muVBFWW2l2vHL":  37,
        "muVBFtautauHL":  38,
        "muVBFmumuHL":    39,
        "muVBFZgaHL":     40,

        "muWHgagaHL":     41,
        "muWHZZ4lHL":     42,
        "muWHWW2l2vHL":   43,
        "muWHbbHL":       44,

        "muZHgagaHL":     45,
        "muZHZZ4lHL":     46,
        "muZHWW2l2vHL":   47,
        "muZHbbHL":       48,

        "muttHgagaHL":    49,
        "muttHZZ4lHL":    50,
        "muttHWW2l2vHL":  51,
        "muttHtautauHL":  52,
        "muttHbbHL":      53,
    }

    if obs in order_dict:
        order = order_dict[obs]
    elif obs.endswith("_C"):
        order = 10000
    elif obs.endswith("_FCCee"):
        order = 20000
    elif obs.endswith("_FCCee161"):
        order = 30000
    elif obs.endswith("_FCCee240"):
        order = 40000
    elif obs.endswith("_FCCee365"):
        order = 50000
    elif obs.endswith("_HLLHC") or obs.endswith("_HLLHC_OO"):
        order = 60000
    else:
        order = 999999

    return order


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
print(f"BPs: {BPs}")


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

# Use SM predictions as the central values for the pulls. Default should be False
compare_with_SM = True

def read_SM_predictions():

    # observables = {}
    central_values_obs = {}
    central_values_gaus_corr_obs = {}

    lmbd = 1
    WITH_LAMBDA = "no"
    
    working_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/large_kappa_lambda_fits/"
    scenario = f"Lambda{lmbd}_FCCee240_FCCee365_{WITH_LAMBDA}HLLHClambda"
    scenario_dir = working_dir + scenario + "/"
    input_file =  scenario_dir + "results_observables/observables.txt"


    print(f"Reading SM predictions")

    with open(input_file, 'r') as infile:

        print("Reading names of configuration files with observables\n")
        observable_files = []
        for line_nr, input_line in enumerate(infile):

            if input_line.startswith("Including File: ../Globalfits/AllOps/../../"):
                # Split the line into columns by whitespace
                columns = input_line.split()
                
                observable_file = columns[2]
                observable_files.append(observable_file)


            if input_line.startswith("Observables:"):
                print(f"Files found in results: \n")
                [print(file_name) for file_name in observable_files]
                print("\n")
                break

        print("Reading Observables:")
        for line_nr, input_line in enumerate(infile):
            # Skip the empty line after "Observables"
            if line_nr == 0:
                continue
            
            if input_line in ['\n', '\r\n']:
                # observables_end = line_nr
                break
            else:
                columns = input_line.split()
                observable = columns[0]
                central_values_obs[observable] = float(columns[2])

        print(central_values_obs)


        print("\nReading Correlated Gaussian Observables: ")
        corr_obs = {}
        for line_nr, input_line in enumerate(infile):
            # Skip the "Correlated Gaussian Observables:" line and the following empty one
            if line_nr <= 1:
                continue

            if input_line in ['\n', '\r\n']:
                if corr_obs == {}: break  # Reached end of file

                central_values_gaus_corr_obs[corr_obs_name] = copy.deepcopy(corr_obs)
                corr_obs = {}
                continue
            elif len(input_line.split()) == 1:
                corr_obs_name = input_line.split()[0]
            else:
                columns = input_line.split()
                observable = columns[0]
                corr_obs[observable] = float(columns[2])

        print(central_values_gaus_corr_obs)

    obs, central_values = zip(*central_values_obs.items())

    gaus_corr_obs = {}
    for dict in central_values_gaus_corr_obs.values():
        gaus_corr_obs.update(dict)
    obs_, central_values_ = zip(*gaus_corr_obs.items())

    obs = list(obs) + list(obs_)
    central_values = list(central_values) + list(central_values_)
    central_values = np.array(central_values)

    print(f"SM observables: {obs}")

    # obs_tex = [np.nan for i in range(len(obs))]

    # return obs, obs_tex, central_values
    return obs, central_values


# spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_small_priors_long"
# spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_no_HLLHC_Higgs_small_priors_long"
# spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_no_C_HG_small_priors_long"
# spec = "fits_realistic_HL_LHC_WFR_kala2_input_small_priors_long"
# spec = "fits_realistic_HL_LHC_WFR_kala2_input_no_HLLHC_Higgs_small_priors_long"
spec = "fits_realistic_HL_LHC_WFR_kala2_input_no_C_HG_small_priors_long"

# spec_compare = "fits"
# spec_compare = "fits_realistic_HL_LHC_smeft_formula_no_cross_small_priors_long"
spec_compare = "fits_realistic_HL_LHC_WFR_kala2_input_small_priors_long"

model_specs = {
    # "IDM_FCCee240" : [spec, "fits"],
    "IDM_FCCee240_FCCee365" : [spec, spec_compare],
    # "IDM_FCCee240_FCCee365_HLLHClambda" : [spec, "fits_realistic_HL_LHC_realistic_HL_LHC_long"],
}

# labels = ["HEPfit formula", "Original"]
# labels = ["w/ h External-leg", "Original"]
labels = [r"No $C_{HG}$", r"w/ $C_{HG}$"]
model_specs_labels = {
    # "IDM_FCCee240" : labels,
    "IDM_FCCee240_FCCee365" : labels,
    # "IDM_FCCee240_FCCee365_HLLHClambda" : labels,
}

results_dir = spec


# Do not plot the following observables
# skip_obs = ["Mw_C", "GammaZ_C"]
skip_obs = ["Mw_C", "Mw_HLLHC", "Mw_FCCee", "GammaZ_C", "GammaZ_FCCee"]

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

exclusive_flag_list = [
    "no_quad",
    "no_1L_BSM",
    "no_1L_BSM_sqrt_s",
    "smeft_formula", 
    "smeft_formula_sqrt", 
    "smeft_formula_no_cross", 
    "smeft_formula_external_leg", 
    "WFR_kala2_input"
]
additional_flag_list = [
    "",
    "_no_HLLHC_Higgs",
    "_no_C_HG",
]
priors_flag_list = [
    "",
    "_small_priors",
    "_test_small_priors",
]
MC_flag_list = [
    "_short",
    "_long",
    "_full",
]

conf_files = {}
for scenario in scenarios:

    conf_files[scenario] = {}
    for model_spec in model_specs[scenario]:

        print(f"\n\n\nSetting configuration files for scenario: {scenario} model spec: {model_spec}")

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

        if "no_HLLHC_Higgs" in model_spec:
            conf_files[scenario][model_spec].remove("ObservablesHiggs_HLLHC_SM_kappa_scaled")


        if scenario == "IDM_FCCee240_FCCee365" or scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
            conf_files[scenario][model_spec].append("ObservablesHiggs_FCCee_365_kappa_scaled")
            conf_files[scenario][model_spec].append("ObservablesVV_OO_FCCee_365")

        if scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs")] = f"ObservablesHiggs_scaled_realistic_HL_LHC"


        if model_spec == "fits_realistic_HL_LHC_all_EW_mods_long":
            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesEW")] = "ObservablesEW_all_mods"
            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesEW_Current_SM_noLFU")] = "ObservablesEW_Current_SM_noLFU_kappa_scaled"

        
        for exclusive_flag in exclusive_flag_list:
            for additional_flag in additional_flag_list:
                for priors_flag in priors_flag_list:
                    for MC_flag in MC_flag_list:
                        full_flag = exclusive_flag + additional_flag + priors_flag + MC_flag
                        if model_spec == f"fits_realistic_HL_LHC_{full_flag}":
                    
                            print(f"Full fit flag: {full_flag}")
                            # print(f"{conf_files[scenario][model_spec]}")

                            Higgs_flag = exclusive_flag
                            
                            if not additional_flag == "_no_HLLHC_Higgs":
                                conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_HLLHC_SM_kappa_scaled")] = f"ObservablesHiggs_HLLHC_SM_kappa_scaled_{Higgs_flag}"
                            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_FCCee_240_SM_kappa_scaled")] = f"ObservablesHiggs_FCCee_240_SM_kappa_scaled_{Higgs_flag}"
                            if scenario == "IDM_FCCee240_FCCee365" or scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
                                conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_FCCee_365_kappa_scaled")] = f"ObservablesHiggs_FCCee_365_kappa_scaled_{Higgs_flag}"

                            if additional_flag == "_no_HLLHC_Higgs":
                                Higgs_flag = "no_HLLHC_" + Higgs_flag
                            if scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
                                conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_scaled_realistic_HL_LHC")] = f"ObservablesHiggs_scaled_realistic_HL_LHC_{Higgs_flag}"
                            else:
                                conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs")] = f"ObservablesHiggs_{Higgs_flag}"



        for i, file in enumerate(conf_files[scenario][model_spec]):
            conf_files[scenario][model_spec][i] = file + ".conf"

        print(f"Files considered:")
        for file in conf_files[scenario][model_spec]:
            print(f"- {file}")


print("\n\n\n")
    


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
                            

            n_obs = len(observables[BP][scenario][model_spec])
            print(f"Found {n_obs} observables")
            print("\n\n")

            if not observables[BP][scenario][model_spec] == observables[BP][scenario][model_specs[scenario][0]]:
                # raise ValueError(f"Observable list for {BP} in {scenario} is not the same for all model specifications!")
                print(f"Warning: Observable list for {BP} in {scenario} is not the same for all model specifications!")
            if not observables_tex[BP][scenario][model_spec] == observables_tex[BP][scenario][model_specs[scenario][0]]:
                # raise ValueError(f"Observable latex label list for {BP} in {scenario} is not the same for all model specifications!")
                print(f"Warning: Observable latex label list for {BP} in {scenario} is not the same for all model specifications!")

            if compare_with_SM:
                obs_SM, central_values_SM = read_SM_predictions()
                central_values_obs[BP][scenario][model_spec] = np.full((n_obs,), np.nan)
                for idx, obs in enumerate(observables[BP][scenario][model_spec]):
                    if obs in obs_SM:
                        idx_SM = obs_SM.index(obs)
                        central_values_obs[BP][scenario][model_spec][idx] = central_values_SM[idx_SM]
                    else:
                        raise ValueError(f"Observable {obs} not found in SM predictions!")

# print(observables)
# print(f"Central values: {central_values_obs}")



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

            index = observables[BP][scenario][model_spec].index("muttHWW2l2vHL")
            print(f"muttHWW2l2vHL results = {results[BP][scenario][model_spec][index,:]}")


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
        # aligned_observables_tex[BP][scenario] = [
        #     find_tex_label_obs(obs) for obs in aligned_observables[BP][scenario]
        # ]

        # aligned_observables_tex[BP][scenario] = []
        # for obs in aligned_observables[BP][scenario]:
        #     try:
        #         observable_tex_label = find_tex_label_obs(obs)
        #     except KeyError:
        #         # print(observable)
        #         observable_tex_label = fix_obs_tex(columns[3], obs)
        #     aligned_observables_tex[BP][scenario].append(observable_tex_label)

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


y_shift = [-0.15, 0.15]


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

            fig= plt.figure(fig_num, figsize=(4,10), dpi=150)
            fig_num = fig_num + 1
            ax = plt.gca()

            for spec_index, model_spec in enumerate(model_specs[scenario]):

                # index = aligned_observables[BP][scenario].index("muttHWW2l2vHL")
                # print(f"muttHWW2l2vHL results = {results[BP][scenario][model_spec][index,:]}")

                results_means  = np.copy((results[BP][scenario][model_spec][:,0] - central_values_obs[BP][scenario][model_spec]) / results[BP][scenario][model_spec][:,1] )
                results_errors = np.copy( results[BP][scenario][model_spec][:,1] / results[BP][scenario][model_spec][:,1] )

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
            if compare_with_SM:
                ax.set_xlabel(r'Pulls (w.r.t. SM prediction)', fontsize=15)
            else:
                ax.set_xlabel(r'Pulls', fontsize=15)
            ax.legend(loc='best', fontsize=8)
            ax.set_title(plot_title[BP][scenario], fontsize=9)
            plt.tight_layout()   # Makes sure labels are not cut off
            plot_filename = f"pull_obs_{BP}_{scenario}_compare"
            if compare_with_SM: 
                plot_filename = plot_filename + "_with_SM"
            plt.savefig(working_dir + f'comparison_plots/results_{results_dir}/{plot_filename}_{k}.pdf')

plt.show()
