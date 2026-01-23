# **`HEPfit_snowmass21`** repository

This repository contains the code used for the $\kappa_{\lambda}$ studies at future colliders. All studies of the indirect sensitivity to $\kappa_{\lambda}$ using HEPfit are stored in this repository.

For the code which determines the benchmark points for each model, see the `future_projections` repository. 

## Repository Structure:

### `IDM_fits/`
Directory containing all IDM studies. Subdivided into FCC-ee, $\text{ILC}_{250}$, and $\text{ILC}_{250+350+500+1000}$ studies. See `IDM_fits/README.md` for more details.

### `Z2SSM_fits_energy_dependence/`

Directory containing all Z2SSM studies after the inclusion of the energy-dependence of the $ZZh$ coupling in the theory predictions. See `Z2SSM_fits_energy_dependence/README.md` for more details. 

### `Fits_HLLHC_ILC_250_350_500_1000/`

Contains the original HEPfit configuration files for $\text{ILC}_{250+350+500+1000}$ as well as all ILC self-consistent (i.e. based on SMEFT, not a UV-complete model) cross-check fits.

### `setup_scripts`
Contains the necessary setup scripts to run the HEPfit studies. The current setup script is `setup_rocky9_jwd_NPs.sh`, which extracts HEPfit (including the new nuisance parameters) into the job working directory (`jwd/`) and sets up ROOT.

This directory also contains scripts to create (and later setup) a necessary python virtual environment used to scale the HEPfit observables, as part of the procedure to set up the fits. The current setup script for this is `setup_python_env_py38.sh`.

Finally, scripts to compile BAT (with the necessary patch) and HEPfit in the `jwd/` are also present.

### `fit_utils`
A python package containing useful modules for post-fit analysis. Includes several plotting scripts, parser scripts to read fit results and inputs, as well as the EFT matching module.


## Current setup procedure:
The current setup procedure is to use remote editing with VSCode in a Rocky9 virtual environment, and running:
- `source setup_scripts/setup_rocky9_jwd_NPs.sh`
- `source setup_scripts/setup_python_env_py38.sh`

This sets up HEPfit as well as the python virtual environment necessary to set up fits and for post-fit analyses. To actually set up fits with HEPfit, see the setup scripts inside the corresponding directory (e.g. `IDM_fits/Fits_HLLHC_ILC_250_350_500_1000/different_BPs/`).

If the HEPfit source code is modified, it should be recompiled with the `compile_hepfit.sh` or `compile_hepfit_NPs.sh` scripts, depending on whether the version without or with the new nuisance parameters is to be compiled.