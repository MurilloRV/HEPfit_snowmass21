# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

import subprocess

# file_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/Z2SSM_BenchmarkPoint_fits_HLLHC_ILC_250"
file_dir = ""

kappas={}
# Definition of IDM benchmark point:
kappas['gg'] = 1.0

kappas['uu'] = 0.9948241544051786
kappas['dd'] = 0.9948241544051786
kappas['ss'] = 0.9948241544051786
kappas['cc'] = 0.9948241544051786
kappas['bb'] = 0.9948241544051786
kappas['tt'] = 0.9948241544051786
kappas['ee'] = 0.9948241544051786
kappas['mumu'] = 0.9948241544051786
kappas['tautau'] = 0.9948241544051786
kappas['ZZ_0'] = 0.9997204701950672
kappas['ZZ_125'] = 1.0005352707783095
kappas['ZZ_240'] = 1.0043116051768355
kappas['ZZ_365'] = 0.9995913581314864
kappas['ZZ_500'] = 0.9979970835336927
kappas['ZZ_550'] = 0.9976923094513526
kappas['ZZ'] = 1.0043116051768355
kappas['WW'] = 0.9997204701950672
kappas['lam'] = 1.854610413951624
kappas['gamgam'] = 0.9855492351284755
kappas['Zgam'] = 0.9946503745655421
Mw = 80.38279456975643
sin2thetaEff = 0.2313859052844633
GammaZ = 2.49575972859559

BrHinv = 0.
BrHexo = 0.

kappas2 = {}
for kappa in kappas.keys():
    kappas2[kappa] = kappas[kappa]**2


# Need to weigh the kappas to get the scaling factor for VBF
wgt_W_VBF = 10.
wgt_Z_VBF = 1.
kappas2["VBF_0"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_0"]) / (wgt_W_VBF + wgt_Z_VBF)
kappas2["VBF_125"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_125"]) / (wgt_W_VBF + wgt_Z_VBF)
kappas2["VBF_240"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_240"]) / (wgt_W_VBF + wgt_Z_VBF)
kappas2["VBF_365"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_365"]) / (wgt_W_VBF + wgt_Z_VBF)

# From HiggsTools, based on LHCHWG
BR_H_to_gg     = 0.08171987918280119
BR_H_to_WW     = 0.21699968783000312
BR_H_to_ZZ     = 0.0266699597333004
BR_H_to_Zga    = 0.0015499999844999998
BR_H_to_gaga   = 0.0022699999773
BR_H_to_mumu   = 0.00021649999783500005
BR_H_to_tautau = 0.0623999093760009
BR_H_to_cc     = 0.028759959712400404
BR_H_to_bb     = 0.5791991542080085
BR_H_to_ss     = 0.00021494999785050001  ## Check this!

total_rate = BR_H_to_gg     + \
             BR_H_to_WW     + \
             BR_H_to_ZZ     + \
             BR_H_to_Zga    + \
             BR_H_to_gaga   + \
             BR_H_to_mumu   + \
             BR_H_to_tautau + \
             BR_H_to_cc     + \
             BR_H_to_bb     + \
             BR_H_to_ss     ## Check this!
print(f"Total decay rate: {total_rate}")



kappas2["H"] = kappas2["gg"]*BR_H_to_gg         + \
               kappas2["WW"]*BR_H_to_WW         + \
               kappas2["ZZ_0"]*BR_H_to_ZZ     + \
               kappas2["Zgam"]*BR_H_to_Zga      + \
               kappas2["gamgam"]*BR_H_to_gaga   + \
               kappas2["mumu"]*BR_H_to_mumu     + \
               kappas2["tautau"]*BR_H_to_tautau + \
               kappas2["cc"]*BR_H_to_cc         + \
               kappas2["bb"]*BR_H_to_bb         + \
               kappas2["ss"]*BR_H_to_ss         ## Check this!

kappas2["H"] = kappas2["H"]/(1.0 - BrHinv - BrHexo)
print(f"kappa_H^2 = {kappas2["H"]}")



final_text = "#\n" + \
             "#\n" + \
             "# IDM Benchmark Point:\n"

for coup, kaps in kappas2.items():
    if coup=="lam":
        final_text = final_text + f"# kappas[{coup}] = {kappas[coup]}\n"
    else:
        final_text = final_text + f"# kappas2[{coup}] = {kaps}\n"
             

print(final_text)


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
                columns[8] = str(kappas2["ZZ_240"]*float(columns[8]))
                columns[9] = str(kappas2["ZZ_240"]*float(columns[9]))

            elif (columns[1].startswith("eeZHbb_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeHvvbb_")):
                columns[8] = str(kappas2["WW"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHcc_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["cc"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["cc"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHgg_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["gg"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["gg"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHWW_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHZZ_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["ZZ_0"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["ZZ_0"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHtautau_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHgaga_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHmumu_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHZga_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["Zgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["Zgam"]*float(columns[9])/kappas2["H"])

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
                columns[8] = str(kappas2["ZZ_365"]*float(columns[8]))
                columns[9] = str(kappas2["ZZ_365"]*float(columns[9]))


            elif (columns[1].startswith("eeZHbb_")):
                columns[8] = str(kappas2["ZZ_365"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_365"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeHvvbb_")):
                columns[8] = str(kappas2["WW"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["bb"]*float(columns[9])/kappas2["H"])


            elif (columns[1].startswith("eeZHcc_")):
                columns[8] = str(kappas2["ZZ_365"]*kappas2["cc"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_365"]*kappas2["cc"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeHvvcc_")):
                columns[8] = str(kappas2["WW"]*kappas2["cc"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["cc"]*float(columns[9])/kappas2["H"])


            elif (columns[1].startswith("eeZHgg_")):
                columns[8] = str(kappas2["ZZ_365"]*kappas2["gg"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_365"]*kappas2["gg"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeHvvgg_")):
                columns[8] = str(kappas2["WW"]*kappas2["gg"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["gg"]*float(columns[9])/kappas2["H"])


            elif (columns[1].startswith("eeZHWW_")):
                columns[8] = str(kappas2["ZZ_365"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_365"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeHvvWW_")):
                columns[8] = str(kappas2["WW"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["WW"]*float(columns[9])/kappas2["H"])


            elif (columns[1].startswith("eeZHZZ_")):
                columns[8] = str(kappas2["ZZ_365"]*kappas2["ZZ_0"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_365"]*kappas2["ZZ_0"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeHvvZZ_")):
                columns[8] = str(kappas2["WW"]*kappas2["ZZ_0"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["ZZ_0"]*float(columns[9])/kappas2["H"])


            elif (columns[1].startswith("eeZHtautau_")):
                columns[8] = str(kappas2["ZZ_365"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_365"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeHvvtautau_")):
                columns[8] = str(kappas2["WW"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])


            elif (columns[1].startswith("eeZHgaga_")):
                columns[8] = str(kappas2["ZZ_365"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_365"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeHvvgaga_")):
                columns[8] = str(kappas2["WW"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])


            elif (columns[1].startswith("eeZHmumu_")):
                columns[8] = str(kappas2["ZZ_365"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_365"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])


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
                columns[8] = str(kappas2["gg"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["gg"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHZZ4lHL")):
                columns[8] = str(kappas2["gg"]*kappas2["ZZ_0"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["gg"]*kappas2["ZZ_0"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHWW2l2vHL")):
                columns[8] = str(kappas2["gg"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["gg"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHtautauHL")):
                columns[8] = str(kappas2["gg"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["gg"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHbbHL")):
                columns[8] = str(kappas2["gg"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["gg"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHmumuHL")):
                columns[8] = str(kappas2["gg"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["gg"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHZgaHL")):
                columns[8] = str(kappas2["gg"]*kappas2["Zgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["gg"]*kappas2["Zgam"]*float(columns[9])/kappas2["H"])


            # VBF
            elif (columns[1].startswith("muVBFgagaHL")):
                columns[8] = str(kappas2["VBF_0"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_0"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muVBFZZ4lHL")):
                columns[8] = str(kappas2["VBF_0"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_0"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muVBFWW2l2vHL")):
                columns[8] = str(kappas2["VBF_0"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_0"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muVBFtautauHL")):
                columns[8] = str(kappas2["VBF_0"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_0"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muVBFmumuHL")):
                columns[8] = str(kappas2["VBF_0"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_0"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muVBFZgaHL")):
                columns[8] = str(kappas2["VBF_0"]*kappas2["Zgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_0"]*kappas2["Zgam"]*float(columns[9])/kappas2["H"])



            # WH
            elif (columns[1].startswith("muWHgagaHL")):
                columns[8] = str(kappas2["WW"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muWHZZ4lHL")):
                columns[8] = str(kappas2["WW"]*kappas2["ZZ_0"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["ZZ_0"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muWHWW2l2vHL")):
                columns[8] = str(kappas2["WW"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muWHbbHL")):
                columns[8] = str(kappas2["WW"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["bb"]*float(columns[9])/kappas2["H"])



            # ZH
            elif (columns[1].startswith("muZHgagaHL")):
                columns[8] = str(kappas2["ZZ_0"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_0"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muZHZZ4lHL")):
                columns[8] = str(kappas2["ZZ_0"]*kappas2["ZZ_0"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_0"]*kappas2["ZZ_0"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muZHWW2l2vHL")):
                columns[8] = str(kappas2["ZZ_0"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_0"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muZHbbHL")):
                columns[8] = str(kappas2["ZZ_0"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_0"]*kappas2["bb"]*float(columns[9])/kappas2["H"])




            # ttH
            elif (columns[1].startswith("muttHgaga")):
                columns[8] = str(kappas2["tt"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["tt"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muttHZZ4lHL")):
                columns[8] = str(kappas2["tt"]*kappas2["ZZ_0"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["tt"]*kappas2["ZZ_0"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muttHWW2l2vHL")):
                columns[8] = str(kappas2["tt"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["tt"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muttHbbHL")):
                columns[8] = str(kappas2["tt"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["tt"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muttHtautauHL")):
                columns[8] = str(kappas2["tt"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["tt"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

            # Rejoin the columns and write to the output file
            outfile.write(" ".join(columns) + "\n")
        else:
            # Write unmodified lines to the output file
            outfile.write(line)

with open(output_file_HLLHC, 'a') as outfile:
    outfile.write(final_text)

print(f"Modified content saved to {output_file_HLLHC}.")





# ###########################################################################################
# ###########################################################################################
# ###################################   kappa_lambda   ######################################
# ###########################################################################################
# ###########################################################################################

# # Open the e+e- collider input file in read mode and output file in write mode
# input_file =  "ObservablesHiggs.conf"
# output_file = "ObservablesHiggs_scaled.conf"

# with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
#     for line in infile:
#         if line.startswith("Observable"):
#             # Split the line into columns by whitespace
#             columns = line.split()
            
#             if (columns[2].startswith("deltalHHH")):
#                 columns[8] = str(kappas['lam']-1)
#                 columns[9] = str(kappas['lam']*0.5)

#             # Rejoin the columns and write to the output file
#             outfile.write(" ".join(columns) + "\n")
#         else:
#             # Write unmodified lines to the output file
#             outfile.write(line)

# with open(output_file, 'a') as outfile:
#     outfile.write(final_text)

# print(f"Modified content saved to {output_file}.")

# subprocess.run(["mv", output_file, input_file])




###########################################################################################
###########################################################################################
#######################################   EWPOs   #########################################
###########################################################################################
###########################################################################################

input_files =  [# "ObservablesEW_Current_SM_noLFU.conf",
               "ObservablesEW_HLLHC.conf",
               "ObservablesEW_FCCee_WW_SM.conf",
               "ObservablesEW_FCCee_Zpole_SM.conf",
               ]

output_files = [# "ObservablesEW_Current_SM_noLFU_kappa_scaled.conf",
               "ObservablesEW_HLLHC_kappa_scaled.conf",
               "ObservablesEW_FCCee_WW_SM_kappa_scaled.conf",
               "ObservablesEW_FCCee_Zpole_SM_kappa_scaled.conf",
              ]

for input_file, output_file in zip(input_files, output_files):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
                if (columns[2].startswith("GammaZ")):
                    columns[8] = str(GammaZ)

                elif (columns[2].startswith("Mw")):
                    columns[8] = str(Mw)

                # Rejoin the columns and write to the output file
                outfile.write(" ".join(columns) + "\n")
            else:
                # Write unmodified lines to the output file
                outfile.write(line)

    with open(output_file, 'a') as outfile:
        outfile.write(final_text)

    print(f"Modified content saved to {output_file}.")

