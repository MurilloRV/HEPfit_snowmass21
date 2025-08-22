import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math
import subprocess
import copy
from .utils import observable_order, parameter_order

plt.rcParams.update({
#   "text.usetex": True,
  'text.latex.preamble': r'\usepackage{txfonts}',
})


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

def find_tex_label_obs(obs):
    ### FCC-ee_240
    if obs == "eeZH_FCCee240":         tex_label = r"$\mu_{ZH}$(FCC-ee$_{240}$)"
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
    elif obs == "eeZH_FCCee365":        tex_label = r"$\mu_{ZH}$(FCC-ee$_{365}$)"
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
    return tex_label



def read_SM_predictions():

    # observables = {}
    central_values_obs = {}
    central_values_gaus_corr_obs = {}

    lmbd = 1
    WITH_LAMBDA = "no"
    
    working_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/large_kappa_lambda_fits"
    scenario = f"Lambda{lmbd}_FCCee240_FCCee365_{WITH_LAMBDA}HLLHClambda"
    scenario_dir = f"{working_dir}/{scenario}"
    input_file =  f"{scenario_dir}/results_observables/observables.txt"


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



# # Open the input file in read mode and output file in write mode
# working_dir = "./"


# # BPs = [f"BP_{i}" for i in range(8)]
# num_BPOs = 2
# num_BPBs = 17
# BPs = [f"BPO_{i}" for i in range(num_BPOs)]
# BPs = BPs + [f"BPB_{i}" for i in range(num_BPBs)]
# BPs = ["BPB_2", "BPB_4", "BPB_6"]
# # BP_Names = ["BPB 2", "BPB 4", "BPB 6"]
# BP_Names = ["BP 1", "BP 2", "BP 3"]
# print(BPs)


# # plot_labels = [f"BP {i}" for i in range(8)]
# plot_labels = [f"BPO {i}" for i in range(num_BPOs)]
# plot_labels = plot_labels + [f"BPB {i}" for i in range(num_BPBs)]

# n_BPs = len(BPs)

# # plot_title = [rf"IDM Central values ({BP}), FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$" for BP in BPs]
# # plot_title = [rf"IDM ({BP}), FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$" for BP in BP_Names]

# # scenarios = ["IDM_FCCee240_FCCee365" for i in range(num_BPOs + num_BPBs)]

# scenarios = [
#     # "IDM_FCCee240",
#     "IDM_FCCee240_FCCee365",
#     # "IDM_FCCee240_FCCee365_HLLHClambda",
# ]


# # spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_small_priors_long"
# # spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_no_HLLHC_Higgs_small_priors_long"
# # spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_no_C_HG_small_priors_long"
# # spec = "fits_realistic_HL_LHC_WFR_kala2_input_small_priors_long"
# spec = "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_small_priors_long"
# # spec = "fits_realistic_HL_LHC_WFR_kala2_input_no_HLLHC_Higgs_small_priors_long"
# # spec = "fits_realistic_HL_LHC_WFR_kala2_input_no_C_HG_small_priors_long"

# # Todo: fix the plots for fits without certain WC, like C_HG

# # compare_spec = "fits"
# compare_spec = "fits_realistic_HL_LHC_WFR_kala2_input_all_small_priors_long"

# model_specs = {
#     # "IDM_FCCee240" : [spec, "fits"],
#     "IDM_FCCee240_FCCee365" : [spec, compare_spec],
#     # "IDM_FCCee240_FCCee365_HLLHClambda" : [spec, "fits_realistic_HL_LHC_realistic_HL_LHC_long"],
# }

# labels = ["With new NPs", "Original"]
# # labels = ["w/ h External-leg", "Original"]
# model_specs_labels = {
#     # "IDM_FCCee240" : labels,
#     "IDM_FCCee240_FCCee365" : labels,
#     # "IDM_FCCee240_FCCee365_HLLHClambda" : labels,
# }

# results_dir = spec

# scenario_titles = [
#     # rf"FCC-ee$_{{240}}$",
#     rf"FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$",
#     # rf"FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$ + $\kappa_{{\lambda}}$ at HL-LHC",
# ]

# plot_titles = {}

# for i, BP in enumerate(BPs):
#     plot_titles[BP] = {}

#     for scenario, scenario_title in zip(scenarios, scenario_titles):
#         plot_titles[BP][scenario] = rf"IDM ({BP_Names[i]}), {scenario_title}"


# colors = [
#     "tab:orange",
#     "tab:blue",
# ]

def generate_pull_plots_pars(
    BPs,
    model_specs,
    working_dir,
    results_dir,
    model_specs_labels,
    plot_titles,
    colors=[],
    show_plots=False,
    nvar_per_plot=15,
):
    """
    Generate pull plots for the given parameters.

    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping scenarios to model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    results_dir : str
        Suffix of the name of the directory to store the results. Results are stored in
        '{working_dir}/comparison_plots/results_{results_dir}/'
    plot_titles : dict
        A dictionary containing the titles for the plots.
    results_dir : str
        Suffix of the name of the directory to store the results. Results are stored in
        '{working_dir}/comparison_plots/results_{results_dir}/'
    colors : list, optional
        List of colors assign to each model specification. If set to
        an empty list, the default matplotlib color cycle will be used.
    show_plots : bool, optional
        Whether to show the plots or not. Default is False.
    nvar_per_plot : int, optional
        The number of variables per plot. Default is 15.

    Returns
    -------
    None

    """

    scenarios = model_specs.keys()
    
    if colors == []:
        # Default matplotlib color cycle
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    files = {}
    for BP in BPs:
        files[BP] = {}
        for scenario in scenarios:
            files[BP][scenario] = {}
            for model_spec in model_specs[scenario]:
                files[BP][scenario][model_spec] = f"{working_dir}/{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"

    # Create the output directory, if it does not yet exist
    subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])

    results = {}
    parameters = {}
    parameters_tex = {}

    for BP in BPs:

        results[BP] = {}
        parameters[BP] = {}
        parameters_tex[BP] = {}
        for scenario in scenarios:

            parameters[BP][scenario] = {}
            parameters_tex[BP][scenario] = {}
            results[BP][scenario] = {}
            for model_spec in model_specs[scenario]:

                line_nrs = []
                parameters[BP][scenario][model_spec] = []
                parameters_tex[BP][scenario][model_spec] = []

                file_path = files[BP][scenario][model_spec]
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    
                    for n, line in enumerate(lines):
                        columns = line.split()
                        if len(columns) < 2:
                            continue
                        
                        if columns[1] == "Observable" and \
                        columns[2].startswith("\"C") and \
                        columns[2].endswith("corr\":"):
                            parameter = columns[2][1:-7]
                            parameters[BP][scenario][model_spec].append(parameter)
                            parameter_tex_label = find_tex_label_par(parameter)
                            parameters_tex[BP][scenario][model_spec].append(parameter_tex_label)
                            line_nrs.append(n)

                    results[BP][scenario][model_spec] = []
                    print(f"Reading results for {BP}, scenario: {scenario}, model spec: {model_spec}")
                    for line_nr, par in zip(line_nrs, parameters[BP][scenario][model_spec]):
                    
                        columns = lines[line_nr + 1].split()
                        means_uncertainties = [float(columns[3]),    # Mean
                                               float(columns[5]),]   # Uncertainty
                        
                        if means_uncertainties[1] != 0:
                            means_uncertainties[0] = means_uncertainties[0]/means_uncertainties[1]
                            means_uncertainties[1] = means_uncertainties[1]/means_uncertainties[1]
                        else:
                            means_uncertainties[0] = np.nan
                            means_uncertainties[1] = np.nan

                        results[BP][scenario][model_spec].append(means_uncertainties)

                results[BP][scenario][model_spec] = np.array(results[BP][scenario][model_spec])


    print(f"\nParameter dictionary: \n{parameters}")
    print(f"\nParameter latex dictionary: \n{parameters_tex}")

    # w = 1.0
    # dimw = w / 2
    # y_shift = np.linspace(0, -dimw, n_BPs) 
    y_shift = [-0.15, 0.15]

    # Align parameters across model_specs
    aligned_parameters = {}
    aligned_parameters_tex = {}

    for BP in BPs:
        aligned_parameters[BP] = {}
        aligned_parameters_tex[BP] = {}

        for scenario in scenarios:
            # Collect all unique parameters across model_specs
            all_parameters = set()
            for model_spec in model_specs[scenario]:
                all_parameters.update(parameters[BP][scenario][model_spec])

            aligned_parameters[BP][scenario] = sorted(all_parameters, key=parameter_order)
            aligned_parameters_tex[BP][scenario] = [
                find_tex_label_par(par) for par in aligned_parameters[BP][scenario]
            ]

            # Align results for each model_spec
            for model_spec in model_specs[scenario]:
                aligned_results = []
                for par in aligned_parameters[BP][scenario]:
                    if par in parameters[BP][scenario][model_spec]:
                        idx = parameters[BP][scenario][model_spec].index(par)
                        aligned_results.append(results[BP][scenario][model_spec][idx])
                    else:
                        # Handle missing parameters (e.g., assign NaN)
                        aligned_results.append([np.nan, np.nan])

                results[BP][scenario][model_spec] = np.array(aligned_results)

    print(f"\n\n\n")
    print(f"Aligned Parameters: {aligned_parameters[BP][scenario]}")
    print(f"Aligned Parameters latex: {aligned_parameters_tex[BP][scenario]}")
    print(f"Results Shape: {results[BP][scenario][model_spec].shape}")

    print(f"\n\n\n")
    num_fig = 0
    for i, BP in enumerate(BPs):
        for scenario in scenarios:

            nvar_per_plot = nvar_per_plot
            param_breaks = np.arange(0, len(aligned_parameters[BP][scenario]), nvar_per_plot)

            if len(param_breaks)==1 or param_breaks[-1] != len(aligned_parameters[BP][scenario]):
                param_breaks = np.append(param_breaks, [len(aligned_parameters[BP][scenario])])

            print(f"\nProducing plots for {BP}, scenario {scenario}")
            print(f"Total number of parameters: {len(aligned_parameters[BP][scenario])}")
            print(f"Parameter breaks: {param_breaks}")

            labels = aligned_parameters_tex[BP][scenario][:]
            for j, par in enumerate(aligned_parameters_tex[BP][scenario]):
                labels[j] = par


            for k in range(len(param_breaks) - 1):

                fig = plt.figure(num_fig, figsize=(5,5), dpi=150)
                num_fig = num_fig + 1
                ax = plt.gca()

                y = np.arange(param_breaks[k],param_breaks[k+1])
                
                plt.axvline(x=0, c='0.6', linewidth=2)

                for spec_index, model_spec in enumerate(model_specs[scenario]):
                    results_plot = np.copy(results[BP][scenario][model_spec])
                    ax.errorbar(results_plot[param_breaks[k]:param_breaks[k+1], 0],
                                -y-y_shift[spec_index], 
                                # -y, 
                                xerr=(results_plot[param_breaks[k]:param_breaks[k+1], 1],), 
                                fmt='o', 
                                linewidth=1.5, 
                                capsize=3.5, 
                                markersize=4, 
                                # label=plot_labels[i],
                                color=colors[spec_index],
                                label=model_specs_labels[scenario][spec_index],
                                # alpha=alphas[i],
                                )

                # ax.set_yticks(-y-dimw/2.)
                ax.set_yticks(-y)
                ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]],fontsize=10)
                x_limits = [plt.xlim()[0], plt.xlim()[1]]
                ax.hlines(y=-y, xmin=x_limits[0], xmax=x_limits[1], color="black", linestyle="--", linewidth=0.5)
                ax.set_xlim(*x_limits)
                ax.tick_params(axis='x', size=10, labelsize=11)
                ax.tick_params(axis='x', which='minor', size=6)
                ax.set_xlabel(r'Pulls', fontsize=15)
                ax.legend(loc='best', fontsize=12)
                ax.set_title(plot_titles[BP][scenario], fontsize=12)
                plt.tight_layout()   # Makes sure labels are not cut off
                plt.savefig(f"{working_dir}/comparison_plots/results_{results_dir}/pull_pars_{BP}_{scenario}_compare_{k}.pdf")

    if show_plots:
        plt.show()


HEPfit_flags = [
    "",
    "use_new_NPs_",
    "use_new_NPs_scale1.52_",
]

exclusive_flag_list = [
    "no_quad",
    "no_BSM",
    "no_1L_BSM",
    "no_1L_BSM_sqrt_s",
    "smeft_formula", 
    "smeft_formula_all", 
    "smeft_formula_sqrt", 
    "smeft_formula_no_cross", 
    "smeft_formula_external_leg", 
    "WFR_kala2_input",
    "WFR_kala2_input_all",
    "use_HEPfit_C1_values_WFR_kala2_input_all",
    "no_BSM_WFR_kala2_input_all",
]
additional_flag_list = [
    "",
    "_no_HLLHC_Higgs",
    "_no_C_HG",
    "_all_EW_mods",
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
    "_strict",
]

def generate_pull_plots_obs(
    BPs,
    model_specs,
    working_dir,
    results_dir,
    model_specs_labels,
    plot_titles,
    model,
    skip_obs=[],
    colors=[],
    show_plots=False,
    nvar_per_plot=50,
    only_higgs_fccee_obs=False,
    compare_with_SM=False,
):
    """
    
    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping scenarios to model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    results_dir : str
        Suffix of the name of the directory to store the results. Results are stored in
        '{working_dir}/comparison_plots/results_{results_dir}/'
    model_specs_labels : dict
        A dictionary containing the labels for the model specifications.
    plot_titles : dict
        A dictionary containing the titles for the plots.
    model : str
        The BSM model considered. Currently can be either "IDM" or "Z2SSM"
    skip_obs : list of str, optional
        A list of observables to skip (i.e., not show in the plots). 
        Default is an empty list.
    colors : list, optional
        List of colors assign to each model specification. If set to
        an empty list, the default matplotlib color cycle will be used.
    show_plots : bool, optional
        Whether to show the plots. Default is False.
    nvar_per_plot : int, optional
        The number of variables to plot per figure. Default is 15.
    only_higgs_fccee_obs : bool, optional
        If set to True, only FCC-ee Higgs observables are considered for 
        the plot. Default is False.
    compare_with_SM : bool, optional
        If set to true, use SM predictions as the central values for the 
        pulls. Default is False
    """

    scenarios = model_specs.keys()
    
    if colors == []:
        # Default matplotlib color cycle
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    if model not in ["IDM", "Z2SSM"]:
        raise ValueError(f"Invalid model specified ({model}). Please choose either 'IDM' or 'Z2SSM'.")

    files = {}
    for BP in BPs:
        files[BP] = {}
        for scenario in scenarios:
            files[BP][scenario] = {}
            for model_spec in model_specs[scenario]:
                files[BP][scenario][model_spec] = f"{working_dir}/{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"

    # Create the output directory, if it does not yet exist
    subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])


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


            if scenario == f"{model}_FCCee240_FCCee365" or scenario == f"{model}_FCCee240_FCCee365_HLLHClambda":
                conf_files[scenario][model_spec].append("ObservablesHiggs_FCCee_365_kappa_scaled")
                conf_files[scenario][model_spec].append("ObservablesVV_OO_FCCee_365")

            if scenario == f"{model}_FCCee240_FCCee365_HLLHClambda":
                conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs")] = f"ObservablesHiggs_scaled_realistic_HL_LHC"


            for hepfit_flag in HEPfit_flags:
                for exclusive_flag in exclusive_flag_list:
                    for additional_flag in additional_flag_list:
                        for priors_flag in priors_flag_list:
                            for MC_flag in MC_flag_list:
                                full_flag = hepfit_flag + exclusive_flag + additional_flag + priors_flag + MC_flag
                                if model_spec == f"fits_realistic_HL_LHC_{full_flag}":
                                    print(f"Full fit flag: {full_flag}")
                            
                                    # print(f"{conf_files[scenario][model_spec]}")

                                    Higgs_flag = exclusive_flag
                                    
                                    if not additional_flag == "_no_HLLHC_Higgs":
                                        conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_HLLHC_SM_kappa_scaled")] = f"ObservablesHiggs_HLLHC_SM_kappa_scaled_{Higgs_flag}"
                                    conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_FCCee_240_SM_kappa_scaled")] = f"ObservablesHiggs_FCCee_240_SM_kappa_scaled_{Higgs_flag}"
                                    if scenario == f"{model}_FCCee240_FCCee365" or scenario == f"{model}_FCCee240_FCCee365_HLLHClambda":
                                        conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_FCCee_365_kappa_scaled")] = f"ObservablesHiggs_FCCee_365_kappa_scaled_{Higgs_flag}"

                                    if additional_flag == "_no_HLLHC_Higgs":
                                        Higgs_flag = "no_HLLHC_" + Higgs_flag
                                    if scenario == f"{model}_FCCee240_FCCee365_HLLHClambda":
                                        conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_scaled_realistic_HL_LHC")] = f"ObservablesHiggs_scaled_realistic_HL_LHC_{Higgs_flag}"
                                    else:
                                        conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs")] = f"ObservablesHiggs_{Higgs_flag}"

                                    if additional_flag == "_all_EW_mods":
                                        conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesEW")] = "ObservablesEW_all_mods"
                                        conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesEW_Current_SM_noLFU")] = "ObservablesEW_Current_SM_noLFU_kappa_scaled"



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

                    file_name = f"{working_dir}/{BP}/{scenario}/{conf_file}"
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
                                if only_higgs_fccee_obs and not observable.startswith("eeZH") and not observable.startswith("eeHvv"):
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
                    print(f"Warning: Observable list for {BP} in {scenario} is not the same for all model specifications!")
                if not observables_tex[BP][scenario][model_spec] == observables_tex[BP][scenario][model_specs[scenario][0]]:
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


    print(f"Reading fit results")
    results = {}

    for BP in BPs:

        results[BP] = {}
        for scenario in scenarios:

            results[BP][scenario] = {}
            for model_spec in model_specs[scenario]:

                file_path = files[BP][scenario][model_spec]
                print(f"Reading file: {file_path}")
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


    y_shift = [-0.15, 0.15]

    fig_num = 0
    for i, BP in enumerate(BPs):

        for scenario in scenarios:

            labels = aligned_observables_tex[BP][scenario][:]
            for j, obs in enumerate(aligned_observables_tex[BP][scenario]):
                labels[j] = obs

            nvar_per_plot = nvar_per_plot
            param_breaks = np.arange(0, len(aligned_observables[BP][scenario]), nvar_per_plot)

            if len(param_breaks)==1 or param_breaks[-1] != len(aligned_observables[BP][scenario]):
                param_breaks = np.append(param_breaks, [len(aligned_observables[BP][scenario])])

            print(len(aligned_observables[BP][scenario]))
            print(param_breaks)

            
            for k in range(len(param_breaks) - 1):

                if only_higgs_fccee_obs:
                    fig= plt.figure(fig_num, figsize=(6,10), dpi=150)
                else:
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
                if only_higgs_fccee_obs:
                    fontsize = 12
                else:
                    fontsize = 8
                ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]],fontsize=fontsize)
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
                if only_higgs_fccee_obs:
                    ax.set_title(plot_titles[BP][scenario], fontsize=16)
                else:
                    ax.set_title(plot_titles[BP][scenario], fontsize=9)
                plt.tight_layout()   # Makes sure labels are not cut off
                plot_filename = f"pull_obs_{BP}_{scenario}_compare"
                if compare_with_SM: 
                    plot_filename = plot_filename + "_with_SM"
                if only_higgs_fccee_obs:
                    plot_filename = plot_filename + "_only_higgs_fccee_obs"
                plt.savefig(f"{working_dir}/comparison_plots/results_{results_dir}/{plot_filename}_{k}.pdf")

    if show_plots:
        plt.show()