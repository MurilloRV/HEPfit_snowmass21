import numpy as np
import copy
import re

def parameter_order(par):
    """
    Simple function which assigns the order of the model parameters for plots 

    Parameters
    ----------
    par : str
        The model parameter for which to determine the order, following HEPfit 
        conventions

    Returns
    -------
    order : int
        The order of the model parameter for plotting purposes.
    """

    order_dict = {
        "CW_corr":             1,
        "CHG_corr":            2,
        "CHWB_corr":           3,
        "CHWHB_gaga_corr":     4,
        "CHWHB_gagaorth_corr": 5,
        "CHW_corr":            6,
        "CHB_corr":            7,
        "CH_corr":             8,
        "CHbox_corr":          9,
        "CHD_corr":            10,
        "CHL1_11_corr":        11,
        "CHL1_22_corr":        12,
        "CHL1_33_corr":        13,
        "CHL3_11_corr":        14,
        "CHL3_22_corr":        15,
        "CHL3_33_corr":        16,
        "CHe_11_corr":         17,
        "CHe_22_corr":         18,
        "CHe_33_corr":         19,
        "CHQ1_11_corr":        20,
        "CHQ1_33_corr":        21,
        "CHQ3_11_corr":        22,
        "CHu_11_corr":         23,
        "CHd_11_corr":         24,
        "CHd_33_corr":         25,
        "CeH_22r_corr":        26,
        "CeH_33r_corr":        27,
        "CuH_22r_corr":        28,
        "CuH_33r_corr":        29,
        "CdH_33r_corr":        30,
        "CLL_1221_corr":       31,
    }
    return order_dict.get(par, 9999)  # Return a large number for unknown parameters

def observable_order(obs):
    """
    Simple function which assigns the order of the observables for plots 

    Parameters
    ----------
    obs : str
        The observable for which to determine the order, following HEPfit 
        conventions

    Returns
    -------
    order : int
        The order of the observable for plotting purposes.
    """

    order_dict = {
        "deltalHHH_HLLHC": 1,

        "eeZH_FCCee240":       2,
        "eeZHbb_FCCee240":     3,
        "eeHvvbb_FCCee240":    4,
        "eeZHcc_FCCee240":     5,
        "eeZHgg_FCCee240":     6,
        "eeZHWW_FCCee240":     7,
        "eeZHZZ_FCCee240":     8,
        "eeZHtautau_FCCee240": 9,
        "eeZHgaga_FCCee240":   10,
        "eeZHmumu_FCCee240":   11,
        "eeZHZga_FCCee240":    12,

        ### FCC-ee_365
        "eeZH_FCCee365":        13,
        "eeZHbb_FCCee365":      14,
        "eeHvvbb_FCCee365":     15,
        "eeZHcc_FCCee365":      16,
        "eeHvvcc_FCCee365":     17,
        "eeZHgg_FCCee365":      18,
        "eeHvvgg_FCCee365":     19,
        "eeZHWW_FCCee365":      20,
        "eeHvvWW_FCCee365":     21,
        "eeZHZZ_FCCee365":      22,
        "eeHvvZZ_FCCee365":     23,
        "eeZHtautau_FCCee365":  24,
        "eeHvvtautau_FCCee365": 25,
        "eeZHgaga_FCCee365":    26,
        "eeHvvgaga_FCCee365":   27,
        "eeZHmumu_FCCee365":    28,
        # "eeHvvmumu_FCCee365":   29,

        ### HL-LHC
        "muggHgagaHL":    29,
        "muggHZZ4lHL":    30,
        "muggHWW2l2vHL":  31,
        "muggHtautauHL":  32,
        "muggHbbHL":      33,
        "muggHmumuHL":    34,
        "muggHZgaHL":     35,

        "muVBFgagaHL":    36,
        "muVBFZZ4lHL":    37,
        "muVBFWW2l2vHL":  38,
        "muVBFtautauHL":  39,
        "muVBFmumuHL":    40,
        "muVBFZgaHL":     41,

        "muWHgagaHL":     42,
        "muWHZZ4lHL":     43,
        "muWHWW2l2vHL":   44,
        "muWHbbHL":       45,

        "muZHgagaHL":     46,
        "muZHZZ4lHL":     47,
        "muZHWW2l2vHL":   48,
        "muZHbbHL":       49,

        "muttHgagaHL":    50,
        "muttHZZ4lHL":    51,
        "muttHWW2l2vHL":  52,
        "muttHtautauHL":  53,
        "muttHbbHL":      54,
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


def find_tex_label_par(par_tex, par):
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
    # elif par == "CHbox":          tex_label = r"$C_{H\boxdot}$"
    elif par == "CHbox":          tex_label = "$C_{H\u25A1}$"
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

def find_tex_label_obs(obs_tex, obs):
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

    else: tex_label = fix_obs_tex(obs_tex, obs)

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
    
    return obs, central_values


def read_WC_predictions(
    working_dir,
    WCs,
    n_WC_values,
    observables,
    matched_predictions=False,
):

    for i in range(2):
        observables = list(observables.values())[0]

    if matched_predictions and n_WC_values != 1:
        print("Warning: Matched predictions should only with n_WC_values=1.")
        n_WC_values = 1

    print("observables:", observables)

    obs_predictions = {}
    for idx, wc in enumerate(WCs):
        obs_predictions[wc] = {}
        for point in range(n_WC_values):
            obs_predictions[wc][point] = np.full(len(observables), np.nan)

            if matched_predictions:
                filename = f"{working_dir}/../smeft_matching_inputs/observables_results/observables_BP{idx}.txt"
            else:
                filename = f"{working_dir}/observables_results/observables_{wc}_{point}.txt"
            with open(filename, "r") as input_file:
                print("Reading Observables:")
                for line_nr, input_line in enumerate(input_file):
                    # Skip the empty line after "Observables"
                    if line_nr == 0:
                        continue
                    
                    if input_line in ['\n', '\r\n']:
                        continue
                    else:
                        columns = input_line.split()
                        observable = columns[0]

                        if observable in observables:
                            idx = observables.index(observable)
                            obs_predictions[wc][point][idx] = float(columns[2])

            if np.isnan(obs_predictions[wc][point]).sum() != 0:
                print(f"Warning: Number of predictions for {wc} does not match number of observables.")
                print(f"Number of predictions: {len(obs_predictions[wc][point]) - np.isnan(obs_predictions[wc][point]).sum()}")
                print(f"Number of observables: {len(observables)}")

    return obs_predictions





def find_configuration_files(
    model_specs,
    model,
    read_WCs=False,
):
    """
    Find the names of the configuration files given a model specification. 

    Parameters
    ----------
    model_specs : dict
        Dictionary mapping scenarios to a list of model specifications.
    model : str
        The BSM model considered. Currently can be either "IDM" or "Z2SSM". Can
        also be set to "SM".
    read_WCs : bool, optional
        If set to True, the function will find the configuration files with the 
        Wilson coefficients, instead of the observables

    Returns
    -------
    conf_files : dict
        Dictionary mapping scenarios and model specifications to a list of 
        configuration files, conf_files[scenario][model_spec].
    """

    scenarios = model_specs.keys()

    if model == "SM" and not read_WCs: 
        conf_file_list = [
            "ObservablesEW.conf",
            "ObservablesEW_Current_SM_noLFU.conf",
            "ObservablesEW_FCCee_Zpole_SM.conf",
            "ObservablesEW_FCCee_WW_SM.conf",
            "ObservablesEW_HLLHC.conf",
            "ObservablesHiggs.conf",
            "ObservablesHiggs_FCCee_240_SM.conf",
            "ObservablesHiggs_FCCee_365.conf",
            "ObservablesHiggs_HLLHC_SM.conf",
            "ObservablesVV.conf",
            "aTGC_observables_Current.conf",
            "aTGC_observables_HLLHC_Full.conf",
            "ObservablesVV_OO_FCCee_161.conf",
            "ObservablesVV_OO_FCCee_240.conf",
            "ObservablesVV_OO_FCCee_365.conf",
            "EffVHcouplings_QFU12.conf",
            "HiggsEW_Par_Corr.conf",
        ]
        conf_files = { scenario : {spec : conf_file_list for spec in model_specs[scenario]} for scenario in scenarios}

        return conf_files


    HEPfit_flags = [
        "",
        "use_new_NPs_",
        "use_new_NPs_scale1.52_",
        "use_new_NPs_scale1.52_theoerr240_0.00107_theoerr365_0.00105_NPmismatch240_0_NPmismatch365_0_",
        # Z2SSM
        ##### ELLIPTIC ESTIMATES #####
        "use_new_NPs_theoerr240_1_theoerr365_1_klam_dependent_a240_1.18e-05_b240_2.3e-05_c240_0.000161_a365_2.12e-05_b365_-6.32e-05_c365_0.000304_",  # Z2SSM: Estimates EXCLUDING the O(1/Lambda_NP^2) curve
        "use_new_NPs_theoerr240_1_theoerr365_1_klam_dependent_a240_0.000754_b240_-0.00149_c240_0.000743_a365_0.000788_b365_-0.00162_c365_0.000845_",  # Z2SSM: Estimates INCLUDING the O(1/Lambda_NP^2) curve
        ##### RECTANGULAR ESTIMATES, with 2D scaling #####
        "use_new_NPs_scale1.52_theoerr240_1_theoerr365_1_klam_dependent_a240_2.06e-05_b240_7.03e-05_c240_-8.83e-05_a365_5.8e-05_b365_-0.000296_c365_0.00031_",   # Z2SSM: Estimates EXCLUDING the O(1/Lambda_NP^2) curve
        "use_new_NPs_scale1.52_theoerr240_1_theoerr365_1_klam_dependent_a240_0.000397_b240_-0.000673_c240_0.000277_a365_0.000403_b365_-0.000848_c365_0.000466_", # Z2SSM: Estimates INCLUDING the O(1/Lambda_NP^2) curve

        # IDM
        "use_new_NPs_klam_dependent_a240_8.42e-06_b240_6.93e-05_c240_0.000124_a365_1.99e-05_b365_-2.66e-05_c365_0.000313_",  # IDM: Estimates EXCLUDING the O(1/Lambda_NP^2) curve
        "use_new_NPs_klam_dependent_a240_0.000763_b240_-0.00152_c240_0.000761_a365_0.000792_b365_-0.00162_c365_0.000835_",   # IDM: Estimates INCLUDING the O(1/Lambda_NP^2) curve
    ]

    loop_order_flags = [
        "",
        "one_loop_inputs_",
    ]

    exclusive_flag_list = [
        "",
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
        "use_HEPfit_C1_values_decayrates_WFR_kala2_input_all",
        "no_BSM_WFR_kala2_input_all",
    ]
    additional_flag_list = [
        "",
        "_no_HLLHC_Higgs",
        "_no_C_HG",
        "_all_EW_mods",
        "_with_Af",
        "_noLoopH3d6Quad",
        "_all_EW_mods_noLoopH3d6Quad",
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
        "_long_bugfix",
    ]

    conf_files = {}
    for scenario in scenarios:

        conf_files[scenario] = {}
        for model_spec in model_specs[scenario]:

            print(f"\nSetting configuration files for scenario: {scenario} model spec: {model_spec}")

            if read_WCs:
                conf_files[scenario][model_spec] = [
                    "Globalfits/AllOps/d6Ops_corr",
                ]

            else:
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

                def determine_flags_in_model_spec(conf_files):
                    found_flag = False
                    for hepfit_flag in HEPfit_flags:
                        for loop_order_flag in loop_order_flags:
                            for exclusive_flag in exclusive_flag_list:
                                for additional_flag1 in additional_flag_list:
                                    for additional_flag2 in additional_flag_list:
                                        for priors_flag in priors_flag_list:
                                            for MC_flag in MC_flag_list:
                                                full_flag = hepfit_flag + loop_order_flag + exclusive_flag + additional_flag1 + additional_flag2 + priors_flag + MC_flag
                                                if model_spec == f"fits_realistic_HL_LHC_{full_flag}":
                                                    print(f"Full fit flag: {full_flag}")
                                                    found_flag = True

                                                    if read_WCs:
                                                        if additional_flag1 == "_no_C_HG" or additional_flag2 == "_no_C_HG":
                                                            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("d6Ops_corr")] = "d6Ops_corr_no_C_HG"

                                                    else:
                                                        Higgs_flag = loop_order_flag + exclusive_flag
                                                        
                                                        if not (additional_flag1 == "_no_HLLHC_Higgs" or additional_flag2 == "_no_HLLHC_Higgs"):
                                                            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_HLLHC_SM_kappa_scaled")] = f"ObservablesHiggs_HLLHC_SM_kappa_scaled_{Higgs_flag}"
                                                        conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_FCCee_240_SM_kappa_scaled")] = f"ObservablesHiggs_FCCee_240_SM_kappa_scaled_{Higgs_flag}"
                                                        if scenario == f"{model}_FCCee240_FCCee365" or scenario == f"{model}_FCCee240_FCCee365_HLLHClambda":
                                                            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_FCCee_365_kappa_scaled")] = f"ObservablesHiggs_FCCee_365_kappa_scaled_{Higgs_flag}"

                                                        if additional_flag1 == "_no_HLLHC_Higgs" or additional_flag2 == "_no_HLLHC_Higgs":
                                                            Higgs_flag = "no_HLLHC_" + Higgs_flag
                                                        if scenario == f"{model}_FCCee240_FCCee365_HLLHClambda":
                                                            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs_scaled_realistic_HL_LHC")] = f"ObservablesHiggs_scaled_realistic_HL_LHC_{Higgs_flag}"
                                                        else:
                                                            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index("ObservablesHiggs")] = f"ObservablesHiggs_{Higgs_flag}"

                                                        EWPO_conf1 = "ObservablesEW"
                                                        EWPO_conf2 = "ObservablesEW_Current_SM_noLFU"
                                                        EWPO_conf3 = "ObservablesEW_FCCee_Zpole_SM_kappa_scaled"
                                                        if additional_flag1 == "_all_EW_mods" or additional_flag2 == "_all_EW_mods":
                                                            EWPO_conf1_new = EWPO_conf1 + "_all_mods"
                                                            EWPO_conf2_new = EWPO_conf2 + "_kappa_scaled"
                                                            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index(EWPO_conf1)] = EWPO_conf1_new
                                                            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index(EWPO_conf2)] = EWPO_conf2_new
                                                            EWPO_conf1 = EWPO_conf1_new
                                                            EWPO_conf2 = EWPO_conf2_new
                                                           
                                                        if additional_flag1 == "_with_Af" or additional_flag2 == "_with_Af":
                                                            EWPO_conf1_new = EWPO_conf1 + "_with_Af"
                                                            EWPO_conf3_new = EWPO_conf3 + "_with_Af"
                                                            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index(EWPO_conf1)] = EWPO_conf1_new
                                                            conf_files[scenario][model_spec][conf_files[scenario][model_spec].index(EWPO_conf3)] = EWPO_conf3_new
                                                            EWPO_conf1 = EWPO_conf1_new
                                                            EWPO_conf3 = EWPO_conf3_new

                                                            if additional_flag1 == "_all_EW_mods" or additional_flag2 == "_all_EW_mods":
                                                                EWPO_conf2_new = EWPO_conf2 + "_with_Af"
                                                                conf_files[scenario][model_spec][conf_files[scenario][model_spec].index(EWPO_conf2)] = EWPO_conf2_new
                                                                EWPO_conf2 = EWPO_conf2_new



                                                    return conf_files
                                                    
                    if found_flag == False:
                        raise ValueError(f"Model specification {model_spec} could not be assigned flags. Make sure all flags are implemented")
                
                conf_files = determine_flags_in_model_spec(conf_files)

            for i, file in enumerate(conf_files[scenario][model_spec]):
                conf_files[scenario][model_spec][i] = file + ".conf"

            print(f"Files considered:")
            for file in conf_files[scenario][model_spec]:
                print(f"- {file}")

    return conf_files


def read_configuration_files(
    working_dir,
    BPs,
    model_specs,
    conf_files,
    only_obs=None,
    skip_obs=None,
    only_higgs_fccee_obs=False,
    read_model_parameters=False,
    compare_with_SM=False,
):
    """
    Function to read the configuration files for a given fit setup, in order to obtain 
    the central values and errors for the observables, which were given as input to such
    fit.

    Parameters
    ----------
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping scenarios to a list of model specifications.
    conf_files : dict
        Dictionary mapping scenarios and model specifications to a list of 
        configuration files, conf_files[scenario][model_spec].
    only_obs : list, optional
        List of observables to include. If set, only these observables will be
        processed.
    skip_obs : list of str, optional
        A list of observables to skip (i.e., don't store results). 
        Default is an empty list.
    only_higgs_fccee_obs : bool, optional
        If set to True, only FCC-ee Higgs observables are considered for 
        the plot. Default is False.
    read_model_parameters : bool, optional
        If set to True, instead of reading the configuration files for the input
        observables, the function reads the config file for the input Wilson 
        coefficients. Although central values and errors are not read in this 
        case, the function can still be used to obtain the list of Wilson coefficients
    compare_with_SM : bool, optional
        If set to true, use SM predictions as the central values for the 
        pulls. Default is False

    Returns
    -------
    observables : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list of observables which were found in the configuration files.
    observables_tex : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list LaTeX labels for observables which were found in the configuration files.
    central_values_obs : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list of central values for observables which were found in the configuration files.
    input_uncertainties_obs : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list of input uncertainties for observables which were found in the configuration files.
    """

    if only_obs is not None and skip_obs is not None:
        raise ValueError("only_obs and skip_obs cannot be both set!")

    scenarios = model_specs.keys()

    observables = {}
    observables_tex = {}
    central_values_obs = {}
    input_uncertainties = {}

    for BP in BPs:
        observables[BP] = {}
        observables_tex[BP] = {}
        central_values_obs[BP] = {}
        input_uncertainties[BP] = {}

        for scenario in scenarios:
            observables[BP][scenario] = {}
            observables_tex[BP][scenario] = {} 
            central_values_obs[BP][scenario] = {}
            input_uncertainties[BP][scenario] = {}

            for model_spec in model_specs[scenario]:
                observables[BP][scenario][model_spec] = []
                observables_tex[BP][scenario][model_spec] = []
                central_values_obs[BP][scenario][model_spec] = []
                input_uncertainties[BP][scenario][model_spec] = []

                for conf_file in conf_files[scenario][model_spec]:

                    file_name = f"{working_dir}/{BP}/{scenario}/{conf_file}"
                    print(f"Reading configuration file {file_name}")

                    with open(file_name, "r") as infile:
                        
                        for line in infile:
                            columns = line.split()

                            if (line.startswith("Observable ") \
                                or line.startswith("AsyGausObservable ")):

                                if read_model_parameters==False and not (columns[6]=="MCMC" and columns[7]=="weight"):
                                    continue

                                observable = columns[1]

                                if  (only_obs is not None and observable not in only_obs) or \
                                    (skip_obs is not None and observable in skip_obs) or \
                                    (only_higgs_fccee_obs and not observable.startswith("eeZH") and not observable.startswith("eeHvv")):
                                    continue

                                if read_model_parameters==True:
                                    observable_tex_label = find_tex_label_par(columns[3], observable[0:-5])
                                    central_value = 0.0
                                    uncertainty = 0.0
                                else:
                                    observable_tex_label = find_tex_label_obs(columns[3], observable)
                                    central_value = float(columns[8])
                                    uncertainty = float(columns[9])

                                observables[BP][scenario][model_spec].append(observable)
                                observables_tex[BP][scenario][model_spec].append(observable_tex_label)
                                central_values_obs[BP][scenario][model_spec].append(central_value)
                                input_uncertainties[BP][scenario][model_spec].append(uncertainty)
                                

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

    return observables, observables_tex, central_values_obs, input_uncertainties


def read_fit_results(
    BPs,
    model_specs,
    files,
    observables,
):
    """
    Read and store the fit results (central values and errors), given certain benchmark points,
    model specifications, and observables. The path to the files to be read must be stored in 
    the {files} dictionary.

    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping scenarios to a list of model specifications.
    files : dict
        Dictionary mapping BPs, scenarios, and model specifications to the Statistics.txt file 
        containing the fit results
    observables : dict or list
        The observables to read. Must be a dictionary mapping benchmark points, scenarios, and 
        model specifications, to a list of observables. A list of observables can also be provided;
        in that case, the same list will be used for all benchmark points, scenarios, and 
        model_specs.

    Returns
    -------
    results : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list of means and standard deviations for the observables which were 
        found in the fit results files.

    """
    scenarios = list(model_specs.keys())

    if isinstance(observables, list):
        observables = {BP: {scenario: {model_spec: observables for model_spec in model_specs[scenario]} for scenario in scenarios} for BP in BPs}
    elif not isinstance(observables, dict):
        raise ValueError("observables must be either a list or a dictionary with the correct structure!")

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

                    # print(f"Line numbers: {line_nrs}")

                    if any(np.isnan(line_nrs)):
                        print(f"Missing observable: {observables[BP][scenario][model_spec][line_nrs.index(np.nan)]}")
                        raise ValueError(f"Not all observables were found in the file {file_path}!")

                    results[BP][scenario][model_spec] = []

                    for line_nr, obs in zip(line_nrs, observables[BP][scenario][model_spec]):                    
                        columns = lines[line_nr + 1].split()
                        results[BP][scenario][model_spec].append([float(columns[3]),    # Mean
                                                                  float(columns[5]),])  # Uncertainty

                results[BP][scenario][model_spec] = np.array(results[BP][scenario][model_spec])

    return results


def read_fit_results_pars(
    BPs,
    model_specs,
    working_dir,
    scenarios,
    model,
    only_pars=None,
):
    """
    Read and store the fit results for the model parameters (the Wilson coefficients), given 
    certain benchmark points, model specifications, and scenarios. The path to the files to be 
    read must be stored in the {files} dictionary.

    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping scenarios to a list of model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    model : str
        The BSM model considered. Currently can be either "IDM" or "Z2SSM"
    only_pars : list, optional
        List of parameters to include. If set, only these parameters will be
        processed.
    

    Returns
    -------
    parameters : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list of parameters which were found in the configuration files.
    observables_tex : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list LaTeX labels for parameters which were found in the configuration files.
    central_values_obs : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list of central values for parameters which were found in the configuration files.
    results : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list of means and standard deviations for the parameters which were 
        found in the fit results files.

    """

    files = {}
    for BP in BPs:
        files[BP] = {}
        for scenario in scenarios:
            files[BP][scenario] = {}
            for model_spec in model_specs[scenario]:
                files[BP][scenario][model_spec] = f"{working_dir}/{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"

    print("\nFinding configuration files for the observables")
    conf_files = find_configuration_files(model_specs, model, read_WCs=True)
        
    print(f"\nReading configuration files for observables")
    parameters, parameters_tex, central_values_obs, _ = read_configuration_files(
        working_dir,
        BPs,
        model_specs,
        conf_files,
        only_obs=only_pars,
        skip_obs=None,
        only_higgs_fccee_obs=False,
        read_model_parameters=True,
        compare_with_SM=False,
    )
    print(parameters)

    print(f"\nReading fit results")
    results = read_fit_results(
        BPs=BPs,
        model_specs=model_specs,
        observables=parameters,
        files=files,
    )

    print(f"\nParameter dictionary: \n{parameters}")
    print(f"\nParameter latex dictionary: \n{parameters_tex}")

    return (
        parameters, 
        parameters_tex, 
        central_values_obs, 
        results, 
    )


def read_fit_results_dim6Ops_correlations(
    BPs,
    model_specs,
    files=None,
    working_dir=None,
    assert_equal_observables=False,
):
    """
    Read and store the fit results for the correlation matrix of the Wilson coefficients, given 
    certain benchmark points, model specifications, and observables. The path to the files to be 
    read must be stored in the {files} dictionary.

    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping scenarios to a list of model specifications.
    files : dict, optional
        Dictionary mapping BPs, scenarios, and model specifications to the Statistics.txt file 
        containing the fit results
    working_dir : str, optional
        Working directory path, containing subdirectories for each benchmark point. Will be used 
        to construct the path to the files containing the fit results, if the {files} dictionary 
        is not provided.
    assert_equal_observables : bool, optional
        If set to True, the function will raise an error if the list of observables found for each
        BP, scenario, and model specification are not the all the same. Default is False, in which 
        case only a warning will be printed instead.

    Returns
    -------
    results : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to the covariance matrix of the Wilson coefficients.

    """
    scenarios = list(model_specs.keys())

    if files is None:
        if working_dir is None:
            raise ValueError("Either 'files' or 'working_dir' must be provided.")
        files = {}
        for BP in BPs:
            files[BP] = {}
            for scenario in scenarios:
                files[BP][scenario] = {}
            for model_spec in model_specs[scenario]:
                files[BP][scenario][model_spec] = f"{working_dir}/{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"

    
    observables = {BP: {scenario: {model_spec: [] for model_spec in model_specs[scenario]} for scenario in scenarios} for BP in BPs}

    corr_matrices = {}
    for BP in BPs:

        corr_matrices[BP] = {}
        for scenario in scenarios:

            corr_matrices[BP][scenario] = {}
            for model_spec in model_specs[scenario]:

                file_path = files[BP][scenario][model_spec]
                print(f"Reading file: {file_path}")
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    
                    for n, line in enumerate(lines):
                        columns = line.split()
                        if len(columns) < 2:
                            continue
                        
                        # Finding the names of the Wilson coefficients in the correlation matrix
                        if (columns[1] == "Observable" \
                            or columns[1] == "AsyGausObservable") \
                            and re.search("^C.*_corr$", columns[2][1:-2]):

                            observables[BP][scenario][model_spec].append(columns[2][1:-2])

                        # Finding the start of the correlation matrix
                        if line.startswith("The correlation matrix for dim6Ops is given by the"):
                            start_line_nr = n + 4

                    n_obs = len(observables[BP][scenario][model_spec])
                    print(f"Found {n_obs} observables in the correlation matrix\n")
                    corr_matrix = np.eye(n_obs)

                    for n, line in enumerate(lines[start_line_nr:]):
                        columns = line.split()

                        # Reached the end of the correlation matrix
                        if len(columns) < 2:
                            break
                        else:
                            row_nr = n
                            for col_nr in range(0, row_nr):
                                corr_matrix[row_nr, col_nr] = float(columns[col_nr + 2])
                                corr_matrix[col_nr, row_nr] = float(columns[col_nr + 2])

                corr_matrices[BP][scenario][model_spec] = corr_matrix

                if not observables[BP][scenario][model_spec] == observables[BPs[0]][scenarios[0]][model_specs[scenarios[0]][0]]:
                    error_msg = "Observable lists are not the same for all BPs, scenarios, and model specifications!"
                    if assert_equal_observables:
                        raise ValueError(error_msg)
                    else:
                        print("Warning: " + error_msg)

    return corr_matrices, observables


def align_observables(
    observable_order_func,
    BPs,
    model_specs,
    observables,
    observables_tex,
    central_values_obs,
    results,
):
    """
    Function to sort observables following a given scheme, defined by the {observable_order_func} 
    argument. 

    Parameters
    ----------
    observable_order_func : callable
        Function defining the order of the observables for the alignment. Must take a single 
        argument (an observable name) and return a numeric value indicating its order.
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping scenarios to a list of model specifications.
    observables : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list of observables which were found in the configuration files.
    observables_tex : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list LaTeX labels for observables which were found in the configuration files.
    central_values_obs : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list of central values for observables which were found in the configuration files.
    results : dict
        Dictionary mapping benchmark points, scenarios, and model specifications, 
        to a list of central values for observables which were found in the configuration files.

    Returns
    -------
    aligned_observables : dict
        The {observables} dictionary, after sorting observables
    aligned_observables_tex : dict
        The {aligned_observables_tex} dictionary, after sorting observables
    central_values_obs : dict
        The {central_values_obs} dictionary, after sorting observables
    results : dict
        The {results} dictionary, after sorting observables

    """
    
    scenarios = model_specs.keys()
    
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

            aligned_observables[BP][scenario] = sorted(all_observables, key=observable_order_func)
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

    return aligned_observables, aligned_observables_tex, central_values_obs, results
