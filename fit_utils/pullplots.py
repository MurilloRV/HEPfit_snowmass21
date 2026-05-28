import numpy as np
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import subprocess
from copy import deepcopy
from .parser import (
    observable_order, 
    parameter_order, 
    find_configuration_files, 
    read_configuration_files, 
    read_fit_results, 
    read_fit_results_pars, 
    align_observables,
    read_fit_results_dim6Ops_correlations,
    find_tex_label_par,
    read_WC_predictions,
)




def generate_bar_plots_pars(
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
    legend_loc="best",
    file_suffix="",
    log_scale=True,
    x_range_min=None,
    x_range_max=None,
    save_fig=True,
):
    """
    Generate bar plots with the absolute values of the fitted model parameters 
    (i.e., the Wilson coefficients). 

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
    model_specs_labels : dict
        A dictionary containing the labels for the model specifications.
    plot_titles : dict
        A dictionary containing the titles for the plots.
    model : str
        The BSM model considered. Currently can be either "IDM" or "Z2SSM"
    colors : list, optional
        List of colors assign to each model specification. If not set, the default 
        matplotlib color cycle will be used.
    show_plots : bool, optional
        Whether to show the plots or not. Default is False.
    nvar_per_plot : int, optional
        The number of variables per plot. Default is 15.
    figsize : tuple, optional
        Figure size for the plots. Default is (5, 7).
    legend_loc : str, optional
        Location of the legend in the plots. Default is "best".
    file_suffix : str, optional
        Suffix to add to the plot filenames. Default is an empty string.
    log_scale : bool, optional
        Whether to use a logarithmic scale for the x-axis. Default is True.
    x_range_min : float, optional
        Minimum value for the x-axis range. If None (default), it will be determined automatically.
    x_range_max : float, optional
        Maximum value for the x-axis range. If None (default), it will be determined automatically.
    save_fig : bool, optional
        Whether to save the figures. Default is True.

    Returns
    -------
    None

    """


    if colors is None:
        # Default matplotlib color cycle
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Create the output directory, if it does not yet exist
    subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])

    scenarios = model_specs.keys()

    parameters, parameters_tex, central_values_obs, results = read_fit_results_pars(
        BPs,
        model_specs,
        working_dir,
        scenarios,
        model,
    )

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
    bar_height = dimw / n_model_specs
    if n_model_specs > 1:
        y_shift = np.linspace(+dimw/2, -dimw/2, n_model_specs) 
    else:
        y_shift = np.array([0])

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
                results[BP][scenario][model_spec][:,0] = np.copy(np.abs(results[BP][scenario][model_spec][:,0]))
                results[BP][scenario][model_spec][:,1] = np.copy(results[BP][scenario][model_spec][:,1])

            for k in range(len(param_breaks) - 1):

                fig = plt.figure(num_fig, figsize=figsize)
                num_fig = num_fig + 1
                ax = plt.gca()

                y = np.arange(param_breaks[k],param_breaks[k+1])
                
                plt.axvline(x=0, c='0.6', linewidth=2)

                for spec_index, model_spec in enumerate(model_specs[scenario]):
                    ax.barh(
                        y = -y+y_shift[spec_index], 
                        width = results[BP][scenario][model_spec][param_breaks[k]:param_breaks[k+1], 0],
                        height = bar_height,
                        # xerr = (results[BP][scenario][model_spec][param_breaks[k]:param_breaks[k+1], 1],), 
                        color=colors[spec_index],
                        label=model_specs_labels[scenario][spec_index],
                        # alpha=alphas[i],
                    )

                ax.set_xscale('log' if log_scale else 'linear')
                    
                # ax.set_yticks(-y-dimw/2.)
                ax.set_yticks(-y)
                y_label_size = min( 250. / (param_breaks[k+1] - param_breaks[k]), 13)
                ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]], fontsize=y_label_size)
                x_limits = [
                    x_range_min if not x_range_min is None else plt.xlim()[0], 
                    x_range_max if not x_range_max is None else plt.xlim()[1], 
                ]
                ax.hlines(y=-y, xmin=x_limits[0], xmax=x_limits[1], color="black", linestyle="--", linewidth=0.5)
                ax.set_xlim(*x_limits)
                ax.tick_params(axis='x', size=10, labelsize=11)
                ax.tick_params(axis='x', which='minor', size=6)
                x_label = r'Absolute value of Wilson coefficients'
                ax.set_xlabel(x_label, fontsize=10)
                ax.legend(loc=legend_loc, fontsize=10)
                ax.set_title(plot_titles[BP][scenario], fontsize=10)
                plt.tight_layout()   # Makes sure labels are not cut off
                if save_fig: plt.savefig(f"{working_dir}/comparison_plots/results_{results_dir}/bar_plot_pars_{BP}_{scenario}_compare_{k}{file_suffix}.pdf")

    if show_plots:
        plt.show()



def generate_WCs_vs_klam_plot(
    BPs,
    BP_lambdas,
    model_specs,
    working_dir,
    results_dirs,
    plot_titles,
    model,
    WC_names=["CH",],
    WC_scale_factors=[None,],
    colors=None,
    show_plots=False,
    figsize=(4, 3),
    legend_fontsize=7,
    file_suffix="",
    log_scale=False,
    save_fig=True,
):
    """
    Generate bar plots with the absolute values of the fitted model parameters 
    (i.e., the Wilson coefficients). 

    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    BP_lambdas : list
        List of the values of kappa_lambda for each benchmark point. Must be in the same 
        order as the BPs list.
    model_specs : dict
        Dictionary mapping scenarios to a list of model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    results_dirs : list
        List of suffixes for the names of the directories to store the results. Results are stored in
        '{working_dir}/comparison_plots/results_{results_dir}/', for each results_dir in results_dirs. 
        Must be in the same order as the model specifications in model_specs.
    plot_titles : dict
        A dictionary containing the titles for the plots.
    model : str
        The BSM model considered. Currently can be either "IDM" or "Z2SSM"
    WC_names : list, optional
        List of Wilson coefficient names to include in the plots. Default is "CH"
    WC_scale_factors : list, optional
        List of scale factors to apply to the Wilson coefficients. Default is None for all WCs 
        (i.e., no scaling).
    colors : list, optional
        List of colors assign to each Wilson coefficient. If not set, the default matplotlib 
        color cycle will be used.
    show_plots : bool, optional
        Whether to show the plots or not. Default is False.
    figsize : tuple, optional
        Figure size for the plots. Default is (5, 7).
    legend_fontsize : int, optional
        Font size for the legend in the plots. Default is 7.
    file_suffix : str, optional
        Suffix to add to the plot filenames. Default is an empty string.
    log_scale : bool, optional
        Whether to use a logarithmic scale for the x-axis. Default is False.
    save_fig : bool, optional
        Whether to save the figures. Default is True.

    Returns
    -------
    None

    """

    n_WCs = len(WC_names)
    if n_WCs != len(WC_scale_factors) or (colors is not None and n_WCs != len(colors)):
        raise ValueError(
            f"""
            Length of WC_names, WC_scale_factors, and colors must be the same
            Length of WC_names: {n_WCs}
            Length of WC_scale_factors: {len(WC_scale_factors)}
            Length of colors: {len(colors) if colors is not None else 0}
            """
        )

    WC_names = [WC + "_corr" for WC in WC_names]  # Add the suffix "_corr" to the WC names, as this is how they are stored in the fit results


    if colors is None:
        # Default matplotlib color cycle
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    scenarios = model_specs.keys()

    parameters, parameters_tex, central_values_obs, results = read_fit_results_pars(
        BPs,
        model_specs,
        working_dir,
        scenarios,
        model,
        only_pars=WC_names,
    )

    WC_order = {WC: i for i, WC in enumerate(WC_names)}
    WC_order_func = lambda obs: WC_order[obs] if obs in WC_order else len(WC_names)  
    # Order function for the WCs, which will be used to sort the observables. WCs not in WC_names will be sorted at the end, in their original order.

    print(f"\nSorting observables")
    aligned_parameters, aligned_parameters_tex, central_values_obs, results = align_observables(
        observable_order_func=WC_order_func,
        BPs=BPs,
        model_specs=model_specs,
        observables=parameters,
        observables_tex=parameters_tex,
        central_values_obs=central_values_obs,
        results=results,
    )


    print(f"\n")
    num_fig = 0
    for scenario in scenarios:
        for spec_index, (model_spec, results_dir) in enumerate(zip(model_specs[scenario], results_dirs)):

            print(f"\nProducing plot for scenario {scenario}, model specification {model_spec}")
            print(f"Total number of WCs considered for the plot: {n_WCs}")
            print(f"WCs considered for the plot: {WC_names}")

            # Create the output directory, if it does not yet exist
            subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])

            for BP in BPs:
                if aligned_parameters[BP][scenario] != WC_names:
                    raise ValueError(f"WC_names does not match the WCs present in the fit results for BP {BP}, scenario {scenario}.")

            labels = aligned_parameters_tex[BP][scenario][:]

            fig = plt.figure(num_fig, figsize=figsize)
            num_fig = num_fig + 1
            ax = plt.gca()
            plt.axhline(y=0, c='0.1', linewidth=1)

            for k, (wc_name, wc_scale, label, color) in enumerate(zip(WC_names, WC_scale_factors, labels, colors)):


                if wc_scale is not None:
                    label = fr"${wc_scale}\cdot$ {label}"

                if wc_scale is None: wc_scale = 1
                y = [results[BP][scenario][model_spec][k,0] * wc_scale for BP in BPs]

                ax.plot(
                    BP_lambdas,
                    y, 
                    'o-',
                    color=color,
                    label=label,
                )

            ax.set_xscale('log' if log_scale else 'linear')                                    
            ax.set_xlabel(r'$\kappa_\lambda$', fontsize=12)
            ax.set_ylabel(r'Fitted Wilson coefficients', fontsize=10)
            ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=legend_fontsize)
            # ax.set_title(plot_titles[BP][scenario], fontsize=10)
            plt.tight_layout()   # Makes sure labels are not cut off
            if save_fig: plt.savefig(f"{working_dir}/comparison_plots/results_{results_dir}/WCs_vs_klam_{scenario}_{file_suffix}.pdf")

    if show_plots:
        plt.show()


def generate_WC_correlations_vs_klam_plot(
    BPs,
    BP_lambdas,
    model_specs,
    working_dir,
    results_dirs,
    WC_pairs=[["CH", "CuH_33r"], ],
    colors=None,
    show_plots=False,
    figsize=(4, 3),
    legend_fontsize=7,
    file_suffix="",
    log_scale=False,
    save_fig=True,
):
    """
    Generate bar plots with the absolute values of the fitted model parameters 
    (i.e., the Wilson coefficients). 

    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    BP_lambdas : list
        List of the values of kappa_lambda for each benchmark point. Must be in the same 
        order as the BPs list.
    model_specs : dict
        Dictionary mapping scenarios to a list of model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    results_dirs : list
        List of suffixes for the names of the directories to store the results. Results are stored in
        '{working_dir}/comparison_plots/results_{results_dir}/', for each results_dir in results_dirs. 
        Must be in the same order as the model specifications in model_specs.
    WC_pairs : list, optional
        List of pairs of Wilson coefficient names to include in the plots. Default is [["CH", "CuH_33r"], ]
    colors : list, optional
        List of colors assign to each Wilson coefficient. If not set, the default matplotlib 
        color cycle will be used.
    show_plots : bool, optional
        Whether to show the plots or not. Default is False.
    figsize : tuple, optional
        Figure size for the plots. Default is (5, 7).
    legend_fontsize : int, optional
        Font size for the legend in the plots. Default is 7.
    file_suffix : str, optional
        Suffix to add to the plot filenames. Default is an empty string.
    log_scale : bool, optional
        Whether to use a logarithmic scale for the x-axis. Default is False.
    save_fig : bool, optional
        Whether to save the figures. Default is True.

    Returns
    -------
    None

    """

    n_WC_pairs = len(WC_pairs)
    scenarios = list(model_specs.keys())

    correlation_matrices, observables = read_fit_results_dim6Ops_correlations(
        BPs=BPs,
        model_specs=model_specs,
        files=None,
        working_dir=working_dir,
        assert_equal_observables=True,
    )

    # The "assert_equal_observables" option above ensures that all lists of observables are equal 
    # between BPs, scenarios and model specs, so we can safely take the list of observables for 
    # the first ones
    observables = observables[BPs[0]][scenarios[0]][model_specs[scenarios[0]][0]]
    observables_tex = [find_tex_label_par(None, obs[:-5]) for obs in observables]

    if colors is None:
        # Default matplotlib color cycle
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']


    print(f"\n")
    num_fig = 0
    for scenario in scenarios:
        for spec_index, (model_spec, results_dir) in enumerate(zip(model_specs[scenario], results_dirs)):

            print(f"\nProducing plot for scenario {scenario}, model specification {model_spec}")
            print(f"Total number of WCs considered for the plot: {n_WC_pairs}")
            print(f"WCs pairs considered for the plot: {WC_pairs}")

            # Create the output directory, if it does not yet exist
            subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])

            fig = plt.figure(num_fig, figsize=figsize)
            num_fig = num_fig + 1
            ax = plt.gca()
            plt.axhline(y=0, c='0.1', linewidth=1)

            for k, (wc_pair, color) in enumerate(zip(WC_pairs, colors)):


                wc_pair_indices = [
                    observables.index(wc_pair[0] + "_corr"), 
                    observables.index(wc_pair[1] + "_corr"),
                ]

                y = [correlation_matrices[BP][scenario][model_spec][wc_pair_indices[0], wc_pair_indices[1]] for BP in BPs]

                label = fr"$\rho(${observables_tex[wc_pair_indices[0]]}, {observables_tex[wc_pair_indices[1]]}$)$"

                ax.plot(
                    BP_lambdas,
                    y, 
                    'o-',
                    color=color,
                    label=label,
                )

            ax.set_xscale('log' if log_scale else 'linear')                                    
            ax.set_xlabel(r'$\kappa_\lambda$', fontsize=12)
            ax.set_ylabel(r'Fitted Wilson coef. correlations', fontsize=10)
            ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=legend_fontsize)
            plt.tight_layout()   # Makes sure labels are not cut off
            if save_fig: plt.savefig(f"{working_dir}/comparison_plots/results_{results_dir}/WC_correlations_vs_klam_{scenario}{file_suffix}.pdf")

    if show_plots:
        plt.show()


def generate_WC_corr_matrix_plot(
    BPs,
    model_specs,
    working_dir,
    results_dirs,
    WC_names=None,
    plot_titles=None,
    show_plots=False,
    figsize=(4, 3),
    file_suffix="",
    labelsize=12,
    save_fig=True,
):
    """
    Generate bar plots with the absolute values of the fitted model parameters 
    (i.e., the Wilson coefficients). 

    Parameters
    ----------
    BPs : list
        List of benchmark point names. Must correspond to the directory name for the BP
    BP_lambdas : list
        List of the values of kappa_lambda for each benchmark point. Must be in the same 
        order as the BPs list.
    model_specs : dict
        Dictionary mapping scenarios to a list of model specifications.
    working_dir : str
        Working directory path, containing subdirectories for each benchmark point.
    results_dirs : list
        List of suffixes for the names of the directories to store the results. Results are stored in
        '{working_dir}/comparison_plots/results_{results_dir}/', for each results_dir in results_dirs. 
        Must be in the same order as the model specifications in model_specs.
    WC_names : list, optional
        List of Wilson coefficient names to include in the plots. If not set, all available Wilson 
        coefficients will be included.
    show_plots : bool, optional
        Whether to show the plots or not. Default is False.
    figsize : tuple, optional
        Figure size for the plots. Default is (5, 7).
    file_suffix : str, optional
        Suffix to add to the plot filenames. Default is an empty string.
    labelsize : int, optional
        Size of the font for the axis labels. Default is 12.
    save_fig : bool, optional
        Whether to save the figures. Default is True.

    Returns
    -------
    None

    """

    correlation_matrices, observables = read_fit_results_dim6Ops_correlations(
        BPs=BPs,
        model_specs=model_specs,
        files=None,
        working_dir=working_dir,
        assert_equal_observables=True,
    )

   
    scenarios = list(model_specs.keys())

    # The "assert_equal_observables" option above ensures that all lists of observables are equal 
    # between BPs, scenarios and model specs, so we can safely take the list of observables for 
    # the first ones
    observables = observables[BPs[0]][scenarios[0]][model_specs[scenarios[0]][0]]

    observables_indices = [observables.index(WC + "_corr") for WC in WC_names] if not WC_names is None else range(len(observables))
    observables_tex = [find_tex_label_par(None, observables[i][:-5]) for i in observables_indices]

    if WC_names is None:
        WC_names = [observables[i][:-5] for i in observables_indices]
    
    n_WCs = len(WC_names)

    cmap = sns.color_palette("vlag", as_cmap=True)

    print(f"\n")
    num_fig = 0
    for scenario in scenarios:
        for spec_index, (model_spec, results_dir) in enumerate(zip(model_specs[scenario], results_dirs)):
            for BP in BPs:
                print(f"\nProducing plot for scenario {scenario}, model specification {model_spec}, BP {BP}")
                print(f"Total number of WCs considered for the plot: {n_WCs}")
                print(f"WCs considered for the plot: {WC_names}")

                # Create the output directory, if it does not yet exist
                subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])

                fig = plt.figure(num_fig, figsize=figsize)
                num_fig = num_fig + 1
                ax = plt.gca()

                # Restrict the matrix to WCs of interest
                corr_matrix = correlation_matrices[BP][scenario][model_spec][np.ix_(observables_indices, observables_indices)]
                corr_dataframe = pd.DataFrame(corr_matrix, index=observables_tex, columns=observables_tex)

                sns.heatmap(corr_dataframe, cmap=cmap, vmax=1., vmin=-1., center=0, square=True, linewidths=1., cbar_kws={"shrink": 1.0}, annot=True, fmt=".2f", ax=ax)

                ax.xaxis.set_tick_params(rotation=75, labelsize=labelsize)
                ax.yaxis.set_tick_params(labelsize=labelsize)

                if plot_titles is not None:
                    ax.set_title(f"{plot_titles[BP][scenario][model_spec]}", fontsize=14)
                plt.tight_layout()   # Makes sure labels are not cut off

                filename = f"{working_dir}/comparison_plots/results_{results_dir}/WC_corr_matrix_{scenario}_{BP}_{scenario}{file_suffix}.pdf"
                if save_fig: plt.savefig(filename)

    if show_plots:
        plt.show()



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
    legend_loc="best",
    normalize_pulls=True,
    true_values=None,
    file_suffix="",
    save_fig=True,
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
    model_specs_labels : dict
        A dictionary containing the labels for the model specifications.
    plot_titles : dict
        A dictionary containing the titles for the plots.
    model : str
        The BSM model considered. Currently can be either "IDM" or "Z2SSM"
    colors : list, optional
        List of colors assign to each model specification. If not set, the default 
        matplotlib color cycle will be used.
    show_plots : bool, optional
        Whether to show the plots or not. Default is False.
    nvar_per_plot : int, optional
        The number of variables per plot. Default is 15.
    figsize : tuple, optional
        Figure size for the plots. Default is (5, 7).
    legend_loc : str, optional
        Location of the legend in the plots. Default is "best".
    normalize_pulls : bool, optional
        If True, normalize the pulls to the uncertainties. Default is True.
    true_values : dict, optional
        A dictionary containing the true values of the Wilson coefficients for each BP
    file_suffix : str, optional
        Suffix to add to the plot filenames. Default is an empty string.
    save_fig : bool, optional
        Whether to save the figures. Default is True.

    Returns
    -------
    None

    """


    if colors is None:
        # Default matplotlib color cycle
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Create the output directory, if it does not yet exist
    subprocess.run(["mkdir", "-p", f"{working_dir}/comparison_plots/results_{results_dir}"])

    scenarios = model_specs.keys()

    parameters, parameters_tex, central_values_obs, results = read_fit_results_pars(
        BPs,
        model_specs,
        working_dir,
        scenarios,
        model,
    )

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
    if n_model_specs > 1:
        y_shift = np.linspace(+dimw/2, -dimw/2, n_model_specs) 
    else:
        y_shift = np.array([0])

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
                if true_values is None or true_values["subtract_true_values"] is False:
                    subtract_values = central_values_obs[BP][scenario][model_spec]
                else:
                    subtract_values = np.array([true_values['values'][WC[:-5]][i] for WC in aligned_parameters[BP][scenario]])
                    # print(f"Subtracting true values: {subtract_values}")

                if normalize_pulls:
                    results[BP][scenario][model_spec][:,0] = np.copy((results[BP][scenario][model_spec][:,0] - subtract_values) / results[BP][scenario][model_spec][:,1] )
                    results[BP][scenario][model_spec][:,1] = np.copy( results[BP][scenario][model_spec][:,1] / results[BP][scenario][model_spec][:,1] )
                else:
                    results[BP][scenario][model_spec][:,0] = np.copy(results[BP][scenario][model_spec][:,0] - subtract_values)
                    results[BP][scenario][model_spec][:,1] = np.copy(results[BP][scenario][model_spec][:,1])

            for k in range(len(param_breaks) - 1):

                fig = plt.figure(num_fig, figsize=figsize)
                num_fig = num_fig + 1
                ax = plt.gca()

                y = np.arange(param_breaks[k],param_breaks[k+1])
                
                plt.axvline(x=0, c='0.6', linewidth=2)

                for spec_index, model_spec in enumerate(model_specs[scenario]):
                    ax.errorbar(results[BP][scenario][model_spec][param_breaks[k]:param_breaks[k+1], 0],
                                -y+y_shift[spec_index], 
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
                    
                if true_values is not None:
                    if true_values['subtract_true_values'] is False:
                        for y_value in y:
                            WC = aligned_parameters[BP][scenario][y_value]
                            if normalize_pulls:
                                plotted_true_value = (true_values['values'][WC[:-5]][i] - central_values_obs[BP][scenario][model_specs[scenario][0]][y_value]) / results[BP][scenario][model_spec][y_value,1]
                            else:
                                plotted_true_value = true_values['values'][WC[:-5]][i]
                            ax.scatter(plotted_true_value, -y_value, **true_values['style'])
                    else: 
                        ax.scatter(np.zeros_like(y), -y, **true_values['style'])

                    ax.scatter([], [], label=true_values['label'], **true_values['style'])

                # ax.set_yticks(-y-dimw/2.)
                ax.set_yticks(-y)
                y_label_size = min( 250. / (param_breaks[k+1] - param_breaks[k]), 13)
                ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]], fontsize=y_label_size)
                x_limits = [plt.xlim()[0], plt.xlim()[1]]
                ax.hlines(y=-y, xmin=x_limits[0], xmax=x_limits[1], color="black", linestyle="--", linewidth=0.5)
                ax.set_xlim(*x_limits)
                ax.tick_params(axis='x', size=10, labelsize=11)
                ax.tick_params(axis='x', which='minor', size=6)
                if normalize_pulls:
                    x_label = r'Pulls'
                else:
                    x_label = r'Wilson coefficients'
                if true_values is not None and true_values['subtract_true_values'] is True:
                    x_label = x_label + f' (w.r.t. {true_values["label"]})'
                ax.set_xlabel(x_label, fontsize=11)
                ax.legend(loc=legend_loc, fontsize=10)
                ax.set_title(plot_titles[BP][scenario], fontsize=10)
                plt.tight_layout()   # Makes sure labels are not cut off
                if save_fig: plt.savefig(f"{working_dir}/comparison_plots/results_{results_dir}/pull_pars_{BP}_{scenario}_compare_{k}{file_suffix}.pdf")

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
    WC_list_for_prediction_pulls=None,
    matched_predictions_vs_BSM=False,
    BP_lambdas=None,
    figsize=(5, 7),
    legend_loc="best",
    file_suffix="",
    save_fig=True,
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
        The BSM model considered. Currently can be either "IDM" or "Z2SSM" or "SM"
    only_obs : list of str, optional
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
    WC_list_for_prediction_pulls: list of str, optional
        If set, the pulls in the plots will illustrate the deviation between
        the predictions for the given WC values and the SM predictions.This
        list should contain the names of the WCs to be included.
    matched_predictions_vs_BSM : bool, optional
        If True, this function will evaluate the pulls of the BSM model 
        predictions w.r.t. to the SMEFT predictions using matched Wilson coef.
    BP_lambdas : list of floats, optional
        List of predictions for kappa_lambda for each BP. If set, kappa_lambda will be added as an 
        observable with the corresponding central value for each BP. 
    figsize : tuple, optional
        Figure size for the plots. Default is (5, 7).
    legend_loc : str, optional
        Location of the legend in the plots. Default is "best".
    file_suffix: str, optional
        Suffix to add to the plot filenames. Default is an empty string.
    save_fig : bool, optional
        Whether to save the figures. Default is True.

    Returns
    -------
    None

    """

    scenarios = model_specs.keys()

    if colors is None:
        # Default matplotlib color cycle
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    if model not in ["IDM", "Z2SSM", "SM"]:
        raise ValueError(f"Invalid model specified ({model}). Please choose either 'IDM', 'Z2SSM', or 'SM'.")

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
    observables, observables_tex, central_values_obs, input_uncertainties = read_configuration_files(
        working_dir=working_dir,
        BPs=BPs,
        model_specs=model_specs,
        conf_files=conf_files,
        only_obs=only_obs,
        skip_obs=skip_obs,
        only_higgs_fccee_obs=only_higgs_fccee_obs,
        read_model_parameters=False,
        compare_with_SM=compare_with_SM,
        BP_lambdas=BP_lambdas,
    )

    print(f"\nReading fit results")
    if WC_list_for_prediction_pulls is not None:
        results = {}
        for BP in BPs:
            results[BP] = {}
            for scenario in scenarios:
                results[BP][scenario] = {}
                for model_spec in model_specs[scenario]:
                    results[BP][scenario][model_spec] = np.zeros((len(observables["Config_Files"]["."]['fits_small_priors_strict']), 2))
                    results[BP][scenario][model_spec] = np.array( 
                        [
                            central_values_obs["Config_Files"]["."]['fits_small_priors_strict'],
                            input_uncertainties["Config_Files"]["."]['fits_small_priors_strict'],
                        ] 
                    ).T
        WC_labels = [ find_tex_label_par(None, wc) for wc in WC_list_for_prediction_pulls ]
    
    elif matched_predictions_vs_BSM:
        results = {}
        for BP in BPs:
            results[BP] = {}
            for scenario in scenarios:
                results[BP][scenario] = {}
                for model_spec in model_specs[scenario]:
                    results[BP][scenario][model_spec] = np.array( 
                        [
                            central_values_obs[BP][scenario][model_spec],
                            input_uncertainties[BP][scenario][model_spec],
                        ] 
                    ).T

    else:
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

    if WC_list_for_prediction_pulls:
        obs_predictions = read_WC_predictions(
            working_dir=working_dir,
            WCs=WC_list_for_prediction_pulls,
            n_WC_values=2,
            observables=aligned_observables,
        )

        n_WCs = len(WC_list_for_prediction_pulls)
        y_shift = np.linspace(+dimw/2, -dimw/2, n_WCs) 
    
    elif matched_predictions_vs_BSM:
        obs_predictions = read_WC_predictions(
            working_dir=working_dir,
            WCs=BPs,
            n_WC_values=1,
            observables=aligned_observables,
            matched_predictions=True,
        )

        y_shift = np.linspace(+dimw/2, -dimw/2, n_model_specs) 

    else:
        y_shift = np.linspace(+dimw/2, -dimw/2, n_model_specs) 

    if len(y_shift) == 1:
        y_shift = np.array([0])


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

                y = np.arange(param_breaks[k],param_breaks[k+1])
                plt.axvline(x=0, c='0.6', linewidth=2)

                if WC_list_for_prediction_pulls is not None:
                    for i, wc in enumerate(WC_list_for_prediction_pulls):
                        plotted_results_low = deepcopy( (obs_predictions[wc][0] - results["Config_Files"]["."]['fits_small_priors_strict'][:,0])/results["Config_Files"]["."]['fits_small_priors_strict'][:,1] )
                        plotted_results_high = deepcopy( (obs_predictions[wc][1] - results["Config_Files"]["."]['fits_small_priors_strict'][:,0])/results["Config_Files"]["."]['fits_small_priors_strict'][:,1] )
                        ax.plot(
                            plotted_results_low[param_breaks[k]:param_breaks[k+1]],
                            -y+y_shift[i], 
                            linestyle="None",
                            marker=4, 
                            markersize=10,
                            color=colors[i],
                            label=WC_labels[i],
                        )

                        ax.plot(
                            plotted_results_high[param_breaks[k]:param_breaks[k+1]],
                            -y+y_shift[i], 
                            linestyle="None",
                            marker=5, 
                            markersize=10,
                            color=colors[i],
                        )

                    ax.plot([], [], marker=5, markersize=10, linestyle="None", color="black", label="$+1\sigma$")
                    ax.plot([], [], marker=4, markersize=10, linestyle="None", color="black", label="$-1\sigma$")

                elif matched_predictions_vs_BSM:
                    for spec_index, model_spec in enumerate(model_specs[scenario]):

                        results_means  = np.copy((obs_predictions[BP][0]  - results[BP][scenario][model_spec][:,0]) / results[BP][scenario][model_spec][:,1] )
                        results_errors = np.copy( results[BP][scenario][model_spec][:,1] / results[BP][scenario][model_spec][:,1] )

                        ax.errorbar(results_means[param_breaks[k]:param_breaks[k+1]],
                                    -y+y_shift[spec_index], 
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

                else:
                    for spec_index, model_spec in enumerate(model_specs[scenario]):

                        results_means  = np.copy((results[BP][scenario][model_spec][:,0] - central_values_obs[BP][scenario][model_spec]) / results[BP][scenario][model_spec][:,1] )
                        results_errors = np.copy( results[BP][scenario][model_spec][:,1] / results[BP][scenario][model_spec][:,1] )

                        ax.errorbar(results_means[param_breaks[k]:param_breaks[k+1]],
                                    -y+y_shift[spec_index], 
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
                y_label_size = min( 400. / (param_breaks[k+1] - param_breaks[k]), 13)
                ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]], fontsize=y_label_size)
                # ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]],fontsize=fontsize)
                x_limits = [plt.xlim()[0], plt.xlim()[1]]
                # y_limits = [plt.ylim()[0] +1.0, plt.ylim()[1] -1.0]
                y_limits = [plt.ylim()[0], plt.ylim()[1]]
                if WC_list_for_prediction_pulls is not None:
                    y_limits = [plt.ylim()[0], plt.ylim()[1]]
                ax.hlines(y=-y, xmin=x_limits[0], xmax=x_limits[1], color="black", linestyle="--", linewidth=0.5)
                ax.set_xlim(*x_limits)
                ax.set_ylim(*y_limits)
                ax.tick_params(axis='x', size=10, labelsize=11)
                ax.tick_params(axis='x', which='minor', size=6)
                if compare_with_SM or (WC_list_for_prediction_pulls is not None):
                    ax.set_xlabel(r'Pulls (w.r.t. SM prediction)', fontsize=15)
                elif matched_predictions_vs_BSM:
                    ax.set_xlabel(r'Pulls for matched SMEFT pred. w.r.t. BSM pred.', fontsize=9)
                else:
                    ax.set_xlabel(r'Pulls', fontsize=15)
                ax.legend(loc=legend_loc, fontsize=8)
                if only_higgs_fccee_obs:
                    ax.set_title(plot_titles[BP][scenario], fontsize=16)
                else:
                    ax.set_title(plot_titles[BP][scenario], fontsize=9)
                plt.tight_layout()   # Makes sure labels are not cut off

                if WC_list_for_prediction_pulls is not None:
                    plot_filename = f"{working_dir}/comparison_plots/results_{results_dir}/pull_plot_obs_compare{file_suffix}"
                elif matched_predictions_vs_BSM:
                    plot_filename = f"{working_dir}/../smeft_matching_inputs/comparison_plots/results_{results_dir}/pull_obs_{BP}_{scenario}_compare{file_suffix}"
                else:
                    plot_filename = f"{working_dir}/comparison_plots/results_{results_dir}/pull_obs_{BP}_{scenario}_compare{file_suffix}"
                if compare_with_SM: 
                    plot_filename = plot_filename + "_with_SM"
                if only_higgs_fccee_obs:
                    plot_filename = plot_filename + "_only_higgs_fccee_obs"
                if save_fig: plt.savefig(f"{plot_filename}_{k}.pdf")

    if show_plots:
        plt.show()


