import copy
import subprocess


working_dir = "./"

LAMBDAS = [x for x in range(-5, 11) for _ in range(2)]

# WITH_LAMBDA=['no', '', 'no', '', 'no', '', 'no', '']
WITH_LAMBDA=['no' if i%2==0 else '' for i in range(len(LAMBDAS))]

HLLHC_lambda_precision = 0.25

observables = {}
central_values_obs = {}
central_values_gaus_corr_obs = {}

k_ZH_240_365_central_values = {}

for i, lmbd in enumerate(LAMBDAS):
    scenario = f"Lambda{lmbd}_FCCee240_FCCee365_{WITH_LAMBDA[i]}HLLHClambda"
    scenario_dir = working_dir + scenario + "/"
    input_file =  scenario_dir + "results_observables/observables.txt"

    k_ZH_240_365_central_values[lmbd] = {}

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
                    k_ZH_240_365_central_values[lmbd][observable] = central_values_obs[observable]

        print(central_values_obs)


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

        print(central_values_gaus_corr_obs)


    observable_files = [working_dir + scenario + obs_file_path[2:] for obs_file_path in observable_files]
    [print(file) for file in observable_files]

    observable_files_new = [obs_file_path[:-5] + "_new.conf" for obs_file_path in observable_files]
    [print(file) for file in observable_files_new]

    for obs_file_path, obs_file_path_new in zip(observable_files, observable_files_new):
        with open(obs_file_path, 'r') as obs_file, open(obs_file_path_new, 'w') as obs_file_new:

            is_obs_correlated = False
            for line in obs_file:
                columns = line.split()

                if line.startswith("Observable "):
                    observable = columns[1]
                    if observable == "deltalHHH_HLLHC" and WITH_LAMBDA[i] == '':
                        columns[6]="MCMC"
                        columns[7]="weight"
                        columns.append(str(central_values_obs[observable]))
                        columns.append(str((float(central_values_obs[observable])+1) * HLLHC_lambda_precision))
                        columns.append(str(0.0))

                    if columns[6]=="MCMC" and columns[7]=="weight":
                        if not is_obs_correlated:
                            columns[8] = str(central_values_obs[observable])
                        else:
                            observable_number = observable_number + 1
                            #print(observable_number)
                            #print(n_corr_obs)
                            columns[8] = str(central_values_gaus_corr_obs[corr_obs_name][observable])
                            if observable_number == n_corr_obs:
                                is_obs_correlated = False

                        # Rejoin the columns and write to the output file
                        obs_file_new.write(" ".join(columns) + "\n")
                    else:
                        # Write unmodified lines to the output file
                        obs_file_new.write(line)

                else:

                    if line.startswith("CorrelatedGaussianObservables") or \
                    line.startswith("ObservablesWithCovarianceInverse"):
                        
                        corr_obs_name = columns[1]
                        n_corr_obs = int(columns[2])
                        observable_number = 0
                        is_obs_correlated = True

                    # Write unmodified lines to the output file
                    obs_file_new.write(line)

        subprocess.run(["mv", obs_file_path_new, obs_file_path])


    central_values_obs[observable]


print(k_ZH_240_365_central_values)

subprocess.run(["mkdir", "-p", "comparison_plots"])
with open(f"comparison_plots/k_ZH_240_365_predictions.txt", "w") as k_ZH_output:

    for i, lmbd in enumerate(LAMBDAS):
        if WITH_LAMBDA[i] == 'no':
            for obs in ['eeZH_FCCee240', 'eeZH_FCCee365',]:
                text = f"{lmbd} " + \
                       f"{obs} " + \
                    f"{k_ZH_240_365_central_values[lmbd][obs]}"
                print(text, file = k_ZH_output)


    #print(f"Modified content saved to {output_file_ILC_250}.")