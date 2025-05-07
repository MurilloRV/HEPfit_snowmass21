# Copy and rename plots for specific parameters/observables
import subprocess

working_dir = "./"
model_specs = "fits_small_priors_long"

lambdas = list(range(-5, 11))
scenarios = [f"Lambda{lamb}_FCCee240_FCCee365_noHLLHClambda" for lamb in lambdas]

copy_obs = [
    # "CH_corr", 
    # "CHbox_corr", 
    # "CHD_corr", 
    "deltalHHH_HLLHC",
]


# Create the output directory
subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{model_specs}"])

for scenario in scenarios:
    for obs in copy_obs:
        subprocess.run(["cp", f"{working_dir}{scenario}/results_{model_specs}/Observables/{obs}.pdf",
                    f"{working_dir}comparison_plots/results_{model_specs}/{obs}_{scenario}.pdf"])
