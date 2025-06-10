import numpy as np
import math
import subprocess



# Open the input file in read mode and output file in write mode
working_dir = "./"

BPs = []
# BPs = BPs + [f"BP_{i}" for i in range(8)]
# num_BPOs = 2
num_BPBs = 19
# BPs = [f"BPO_{i}" for i in range(num_BPOs)]
BPs = BPs + [f"BPB_{i}" for i in range(num_BPBs)]
# BPs = ["BPB_2", "BPB_4", "BPB_6"]
# BP_Names = ["BPB 2", "BPB 4", "BPB 6"]
print(BPs)

n_BPs = len(BPs)


scenarios = [
    # "IDM_FCCee240",
    "IDM_FCCee240_FCCee365",
    # "IDM_FCCee240_FCCee365_HLLHClambda",
]


# spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_small_priors_long"
# spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_no_HLLHC_Higgs_small_priors_long"
# spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_no_C_HG_small_priors_long"
# spec = "fits_realistic_HL_LHC_WFR_kala2_input_small_priors_long"
spec = "fits_realistic_HL_LHC_WFR_kala2_input_all_small_priors_long"
# spec = "fits_realistic_HL_LHC_WFR_kala2_input_no_HLLHC_Higgs_small_priors_long"
# spec = "fits_realistic_HL_LHC_WFR_kala2_input_no_C_HG_small_priors_long"

# Todo: fix the plots for fits without certain WC, like C_HG

model_specs = {
    # "IDM_FCCee240" : [spec,],
    "IDM_FCCee240_FCCee365" : [spec,],
    # "IDM_FCCee240_FCCee365_HLLHClambda" : [spec,],
}

results_dir = spec

files = {}
for BP in BPs:
    files[BP] = {}
    for scenario in scenarios:
        files[BP][scenario] = {}
        for model_spec in model_specs[scenario]:
            files[BP][scenario][model_spec] = f"{working_dir}{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"


subprocess.run(["mkdir", "-p", f"{working_dir}comparison_plots/results_{results_dir}"])


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

                nobs = len(parameters[BP][scenario][model_spec])

                results[BP][scenario][model_spec] = []
                print(f"Reading results for {BP}, scenario: {scenario}, model spec: {model_spec}")
                for line_nr, par in zip(line_nrs, parameters[BP][scenario][model_spec]):
                
                    columns = lines[line_nr + 1].split()
                    means_uncertainties = [float(columns[3]),    # Mean
                                           float(columns[5]),]   # Uncertainty

                    results[BP][scenario][model_spec].append(means_uncertainties)

            results[BP][scenario][model_spec] = np.array(results[BP][scenario][model_spec])


print(f"\nParameter dictionary: \n{parameters}")
print(f"\nResults dictionary: \n{results}")


output_file = f"{working_dir}comparison_plots/results_{results_dir}/klam_results.txt"
with open(output_file, 'w') as f:
    print(f"Writing results to {output_file}")
    print(f"BP,klam,error", file=f)
    for BP in BPs:
        for scenario in scenarios:
            for model_spec in model_specs[scenario]:
                if BP not in results or scenario not in results[BP] or model_spec not in results[BP][scenario]:
                    print(f"Skipping {BP}, {scenario}, {model_spec} as results are missing.")
                    continue
                
                klams = results[BP][scenario][model_spec][:, 0]
                errors = results[BP][scenario][model_spec][:, 1]

                for k, e in zip(klams, errors):
                    print(f"{BP},{k+1},{e}", file=f)
 
