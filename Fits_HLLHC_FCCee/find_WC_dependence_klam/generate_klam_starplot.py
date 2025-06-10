import numpy as np
import subprocess
from matplotlib import pyplot as plt

WCs = ["CH", "CHbox", "CHD", "CHW", "CHB", "CHWB",]
WC_values = np.linspace(-10, 10, 21)
n_WC_values = len(WC_values)
working_dir = "."

plot_dir = f"{working_dir}/plots/"
subprocess.run(["mkdir", "-p", f"{plot_dir}"])

klam_central_values = {}

for wc in WCs:

    klam_central_values[wc] = []
    for point in range(n_WC_values):

        filename = f"{working_dir}/observables_results/observables_{wc}_{point}.txt"
        with open(filename, "r") as input_file:

            print("Reading names of configuration files with observables\n")
            observable_files = []
            for line_nr, input_line in enumerate(input_file):

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
            for line_nr, input_line in enumerate(input_file):
                # Skip the empty line after "Observables"
                if line_nr == 0:
                    continue
                
                if input_line in ['\n', '\r\n']:
                    observables_end = line_nr
                    break
                else:
                    columns = input_line.split()
                    observable = columns[0]

                    if observable == "deltalHHH_HLLHC":
                        klam_central_values[wc].append(float(columns[2]))

print(klam_central_values)

fig, ax = plt.subplots(figsize=(4.0, 3.5), dpi=300)
plt.grid(which='both', linestyle='--', linewidth=0.5)

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:brown", "tab:purple"]
# labels = [r"$C_{H}$", r"$C_{H\boxdot}$", r"$10\cdot C_{HD}$", r"$10^3\cdot C_{HW}$", r"$10^3\cdot C_{HB}$", r"$10^3\cdot C_{HWB}$"]
labels = [r"$C_{H}$", r"$C_{H\boxdot}$", r"$C_{HD}$", r"$C_{HW}$", r"$C_{HB}$", r"$C_{HWB}$"]
for wc, label, color in zip(WCs, labels, colors):
    # if wc == "CHD":
    #     curve = 10*np.array(klam_central_values[wc])
    # elif wc in ["CHW", "CHB", "CHWB",]:
    #     curve = 1e3*np.array(klam_central_values[wc])
    # else:
    curve = klam_central_values[wc]
    plt.plot(WC_values, curve, label=label, color=color)
    plt.scatter(WC_values, curve, color=color)
    
plt.title(r"$\kappa_\lambda$ dependence on Wilson coefficients")
plt.xlabel(r"Wilson Coefficient", fontsize=13)
plt.ylabel(r"$\kappa_\lambda$", fontsize=13)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(f"{plot_dir}/WCs_vs_klam.pdf")
# plt.show()



