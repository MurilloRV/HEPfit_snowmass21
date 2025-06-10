import copy
import subprocess


working_dir = "./"

WC_list = ["CH", "CHbox", "CHD", "CHW", "CHB", "CHWB", ]
WC_values = {}
with open(f"{working_dir}WC_results.txt", 'r') as f:
    lines = f.readlines()
    WC_values = {WC: [] for WC in WC_list}
    for i, line in enumerate(lines):
        if i == 0:  # Skip header line
            continue

        _, CH, CHbox, CHD, CHW, CHB, CHWB = line.split(",")
        WC_values["CH"].append(float(CH))
        WC_values["CHbox"].append(float(CHbox))
        WC_values["CHD"].append(float(CHD))
        WC_values["CHW"].append(float(CHW))
        WC_values["CHB"].append(float(CHB))
        WC_values["CHWB"].append(float(CHWB))

n_BPs = len(WC_values["CH"])

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

for i in range(n_BPs):
    scenario = f"WCs_BPs_{i}_FCCee240_FCCee365"
    scenario_dir = working_dir + scenario + "/"

    CH = WC_values["CH"][i]
    CHbox = WC_values["CHbox"][i]
    CHD = WC_values["CHD"][i]
    CHW = WC_values["CHW"][i]
    CHB = WC_values["CHB"][i]
    CHWB = WC_values["CHWB"][i]

    k_ZH_240_365_central_values[i] = {}
    for flag in flags:
        input_file = scenario_dir + f"results_observables/observables{flag}.txt"

        k_ZH_240_365_central_values[i][flag] = {}
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
                        k_ZH_240_365_central_values[i][flag][observable] = central_values_obs[observable]

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

            # print(central_values_gaus_corr_obs)


        # observable_files = [working_dir + scenario + obs_file_path[2:] for obs_file_path in observable_files]
        # [print(file) for file in observable_files]

        # observable_files_new = [obs_file_path[:-5] + "_new.conf" for obs_file_path in observable_files]
        # [print(file) for file in observable_files_new]

        # for obs_file_path, obs_file_path_new in zip(observable_files, observable_files_new):
        #     with open(obs_file_path, 'r') as obs_file, open(obs_file_path_new, 'w') as obs_file_new:

        #         is_obs_correlated = False
        #         for line in obs_file:
        #             columns = line.split()

        #             if line.startswith("Observable "):
        #                 observable = columns[1]
        #                 if observable == "deltalHHH_HLLHC" and WITH_LAMBDA[i] == '':
        #                     columns[6]="MCMC"
        #                     columns[7]="weight"
        #                     columns.append(str(central_values_obs[observable]))
        #                     columns.append(str((float(central_values_obs[observable])+1) * HLLHC_lambda_precision))
        #                     columns.append(str(0.0))

        #                 if columns[6]=="MCMC" and columns[7]=="weight":
        #                     if not is_obs_correlated:
        #                         columns[8] = str(central_values_obs[observable])
        #                     else:
        #                         observable_number = observable_number + 1
        #                         #print(observable_number)
        #                         #print(n_corr_obs)
        #                         columns[8] = str(central_values_gaus_corr_obs[corr_obs_name][observable])
        #                         if observable_number == n_corr_obs:
        #                             is_obs_correlated = False

        #                     # Rejoin the columns and write to the output file
        #                     obs_file_new.write(" ".join(columns) + "\n")
        #                 else:
        #                     # Write unmodified lines to the output file
        #                     obs_file_new.write(line)

        #             else:

        #                 if line.startswith("CorrelatedGaussianObservables") or \
        #                 line.startswith("ObservablesWithCovarianceInverse"):
                            
        #                     corr_obs_name = columns[1]
        #                     n_corr_obs = int(columns[2])
        #                     observable_number = 0
        #                     is_obs_correlated = True

        #                 # Write unmodified lines to the output file
        #                 obs_file_new.write(line)

        #     subprocess.run(["mv", obs_file_path_new, obs_file_path])


        # central_values_obs[observable]


print(k_ZH_240_365_central_values)

subprocess.run(["mkdir", "-p", "comparison_plots"])
for flag in flags:
    with open(f"comparison_plots/k_ZH_240_365_predictions_BPs_{flag}.txt", "w") as k_ZH_output:

        for i in range(n_BPs):
            CH = WC_values["CH"][i]
            CHbox = WC_values["CHbox"][i]
            CHD = WC_values["CHD"][i]
            CHW = WC_values["CHW"][i]
            CHB = WC_values["CHB"][i]
            CHWB = WC_values["CHWB"][i]

            for obs in ['eeZH_FCCee240', 'eeZH_FCCee365',]:
                text = f"{CH} " + \
                       f"{CHbox} " + \
                       f"{CHD} " + \
                       f"{CHW} " + \
                       f"{CHB} " + \
                       f"{CHWB} " + \
                       f"{obs} " + \
                       f"{k_ZH_240_365_central_values[i][flag][obs]}"
                print(text, file = k_ZH_output)


        #print(f"Modified content saved to {output_file_ILC_250}.")