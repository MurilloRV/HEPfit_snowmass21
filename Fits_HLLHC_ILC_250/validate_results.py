import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math


# Short script to compare the results

# Open the input file in read mode and output file in write mode
file_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21" + \
            "/Fits_HLLHC_ILC_250/"
new_results_file =  "results_batch/MonteCarlo_results.txt"
original_results_file = "MonteCarlo_results_original.txt"


new_results = []
orig_results = []
parameters = []


found_results = False
nline=0
with open(new_results_file, 'r') as new_file:
    for line in new_file:
        if not found_results:
            if line.startswith(" Global mode:"):
                found_results = True
            continue

        # Reached end of the relevant data
        if line in ['\n', '\r\n']:
            break

        # Split the line into columns by whitespace
        columns = line.split()

        parameters.append(columns[2].strip("\""))
        new_results.append([float(columns[4]), float(columns[6])])

new_results = np.array(new_results)

print(parameters)
print(new_results)


found_results = False
with open(original_results_file, 'r') as orig_file:
    for line in orig_file:
        if not found_results:
            if line.startswith(" Global mode:"):
                found_results = True
            continue

        # Reached end of the relevant data
        if line in ['\n', '\r\n']:
            break

        # Split the line into columns by whitespace
        columns = line.split()

        orig_results.append([float(columns[4]), float(columns[6])])

orig_results = np.array(orig_results)

print(orig_results)


w = 0.5
dimw = w / 2 

parameter_order = [math.ceil(np.log10(par)) for par in orig_results[:, 1]]
parameter_order = np.array(parameter_order)

orig_results = [par/10.**parameter_order[i] for i, par in enumerate(orig_results)]
orig_results = np.array(orig_results)
print(orig_results)

new_results = [par/10.**parameter_order[i] for i, par in enumerate(new_results)]
new_results = np.array(new_results)
print(new_results)

labels = [f"{10**(-parameter_order[i])}*"+par for i, par in enumerate(parameters)]

param_breaks = np.arange(0, len(parameters), 8)
if param_breaks[-1] != len(parameters)-1:
    param_breaks = np.append(param_breaks, [len(parameters)-1])

print(param_breaks)
for k in range(len(param_breaks) - 1):
    fig= plt.figure(k,dpi=150)
    ax = plt.gca()
    #fig, ax = plt.subplots(1,1,figsize=(7,5))
    x = np.arange(param_breaks[k],param_breaks[k+1])
    

    ax.errorbar(np.zeros(param_breaks[k+1]-param_breaks[k]),
                -x, xerr=(orig_results[param_breaks[k]:param_breaks[k+1], 1],), fmt='o', linewidth=2, capsize=6, label = "Original results")
    ax.errorbar(new_results[param_breaks[k]:param_breaks[k+1], 0] - new_results[param_breaks[k]:param_breaks[k+1], 0],
                -x-dimw, xerr=(new_results[param_breaks[k]:param_breaks[k+1], 1],), fmt='o', linewidth=2, capsize=6, label = "New results")


    plt.axvline(c='0.6', linewidth=2)
    ax.set_xlim([-1,1])
    #ax.set_yticks(-x - dimw / 2)
    ax.set_yticks(-x)
    ax.set_yticklabels(labels[param_breaks[k]:param_breaks[k+1]],fontsize=12)
    ax.tick_params(axis='x', size=10, labelsize=12)
    ax.tick_params(axis='x', which='minor', size=6)
    ax.set_xlabel(r'Global mode with uncertainty', fontsize=15)
    ax.legend(loc='best', fontsize=11)
    plt.tight_layout()   # Makes sure labels are not cut off
    plt.savefig(file_dir + f'validation_plots/pull_plots_{k}.pdf')

#plt.show()
# print(f"Processing complete. Modified content saved to {output_file}.")
