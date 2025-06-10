import copy
import subprocess
import argparse
import os
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", help = "Name of the input file", type=str)
parser.add_argument("-o", "--output_file", help = "Name of the output file", type=str)
parser.add_argument("--CH", help = "Value of CH", type=float)
parser.add_argument("--CHBox", help = "Value of CHBox", type=float)
args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file
CH = args.CH
CHBox = args.CHBox


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

            if observable == 'eeZH_FCCee240':
                k_ZH_240_central_value = np.sqrt(float(columns[2]))
            elif observable == 'eeZH_FCCee365':
                k_ZH_365_central_value = np.sqrt(float(columns[2]))
            elif observable == "deltalHHH_HLLHC":
                lmbd = float(columns[2]) + 1

    print(k_ZH_240_central_value)
    print(k_ZH_365_central_value)
    print(lmbd)


if not os.path.isfile(output_file):
    with open(file=output_file, mode="w") as outfile:
        line = f"k_ZH_240,k_ZH_365_central_value,lmbd,CH,CHBox"
        print(line, file=outfile)

with open(file=output_file, mode="a") as outfile:
    line = f"{k_ZH_240_central_value},{k_ZH_365_central_value},{lmbd},{CH},{CHBox}"
    print(line, file=outfile)
