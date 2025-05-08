# `IDM_fits` directory

Directory containing all IDM studies. Subdivided into FCC-ee, $\text{ILC}_{250}$, and $\text{ILC}_{250+350+500+1000}$ studies. `ProcessHistograms` contains the scripts to perform the aesthetic changes to the output HEPfit plots.

## `Fits_HLLHC_FCCee`

Contains the FCC-ee studies. The studies for the different benchmark points are located in `Fits_HLLHC_FCCee/different_BPs`

### `Fits_HLLHC_FCCee/different_scenario_fits`

Containts the basic configuration files for the different scenario fits. These are copied for the different BPs into the `Fits_HLLHC_FCCee/different_BPs`, and overwriten with the specific predictions for each BP.

### `Fits_HLLHC_FCCee/different_BPs`

The configuration files and results for the different IDM benchmark points are stored here. Each BP has a corresponding directory. For the determination and nomenclature of the BPs, see the `future_projections` repository. Within each of these directories, there are 3 subfolders corresponding to the 3 different fit scenarios (as defined in the contribution to the ECFA Higgs study):

1. $\text{FCC-ee}_{240}$
2. $\text{FCC-ee}_{240}+\text{FCC-ee}_{365}$
3. $\text{FCC-ee}_{240}+\text{FCC-ee}_{365}+\kappa_\lambda\text{ at HL-LHC}$


The scripts used to setup the fits are the following:

- `setup_fits_realistic_HL_LHC_all_flags_simplified.sh`: The main bash script to setup the fits. Initially creates the separate directories for each BP and scenario, copies the basic configuration files from `Fits_HLLHC_FCCee/different_scenario_fits` into these directories, and later performs the necessary modifications:
    - Setting up configuration files with reduced priors, to increase the probability of convergence and reduce the convergence time.
    - Setting up different Monte Carlo configuration files, corresponding to different choices of number of total and burn-in events generated ("`_short`", "`_long`", and "`_full`").
    - Creating and properly naming the configuration files according to the selected flags
    - Finally, the `scale_observables_kappas.py` python script is called to actually scale the HEPfit Higgs/EW observables, according to the IDM BP predictions, in the configuration files for the fit.

- `scale_observables_kappas.py`: Python script to scale the Higgs and EW observables, given a specific BP, a fit scenario (e.g. $\text{FCC-ee}_{240}$), and a set of optional flags which determine how precisely the observables are modified. The different flags are explain in the script. A series of `if-else` statements contains the IDM predictions for each BP; these lines are generated in the `future_projections` repository.



Post-fit scripts:

- `generate_pull_plots_obs.py`: Python script to create the pull plots for the HEPfit observables

- `generate_pull_plots_pars.py`: Python script to create the pull plots for the HEPfit model parameters (i.e. the Wilson coefficients)

- `group_plots.py`: Groups together HEPfit output plots into the `comparison_plots` directory. 

- `comparison_plots`: The final plots for group meetings / presentations are stored here. After being modified by the `ProcessHistograms` scripts, the plots for the different BPs and fit scenarios are compiled together in folders corresponding to the different studies performed.