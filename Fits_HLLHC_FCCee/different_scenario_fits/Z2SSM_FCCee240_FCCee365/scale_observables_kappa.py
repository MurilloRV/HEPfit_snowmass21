# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

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

final_text = "#\n" + \
             "#\n" + \
             "# Z2SSM Benchmark Point:\n" + \
             f"# kappa_lambda = {kappas["Lam"]}\n" + \
             f"# kappa_Z = 1 - {1 - kappas["ZZ"]} = {kappas["ZZ"]}\n" + \
             f"# kappa_Z**2 = {kappas["ZZ"]**2}\n" + \
             f"# k_Z = k_W = k_Zgam = k_g = k_gam = k_f\n"





###########################################################################################
###########################################################################################
#################################   FCC-ee at 240 GeV   ###################################
###########################################################################################
###########################################################################################

# Open the FCCee_240 input file in read mode and output file in write mode
input_file_FCCee240 =  "ObservablesHiggs_FCCee_240_SM.conf"
output_file_FCCee240 = "ObservablesHiggs_FCCee_240_SM_kappa_scaled.conf"


with open(input_file_FCCee240, 'r') as infile, open(output_file_FCCee240, 'w') as outfile:
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

            elif (columns[1].startswith("eeZHZZ_")):
                columns[8] = str(kappas["ZZ"]*kappas["ZZ"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["ZZ"]*float(columns[9]))

            elif (columns[1].startswith("eeZHtautau_")):
                columns[8] = str(kappas["ZZ"]*kappas["tautau"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["tautau"]*float(columns[9]))

            elif (columns[1].startswith("eeZHgaga_")):
                columns[8] = str(kappas["ZZ"]*kappas["gamgam"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["gamgam"]*float(columns[9]))

            elif (columns[1].startswith("eeZHmumu_")):
                columns[8] = str(kappas["ZZ"]*kappas["mumu"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["mumu"]*float(columns[9]))

            elif (columns[1].startswith("eeZHZga_")):
                columns[8] = str(kappas["ZZ"]*kappas["Zgam"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["Zgam"]*float(columns[9]))

            # Rejoin the columns and write to the output file
            outfile.write(" ".join(columns) + "\n")
        else:
            # Write unmodified lines to the output file
            outfile.write(line)

with open(output_file_FCCee240, 'a') as outfile:
    outfile.write(final_text)

# Z2SSM Benchmark Point:
# kappa_lambda = 2.482538926
# kappa_Z = 1 - 0.004239875933 = 0.995760124067
# kappa_Z**2 = 0.9915382246819272
# k_Z = k_W = k_Zgam = k_g = k_gam = k_f
#

print(f"Modified content saved to {output_file_FCCee240}.")






###########################################################################################
###########################################################################################
#################################   FCC-ee at 365 GeV   ###################################
###########################################################################################
###########################################################################################

# Open the FCCee_365 input file in read mode and output file in write mode
input_file_FCCee365 =  "ObservablesHiggs_FCCee_365.conf"
output_file_FCCee365 = "ObservablesHiggs_FCCee_365_kappa_scaled.conf"


with open(input_file_FCCee365, 'r') as infile, open(output_file_FCCee365, 'w') as outfile:
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

            elif (columns[1].startswith("eeHvvcc_")):
                columns[8] = str(kappas["WW"]*kappas["cc"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["cc"]*float(columns[9]))


            elif (columns[1].startswith("eeZHgg_")):
                columns[8] = str(kappas["ZZ"]*kappas["gg"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["gg"]*float(columns[9]))

            elif (columns[1].startswith("eeHvvgg_")):
                columns[8] = str(kappas["WW"]*kappas["gg"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["gg"]*float(columns[9]))


            elif (columns[1].startswith("eeZHWW_")):
                columns[8] = str(kappas["ZZ"]*kappas["WW"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["WW"]*float(columns[9]))

            elif (columns[1].startswith("eeHvvWW_")):
                columns[8] = str(kappas["WW"]*kappas["WW"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["WW"]*float(columns[9]))


            elif (columns[1].startswith("eeZHZZ_")):
                columns[8] = str(kappas["ZZ"]*kappas["ZZ"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["ZZ"]*float(columns[9]))

            elif (columns[1].startswith("eeHvvZZ_")):
                columns[8] = str(kappas["WW"]*kappas["ZZ"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["ZZ"]*float(columns[9]))


            elif (columns[1].startswith("eeZHtautau_")):
                columns[8] = str(kappas["ZZ"]*kappas["tautau"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["tautau"]*float(columns[9]))

            elif (columns[1].startswith("eeHvvtautau_")):
                columns[8] = str(kappas["WW"]*kappas["tautau"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["tautau"]*float(columns[9]))


            elif (columns[1].startswith("eeZHgaga_")):
                columns[8] = str(kappas["ZZ"]*kappas["gamgam"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["gamgam"]*float(columns[9]))

            elif (columns[1].startswith("eeHvvgaga_")):
                columns[8] = str(kappas["WW"]*kappas["gamgam"]*float(columns[8]))
                columns[9] = str(kappas["WW"]*kappas["gamgam"]*float(columns[9]))


            elif (columns[1].startswith("eeZHmumu_")):
                columns[8] = str(kappas["ZZ"]*kappas["mumu"]*float(columns[8]))
                columns[9] = str(kappas["ZZ"]*kappas["mumu"]*float(columns[9]))


            # Rejoin the columns and write to the output file
            outfile.write(" ".join(columns) + "\n")
        else:
            # Write unmodified lines to the output file
            outfile.write(line)

with open(output_file_FCCee365, 'a') as outfile:
    outfile.write(final_text)

print(f"Modified content saved to {output_file_FCCee365}.")






###########################################################################################
###########################################################################################
######################################   HL-HLC   #########################################
###########################################################################################
###########################################################################################


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

with open(output_file_HLLHC, 'a') as outfile:
    outfile.write(final_text)

print(f"Modified content saved to {output_file_HLLHC}.")
