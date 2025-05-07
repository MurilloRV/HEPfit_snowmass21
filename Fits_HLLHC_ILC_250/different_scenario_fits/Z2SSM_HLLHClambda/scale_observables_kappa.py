# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

# file_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/Z2SSM_BenchmarkPoint_fits_HLLHC_ILC_250"
file_dir = ""

# Definition of benchmark point:
# Z2SSM case:
points = [(1.801875586, 1 - 0.002789967621), (2.482538926, 1 - 0.004239875933)]
point = points[1]
kappas = {}
kappas["Lam"] = point[0]
for kappa in ['WW', 'ZZ', 'gg', 'gamgam', 'Zgam', 'cc', 'tt', 'bb', 'mumu', 'tautau']:
        kappas[kappa] = point[1]

# Need to weigh the kappas to get the scaling factor for VBF
wgt_W_VBF = 10.
wgt_Z_VBF = 1.
kappas["VBF"] = (wgt_W_VBF*kappas["WW"] + wgt_Z_VBF*kappas["ZZ"]) / (wgt_W_VBF + wgt_Z_VBF)



# Open the e+e- collider input file in read mode and output file in write mode
input_file_ee =  "ObservablesHiggs_ILC_250_SM.conf"
output_file_ee = "ObservablesHiggs_ILC_250_SM_kappa_scaled.conf"


with open(input_file_ee, 'r') as infile, open(output_file_ee, 'w') as outfile:
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

print(f"Modified content saved to {output_file_ee}.")





# Open the HL-LHC input file in read mode and output file in write mode
input_file_HLLHC =  "ObservablesHiggs_HLLHC_SM.conf"
output_file_HLLHC = "ObservablesHiggs_HLLHC_SM_kappa_scaled.conf"


with open(input_file_HLLHC, 'r') as infile, open(output_file_HLLHC, 'w') as outfile:
    for line in infile:
        if line.startswith("Observable"):
            # Split the line into columns by whitespace
            columns = line.split()

            # ggF
            if (columns[1].startswith("muggHgagaHL")):
                columns[8] = str(kappas["gg"]*kappas["gamgam"]*float(columns[8]))
                columns[9] = str(kappas["gg"]*kappas["gamgam"]*float(columns[9]))

            elif (columns[1].startswith("muggHZZ4lHL")):
                columns[8] = str(kappas["gg"]*kappas["ZZ"]*float(columns[8]))
                columns[9] = str(kappas["gg"]*kappas["ZZ"]*float(columns[9]))

            elif (columns[1].startswith("muggHWW2l2vHL")):
                columns[8] = str(kappas["gg"]*kappas["WW"]*float(columns[8]))
                columns[9] = str(kappas["gg"]*kappas["WW"]*float(columns[9]))

            elif (columns[1].startswith("muggHtautauHL")):
                columns[8] = str(kappas["gg"]*kappas["tautau"]*float(columns[8]))
                columns[9] = str(kappas["gg"]*kappas["tautau"]*float(columns[9]))

            elif (columns[1].startswith("muggHbbHL")):
                columns[8] = str(kappas["gg"]*kappas["bb"]*float(columns[8]))
                columns[9] = str(kappas["gg"]*kappas["bb"]*float(columns[9]))

            elif (columns[1].startswith("muggHmumuHL")):
                columns[8] = str(kappas["gg"]*kappas["mumu"]*float(columns[8]))
                columns[9] = str(kappas["gg"]*kappas["mumu"]*float(columns[9]))

            elif (columns[1].startswith("muggHZgaHL")):
                columns[8] = str(kappas["gg"]*kappas["Zgam"]*float(columns[8]))
                columns[9] = str(kappas["gg"]*kappas["Zgam"]*float(columns[9]))


            # VBF
            elif (columns[1].startswith("muVBFgagaHL")):
                columns[8] = str(kappas["VBF"]*kappas["gamgam"]*float(columns[8]))
                columns[9] = str(kappas["VBF"]*kappas["gamgam"]*float(columns[9]))

            elif (columns[1].startswith("muVBFZZ4lHL")):
                columns[8] = str(kappas["VBF"]*kappas["ZZ"]*float(columns[8]))
                columns[9] = str(kappas["VBF"]*kappas["ZZ"]*float(columns[9]))

            elif (columns[1].startswith("muVBFWW2l2vHL")):
                columns[8] = str(kappas["VBF"]*kappas["WW"]*float(columns[8]))
                columns[9] = str(kappas["VBF"]*kappas["WW"]*float(columns[9]))

            elif (columns[1].startswith("muVBFtautauHL")):
                columns[8] = str(kappas["VBF"]*kappas["tautau"]*float(columns[8]))
                columns[9] = str(kappas["VBF"]*kappas["tautau"]*float(columns[9]))

            elif (columns[1].startswith("muVBFmumuHL")):
                columns[8] = str(kappas["VBF"]*kappas["mumu"]*float(columns[8]))
                columns[9] = str(kappas["VBF"]*kappas["mumu"]*float(columns[9]))

            elif (columns[1].startswith("muVBFZgaHL")):
                columns[8] = str(kappas["VBF"]*kappas["Zgam"]*float(columns[8]))
                columns[9] = str(kappas["VBF"]*kappas["Zgam"]*float(columns[9]))



            # WH
            elif (columns[1].startswith("muWHgagaHL")):
                columns[8] = str(kappas["WW"]*kappas["gamgam"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["gamgam"]*float(columns[9]))

            elif (columns[1].startswith("muWHZZ4lHL")):
                columns[8] = str(kappas["WW"]*kappas["ZZ"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["ZZ"]*float(columns[9]))

            elif (columns[1].startswith("muWHWW2l2vHL")):
                columns[8] = str(kappas["WW"]*kappas["WW"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["WW"]*float(columns[9]))

            elif (columns[1].startswith("muWHbbHL")):
                columns[8] = str(kappas["WW"]*kappas["bb"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["bb"]*float(columns[9]))



            # ZH
            elif (columns[1].startswith("muZHgagaHL")):
                columns[8] = str(kappas["ZZ"]*kappas["gamgam"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["gamgam"]*float(columns[9]))

            elif (columns[1].startswith("muZHZZ4lHL")):
                columns[8] = str(kappas["ZZ"]*kappas["ZZ"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["ZZ"]*float(columns[9]))

            elif (columns[1].startswith("muZHWW2l2vHL")):
                columns[8] = str(kappas["WW"]*kappas["WW"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["WW"]*float(columns[9]))

            elif (columns[1].startswith("muZHbbHL")):
                columns[8] = str(kappas["ZZ"]*kappas["bb"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["bb"]*float(columns[9]))




            # ttH
            elif (columns[1].startswith("muttHgaga")):
                columns[8] = str(kappas["tt"]*kappas["gamgam"]*float(columns[8]))
                columns[9] = str(kappas["tt"]*kappas["gamgam"]*float(columns[9]))

            elif (columns[1].startswith("muttHZZ4lHL")):
                columns[8] = str(kappas["tt"]*kappas["ZZ"]*float(columns[8]))
                columns[9] = str(kappas["tt"]*kappas["ZZ"]*float(columns[9]))

            elif (columns[1].startswith("muttHWW2l2vHL")):
                columns[8] = str(kappas["tt"]*kappas["WW"]*float(columns[8]))
                columns[9] = str(kappas["tt"]*kappas["WW"]*float(columns[9]))

            elif (columns[1].startswith("muttHbbHL")):
                columns[8] = str(kappas["tt"]*kappas["bb"]*float(columns[8]))
                columns[9] = str(kappas["tt"]*kappas["bb"]*float(columns[9]))

            elif (columns[1].startswith("muttHtautauHL")):
                columns[8] = str(kappas["tt"]*kappas["tautau"]*float(columns[8]))
                columns[9] = str(kappas["tt"]*kappas["tautau"]*float(columns[9]))

            # Rejoin the columns and write to the output file
            outfile.write(" ".join(columns) + "\n")
        else:
            # Write unmodified lines to the output file
            outfile.write(line)

print(f"Modified content saved to {output_file_HLLHC}.")
