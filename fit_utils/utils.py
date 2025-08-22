import uproot
import subprocess
import hist
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import math
import os.path

plt.rcParams.update({
    #   "text.usetex": True,
    'text.latex.preamble': r'\usepackage{txfonts}'+'\n'+r'\usepackage{amsmath}',
    'savefig.dpi' : 300,
})


def print_to_file(message, file):
    """
    Function to print a message both to terminal output and to a file
    """
    print(message)
    print(message, file=file)

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
        "CW":             1,
        "CHG":            2,
        "CHWB":           3,
        "CHWHB_gaga":     4,
        "CHWHB_gagaorth": 5,
        "CHW":            6,
        "CHB":            7,
        "CH":             8,
        "CHD":            9,
        "CHbox":          10,
        "CHL1_11":        11,
        "CHL1_22":        12,
        "CHL1_33":        13,
        "CHL3_11":        14,
        "CHL3_22":        15,
        "CHL3_33":        16,
        "CHe_11":         17,
        "CHe_22":         18,
        "CHe_33":         19,
        "CHQ1_11":        20,
        "CHQ1_33":        21,
        "CHQ3_11":        22,
        "CHu_11":         23,
        "CHd_11":         24,
        "CHd_33":         25,
        "CeH_22r":        26,
        "CeH_33r":        27,
        "CuH_22r":        28,
        "CuH_33r":        29,
        "CdH_33r":        30,
        "CLL_1221":       31,
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



def group_plots(
    BPs,
    model_specs,
    working_dir,
    results_dirs,
    copy_obs=["deltalHHH_HLLHC_mod",],
):
    """
    Copy plots with the posterior distribution for observables from global fit results.
    The <model_specs> dictionary maps each collider configurations to a list of model 
    specifications. The latter must all have the same length, equal to the length of the
    {results_dirs} list. The function copies the relevant plots for each benchmark point
    and collider scenario, with the results for the i-th model specification
    <model_specs[scenario][i]> results being stored in the directory corresponding to the
    i-th entry in the {results_dirs} list.

    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping collider scenarios to model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    results_dirs : list of str
        List of suffixes for the result directories. For each {results_dir} in this list,
        the corresponding results will be stored in the directory
        '{working_dir}/comparison_plots/results_{results_dir}/'
    copy_obs : list of str
        List of observables to copy. Default is ["deltalHHH_HLLHC_mod"].

    Returns
    -------
    None
    """

    # Create the output directories, if they do not yet exist
    for results_dir in results_dirs:
        subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])

    all_scenarios = model_specs.keys()

    for scenario in all_scenarios:
        for spec, results_dir in zip(model_specs[scenario] , results_dirs):
            for BP in BPs:
                for obs in copy_obs:
                    try:
                        input_path  = f"{working_dir}/{BP}/{scenario}/results_{spec}/Observables/{obs}.pdf"
                        output_path = f"{working_dir}/comparison_plots/results_{results_dir}/{obs}_{BP}_{scenario}.pdf"
                        subprocess.run(["cp", input_path, output_path])
                        print(F"Succesfully copied plot to {output_path}")
                    except:
                        print(f"file not found: {working_dir}/{BP}/{scenario}/results_{spec}/Observables/{obs}.pdf")

def print_klam_results(
    BPs,
    model_specs,
    working_dir,
    results_dirs,
):
    """
    Function to read the Statistics.txt file, generated by the global fit, and extract the 
    central value and uncertainty in the fitted kappa_lambda-1. The results are printed to
    the "{working_dir}/comparison_plots/results_{results_dir}/klam_results.txt" file, according
    to the "{BP},{kappa_lambda central value},{kappa_lambda error}" format.

    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping scenarios to model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    results_dirs : list of str
        List of suffixes for the result directories. For each {results_dir} in this list,
        the corresponding results will be stored in the directory
        '{working_dir}/comparison_plots/results_{results_dir}/'

    Returns
    -------
    None

    """

    scenarios = model_specs.keys()

    files = {}
    for BP in BPs:
        files[BP] = {}
        for scenario in scenarios:
            files[BP][scenario] = {}
            for model_spec in model_specs[scenario]:
                files[BP][scenario][model_spec] = f"{working_dir}/{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"

    # Create the output directories, if they do not yet exist
    for results_dir in results_dirs:
        subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])

    results = {}
    parameters = {}

    for BP in BPs:

        results[BP] = {}
        parameters[BP] = {}
        for scenario in scenarios:

            parameters[BP][scenario] = {}
            results[BP][scenario] = {}
            for model_spec in model_specs[scenario]:

                line_nrs = []
                parameters[BP][scenario][model_spec] = []

                file_path = files[BP][scenario][model_spec]
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    
                    for n, line in enumerate(lines):
                        columns = line.split()
                        if len(columns) < 2:
                            continue
                        
                        if columns[1] == "Observable":
                            parameter = columns[2][1:-2]
                            # print(f"Found parameter: {parameter} in file {file_path} at line {n}")
                            if parameter == "deltalHHH_HLLHC":
                                parameters[BP][scenario][model_spec].append(parameter)
                                line_nrs.append(n)

                    results[BP][scenario][model_spec] = []
                    print(f"Reading results for {BP}, scenario: {scenario}, model spec: {model_spec}")
                    for line_nr, par in zip(line_nrs, parameters[BP][scenario][model_spec]):
                    
                        columns = lines[line_nr + 1].split()
                        means_uncertainties = [float(columns[3]),    # Mean
                                               float(columns[5]),]   # Uncertainty

                        results[BP][scenario][model_spec].append(means_uncertainties)

                results[BP][scenario][model_spec] = np.array(results[BP][scenario][model_spec])


    # print(f"\nParameter dictionary: \n{parameters}")
    # print(f"\nResults dictionary: \n{results}")

    for scenario in scenarios:
        for model_spec, results_dir in zip(model_specs[scenario], results_dirs):
            output_file = f"{working_dir}/comparison_plots/results_{results_dir}/klam_results_{scenario}.txt"
            with open(output_file, 'w') as f:
                print(f"Writing results to {output_file}")
                print(f"BP,klam,error", file=f)
                for BP in BPs:
                    if BP not in results or scenario not in results[BP] or model_spec not in results[BP][scenario]:
                        print(f"Skipping {BP}, {scenario}, {model_spec} as results are missing.")
                        continue
                    
                    klams = results[BP][scenario][model_spec][:, 0]
                    errors = results[BP][scenario][model_spec][:, 1]

                    for k, e in zip(klams, errors):
                        print(f"{BP},{k+1},{e}", file=f)

def generate_klam_comparison_plot(
    BPs,
    model_specs,
    working_dir,
    results_dirs,
    BP_names,
    BP_lambdas,
    model,
    plot_labels=None,
    plot_titles=None,
    colors=[],
    show_plots=False,
    figsize=(3.5, 4),
    fig_kwargs={},
):
    r"""
    Compare the fit results for kappa_lambda between the benchmark points

    Parameters
    ----------
    BPs : list of str
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping collider scenarios to model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    results_dirs : list of str
        List of suffixes for the result directories. For each {results_dir} in this list,
        the corresponding results will be stored in the directory
        '{working_dir}/comparison_plots/results_{results_dir}/'
    BP_names : list of str
        List with the names for the benchmark point, used in plots.
    BP_lambdas : list of float
        List of the corresponding BSM model prediction for kappa_lambda for each BP.
    model : str
        The BSM model considered. Currently can be either "IDM" or "Z2SSM"
    plot_labels : list of str
        List with the labels for each model benchmark point. Must have the same length as 
        the BP_names and BP_lambdas lists. If not set, labels will default to the 
        "{BP_name} $(\kappa_\lambda={klam})$" format, where "klam" is the corresponding
        prediction for kappa_lambda.
    plot_titles : dict, optional
        A dictionary in the form plot_titles[scenario][model_spec] containing the titles 
        for the plots. If not provided, no title is shown.
    colors : list, optional
        List of colors assign to each model specification. If set to
        an empty list, the default matplotlib color cycle will be used.
    show_plots : bool, optional
        Whether to show the plots or not. Default is False.
    figsize : tuple, optional
        Size for the generated plot. Default is (3.5, 4).
    fig_kwargs : dict, optional
        Additional keyword arguments for the figure.
    

    Returns
    -------
    None

    """

    scenarios = model_specs.keys()
    
    if colors == []:
        # Default matplotlib color cycle
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    if plot_labels is None:
        plot_labels = [ rf"{BP_name} $(\kappa_\lambda={klam:.3g})$" for BP_name, klam in zip(BP_names, BP_lambdas) ]

    if model not in ["IDM", "Z2SSM"]:
        raise ValueError(f"Invalid model specified ({model}). Please choose either 'IDM' or 'Z2SSM'.")
    
    # Create the output directories, if they do not yet exist
    for results_dir in results_dirs:
        subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])

    # files = [working_dir + file_dir + f"/results_{model_specs}/Observables/Statistics.txt" for file_dir in scenarios]
    files = {}
    for BP in BPs:
        files[BP] = {}
        for scenario in scenarios:
            files[BP][scenario] = {}
            for model_spec in model_specs[scenario]:
                files[BP][scenario][model_spec] = f"{working_dir}/{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"

    
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
                    
    for scenario in scenarios:
        for model_spec, results_dir in zip(model_specs[scenario], results_dirs):                
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=figsize, height_ratios=[0.7, 0.3], gridspec_kw=dict(hspace=0.), **fig_kwargs)

            means  = {BP : kappa_lambda_results[BP][scenario][model_spec][0] for BP in BPs}
            errors = {BP : kappa_lambda_results[BP][scenario][model_spec][1] for BP in BPs}
            for i, BP in enumerate(BPs):
                ax1.errorbar(x=BP_lambdas[i],
                            y=means[BP],
                            yerr=(errors[BP],), 
                            fmt='o', 
                            linewidth=1.5, 
                            capsize=3.5, 
                            markersize=4, 
                            label=plot_labels[i],
                            color=colors[i])
                
                ax2.errorbar(x=BP_lambdas[i],
                            y=means[BP] - BP_lambdas[i],
                            yerr=(errors[BP],), 
                            fmt='o', 
                            linewidth=1.5, 
                            capsize=3.5, 
                            markersize=4, 
                            color=colors[i])
                
            plt.axhline(y=0, c='0.6', linewidth=1)

            # ax2.tick_params(axis='x', size=10, labelsize=12)
            # ax2.tick_params(axis='x', which='minor', size=6)

            # ax1.set_yticks(BP_lambdas)
            # ax2.set_xticks(BP_lambdas)
            # ax2.set_xticklabels(BP_lambdas,fontsize=16)
            # ax1.set_xlim(2.0, 5.0)
            # ax2.set_ylim(-0.9, 0.9)
                
            ax1.set_ylabel(r'$\kappa_{\lambda}^\text{fit}$', fontsize=15)
            ax2.set_ylabel(r'$\kappa_{\lambda}^\text{fit} - \kappa_{\lambda}^\text{true}$', fontsize=15)

            ax2.set_xlabel(r'$\kappa_{\lambda}^\text{true}$', fontsize=15)

            ax1.grid(which='both', linestyle='--', linewidth=0.5)
            ax2.grid(which='both', linestyle='--', linewidth=0.5)
            ax1.legend(loc='best', fontsize=9)

            if plot_titles is not None and scenario in plot_titles and model_spec in plot_titles[scenario]:
                ax1.set_title(plot_titles[scenario][model_spec], fontsize=10)
            plt.tight_layout()   # Makes sure labels are not cut off

            plt.savefig(working_dir + f'/comparison_plots/results_{results_dir}/kappa_lambda_results_{scenario}.pdf')

    if show_plots:
        plt.show()

def compare_BP_results_uproot(
    BPs,
    model_specs,
    working_dir,
    results_dir,
    spec_labels,
    BP_names,
    BP_lambdas,
    model,
    scenario_titles=None,
    plot_titles=None,
    colors=[],
    show_plots=False,
    legend_fontsize=8.,
):
    """
    Compare the posterior kappa_lambda distribution between different model specifications.
    The distributions are read from the MCout.root files with the uproot package. The function 
    generates comparison plots between the model_specs, as well as a summary latex table.

    Parameters
    ----------
    BPs : list of str
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping collider scenarios to model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    results_dir : str
        Suffix of the name of the directory to store the results. Results are stored in
        '{working_dir}/comparison_plots/results_{results_dir}/'.
    spec_labels : list of str
        List with the labels for each model specification. Must have the same length as the
        model_specs[scenario] lists, for each collider scenario.
    BP_names : list of str
        List with the names for the benchmark point, used in plots.
    BP_lambda : list of float
        List of the corresponding BSM model prediction for kappa_lambda for each BP.
    model : str
        The BSM model considered. Currently can be either "IDM" or "Z2SSM"
    scenario_titles : list, optional
        A list containing the titles for the scenarios. If not provided, default titles 
        will be used.
    plot_titles : dict, optional
        A dictionary in the form plot_titles[BP][scenario] containing the titles for 
        the plots. If not provided, the format "<model> <BP_name>, <scenario_title>"
        will be used.
    colors : list, optional
        List of colors assign to each model specification. If set to
        an empty list, the default matplotlib color cycle will be used.
    show_plots : bool, optional
        Whether to show the plots or not. Default is False.
    legend_fontsize : float, optional
        Font size for the legend. Default is 8.

    Returns
    -------
    None

    """

    scenarios = model_specs.keys()

    # Deal with optional arguments
    if colors == []:
        # Default matplotlib color cycle
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    colors_rgb_list = [ matplotlib.colors.to_rgb(c) for c in colors ]
    # print(colors_rgb_list)

    if model not in ["IDM", "Z2SSM"]:
        raise ValueError(f"Invalid model specified ({model}). Please choose either 'IDM' or 'Z2SSM'.")
    
    if scenario_titles is None:
        for scenario in scenarios:
            if scenario == f"{model}_FCCee240":
                scenario_titles = [rf"FCC-ee$_{{240}}$"]
            elif scenario == f"{model}_FCCee240_FCCee365":
                scenario_titles = [rf"FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$"]
            elif scenario == f"{model}_FCCee240_FCCee365_HLLHClambda":
                scenario_titles = [rf"FCC-ee$_{{240}}$ + FCC-ee$_{{365}}$ + $\kappa_{{\lambda}}$ at HL-LHC"]

    if plot_titles is None:
        plot_titles = {BP: {scenario: rf"{model} {BP_name}, {scenario_title}" for scenario_title in scenario_titles} for BP, BP_name in zip(BPs, BP_names)}


    # Create the output directory, if it does not yet exist
    subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])

    fig_num = 0
    for scenario in scenarios:
        for BP, BP_name, BP_lambda in zip(BPs, BP_names, BP_lambdas):

            # BP_lambda = BP_lambdas[BP]
            fig = plt.figure(fig_num, figsize=(4.0, 3.5))
            fig_num += 1
            ax = plt.gca()
            ax.set_title(plot_titles[BP][scenario])
            ax.set_xlabel(r"$\kappa_{\lambda}$", fontsize=14)
            ax.set_ylabel("Posterior distribution", fontsize=12)

            for spec, label, color_rgb in zip(model_specs[scenario], spec_labels, colors_rgb_list):

                # Open the ROOT file
                if BP == "BP_lambda1" and spec == "fits_realistic_HL_LHC_WFR_kala2_input_all_all_EW_mods_small_priors_long":
                    file_path = f"{working_dir}/{BP}/{scenario}/results_{spec[:-5]}_strict/MCout.root"
                else:
                    file_path = f"{working_dir}/{BP}/{scenario}/results_{spec}/MCout.root"
                with uproot.open(file_path) as file:

                    hist_lmbd_y, hist_lmbd_x = file["deltalHHH_HLLHC"].to_numpy()
                    hist_lmbd_x = hist_lmbd_x + 1 
                    plt.hist(hist_lmbd_x[:-1], hist_lmbd_x, weights=hist_lmbd_y, label=label, density=True, histtype="step", edgecolor=(*color_rgb, 1.0), facecolor=(*color_rgb, 0.5), linewidth=1.5, fill=True)

            scale = 1.2
            ylow, yhigh = ax.get_ylim()
            ax.set_ylim(ylow, yhigh + (scale-1)*(yhigh-ylow))

            plt.axvline(BP_lambda, color="black", linestyle="--", label=rf"{model} {BP_name} value"+"\n"+rf"($\kappa_{{\lambda}}$ = {BP_lambda:.2f})")
            plt.legend(fontsize=legend_fontsize, loc="best")
            plt.tight_layout()
            plt.savefig(f"{working_dir}/comparison_plots/results_{results_dir}/IDM_{BP}_{scenario}_final.pdf")

    if show_plots:
        plt.show()


    obs_list = ["deltalHHH_HLLHC",]
    obs_tex_list = [r"$\kappa_{\lambda}$",]
    

    files = {}
    for BP in BPs:
        files[BP] = {}
        for scenario in scenarios:
            files[BP][scenario] = {}
            for model_spec in model_specs[scenario]:
                if BP == "BP_lambda1" and model_spec == "fits_realistic_HL_LHC_WFR_kala2_input_all_all_EW_mods_small_priors_long":
                    files[BP][scenario][model_spec] = f"{working_dir}/{BP}/{scenario}/results_{model_spec[:-5]}_strict/Observables/Statistics.txt"
                else:
                    files[BP][scenario][model_spec] = f"{working_dir}/{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"


    print(f"Reading fit results")
    results = {}
    observables = {}
    observables_tex = {}
    central_values_obs = {}

    for BP, BP_lambda in zip(BPs, BP_lambdas):

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
                central_values_obs[BP][scenario][model_spec] = [BP_lambda,]

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

                        # print(f"Line numbers: {line_nrs}")

                        if any(np.isnan(line_nrs)):
                            print(f"Missing observable: {observables[BP][scenario][model_spec][line_nrs.index(np.nan)]}")
                            raise ValueError(f"Not all observables were found in the file {file_path}!")

                        results[BP][scenario][model_spec] = []
                        # print(BP)

                        for line_nr, obs in zip(line_nrs, observables[BP][scenario][model_spec]):
                        
                            columns = lines[line_nr + 1].split()
                            if obs == "deltalHHH_HLLHC":
                                results[BP][scenario][model_spec].append([float(columns[3])+1,  # Mean
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

    print(f"\n\n")
    print(f"Aligned observables: {aligned_observables[BP][scenario]}")
    print(f"Aligned observables (LaTeX): {aligned_observables_tex[BP][scenario]}")
    print(f"Central values shape: {central_values_obs[BP][scenario][model_spec].shape}")
    print(f"results shape: {results[BP][scenario][model_spec].shape}")
    # print(f"results: {results}")
    print("\n")



    table_tex_output_file = working_dir + f'/comparison_plots/results_{results_dir}/klam_results.tex'
    headers = ["", "True value",] + spec_labels
    columns = BP_names
    # table_text = "\\hline\n" + " & ".join(headers) + "\\\\\n"
    table_text = " & ".join(headers) + "\\\\\n"
    table_text += "\\hline"
    for idx, (column, BP, BP_lambda) in enumerate(zip(columns, BPs, BP_lambdas)):
        table_text += "\\hline\n"
        table_text += f"{column} & {BP_lambda:.3g}"
        for model_spec in model_specs[scenario]:
            klam = results[BP][scenario][model_spec][0,0]
            klam_err_abs = results[BP][scenario][model_spec][0,1]
            klam_err_rel = klam_err_abs / klam
            table_text += rf" & ${klam:.2f}\pm{klam_err_abs:.2f}\;[\textcolor{{violet}}{{{100*klam_err_rel:.2g}\%}}]$"
        table_text += "\\\\"

    with open(table_tex_output_file, "w") as out_file:
        print_to_file("\\begin{tabular}{c||c|c|c}", file=out_file)
        print_to_file(table_text, file=out_file)
        print_to_file("\\end{tabular}", file=out_file)
        # print("\\hline\n\\end{tabular}", file=out_file)

    print(f"Saved summary latex table onto file {table_tex_output_file}")
