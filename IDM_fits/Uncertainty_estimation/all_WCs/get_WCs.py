import os
import subprocess
import numpy as np

working_dir = "./"


# BPs = [f"BP_{i}" for i in range(n_BPs)]
BPs = []

# BPOs = [f"BPO_{i}" for i in range(n_BPOs)]
BPOs = []

n_BPBs = 19
BPBs = [f"BPB_{i}" for i in range(n_BPBs)]
# BPBs = ["BPB_2", "BPB_4", "BPB_6", ]
# BPBs = ["BP_lambda1", ]

# BPs_new = [f"BP_new_{i}" for i in range(n_BPs_new)]
BPs_new = []

BPs_total = BPs + BPOs + BPBs + BPs_new

scenarios = [
    # "IDM_FCCee240",
    "IDM_FCCee240_FCCee365",
    # "IDM_FCCee240_FCCee365_HLLHClambda",
]

spec = "fits_realistic_HL_LHC_WFR_kala2_input_all_small_priors_long"
# spec = "fits_realistic_HL_LHC_WFR_kala2_input_small_priors_long"

model_specs = {
    # "IDM_FCCee240" : [spec, ],
    "IDM_FCCee240_FCCee365" : [spec, ],
    # "IDM_FCCee240_FCCee365_HLLHClambda" : [spec, ],
}

files = {}
fit_results_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/IDM_fits/Fits_HLLHC_FCCee/different_BPs/"
for BP in BPs_total:
    files[BP] = {}
    for scenario in scenarios:
        files[BP][scenario] = {}
        for model_spec in model_specs[scenario]:
            files[BP][scenario][model_spec] = f"{fit_results_dir}{BP}/{scenario}/results_{model_spec}/Observables/Statistics.txt"

print(f"Files to read: {files}")

WC_list = ["CH", "CHbox", "CHD", "CHW", "CHB", "CHWB", ]
WC_list = [f"{WC}_corr" for WC in WC_list]
WCs = {}


results = {}
parameters = {}
parameters_tex = {}

for BP in BPs_total:

    results[BP] = {}
    parameters[BP] = {}
    parameters_tex[BP] = {}
    for scenario in scenarios:

        parameters[BP][scenario] = {}
        parameters_tex[BP][scenario] = {}
        results[BP][scenario] = {}
        for model_spec in model_specs[scenario]:

            line_nrs = []
            parameters[BP][scenario][model_spec] = []
            parameters_tex[BP][scenario][model_spec] = []

            file_path = files[BP][scenario][model_spec]

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            with open(file_path, 'r') as file:
                print(f"Reading file: {file_path}")
                lines = file.readlines()
                
                for n, line in enumerate(lines):
                    columns = line.split()
                    if len(columns) < 2:
                        continue
                    
                    # print(columns[2][1:-2])
                    if columns[1] == "Observable" and \
                       columns[2][1:-2] in WC_list:
                        parameter = columns[2][1:-7]
                        parameters[BP][scenario][model_spec].append(parameter)
                        line_nrs.append(n)

                nobs = len(parameters[BP][scenario][model_spec])

                results[BP][scenario][model_spec] = []
                print(f"Reading results for {BP}, scenario: {scenario}, model spec: {model_spec}")
                for line_nr, par in zip(line_nrs, parameters[BP][scenario][model_spec]):
                
                    columns = lines[line_nr + 1].split()
                    means_uncertainties = [float(columns[3]),    # Mean
                                           float(columns[5]),]   # Uncertainty

                    # means_uncertainties[0] = means_uncertainties[0]/means_uncertainties[1]
                    # means_uncertainties[1] = means_uncertainties[1]/means_uncertainties[1]

                    results[BP][scenario][model_spec].append(means_uncertainties)

            results[BP][scenario][model_spec] = np.array(results[BP][scenario][model_spec])

print("\nResults dictionary:")
print(f"{results}")

print(f"\nParameter dictionary: \n{parameters}")


with open(f"{working_dir}WC_results.txt", 'w') as f:
    print(f"BP,CH,CHbox,CHD,CHW,CHB,CHWB", file=f)
    for BP in BPs_total:
        for scenario in scenarios:
            for model_spec in model_specs[scenario]:
                WC_results = []
                for WC in WC_list:
                    WC = WC[:-5]  # Remove the "_corr" suffix
                    if WC in parameters[BP][scenario][model_spec]:
                        index = parameters[BP][scenario][model_spec].index(WC)
                        result = results[BP][scenario][model_spec][index]
                        WC_results.append(result[0])  # Append the mean value
                    else:
                        raise ValueError(f"WC {WC} not found in parameters for {BP}, {scenario}, {model_spec}")
                WC_results_str = "".join([f",{result}" for result in WC_results])
                print(f"{BP}{WC_results_str}", file=f)
