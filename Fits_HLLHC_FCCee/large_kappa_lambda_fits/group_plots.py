import subprocess

# Open the input file in read mode and output file in write mode
working_dir = "./"

lambdas = list(range(-5, 11))  # Lambda values from -5 to 10
all_scenarios = [f"Lambda{lamb}_FCCee240_FCCee365_noHLLHClambda" for lamb in lambdas]

spec = "fits"
model_spec = spec

results_dirs = spec

# Create the output directories
for results_dir in results_dirs:
    subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{results_dir}"])

# Copy and rename plots for specific parameters/observables

copy_obs = [
    # "CH_corr", 
    # "CHbox_corr", 
    # "CHD_corr", 
    "deltalHHH_HLLHC",
]

# copy_obs = [
#     # "CH_corr_mod", 
#     # "CHbox_corr_mod", 
#     # "CHD_corr_mod", 
#     "deltalHHH_HLLHC_mod",
# ]


for scenario in all_scenarios:
    for obs in copy_obs:
            try:
                subprocess.run(["cp", f"{working_dir}{scenario}/results_{model_spec}/Observables/{obs}.pdf",
                    f"{working_dir}comparison_plots/results_{model_spec}/{obs}_{scenario}.pdf"])
            except:
                print(f"file not found: {working_dir}{scenario}/results_{model_spec}/Observables/{obs}.pdf")