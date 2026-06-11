
import numpy as np
sqrt = np.sqrt

from math import floor, log10

def format_sig(x, sig=6):
    if x == 0:
        return "0"

    decimals = max(0, sig - 1 - floor(log10(abs(x))))
    s = f"{x:.{decimals}f}"
    return s.rstrip('0').rstrip('.')

###########################################################################################
###########################################################################################
#######################################   EWPOs   #########################################
###########################################################################################
###########################################################################################

file_dir = "./GIMR/"

# Snowmass 2021 projections
# updated_projections = {
#     "Mw"     : [0.25e-3, 0.3e-3],
#     "GammaW" : [1.2e-3, 0.3e-3],

#     "Mz"     : [0.004e-3, 0.1e-3],
#     "GammaZ" : [0.004e-3, 0.025e-3],

#     "Aelectron" : [0.70e-5, 2.00e-5],
#     "Amu"       : [2.30e-5, 2.20e-5],
#     "Atau"      : [0.50e-5, 20.0e-5],
#     "Abottom"   : [2.40e-5, 21.0e-5],
#     "Acharm"    : [20.0e-5, 15.0e-5],

#     "sigmaHadron" : [0.035e-3, 4.0e-3],

#     "Relectron" : [0.004e-3,  0.3e-3],
#     "Rmu"       : [0.003e-3,  0.05e-3],
#     "Rtau"      : [0.003e-3,  0.1e-3],
#     "Rbottom"   : [0.0014e-3, 0.3e-3],
#     "Rcharm"    : [0.015e-3,  1.5e-3],
# }

# Updated projections 
updated_projections = {
    "Mw"     : [0.18e-3, 0.16e-3],
    "GammaW" : [0.27e-3, 0.2e-3],

    "Mz"     : [0.004e-3, 0.1e-3],
    "GammaZ" : [0.004e-3, 0.012e-3],

    "Aelectron" : [13.5e-6],
    "Amuon"       : [32.0e-6],
    "Atau"      : [34.0e-6],
    "Abottom"   : [98.0e-6],
    "Acharm"    : [60.0e-6],

    "sigmaHadron" : [0.030e-3, 0.8e-3],

    "Relectron" : [3.4e-6,  2.3e-6],
    "Rmuon"       : [2.4e-6,  2.3e-6],
    "Rtau"      : [2.7e-6,  2.3e-6],
    "Rbottom"   : [1.2e-6,  1.6e-6],
    "Rcharm"    : [1.4e-6,  2.2e-6],
}

input_files =  [
               file_dir + "ObservablesEW_FCCee_WW_SM",
               file_dir + "ObservablesEW_FCCee_Zpole_SM",
               ]

output_files = [
               file_dir + "ObservablesEW_FCCee_WW_SM_updated_lumi",
               file_dir + "ObservablesEW_FCCee_Zpole_SM_updated_lumi",
              ]


for input_file, output_file in zip(input_files, output_files):
    input_file = input_file  + ".conf"
    output_file = output_file + ".conf"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
                obs = columns[2]
                if (obs in updated_projections.keys()):
                    if len(updated_projections[obs]) == 1:
                        # If only one uncertainty is provided, assume it's the total uncertainty
                        combined_unc = updated_projections[obs][0]
                    else:
                        stat_unc = updated_projections[obs][0]
                        syst_unc = updated_projections[obs][1]
                        combined_unc = sqrt(stat_unc**2 + syst_unc**2)

                    if obs.startswith("R"):
                        # For R observables, what is given is the relative uncertainty
                        columns[9] = format_sig(combined_unc * float(columns[8]))
                    else:
                        columns[9] = format_sig(combined_unc)

                # Rejoin the columns and write to the output file
                outfile.write(" ".join(columns) + "\n")
            else:
                # Write unmodified lines to the output file
                outfile.write(line)

        print(f"Modified content saved to {output_file}.")