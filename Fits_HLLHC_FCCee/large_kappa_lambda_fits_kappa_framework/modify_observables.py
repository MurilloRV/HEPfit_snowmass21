import copy
import subprocess
import numpy as np


# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

import argparse

# Initialize parser
parser = argparse.ArgumentParser()
# parser.add_argument("--noHLLHClambda", help = "No on-shell kappa_lambda constraint", action="store_true")
parser.add_argument("--realistic", help = "Use realistic, asymmetric uncertainties for the on-shell kappa_lambda measurement at HL-LHC", action="store_true")
parser.add_argument("--ewpos_all", help = "Modify also the EWPO central values for current observables", action="store_true")
parser.add_argument("--no_1L_BSM_sqrt_s", help = "Do not include momentum dependent BSM 1L corrections to Z->ZH", action="store_true")
parser.add_argument("--no_quad", help = "Do not include quadratic momentum dependent BSM 1L corrections to Z->ZH", action="store_true")


args = parser.parse_args()
# noHLLHClambda = args.noHLLHClambda
realistic_HL_LHC_k_lambda_uncertainties = args.realistic
modify_all_ewpos = args.ewpos_all
no_1L_BSM_sqrt_s = args.no_1L_BSM_sqrt_s
no_quad = args.no_quad


def scale_observables(lambda_scenario, file_dir, kappas, Mw, GammaZ):

    if no_1L_BSM_sqrt_s:
        raise NotImplementedError("This option is not valid!")
    
    if lambda_scenario.endswith("FCCee240_FCCee365_HLLHClambda"):
        scenario = "FCCee240_FCCee365_HLLHClambda"
    elif lambda_scenario.endswith("FCCee240_FCCee365_noHLLHClambda"):
        scenario = "FCCee240_FCCee365"
    else:
        raise ValueError("Invalid scenario name!")

    BrHinv = 0.
    BrHexo = 0.

    kappas2 = {}
    for kappa in kappas.keys():
        kappas2[kappa] = kappas[kappa]**2

    if no_quad:
        for kappa in ['ZZ_0', 'ZZ_240', 'ZZ_365', 'ZZ_500', 'ZZ_550', ]:
            kappas2[kappa] = 2*kappas[kappa] - 1
            # Only linear correction to the Z->ZH cross sections are included


    # Need to weigh the kappas to get the scaling factor for VBF
    wgt_W_VBF = 10.
    wgt_Z_VBF = 1.
    kappas2["VBF"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ"]) / (wgt_W_VBF + wgt_Z_VBF)
    kappas2["VBF_0"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_0"]) / (wgt_W_VBF + wgt_Z_VBF)
    # kappas2["VBF_125"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_125"]) / (wgt_W_VBF + wgt_Z_VBF)
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
    # BR_H_to_ss     = 0.00021494999785050001  ## No ss information

    total_rate = BR_H_to_gg     + \
                BR_H_to_WW     + \
                BR_H_to_ZZ     + \
                BR_H_to_Zga    + \
                BR_H_to_gaga   + \
                BR_H_to_mumu   + \
                BR_H_to_tautau + \
                BR_H_to_cc     + \
                BR_H_to_bb
                # BR_H_to_ss     ## No ss information
    print(f"Total decay rate: {total_rate}")



    kappas2["H_BR"] = kappas2["gg"]*BR_H_to_gg         + \
                      kappas2["WW"]*BR_H_to_WW         + \
                      kappas2["ZZ"]*BR_H_to_ZZ     + \
                      kappas2["Zgam"]*BR_H_to_Zga      + \
                      kappas2["gamgam"]*BR_H_to_gaga   + \
                      kappas2["mumu"]*BR_H_to_mumu     + \
                      kappas2["tautau"]*BR_H_to_tautau + \
                      kappas2["cc"]*BR_H_to_cc         + \
                      kappas2["bb"]*BR_H_to_bb
                    #   kappas2["ss"]*BR_H_to_ss         ## No ss information

    kappas2["H_"] = kappas2["H"]/(1.0 - BrHinv - BrHexo)
    print(f"kappa_H^2 (from GammaHRatio) = {kappas2["H"]}")
    print(f"kappa_H^2 (from kappas and BRs) = {kappas2["H_BR"]}")
    print(f"Difference = {kappas2["H"] - kappas2["H_BR"]}")


    final_text = ""
    final_text = "#\n" + \
                 "#\n" + \
                 "# IDM Benchmark Point:\n"

    # for coup, kaps in kappas2.items():
    #     if coup=="lam":
    #         final_text = final_text + f"# kappas[{coup}] = {kappas[coup]}\n"
    #     else:
    #         final_text = final_text + f"# kappas2[{coup}] = {kaps}\n"

    for coup, kaps in kappas.items():
        final_text = final_text + f"# kappas[{coup}] = {kaps}\n"
                
    print(final_text)


    ###########################################################################################
    ###########################################################################################
    #################################   FCC-ee at 240 GeV   ###################################
    ###########################################################################################
    ###########################################################################################

    # Open the FCCee_240 input file in read mode and output file in write mode
    input_file_FCCee240 =  file_dir + "ObservablesHiggs_FCCee_240_SM.conf"
    output_file_FCCee240 = file_dir + "ObservablesHiggs_FCCee_240_SM_kappa_scaled.conf"
    if no_1L_BSM_sqrt_s:
        output_file_FCCee240 = file_dir + "ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_1L_BSM_sqrt_s.conf"
    elif no_quad:
        output_file_FCCee240 = file_dir + "ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_quad.conf"

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
                    columns[8] = str(kappas2["ZZ_240"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_240"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

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


    print(f"Modified content saved to {output_file_FCCee240}.")






    ###########################################################################################
    ###########################################################################################
    #################################   FCC-ee at 365 GeV   ###################################
    ###########################################################################################
    ###########################################################################################

    if (scenario == "FCCee240_FCCee365" 
        or scenario == "FCCee240_FCCee365_HLLHClambda"):
        # Open the FCCee_365 input file in read mode and output file in write mode
        input_file_FCCee365 =  file_dir + "ObservablesHiggs_FCCee_365.conf"
        output_file_FCCee365 = file_dir + "ObservablesHiggs_FCCee_365_kappa_scaled.conf"
        if no_1L_BSM_sqrt_s:
            output_file_FCCee365 = file_dir + "ObservablesHiggs_FCCee_365_kappa_scaled_no_1L_BSM_sqrt_s.conf"
        elif no_quad:
            output_file_FCCee365 = file_dir + "ObservablesHiggs_FCCee_365_kappa_scaled_no_quad.conf"


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
                        columns[8] = str(kappas2["ZZ_365"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                        columns[9] = str(kappas2["ZZ_365"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

                    elif (columns[1].startswith("eeHvvZZ_")):
                        columns[8] = str(kappas2["WW"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                        columns[9] = str(kappas2["WW"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])


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
    input_file_HLLHC =  file_dir + "ObservablesHiggs_HLLHC_SM.conf"
    output_file_HLLHC = file_dir + "ObservablesHiggs_HLLHC_SM_kappa_scaled.conf"
    if no_1L_BSM_sqrt_s:
        output_file_HLLHC = file_dir + "ObservablesHiggs_HLLHC_SM_kappa_scaled_no_1L_BSM_sqrt_s.conf"
    if no_quad:
        output_file_HLLHC = file_dir + "ObservablesHiggs_HLLHC_SM_kappa_scaled_no_quad.conf"


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
                    columns[8] = str(kappas2["gg"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["gg"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

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
                    columns[8] = str(kappas2["VBF"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["VBF"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("muVBFZZ4lHL")):
                    columns[8] = str(kappas2["VBF"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["VBF"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("muVBFWW2l2vHL")):
                    columns[8] = str(kappas2["VBF"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["VBF"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("muVBFtautauHL")):
                    columns[8] = str(kappas2["VBF"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["VBF"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("muVBFmumuHL")):
                    columns[8] = str(kappas2["VBF"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["VBF"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("muVBFZgaHL")):
                    columns[8] = str(kappas2["VBF"]*kappas2["Zgam"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["VBF"]*kappas2["Zgam"]*float(columns[9])/kappas2["H"])



                # WH
                elif (columns[1].startswith("muWHgagaHL")):
                    columns[8] = str(kappas2["WW"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("muWHZZ4lHL")):
                    columns[8] = str(kappas2["WW"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

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
                    columns[8] = str(kappas2["ZZ_0"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_0"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

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
                    columns[8] = str(kappas2["tt"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["tt"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

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


    from scipy.interpolate import interp1d

    data_high = {
        "x":[-1.487,-0.986,-0.484,0.029,0.497,0.999,1.512,2.025,2.515,2.994,3.485,3.998,4.499,5.012,5.492,6.016,6.506,6.986,7.498,8.017],
        "y":[-1.091,-0.584,-0.022,0.486,1.02,1.688,2.437,4.922,5.056,5.029,5.109,5.269,5.51,5.831,6.205,6.579,7.033,7.488,7.915,8.423]
    }

    data_low = {
        "x":[-1.493,-0.987,-0.486,0.004,0.506,1.007,1.508,2.009,2.51,3.011,3.501,4.013,4.503,4.993,5.506,5.996,6.508,6.998,7.51,8.006],
        "y":[-1.893,-1.413,-0.933,-0.453,-0.027,0.453,0.853,1.227,1.493,1.733,1.893,1.92,1.92,2.187,4.56,5.253,5.867,6.48,7.013,7.547]
    }


    curve_high = interp1d(data_high["x"], data_high["y"], kind='linear', fill_value="extrapolate")
    curve_low = interp1d(data_low["x"], data_low["y"], kind='linear', fill_value="extrapolate")


    def uncertanties_high(lmbd):
        if lmbd < -1.5:
            lmbd = -1.5
        elif lmbd > 8.:
            lmbd = 8.
        sigma = (curve_high(lmbd) - lmbd)/2.
        return sigma

    def uncertanties_low(lmbd):
        if lmbd < -1.5:
            lmbd = -1.5
        elif lmbd > 8.:
            lmbd = 8.
        sigma = (lmbd - curve_low(lmbd))/2.
        return sigma

    if scenario == "FCCee240_FCCee365_HLLHClambda":
        # Open the e+e- collider input file in read mode and output file in write mode
        input_file =  file_dir + "ObservablesHiggs.conf"
        if not realistic_HL_LHC_k_lambda_uncertainties:
            output_file = file_dir + "ObservablesHiggs_scaled.conf"
        else:
            output_file = file_dir + "ObservablesHiggs_scaled_realistic_HL_LHC.conf"
        

        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if line.startswith("Observable"):
                    # Split the line into columns by whitespace
                    columns = line.split()
                    
                    if (columns[2].startswith("deltalHHH")):
                        columns[6]="MCMC"
                        columns[7]="weight"
                        columns.append(str(kappas['lam']-1))
                        if not realistic_HL_LHC_k_lambda_uncertainties:
                            columns.append(str(kappas['lam']*0.5))
                            columns.append(str(0.0))
                        else:
                            columns[0] = "AsyGausObservable"
                            columns.append(str(uncertanties_low(kappas['lam'])))
                            columns.append(str(uncertanties_high(kappas['lam'])))

                        if kappas['lam'] < -1.5 or kappas['lam'] > 8.:
                            print("Warning: kappa_lambda outside of the (-1.5, 8) range. Uncertainty evaluated at closest interval edge")



                    # Rejoin the columns and write to the output file
                    outfile.write(" ".join(columns) + "\n")
                else:
                    # Write unmodified lines to the output file
                    outfile.write(line)

        with open(output_file, 'a') as outfile:
            outfile.write(final_text)

        print(f"Modified content saved to {output_file}.")

        if not realistic_HL_LHC_k_lambda_uncertainties:
            subprocess.run(["mv", output_file, input_file])




    ###########################################################################################
    ###########################################################################################
    #######################################   EWPOs   #########################################
    ###########################################################################################
    ###########################################################################################

    input_files =  [# "ObservablesEW_Current_SM_noLFU.conf",
                file_dir + "ObservablesEW_HLLHC.conf",
                file_dir + "ObservablesEW_FCCee_WW_SM.conf",
                file_dir + "ObservablesEW_FCCee_Zpole_SM.conf",
                ]
    if modify_all_ewpos:
        input_files.append(file_dir + "ObservablesEW_Current_SM_noLFU.conf")

    output_files = [# "ObservablesEW_Current_SM_noLFU_kappa_scaled.conf",
                file_dir + "ObservablesEW_HLLHC_kappa_scaled.conf",
                file_dir + "ObservablesEW_FCCee_WW_SM_kappa_scaled.conf",
                file_dir + "ObservablesEW_FCCee_Zpole_SM_kappa_scaled.conf",
                ]
    if modify_all_ewpos:
        output_files.append(file_dir + "ObservablesEW_Current_SM_noLFU_kappa_scaled.conf")

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








working_dir = "./"

LAMBDAS = [x for x in range(-5, 11) for _ in range(2)]

# WITH_LAMBDA=['no', '', 'no', '', 'no', '', 'no', '']
WITH_LAMBDA=['no' if i%2==0 else '' for i in range(len(LAMBDAS))]

HLLHC_lambda_precision = 0.25

observables = {}
central_values_obs = {}
central_values_gaus_corr_obs = {}

k_ZH_240_365_central_values = {}

for i, lmbd in enumerate(LAMBDAS):
    scenario = f"Lambda{lmbd}_FCCee240_FCCee365_{WITH_LAMBDA[i]}HLLHClambda"
    scenario_dir = working_dir + scenario + "/"
    input_file =  scenario_dir + "results_observables/observables.txt"

    k_ZH_240_365_central_values[lmbd] = {}

    print(f"Running scenario {scenario}")

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
                central_values_obs[observable] = float(columns[2])

                if observable in ['eeZH_FCCee240', 'eeZH_FCCee365']:
                    k_ZH_240_365_central_values[lmbd][observable] = central_values_obs[observable]

        print(central_values_obs)


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
                corr_obs[observable] = float(columns[2])

        print(central_values_gaus_corr_obs)


    observable_files = [working_dir + scenario + obs_file_path[2:] for obs_file_path in observable_files]
    [print(file) for file in observable_files]

    observable_files_new = [obs_file_path[:-5] + "_new.conf" for obs_file_path in observable_files]
    [print(file) for file in observable_files_new]

    # for obs_file_path, obs_file_path_new in zip(observable_files, observable_files_new):
    #     with open(obs_file_path, 'r') as obs_file, open(obs_file_path_new, 'w') as obs_file_new:

    #         is_obs_correlated = False
    #         for line in obs_file:
    #             columns = line.split()

    #             if line.startswith("Observable "):
    #                 observable = columns[1]
    #                 if observable == "deltalHHH_HLLHC" and WITH_LAMBDA[i] == '':
    #                     columns[6]="MCMC"
    #                     columns[7]="weight"
    #                     columns.append(str(central_values_obs[observable]))
    #                     columns.append(str((float(central_values_obs[observable])+1) * HLLHC_lambda_precision))
    #                     columns.append(str(0.0))

    #                 if columns[6]=="MCMC" and columns[7]=="weight":
    #                     if not is_obs_correlated:
    #                         columns[8] = str(central_values_obs[observable])
    #                     else:
    #                         observable_number = observable_number + 1
    #                         #print(observable_number)
    #                         #print(n_corr_obs)
    #                         columns[8] = str(central_values_gaus_corr_obs[corr_obs_name][observable])
    #                         if observable_number == n_corr_obs:
    #                             is_obs_correlated = False

    #                     # Rejoin the columns and write to the output file
    #                     obs_file_new.write(" ".join(columns) + "\n")
    #                 else:
    #                     # Write unmodified lines to the output file
    #                     obs_file_new.write(line)

    #             else:

    #                 if line.startswith("CorrelatedGaussianObservables") or \
    #                 line.startswith("ObservablesWithCovarianceInverse"):
                        
    #                     corr_obs_name = columns[1]
    #                     n_corr_obs = int(columns[2])
    #                     observable_number = 0
    #                     is_obs_correlated = True

    #                 # Write unmodified lines to the output file
    #                 obs_file_new.write(line)

    #     subprocess.run(["mv", obs_file_path_new, obs_file_path])


    Mw = central_values_obs["Mw_C"]
    GammaZ = central_values_gaus_corr_obs["Zpole1"]["GammaZ_C"]

    kappas = {}

    kappas['H'] = np.sqrt(central_values_obs["GammaHRatio"])  # Modifier to the Higgs width

    # kappas['ZZ_0']   = 1.0
    # kappas['ZZ_125'] = 1.0
    kappas['ZZ_240']   = np.sqrt(central_values_obs["eeZH_FCCee240"])
    kappas['ZZ_365']   = np.sqrt(central_values_obs["eeZH_FCCee365"])
    # kappas['ZZ_500'] = 1.0
    # kappas['ZZ_550'] = 1.0
    # kappas['uu']     = 1.0
    # kappas['dd']     = 1.0
    # kappas['ss']     = 1.0
    kappas['cc']       = np.sqrt(central_values_obs["eeZHcc_FCCee240"])     * kappas['H'] / kappas['ZZ_240']
    kappas['bb']       = np.sqrt(central_values_obs["eeZHbb_FCCee240"])     * kappas['H'] / kappas['ZZ_240']
    # kappas['tt']     = 1.0
    # kappas['ee']     = 1.0
    kappas['mumu']     = np.sqrt(central_values_obs["eeZHmumu_FCCee240"])   * kappas['H'] / kappas['ZZ_240']
    kappas['tautau']   = np.sqrt(central_values_obs["eeZHtautau_FCCee240"]) * kappas['H'] / kappas['ZZ_240']
    kappas['ZZ']       = np.sqrt(central_values_obs["eeZHZZ_FCCee240"])     * kappas['H'] / kappas['ZZ_240']
    kappas['WW']       = np.sqrt(central_values_obs["eeZHWW_FCCee240"])     * kappas['H'] / kappas['ZZ_240']
    kappas['gg']       = np.sqrt(central_values_obs["eeZHgg_FCCee240"])     * kappas['H'] / kappas['ZZ_240']
    kappas['gamgam']   = np.sqrt(central_values_obs["eeZHgaga_FCCee240"])   * kappas['H'] / kappas['ZZ_240']
    kappas['Zgam']     = np.sqrt(central_values_obs["eeZHZga_FCCee240"])    * kappas['H'] / kappas['ZZ_240']

    kappas['lam']  = central_values_obs["deltalHHH_HLLHC"] + 1

    kappas['ZZ_0'] = kappas['ZZ']  # No information on ZH at 0 momentum, using energy-independent HZZ coupling
    kappas['tt']   = np.sqrt(central_values_obs["muttHZZ4lHL"]) * kappas['H'] / kappas['ZZ']  # Extracting the ttH coupling from the ttHZZ observable


    scale_observables(scenario, scenario_dir, kappas, Mw, GammaZ)

    # central_values_obs[observable]


print(k_ZH_240_365_central_values)

subprocess.run(["mkdir", "-p", "comparison_plots"])
with open(f"comparison_plots/k_ZH_240_365_predictions.txt", "w") as k_ZH_output:

    for i, lmbd in enumerate(LAMBDAS):
        if WITH_LAMBDA[i] == 'no':
            for obs in ['eeZH_FCCee240', 'eeZH_FCCee365',]:
                text = f"{lmbd} " + \
                       f"{obs} " + \
                    f"{k_ZH_240_365_central_values[lmbd][obs]}"
                print(text, file = k_ZH_output)


    #print(f"Modified content saved to {output_file_ILC_250}.")




