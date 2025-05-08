# **`HEPfit_snowmass21`** repository

This repository contains the code used for the $\kappa_{\lambda}$ studies at future colliders. All studies of the indirect sensitivity to $\kappa_{\lambda}$ using HEPfit are stored in this repository.

For the code which determines the benchmark points for each model, see the `future_projections` repository. 

## Repository Structure:

### `IDM_fits/`
Directory containing all IDM studies. Subdivided into FCC-ee, $\text{ILC}_{250}$, and $\text{ILC}_{250+350+500+1000}$ studies. `ProcessHistograms` contains the scripts to perform the aesthetic changes to the output HEPfit plots. See `IDM_fits/README.md` for more details.

### `Z2SSM_fits_energy_dependence/`

Directory containing all Z2SSM studies after the inclusion of the energy-dependence of the $ZZh$ coupling in the theory predictions. 

The original Z2SSM studies with **energy-independent** couplings are in `Fits_HLLHC_ILC_250/Z2SSM_BenchmarkPoint_fits_HLLHC_ILC_250`.

### `Fits_HLLHC_FCCee/`

Contains the original HEPfit FCCee configuration files as well as all FCCee self-consistent (i.e. based on SMEFT, not a UV-complete model) cross-check fits.

### `Fits_HLLHC_ILC_250/`

Contains the original HEPfit $\text{ILC}_{250}$ configuration files as well as all $\text{ILC}_{250}$ self-consistent (i.e. based on SMEFT, not a UV-complete model) cross-check fits. Also includes the original Z2SSM studies with **energy-independent** couplings, which were only performed for $\text{ILC}_{250}$.

### `Fits_HLLHC_ILC_250_350_500_1000/`

Contains the original HEPfit configuration files for $\text{ILC}_{250+350+500+1000}$ as well as all ILC self-consistent (i.e. based on SMEFT, not a UV-complete model) cross-check fits.

### `ProcessHistograms`
Scripts (based on BAT and ROOT) that perform the aesthetic modifications to the HEPfit output plots. This includes changing the plotted variable from $\kappa_\lambda - 1$ to $\kappa_\lambda$, plotting the "true" model value for $\kappa_\lambda$, and minor optional modifications, such as shifting/scaling the x-axis, plotting the HL-LHC constraint on $\kappa_\lambda$, plotting the HEPfit logo, and changing the position of the legend.

This is the original set of scripts, each subdirectory in this repository has a specialized version of these.

### `setup_scripts`
Contains the necessary setup scripts to run the HEPfit studies. The current setup script is `setup_rocky9_jwd.sh`, which extracts HEPfit into the job working directory (`jwd/`) and sets up ROOT.

This directory also contains scripts to create (and later setup) a necessary python virtual environment used to scale the HEPfit observables, as part of the procedure to set up the fits.

Finally, scripts to compile BAT (with the necessary patch) and HEPfit in the `jwd/` are also present.

### `illustrations`
Contains scripts to generate useful illustrations for presentations. Currently includes a python script that generates an illustration of principle of EFTs.