import numpy as np
from matplotlib import pyplot as plt
import subprocess
from .parser import observable_order, parameter_order, find_configuration_files, read_configuration_files, read_fit_results, align_observables


def generate_pull_plots_pars(
    BPs,
    model_specs,
    working_dir,
    results_dir,
    model_specs_labels,
    plot_titles,
    model,
    colors=None,
    show_plots=False,
    nvar_per_plot=15,
    figsize=(5, 7),
):
    """
    Generate pull plots for the model parameters.

    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    model_specs : dict
        Dictionary mapping scenarios to a list of model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    results_dir : str
        Suffix of the name of the directory to store the results. Results are stored in
        '{working_dir}/comparison_plots/results_{results_dir}/'
    plot_titles : dict
        A dictionary containing the titles for the plots.
    model : str
        The BSM model considered. Currently can be either "IDM" or "Z2SSM"
    results_dir : str
        Suffix of the name of the directory to store the results. Results are stored in
        '{working_dir}/comparison_plots/results_{results_dir}/'
    colors : list, optional
        List of colors assign to each model specification. If not set, the default 
        matplotlib color cycle will be used.
    show_plots : bool, optional
        Whether to show the plots or not. Default is False.
    nvar_per_plot : int, optional
        The number of variables per plot. Default is 15.

    Returns
    -------
    None

    """

    scenarios = model_specs.keys()

    if colors is None:
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


    print("\nFinding configuration files for the observables")
    conf_files = find_configuration_files(model_specs, model, read_WCs=True)
        
    print(f"\nReading configuration files for observables")
    parameters, parameters_tex, central_values_obs = read_configuration_files(
        working_dir,
        BPs,
        model_specs,
        conf_files,
        only_obs=None,
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

    print(f"\nSorting observables")
    aligned_parameters, aligned_parameters_tex, central_values_obs, results = align_observables(
        observable_order_func=parameter_order,
        BPs=BPs,
        model_specs=model_specs,
        observables=parameters,
        observables_tex=parameters_tex,
        central_values_obs=central_values_obs,
        results=results,
    )

    n_model_specs = len(list(model_specs.values())[0])
    w = 1.0
    dimw = w / 2
    y_shift = np.linspace(+dimw/2, -dimw/2, n_model_specs) 

    print(f"\n")
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

            for model_spec in model_specs[scenario]:
                results[BP][scenario][model_spec][:,0] = np.copy((results[BP][scenario][model_spec][:,0] - central_values_obs[BP][scenario][model_spec]) / results[BP][scenario][model_spec][:,1] )
                results[BP][scenario][model_spec][:,1] = np.copy( results[BP][scenario][model_spec][:,1] / results[BP][scenario][model_spec][:,1] )

            for k in range(len(param_breaks) - 1):

                fig = plt.figure(num_fig, figsize=figsize)
                num_fig = num_fig + 1
                ax = plt.gca()

                y = np.arange(param_breaks[k],param_breaks[k+1])
                
                plt.axvline(x=0, c='0.6', linewidth=2)

                for spec_index, model_spec in enumerate(model_specs[scenario]):
                    ax.errorbar(results[BP][scenario][model_spec][param_breaks[k]:param_breaks[k+1], 0],
                                -y-y_shift[spec_index], 
                                # -y, 
                                xerr=(results[BP][scenario][model_spec][param_breaks[k]:param_breaks[k+1], 1],), 
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





def generate_pull_plots_obs(
    BPs,
    model_specs,
    working_dir,
    results_dir,
    model_specs_labels,
    plot_titles,
    model,
    only_obs=None,
    skip_obs=None,
    colors=None,
    show_plots=False,
    nvar_per_plot=50,
    only_higgs_fccee_obs=False,
    compare_with_SM=False,
    figsize=(5, 7),
):
    """
    Generate pull plots for the fit observables.
    
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
    only_obs : list, optional
        List of observables to include. If set, only these observables will be
        processed.
    skip_obs : list of str, optional
        A list of observables to skip (i.e., not show in the plots). 
        Default is an empty list.
    colors : list, optional
        List of colors assign to each model specification. If not set, the 
        default matplotlib color cycle will be used.
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

    if colors is None:
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


    print("\nFinding configuration files for the observables")
    conf_files = find_configuration_files(model_specs, model)
        
    print(f"\nReading configuration files for observables")
    observables, observables_tex, central_values_obs = read_configuration_files(
        working_dir=working_dir,
        BPs=BPs,
        model_specs=model_specs,
        conf_files=conf_files,
        only_obs=only_obs,
        skip_obs=skip_obs,
        only_higgs_fccee_obs=only_higgs_fccee_obs,
        read_model_parameters=False,
        compare_with_SM=compare_with_SM,
    )

    print(f"\nReading fit results")
    results = read_fit_results(
        BPs=BPs,
        model_specs=model_specs,
        observables=observables,
        files=files,
    )

    print(f"\nSorting observables")
    aligned_observables, aligned_observables_tex, central_values_obs, results = align_observables(
        observable_order_func=observable_order,
        BPs=BPs,
        model_specs=model_specs,
        observables=observables,
        observables_tex=observables_tex,
        central_values_obs=central_values_obs,
        results=results,
    )

    n_model_specs = len(list(model_specs.values())[0])
    w = 1.0
    dimw = w / 2
    y_shift = np.linspace(+dimw/2, -dimw/2, n_model_specs) 

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
                fig = plt.figure(fig_num, figsize=figsize)
                fig_num = fig_num + 1
                ax = plt.gca()

                for spec_index, model_spec in enumerate(model_specs[scenario]):

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