import copy
import subprocess


working_dir = "./"

CH_values = []
CHbox_values = []
with open(f"{working_dir}CH_CHbox_interpolator_results.txt", 'r') as f:
    lines = f.readlines()
    for line in lines:
        CH, CHbox = line.split(",")
        CH_values.append(float(CH))
        CHbox_values.append(float(CHbox))

HLLHC_lambda_precision = 0.25

observables = {}
central_values_obs = {}
central_values_gaus_corr_obs = {}

k_ZH_240_365_central_values = {}

flags = {
    "", 
    "_noLoopH3d6Quad",
    "_LoopHd6NoSubleading",
    "_LoopH3d6Quad_C1term",
    "_LoopH3d6Cubi",
    "_LoopH3d6Full",
}

for i, (CH, CHbox) in enumerate(zip(CH_values, CHbox_values)):
    # scenario = f"Lambda{lmbd}_FCCee240_FCCee365_{WITH_LAMBDA[i]}HLLHClambda"
    scenario = f"CH_CHbox_{i}_FCCee240_FCCee365"
    scenario_dir = working_dir + scenario + "/"

    k_ZH_240_365_central_values[CH] = {}
    for flag in flags:
        input_file = scenario_dir + f"results_observables/observables{flag}.txt"

        k_ZH_240_365_central_values[CH][flag] = {}
        print(f"Running scenario {scenario}")

        with open(input_file, 'r') as infile:

            print("Reading names of configuration files with observables\n")
            observable_files = []
            for line_nr, input_line in enumerate(infile):

                if input_line.startswith("Including File: ../Globalfits/AllOps/../../"):
                    # Split the line into columns by whitespace
                    columns = input_line.split()
                    
                    observable_file = columns[2]
                    observable_files.append(observable_file)


                if input_line.startswith("Observables:"):
                    print(f"Files found in results: \n")
                    [print(file_name) for file_name in observable_files]
                    print("\n")
                    break

            print("Reading Observables:")
            for line_nr, input_line in enumerate(infile):
                # Skip the empty line after "Observables"
                if line_nr == 0:
                    continue
                
                if input_line in ['\n', '\r\n']:
                    observables_end = line_nr
                    break
                else:
                    columns = input_line.split()
                    observable = columns[0]
                    central_values_obs[observable] = float(columns[2])

                    if observable in ['eeZH_FCCee240', 'eeZH_FCCee365']:
                        k_ZH_240_365_central_values[CH][flag][observable] = central_values_obs[observable]

            # print(central_values_obs)


            print("\nReading Correlated Gaussian Observables: ")
            corr_obs = {}
            for line_nr, input_line in enumerate(infile):
                # Skip the "Correlated Gaussian Observables:" line and the following empty one
                if line_nr <= 1:
                    continue

                if input_line in ['\n', '\r\n']:
                    if corr_obs == {}: break  # Reached end of file

                    central_values_gaus_corr_obs[corr_obs_name] = copy.deepcopy(corr_obs)
                    corr_obs = {}
                    continue
                elif len(input_line.split()) == 1:
                    corr_obs_name = input_line.split()[0]
                else:
                    columns = input_line.split()
                    observable = columns[0]
                    corr_obs[observable] = float(columns[2])


print(k_ZH_240_365_central_values)

subprocess.run(["mkdir", "-p", "comparison_plots"])
for flag in flags:
    with open(f"comparison_plots/k_ZH_240_365_predictions{flag}.txt", "w") as k_ZH_output:

        for i, (CH, CHbox) in enumerate(zip(CH_values, CHbox_values)):
            for obs in ['eeZH_FCCee240', 'eeZH_FCCee365',]:
                text = f"{CH} " + \
                       f"{CHbox} " + \
                       f"{obs} " + \
                       f"{k_ZH_240_365_central_values[CH][flag][obs]}"
                print(text, file = k_ZH_output)

