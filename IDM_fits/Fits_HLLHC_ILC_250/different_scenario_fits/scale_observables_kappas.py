# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

import subprocess
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scenario", help = "Name of the scenario (e.g. IDM_HLLHClambda)", type=str)
parser.add_argument("-b", "--bp", help = "Which benchmark point to use", type=str)
parser.add_argument("--noHLLHClambda", help = "No on-shell kappa_lambda constraint", action="store_true")




args = parser.parse_args()
scenario = args.scenario
BP = args.bp
noHLLHClambda = args.noHLLHClambda


# file_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/Z2SSM_BenchmarkPoint_fits_HLLHC_ILC_250"
file_dir = scenario


kappas={}
# Definition of IDM benchmark point:
kappas['gg'] = 1.0

if BP == "BP_0":
    kappas['uu'] = 0.9951626506866794
    kappas['dd'] = 0.9951626506866794
    kappas['ss'] = 0.9951626506866794
    kappas['cc'] = 0.9951626506866794
    kappas['bb'] = 0.9951626506866794
    kappas['tt'] = 0.9951626506866794
    kappas['ee'] = 0.9951626506866794
    kappas['mumu'] = 0.9951626506866794
    kappas['tautau'] = 0.9951626506866794
    kappas['ZZ_0'] = 1.0010507073661603
    kappas['ZZ_125'] = 1.0017203173897145
    kappas['ZZ_240'] = 1.0047983817820756
    kappas['ZZ_365'] = 1.0010602943645246
    kappas['ZZ_500'] = 0.9998784421726016
    kappas['ZZ_550'] = 0.9996800012459942
    kappas['ZZ'] = 0.9977727886031684
    kappas['WW'] = 0.9977727886031684
    kappas['lam'] = 1.6885444220830157
    kappas['gamgam'] = 0.9851119781939329
    kappas['Zgam'] = 0.9944879991522521
    Mw = 80.35709227008113
    sin2thetaEff = 0.2315235058034713
    GammaZ = 2.4943351053320364

elif BP == "BP_1":
    kappas['uu'] = 0.9958390244744362
    kappas['dd'] = 0.9958390244744362
    kappas['ss'] = 0.9958390244744362
    kappas['cc'] = 0.9958390244744362
    kappas['bb'] = 0.9958390244744362
    kappas['tt'] = 0.9958390244744362
    kappas['ee'] = 0.9958390244744362
    kappas['mumu'] = 0.9958390244744362
    kappas['tautau'] = 0.9958390244744362
    kappas['ZZ_0'] = 0.9994255438865846
    kappas['ZZ_125'] = 0.9999361910463384
    kappas['ZZ_240'] = 1.0022422066243255
    kappas['ZZ_365'] = 0.9996205177104408
    kappas['ZZ_500'] = 0.9989265161483839
    kappas['ZZ_550'] = 0.9988588243740757
    kappas['ZZ'] = 0.996321215883244
    kappas['WW'] = 0.996321215883244
    kappas['lam'] = 1.5026696187124242
    kappas['gamgam'] = 0.9851069592761637
    kappas['Zgam'] = 0.9944857943543188
    Mw = 80.36739334215532
    sin2thetaEff = 0.2314690313111513
    GammaZ = 2.4949079898251485

elif BP == "BP_2":
    kappas['uu'] = 0.989299511791139
    kappas['dd'] = 0.989299511791139
    kappas['ss'] = 0.989299511791139
    kappas['cc'] = 0.989299511791139
    kappas['bb'] = 0.989299511791139
    kappas['tt'] = 0.989299511791139
    kappas['ee'] = 0.989299511791139
    kappas['mumu'] = 0.989299511791139
    kappas['tautau'] = 0.989299511791139
    kappas['ZZ_0'] = 1.0002280615561772
    kappas['ZZ_125'] = 1.001430994535743
    kappas['ZZ_240'] = 1.0065580594688865
    kappas['ZZ_365'] = 1.0024068502567152
    kappas['ZZ_500'] = 1.0032396772504224
    kappas['ZZ_550'] = 1.004624907009377
    kappas['ZZ'] = 0.9925701786469326
    kappas['WW'] = 0.9925701786469326
    kappas['lam'] = 2.003326933459748
    kappas['gamgam'] = 0.9506442575856744
    kappas['Zgam'] = 0.9816896759319687
    Mw = 80.3668190104635
    sin2thetaEff = 0.2314412660974903
    GammaZ = 2.494754604553479

elif BP == "BP_3":
    kappas['uu'] = 0.989299511791139
    kappas['dd'] = 0.989299511791139
    kappas['ss'] = 0.989299511791139
    kappas['cc'] = 0.989299511791139
    kappas['bb'] = 0.989299511791139
    kappas['tt'] = 0.989299511791139
    kappas['ee'] = 0.989299511791139
    kappas['mumu'] = 0.989299511791139
    kappas['tautau'] = 0.989299511791139
    kappas['ZZ_0'] = 1.0002280615561772
    kappas['ZZ_125'] = 1.001430994535743
    kappas['ZZ_240'] = 1.0065580594688865
    kappas['ZZ_365'] = 1.0024068502567152
    kappas['ZZ_500'] = 1.0032396772504224
    kappas['ZZ_550'] = 1.004624907009377
    kappas['ZZ'] = 0.9925701786469326
    kappas['WW'] = 0.9925701786469326
    kappas['lam'] = 2.003326933459748
    kappas['gamgam'] = 0.9506442575856744
    kappas['Zgam'] = 0.9816896759319687
    Mw = 80.3668190104635
    sin2thetaEff = 0.2314412660974903
    GammaZ = 2.494754604553479

elif BP == "BP_4":
    kappas['uu'] = 0.9922066823296164
    kappas['dd'] = 0.9922066823296164
    kappas['ss'] = 0.9922066823296164
    kappas['cc'] = 0.9922066823296164
    kappas['bb'] = 0.9922066823296164
    kappas['tt'] = 0.9922066823296164
    kappas['ee'] = 0.9922066823296164
    kappas['mumu'] = 0.9922066823296164
    kappas['tautau'] = 0.9922066823296164
    kappas['ZZ_0'] = 0.9995440099827713
    kappas['ZZ_125'] = 1.0003009582425018
    kappas['ZZ_240'] = 1.0033105386486372
    kappas['ZZ_365'] = 1.002154474320703
    kappas['ZZ_500'] = 1.004902605630624
    kappas['ZZ_550'] = 1.006775403556579
    kappas['ZZ'] = 0.9952035995782093
    kappas['WW'] = 0.9952035995782093
    kappas['lam'] = 1.5027312712751126
    kappas['gamgam'] = 0.9511673913600965
    kappas['Zgam'] = 0.9818672684619811
    Mw = 80.35935286139284
    sin2thetaEff = 0.2314822952404524
    GammaZ = 2.494346193565529

elif BP == "BP_5":
    kappas['uu'] = 0.9922066823296164
    kappas['dd'] = 0.9922066823296164
    kappas['ss'] = 0.9922066823296164
    kappas['cc'] = 0.9922066823296164
    kappas['bb'] = 0.9922066823296164
    kappas['tt'] = 0.9922066823296164
    kappas['ee'] = 0.9922066823296164
    kappas['mumu'] = 0.9922066823296164
    kappas['tautau'] = 0.9922066823296164
    kappas['ZZ_0'] = 0.9995440099827713
    kappas['ZZ_125'] = 1.0003009582425018
    kappas['ZZ_240'] = 1.0033105386486372
    kappas['ZZ_365'] = 1.002154474320703
    kappas['ZZ_500'] = 1.004902605630624
    kappas['ZZ_550'] = 1.006775403556579
    kappas['ZZ'] = 0.9952035995782093
    kappas['WW'] = 0.9952035995782093
    kappas['lam'] = 1.5027312712751126
    kappas['gamgam'] = 0.9511673913600965
    kappas['Zgam'] = 0.9818672684619811
    Mw = 80.35935286139284
    sin2thetaEff = 0.2314822952404524
    GammaZ = 2.494346193565529

elif BP == "BP_6":
    kappas['uu'] = 0.9978323657528287
    kappas['dd'] = 0.9978323657528287
    kappas['ss'] = 0.9978323657528287
    kappas['cc'] = 0.9978323657528287
    kappas['bb'] = 0.9978323657528287
    kappas['tt'] = 0.9978323657528287
    kappas['ee'] = 0.9978323657528287
    kappas['mumu'] = 0.9978323657528287
    kappas['tautau'] = 0.9978323657528287
    kappas['ZZ_0'] = 0.9989074954614838
    kappas['ZZ_125'] = 0.9991097228230613
    kappas['ZZ_240'] = 0.9999996031219985
    kappas['ZZ_365'] = 0.9990889923416056
    kappas['ZZ_500'] = 0.9989275368970878
    kappas['ZZ_550'] = 0.9989456807488839
    kappas['ZZ'] = 0.9974486740906632
    kappas['WW'] = 0.9974486740906632
    kappas['lam'] = 1.186487087345143
    kappas['gamgam'] = 0.9901556377306285
    kappas['Zgam'] = 0.9963555931330301
    Mw = 80.38104920223586
    sin2thetaEff = 0.2313970261227002
    GammaZ = 2.4956694257811467

elif BP == "BP_7":
    kappas['uu'] = 0.9977913809334535
    kappas['dd'] = 0.9977913809334535
    kappas['ss'] = 0.9977913809334535
    kappas['cc'] = 0.9977913809334535
    kappas['bb'] = 0.9977913809334535
    kappas['tt'] = 0.9977913809334535
    kappas['ee'] = 0.9977913809334535
    kappas['mumu'] = 0.9977913809334535
    kappas['tautau'] = 0.9977913809334535
    kappas['ZZ_0'] = 0.9991459359567888
    kappas['ZZ_125'] = 0.9993645365894596
    kappas['ZZ_240'] = 1.0003413776807617
    kappas['ZZ_365'] = 0.9992744901911946
    kappas['ZZ_500'] = 0.9990253374763355
    kappas['ZZ_550'] = 0.9990148782978254
    kappas['ZZ'] = 0.9976893468388027
    kappas['WW'] = 0.9976893468388027
    kappas['lam'] = 1.2096708258013975
    kappas['gamgam'] = 0.9907353484177382
    kappas['Zgam'] = 0.9965703869084765
    Mw = 80.38143366266203
    sin2thetaEff = 0.2313950375810892
    GammaZ = 2.4956912542658984

else:
    raise ValueError("Could not determine benchmark point!")



# kappas['uu'] = 0.9948241544051786
# kappas['dd'] = 0.9948241544051786
# kappas['ss'] = 0.9948241544051786
# kappas['cc'] = 0.9948241544051786
# kappas['bb'] = 0.9948241544051786
# kappas['tt'] = 0.9948241544051786
# kappas['ee'] = 0.9948241544051786
# kappas['mumu'] = 0.9948241544051786
# kappas['tautau'] = 0.9948241544051786
# kappas['ZZ_0'] = 0.9997204701950672
# kappas['ZZ_125'] = 1.0005352707783095
# kappas['ZZ_240'] = 1.0043116051768355
# kappas['ZZ_365'] = 0.9995913581314864
# kappas['ZZ_500'] = 0.9979970835336927
# kappas['ZZ_550'] = 0.9976923094513526
# kappas['ZZ'] = 1.0043116051768355
# kappas['WW'] = 0.9997204701950672
# kappas['lam'] = 1.854610413951624
# kappas['gamgam'] = 0.9855492351284755
# kappas['Zgam'] = 0.9946503745655421
# Mw = 80.38279456975643
# sin2thetaEff = 0.2313859052844633
# GammaZ = 2.49575972859559

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
###################################   ILC at 250 GeV   ####################################
###########################################################################################
###########################################################################################

# Open the e+e- collider input file in read mode and output file in write mode
input_file_ee = file_dir + "/ObservablesHiggs_ILC_250_SM.conf"
output_file_ILC_250 = file_dir + "/ObservablesHiggs_ILC_250_SM_kappa_scaled.conf"


with open(input_file_ee, 'r') as infile, open(output_file_ILC_250, 'w') as outfile:
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

            elif (columns[1].startswith("eeZHtautau_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHZZ_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["ZZ_0"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["ZZ_0"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHgaga_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHmumu_")):
                columns[8] = str(kappas2["ZZ_240"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_240"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])

            # Rejoin the columns and write to the output file
            outfile.write(" ".join(columns) + "\n")
        else:
            # Write unmodified lines to the output file
            outfile.write(line)

with open(output_file_ILC_250, 'a') as outfile:
    outfile.write(final_text)

print(f"Modified content saved to {output_file_ILC_250}.")




###########################################################################################
###########################################################################################
######################################   HL-HLC   #########################################
###########################################################################################
###########################################################################################


# Open the HL-LHC input file in read mode and output file in write mode
input_file_HLLHC = file_dir + "/ObservablesHiggs_HLLHC_SM.conf"
output_file_HLLHC = file_dir + "/ObservablesHiggs_HLLHC_SM_kappa_scaled.conf"


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
                columns[8] = str(kappas2["VBF_0"]*kappas2["ZZ_0"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_0"]*kappas2["ZZ_0"]*float(columns[9])/kappas2["H"])

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






###########################################################################################
###########################################################################################
###################################   kappa_lambda   ######################################
###########################################################################################
###########################################################################################

if not noHLLHClambda:

    # Open the e+e- collider input file in read mode and output file in write mode
    input_file =  file_dir + "/ObservablesHiggs.conf"
    output_file = file_dir + "/ObservablesHiggs_scaled.conf"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
                if (columns[2].startswith("deltalHHH")):
                    columns[8] = str(kappas['lam']-1)
                    columns[9] = str(kappas['lam']*0.5)

                # Rejoin the columns and write to the output file
                outfile.write(" ".join(columns) + "\n")
            else:
                # Write unmodified lines to the output file
                outfile.write(line)

    with open(output_file, 'a') as outfile:
        outfile.write(final_text)

    print(f"Modified content saved to {output_file}.")

    subprocess.run(["mv", output_file, input_file])




###########################################################################################
###########################################################################################
#######################################   EWPOs   #########################################
###########################################################################################
###########################################################################################

# Open the e+e- collider input file in read mode and output file in write mode
input_files =  [# "ObservablesEW_Current_SM_noLFU.conf",
               file_dir + "/ObservablesEW_HLLHC.conf",
               file_dir + "/ObservablesEW_ILC_250_SM.conf",
              ]

output_files = [# "ObservablesEW_Current_SM_noLFU_kappa_scaled.conf",
               file_dir + "/ObservablesEW_HLLHC_kappa_scaled.conf",
               file_dir + "/ObservablesEW_ILC_250_SM_kappa_scaled.conf",
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



