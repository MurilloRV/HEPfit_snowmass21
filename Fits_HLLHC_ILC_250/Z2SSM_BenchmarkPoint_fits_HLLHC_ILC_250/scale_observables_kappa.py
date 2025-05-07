# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

# Open the input file in read mode and output file in write mode
file_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/Z2SSM_BenchmarkPoint_fits_HLLHC_ILC_250"
input_file =  "ObservablesHiggs_ILC_250_SM.conf"
output_file = "ObservablesHiggs_ILC_250_SM_kappa_scaled.conf"

# Definition of benchmark point:
# Z2SSM case:
points = [(1.801875586, 1 - 0.002789967621), (2.482538926, 1 - 0.004239875933)]
point = points[1]
kappas = {}
kappas["Lam"] = point[0]
for kappa in ['WW', 'ZZ', 'gg', 'gamgam', 'Zgam', 'cc', 'tt', 'bb', 'mumu', 'tautau']:
        kappas[kappa] = point[1]


with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        if line.startswith("Observable"):
            # Split the line into columns by whitespace
            columns = line.split()
            
            if (columns[1].startswith("eeZH_")):
                columns[8] = str(kappas["ZZ"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*float(columns[9]))

            elif (columns[1].startswith("eeZHbb_")):
                columns[8] = str(kappas["ZZ"]*kappas["bb"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["bb"]*float(columns[9]))

            elif (columns[1].startswith("eeHvvbb_")):
                columns[8] = str(kappas["WW"]*kappas["bb"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["bb"]*float(columns[9]))

            elif (columns[1].startswith("eeZHcc_")):
                columns[8] = str(kappas["ZZ"]*kappas["cc"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["cc"]*float(columns[9]))

            elif (columns[1].startswith("eeZHgg_")):
                columns[8] = str(kappas["ZZ"]*kappas["gg"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["gg"]*float(columns[9]))

            elif (columns[1].startswith("eeZHWW_")):
                columns[8] = str(kappas["ZZ"]*kappas["WW"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["WW"]*float(columns[9]))

            elif (columns[1].startswith("eeZHtautau_")):
                columns[8] = str(kappas["ZZ"]*kappas["tautau"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["tautau"]*float(columns[9]))

            elif (columns[1].startswith("eeZHZZ_")):
                columns[8] = str(kappas["ZZ"]*kappas["ZZ"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["ZZ"]*float(columns[9]))

            elif (columns[1].startswith("eeZHgaga_")):
                columns[8] = str(kappas["ZZ"]*kappas["gamgam"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["gamgam"]*float(columns[9]))

            elif (columns[1].startswith("eeZHmumu_")):
                columns[8] = str(kappas["ZZ"]*kappas["mumu"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["mumu"]*float(columns[9]))

            # Rejoin the columns and write to the output file
            outfile.write(" ".join(columns) + "\n")
        else:
            # Write unmodified lines to the output file
            outfile.write(line)

print(f"Processing complete. Modified content saved to {output_file}.")
