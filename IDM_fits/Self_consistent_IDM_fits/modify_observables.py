import numpy as np
import copy
import subprocess
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scenario", help = "Name of the scenario (e.g. IDM_FCCee240)", type=str)
parser.add_argument("-b", "--bp", help = "Which benchmark point to use", type=str)
parser.add_argument("--conf", help = "Name of the configuration file", type=str)
parser.add_argument("--workingdir", help = "Path of working directory", type=str)
parser.add_argument("--copydir", help = "Path of directory from which to copy config files", type=str)

args = parser.parse_args()
scenario    = args.scenario
BP          = args.bp
conf        = args.conf
working_dir = args.workingdir
copy_dir    = args.copydir

all_observables = []
central_values_obs = {}
central_values_gaus_corr_obs = {}


scenario_dir = f"{working_dir}/{BP}/{scenario}"
input_file_predictions =  scenario_dir + f"/results_{conf}_observables/observables.txt"



print(f"Running scenario {scenario}")
with open(input_file_predictions, 'r') as infile:

    print("Reading names of configuration files with observables\n")
    observable_files = []
    for line_nr, input_line in enumerate(infile):

        if input_line.startswith("Including File: ./Globalfits/AllOps/../../"):
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
            # central_values_obs[observable] = float(columns[2])
            central_values_obs[observable] = np.nan
            all_observables.append(observable)

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
            # corr_obs[observable] = float(columns[2])
            corr_obs[observable] = np.nan
            all_observables.append(observable)

    # print(central_values_gaus_corr_obs)


file_path = f"{copy_dir}/results_{conf[6:]}_long/Observables/Statistics.txt"
with open(file_path, 'r') as file:
    lines = file.readlines()
    
    line_nrs = [np.nan for obs in all_observables]
    for n, line in enumerate(lines):
        columns = line.split()
        if len(columns) < 2:
            continue
        
        if (columns[1] == "Observable" \
            or columns[1] == "AsyGausObservable") \
            and columns[2][1:-2] in all_observables:

            observable_index = all_observables.index(columns[2][1:-2])
            line_nrs[observable_index] = n

    # print(line_nrs)

    for line_nr, obs in zip(line_nrs, all_observables):
    
        # print(line_nr, obs)
        columns = lines[line_nr + 1].split()
        if obs in central_values_obs.keys():
            central_values_obs[obs] = float(columns[3])    # Mean
        else:
            for corr_obs_name, corr_obs in central_values_gaus_corr_obs.items():
                if obs in corr_obs.keys():
                    central_values_gaus_corr_obs[corr_obs_name][obs] = float(columns[3])

print(central_values_obs)
print(central_values_gaus_corr_obs)

for obs, value in central_values_obs.items():
    if np.isnan(value):
        raise ValueError(f"Error: Central value for observable {obs} is NaN. Please check the input files.")

for corr_obs_name, corr_obs in central_values_gaus_corr_obs.items():
    for obs, value in corr_obs.items():
        if np.isnan(value):
            raise ValueError(f"Error: Central value for correlated observable {obs} in {corr_obs_name} is NaN. Please check the input files.")



print("\nModifying observables in configuration files")
# print(observable_files)

observable_files_old = [ f"{copy_dir}/{obs_file_path[2:]}" for obs_file_path in observable_files]
[print(file) for file in observable_files_old]

observable_files_new = [ f"{scenario_dir}/{obs_file_path[2:-5]}" + "_new.conf" for obs_file_path in observable_files]
[print(file) for file in observable_files_new]

for old, new in zip(observable_files_old, observable_files_new):
    subprocess.run(["cp", old, new])

for obs_file_path, obs_file_path_new in zip(observable_files_old, observable_files_new):
    with open(obs_file_path, 'r') as obs_file, open(obs_file_path_new, 'w') as obs_file_new:

        is_obs_correlated = False
        for line in obs_file:
            columns = line.split()

            if line.startswith("Observable "):
                observable = columns[1]

                if columns[6]=="MCMC" and columns[7]=="weight":
                    if not is_obs_correlated:
                        columns[8] = str(central_values_obs[observable])
                    else:
                        observable_number = observable_number + 1
                        #print(observable_number)
                        #print(n_corr_obs)
                        for corr_obs_name, corr_obs in central_values_gaus_corr_obs.items():
                            if observable in corr_obs.keys():
                                columns[8] = str(corr_obs[observable])
                                break
                        # columns[8] = str(central_values_obs[observable])
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

    obs_file_path_new_rename = obs_file_path_new[:-9] + ".conf"
    subprocess.run(["mv", obs_file_path_new, obs_file_path_new_rename])


# central_values_obs[observable]

