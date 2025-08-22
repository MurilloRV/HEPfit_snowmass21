# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

import subprocess
import argparse
import numpy as np

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scenario", help = "Name of the scenario (e.g. Z2SSM_FCCee240)", type=str)
parser.add_argument("-b", "--bp", help = "Which benchmark point to use", type=str)
parser.add_argument("--realistic", help = "Use realistic, asymmetric uncertainties for the on-shell kappa_lambda measurement at HL-LHC", action="store_true")
# parser.add_argument("--ewpos_all", help = "Modify also the EWPO central values for current observables", action="store_true")
parser.add_argument("--no_BSM", help = "Do not include corrections to Z->ZH from diagrams with BSM particles (S)", action="store_true")
parser.add_argument("--no_quad", help = "Do not include quadratic momentum dependent BSM 1L corrections to Z->ZH", action="store_true")
parser.add_argument("--smeft_formula", help = "Use the HEPfit SMEFT expression for the Zh cross-section, plus vertex corrections", action="store_true")
parser.add_argument("--smeft_formula_sqrt", help = "Use the HEPfit SMEFT expression for the Zh cross-section, with dkappaf**2 inside the square root", action="store_true")
parser.add_argument("--smeft_formula_no_cross", help = "Use the HEPfit SMEFT expression for the Zh cross-section, without cross terms", action="store_true")
parser.add_argument("--smeft_formula_external_leg", help = "Use the HEPfit SMEFT expression for the Zh cross-section, without vertex corrections", action="store_true")
parser.add_argument("--smeft_formula_all", help = "Use the HEPfit SMEFT expression for all XS and BR, including 2*dkappaf in the square root to stand in for C_Hbox (as \"_no_cross\")", action="store_true")
parser.add_argument("--WFR_kala2_input", help = "Include the WFR contribution, proportional to kappa_lambda**2, into the Z2SSM ZH cross-section prediction", action="store_true")
parser.add_argument("--WFR_kala2_input_all", help = "Include the WFR contribution, proportional to kappa_lambda**2, into the Z2SSM predictions for all the XS and BR", action="store_true")
parser.add_argument("--use_HEPfit_C1_values_WFR_kala2_input_all", help = "Use the HEPfit C1 values, instead of the Z2SSM values. Activates WFR_kala2_input_all as well", action="store_true")
parser.add_argument("--use_HEPfit_C1_values_decayrates_WFR_kala2_input_all", help = "Use the HEPfit C1 values, also for the Higgs decay rates, instead of the Z2SSM values. Activates WFR_kala2_input_all as well", action="store_true")
parser.add_argument("--no_BSM_WFR_kala2_input_all", help = "Do not include corrections to Z->ZH from diagrams with BSM particles (S). Activates WFR_kala2_input_all as well", action="store_true")
parser.add_argument("--higgsconf", help = "Name of the ObsevablesHiggs configuration file", type=str, default=None)


args = parser.parse_args()
scenario                                            = args.scenario
BP                                                  = args.bp
realistic_HL_LHC_k_lambda_uncertainties             = args.realistic
# modify_all_ewpos                                    = args.ewpos_all
no_BSM                                              = args.no_BSM
no_quad                                             = args.no_quad
smeft_formula                                       = args.smeft_formula
smeft_formula_sqrt                                  = args.smeft_formula_sqrt
smeft_formula_no_cross                              = args.smeft_formula_no_cross
smeft_formula_external_leg                          = args.smeft_formula_external_leg
smeft_formula_all                                   = args.smeft_formula_all
WFR_kala2_input                                     = args.WFR_kala2_input
WFR_kala2_input_all                                 = args.WFR_kala2_input_all
use_HEPfit_C1_values_WFR_kala2_input_all            = args.use_HEPfit_C1_values_WFR_kala2_input_all
use_HEPfit_C1_values_decayrates_WFR_kala2_input_all = args.use_HEPfit_C1_values_decayrates_WFR_kala2_input_all
no_BSM_WFR_kala2_input_all                          = args.no_BSM_WFR_kala2_input_all
higgsconf                                           = args.higgsconf

exclusive_flag_count = sum([
    no_BSM, 
    no_quad,
    smeft_formula, 
    smeft_formula_sqrt, 
    smeft_formula_no_cross, 
    smeft_formula_external_leg, 
    smeft_formula_all, 
    WFR_kala2_input,
    WFR_kala2_input_all,
    use_HEPfit_C1_values_WFR_kala2_input_all,
    use_HEPfit_C1_values_decayrates_WFR_kala2_input_all,
    no_BSM_WFR_kala2_input_all,
])

# These flags are mutually exclusive, and can only be used one at a time
if exclusive_flag_count > 1:
    raise ValueError("""You can only use at most one of the following options:
        --no_BSM,
        --no_quad,
        --smeft_formula,
        --smeft_formula_sqrt,
        --smeft_formula_no_cross,
        --smeft_formula_external_leg,
        --smeft_formula_all,
        --WFR_kala2_input
        --WFR_kala2_input_all
        --use_HEPfit_C1_values_WFR_kala2_input_all
        --use_HEPfit_C1_values_decayrates_WFR_kala2_input_all
        --no_BSM_WFR_kala2_input_all
        """)
        # --ewpos_all,

# Use of these flags is not currently possible without use of the realistic HL-LHC kappa_lambda uncertainties
elif exclusive_flag_count == 1 and not realistic_HL_LHC_k_lambda_uncertainties:
    raise ValueError("""The following options are only be currently used along with the --realistic option:
        --no_BSM,
        --no_quad,
        --smeft_formula,
        --smeft_formula_sqrt,
        --smeft_formula_no_cross,
        --smeft_formula_external_leg,
        --smeft_formula_all,
        --WFR_kala2_input
        --WFR_kala2_input_all
        --use_HEPfit_C1_values_WFR_kala2_input_all
        --use_HEPfit_C1_values_decayrates_WFR_kala2_input_all
        --no_BSM_WFR_kala2_input_all
        """)
        # --ewpos_all,



file_dir = f"{BP}/{scenario}/"


kappas={}
# Definition of Z2SSM benchmark point:
kappas['gg'] = 1.0

if BP == "BP_0":
    kappas['lam'] = 2.8901885159873064
    kappas['uu'] = 0.9950075123974438
    kappas['dd'] = 0.9950075123974438
    kappas['ss'] = 0.9950075123974438
    kappas['cc'] = 0.9950075123974438
    kappas['bb'] = 0.9950075123974438
    kappas['tt'] = 0.9950075123974438
    kappas['ee'] = 0.9950075123974438
    kappas['mumu'] = 0.9950075123974438
    kappas['tautau'] = 0.9950075123974438
    kappas['ZZ'] = 0.9950075123974438
    kappas['WW'] = 0.9950075123974438
    kappas['gamgam'] = 0.9950075123974438
    kappas['Zgam'] = 0.9950075123974438
    kappas['gg'] = 0.9950075123974438
    kappas['ZZ_0'] = 1.0027339432111269
    kappas['ZZ_240'] = 1.0123684158107078
    kappas['ZZ_365'] = 1.0011974481673722
    kappas['ZZ_500'] = 0.9965533007108748
    kappas['ZZ_550'] = 0.9953733190544404

elif BP == "BP_1":
    kappas['lam'] = 1.500069302100464
    kappas['uu'] = 0.9975951650479348
    kappas['dd'] = 0.9975951650479348
    kappas['ss'] = 0.9975951650479348
    kappas['cc'] = 0.9975951650479348
    kappas['bb'] = 0.9975951650479348
    kappas['tt'] = 0.9975951650479348
    kappas['ee'] = 0.9975951650479348
    kappas['mumu'] = 0.9975951650479348
    kappas['tautau'] = 0.9975951650479348
    kappas['ZZ'] = 0.9975951650479348
    kappas['WW'] = 0.9975951650479348
    kappas['gamgam'] = 0.9975951650479348
    kappas['Zgam'] = 0.9975951650479348
    kappas['gg'] = 0.9975951650479348
    kappas['ZZ_0'] = 0.9996392737873786
    kappas['ZZ_240'] = 1.002188175099723
    kappas['ZZ_365'] = 0.9992327778227102
    kappas['ZZ_500'] = 0.9980041196450844
    kappas['ZZ_550'] = 0.997691943056118

elif BP == "BP_2":
    kappas['lam'] = 10.76349876455617
    kappas['uu'] = 0.9756933755835758
    kappas['dd'] = 0.9756933755835758
    kappas['ss'] = 0.9756933755835758
    kappas['cc'] = 0.9756933755835758
    kappas['bb'] = 0.9756933755835758
    kappas['tt'] = 0.9756933755835758
    kappas['ee'] = 0.9756933755835758
    kappas['mumu'] = 0.9756933755835758
    kappas['tautau'] = 0.9756933755835758
    kappas['ZZ'] = 0.9756933755835758
    kappas['WW'] = 0.9756933755835758
    kappas['gamgam'] = 0.9756933755835758
    kappas['Zgam'] = 0.9756933755835758
    kappas['gg'] = 0.9756933755835758
    kappas['ZZ_0'] = 1.0156031502255094
    kappas['ZZ_240'] = 1.0653686421473691
    kappas['ZZ_365'] = 1.0076666045664062
    kappas['ZZ_500'] = 0.9836779242996421
    kappas['ZZ_550'] = 0.9775828976145505

elif BP == "BP_3":
    kappas['lam'] = 2.0000017431283923
    kappas['uu'] = 0.993172422129435
    kappas['dd'] = 0.993172422129435
    kappas['ss'] = 0.993172422129435
    kappas['cc'] = 0.993172422129435
    kappas['bb'] = 0.993172422129435
    kappas['tt'] = 0.993172422129435
    kappas['ee'] = 0.993172422129435
    kappas['mumu'] = 0.993172422129435
    kappas['tautau'] = 0.993172422129435
    kappas['ZZ'] = 0.993172422129435
    kappas['WW'] = 0.993172422129435
    kappas['gamgam'] = 0.993172422129435
    kappas['Zgam'] = 0.993172422129435
    kappas['gg'] = 0.993172422129435
    kappas['ZZ_0'] = 0.9972600801680345
    kappas['ZZ_240'] = 1.0023571851986781
    kappas['ZZ_365'] = 0.9964471994902254
    kappas['ZZ_500'] = 0.9939902193993179
    kappas['ZZ_550'] = 0.9933659516591885

elif BP == "BP_4":
    kappas['lam'] = 10.76349876455617
    kappas['uu'] = 0.9756933755835758
    kappas['dd'] = 0.9756933755835758
    kappas['ss'] = 0.9756933755835758
    kappas['cc'] = 0.9756933755835758
    kappas['bb'] = 0.9756933755835758
    kappas['tt'] = 0.9756933755835758
    kappas['ee'] = 0.9756933755835758
    kappas['mumu'] = 0.9756933755835758
    kappas['tautau'] = 0.9756933755835758
    kappas['ZZ'] = 0.9756933755835758
    kappas['WW'] = 0.9756933755835758
    kappas['gamgam'] = 0.9756933755835758
    kappas['Zgam'] = 0.9756933755835758
    kappas['gg'] = 0.9756933755835758
    kappas['ZZ_0'] = 1.0156031502255094
    kappas['ZZ_240'] = 1.0653686421473691
    kappas['ZZ_365'] = 1.0076666045664062
    kappas['ZZ_500'] = 0.9836779242996421
    kappas['ZZ_550'] = 0.9775828976145505

elif BP == "BP_5":
    kappas['lam'] = 1.500069302100464
    kappas['uu'] = 0.9975951650479348
    kappas['dd'] = 0.9975951650479348
    kappas['ss'] = 0.9975951650479348
    kappas['cc'] = 0.9975951650479348
    kappas['bb'] = 0.9975951650479348
    kappas['tt'] = 0.9975951650479348
    kappas['ee'] = 0.9975951650479348
    kappas['mumu'] = 0.9975951650479348
    kappas['tautau'] = 0.9975951650479348
    kappas['ZZ'] = 0.9975951650479348
    kappas['WW'] = 0.9975951650479348
    kappas['gamgam'] = 0.9975951650479348
    kappas['Zgam'] = 0.9975951650479348
    kappas['gg'] = 0.9975951650479348
    kappas['ZZ_0'] = 0.9996392737873786
    kappas['ZZ_240'] = 1.002188175099723
    kappas['ZZ_365'] = 0.9992327778227102
    kappas['ZZ_500'] = 0.9980041196450844
    kappas['ZZ_550'] = 0.997691943056118

elif BP == "BP_6":
    kappas['lam'] = 1.138105762218659
    kappas['uu'] = 0.9987315109773176
    kappas['dd'] = 0.9987315109773176
    kappas['ss'] = 0.9987315109773176
    kappas['cc'] = 0.9987315109773176
    kappas['bb'] = 0.9987315109773176
    kappas['tt'] = 0.9987315109773176
    kappas['ee'] = 0.9987315109773176
    kappas['mumu'] = 0.9987315109773176
    kappas['tautau'] = 0.9987315109773176
    kappas['ZZ'] = 0.9987315109773176
    kappas['WW'] = 0.9987315109773176
    kappas['gamgam'] = 0.9987315109773176
    kappas['Zgam'] = 0.9987315109773176
    kappas['gg'] = 0.9987315109773176
    kappas['ZZ_0'] = 0.9992960391223825
    kappas['ZZ_240'] = 0.9999999774706932
    kappas['ZZ_365'] = 0.9991837758124702
    kappas['ZZ_500'] = 0.9988444532957421
    kappas['ZZ_550'] = 0.9987582384739466

elif BP == "BP_7":
    kappas['lam'] = 0.066878038392428
    kappas['uu'] = 0.9905412507001218
    kappas['dd'] = 0.9905412507001218
    kappas['ss'] = 0.9905412507001218
    kappas['cc'] = 0.9905412507001218
    kappas['bb'] = 0.9905412507001218
    kappas['tt'] = 0.9905412507001218
    kappas['ee'] = 0.9905412507001218
    kappas['mumu'] = 0.9905412507001218
    kappas['tautau'] = 0.9905412507001218
    kappas['ZZ'] = 0.9905412507001218
    kappas['WW'] = 0.9905412507001218
    kappas['gamgam'] = 0.9905412507001218
    kappas['Zgam'] = 0.9905412507001218
    kappas['gg'] = 0.9905412507001218
    kappas['ZZ_0'] = 0.9867269738615371
    kappas['ZZ_240'] = 0.981970761507512
    kappas['ZZ_365'] = 0.9874854893519773
    kappas['ZZ_500'] = 0.9897781474376383
    kappas['ZZ_550'] = 0.9903606643604744


elif BP == "BPO_0":
    kappas['lam'] = -0.2508742207313748
    kappas['uu'] = 1.0393799170799365
    kappas['dd'] = 1.0393799170799365
    kappas['ss'] = 1.0393799170799365
    kappas['cc'] = 1.0393799170799365
    kappas['bb'] = 1.0393799170799365
    kappas['tt'] = 1.0393799170799365
    kappas['ee'] = 1.0393799170799365
    kappas['mumu'] = 1.0393799170799365
    kappas['tautau'] = 1.0393799170799365
    kappas['ZZ'] = 1.0393799170799365
    kappas['WW'] = 1.0393799170799365
    kappas['gamgam'] = 1.0393799170799365
    kappas['Zgam'] = 1.0393799170799365
    kappas['gg'] = 1.0393799170799365
    kappas['ZZ_0'] = 1.0342667799291414
    kappas['ZZ_240'] = 1.0278909537598329
    kappas['ZZ_365'] = 1.0352835896411137
    kappas['ZZ_500'] = 1.0383569573404057
    kappas['ZZ_550'] = 1.0391378364021953
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.2650549688955889
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.007392635881280807
    # Best scan point row: 17704 out of 203446

elif BP == "BPO_1":
    kappas['lam'] = -0.3647055096736148
    kappas['uu'] = 1.022300538236441
    kappas['dd'] = 1.022300538236441
    kappas['ss'] = 1.022300538236441
    kappas['cc'] = 1.022300538236441
    kappas['bb'] = 1.022300538236441
    kappas['tt'] = 1.022300538236441
    kappas['ee'] = 1.022300538236441
    kappas['mumu'] = 1.022300538236441
    kappas['tautau'] = 1.022300538236441
    kappas['ZZ'] = 1.022300538236441
    kappas['WW'] = 1.022300538236441
    kappas['gamgam'] = 1.022300538236441
    kappas['Zgam'] = 1.022300538236441
    kappas['gg'] = 1.022300538236441
    kappas['ZZ_0'] = 1.016722098513439
    kappas['ZZ_240'] = 1.0097660633199972
    kappas['ZZ_365'] = 1.017831439319429
    kappas['ZZ_500'] = 1.021184487741855
    kappas['ZZ_550'] = 1.0220364278812801
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8258574345833879
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.0080653759994318
    # Best scan point row: 29781 out of 203446

elif BP == "BPO_2":
    kappas['lam'] = -0.283207588738505
    kappas['uu'] = 0.997161661245658
    kappas['dd'] = 0.997161661245658
    kappas['ss'] = 0.997161661245658
    kappas['cc'] = 0.997161661245658
    kappas['bb'] = 0.997161661245658
    kappas['tt'] = 0.997161661245658
    kappas['ee'] = 0.997161661245658
    kappas['mumu'] = 0.997161661245658
    kappas['tautau'] = 0.997161661245658
    kappas['ZZ'] = 0.997161661245658
    kappas['WW'] = 0.997161661245658
    kappas['gamgam'] = 0.997161661245658
    kappas['Zgam'] = 0.997161661245658
    kappas['gg'] = 0.997161661245658
    kappas['ZZ_0'] = 0.9919163565735986
    kappas['ZZ_240'] = 0.9853757241188417
    kappas['ZZ_365'] = 0.9929594494098575
    kappas['ZZ_500'] = 0.9961122594121367
    kappas['ZZ_550'] = 0.9969133231173185
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.5185709947380404
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.007583725291015808
    # Best scan point row: 92768 out of 203446

elif BP == "BPO_3":
    kappas['lam'] = -0.2265153925052781
    kappas['uu'] = 0.970154144419945
    kappas['dd'] = 0.970154144419945
    kappas['ss'] = 0.970154144419945
    kappas['cc'] = 0.970154144419945
    kappas['bb'] = 0.970154144419945
    kappas['tt'] = 0.970154144419945
    kappas['ee'] = 0.970154144419945
    kappas['mumu'] = 0.970154144419945
    kappas['tautau'] = 0.970154144419945
    kappas['ZZ'] = 0.970154144419945
    kappas['WW'] = 0.970154144419945
    kappas['gamgam'] = 0.970154144419945
    kappas['Zgam'] = 0.970154144419945
    kappas['gg'] = 0.970154144419945
    kappas['ZZ_0'] = 0.9651405776555952
    kappas['ZZ_240'] = 0.9588889107757529
    kappas['ZZ_365'] = 0.9661375865812838
    kappas['ZZ_500'] = 0.9691511052289109
    kappas['ZZ_550'] = 0.9699167778865583
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.17631923508501132
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.007248675805530902
    # Best scan point row: 183619 out of 203446

elif BP == "BPO_4":
    kappas['lam'] = 0.8270343237975535
    kappas['uu'] = 0.9669355487722888
    kappas['dd'] = 0.9669355487722888
    kappas['ss'] = 0.9669355487722888
    kappas['cc'] = 0.9669355487722888
    kappas['bb'] = 0.9669355487722888
    kappas['tt'] = 0.9669355487722888
    kappas['ee'] = 0.9669355487722888
    kappas['mumu'] = 0.9669355487722888
    kappas['tautau'] = 0.9669355487722888
    kappas['ZZ'] = 0.9669355487722888
    kappas['WW'] = 0.9669355487722888
    kappas['gamgam'] = 0.9669355487722888
    kappas['Zgam'] = 0.9669355487722888
    kappas['gg'] = 0.9669355487722888
    kappas['ZZ_0'] = 0.9662285254679905
    kappas['ZZ_240'] = 0.965346902786472
    kappas['ZZ_365'] = 0.9663691256790155
    kappas['ZZ_500'] = 0.9667940981610736
    kappas['ZZ_550'] = 0.9669020748646592
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.02949874541501128
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.0010222228925435006
    # Best scan point row: 35130 out of 203446

elif BP == "BPB_0":
    kappas['lam'] = 0.8918170746898771
    kappas['uu'] = 0.9984287707514746
    kappas['dd'] = 0.9984287707514746
    kappas['ss'] = 0.9984287707514746
    kappas['cc'] = 0.9984287707514746
    kappas['bb'] = 0.9984287707514746
    kappas['tt'] = 0.9984287707514746
    kappas['ee'] = 0.9984287707514746
    kappas['mumu'] = 0.9984287707514746
    kappas['tautau'] = 0.9984287707514746
    kappas['ZZ'] = 0.9984287707514746
    kappas['WW'] = 0.9984287707514746
    kappas['gamgam'] = 0.9984287707514746
    kappas['Zgam'] = 0.9984287707514746
    kappas['gg'] = 0.9984287707514746
    kappas['ZZ_0'] = 0.9979865567180273
    kappas['ZZ_240'] = 0.9974351379463932
    kappas['ZZ_365'] = 0.9980744963743907
    kappas['ZZ_500'] = 0.9983402992047253
    kappas['ZZ_550'] = 0.998407834197307
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.2492759511563055
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.0006393584279975606
    # Best scan point row: 202954 out of 203446

elif BP == "BPB_1":
    kappas['lam'] = 3.4771963023861323
    kappas['uu'] = 0.9888663133959416
    kappas['dd'] = 0.9888663133959416
    kappas['ss'] = 0.9888663133959416
    kappas['cc'] = 0.9888663133959416
    kappas['bb'] = 0.9888663133959416
    kappas['tt'] = 0.9888663133959416
    kappas['ee'] = 0.9888663133959416
    kappas['mumu'] = 0.9888663133959416
    kappas['tautau'] = 0.9888663133959416
    kappas['ZZ'] = 0.9888663133959416
    kappas['WW'] = 0.9888663133959416
    kappas['gamgam'] = 0.9888663133959416
    kappas['Zgam'] = 0.9888663133959416
    kappas['gg'] = 0.9888663133959416
    kappas['ZZ_0'] = 0.9989922271238115
    kappas['ZZ_240'] = 1.0116187348489714
    kappas['ZZ_365'] = 0.9969785656245321
    kappas['ZZ_500'] = 0.9908921542376964
    kappas['ZZ_550'] = 0.9893457231957767
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 1.2600484833110177
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.014640169224439226
    # Best scan point row: 200101 out of 203446

elif BP == "BPB_2":
    kappas['lam'] = 0.9196804937486558
    kappas['uu'] = 0.999997529991834
    kappas['dd'] = 0.999997529991834
    kappas['ss'] = 0.999997529991834
    kappas['cc'] = 0.999997529991834
    kappas['bb'] = 0.999997529991834
    kappas['tt'] = 0.999997529991834
    kappas['ee'] = 0.999997529991834
    kappas['mumu'] = 0.999997529991834
    kappas['tautau'] = 0.999997529991834
    kappas['ZZ'] = 0.999997529991834
    kappas['WW'] = 0.999997529991834
    kappas['gamgam'] = 0.999997529991834
    kappas['Zgam'] = 0.999997529991834
    kappas['gg'] = 0.999997529991834
    kappas['ZZ_0'] = 0.99966921188875
    kappas['ZZ_240'] = 0.9992598156430077
    kappas['ZZ_365'] = 0.9997345019496239
    kappas['ZZ_500'] = 0.9999318450334006
    kappas['ZZ_550'] = 0.9999819858226546
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.6413082121122371
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.00047468630661617883
    # Best scan point row: 203443 out of 203446

elif BP == "BPB_3":
    kappas['lam'] = 4.703937706690645
    kappas['uu'] = 0.986070175066104
    kappas['dd'] = 0.986070175066104
    kappas['ss'] = 0.986070175066104
    kappas['cc'] = 0.986070175066104
    kappas['bb'] = 0.986070175066104
    kappas['tt'] = 0.986070175066104
    kappas['ee'] = 0.986070175066104
    kappas['mumu'] = 0.986070175066104
    kappas['tautau'] = 0.986070175066104
    kappas['ZZ'] = 0.986070175066104
    kappas['WW'] = 0.986070175066104
    kappas['gamgam'] = 0.986070175066104
    kappas['Zgam'] = 0.986070175066104
    kappas['gg'] = 0.986070175066104
    kappas['ZZ_0'] = 1.0012105794156612
    kappas['ZZ_240'] = 1.0200899060245343
    kappas['ZZ_365'] = 0.998199725270389
    kappas['ZZ_500'] = 0.9890992399304032
    kappas['ZZ_550'] = 0.9867869951392069
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 1.089610908453849
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.021890180754145283
    # Best scan point row: 142666 out of 203446

elif BP == "BPB_4":
    kappas['lam'] = 3.013431564284278
    kappas['uu'] = 0.9946746322090492
    kappas['dd'] = 0.9946746322090492
    kappas['ss'] = 0.9946746322090492
    kappas['cc'] = 0.9946746322090492
    kappas['bb'] = 0.9946746322090492
    kappas['tt'] = 0.9946746322090492
    kappas['ee'] = 0.9946746322090492
    kappas['mumu'] = 0.9946746322090492
    kappas['tautau'] = 0.9946746322090492
    kappas['ZZ'] = 0.9946746322090492
    kappas['WW'] = 0.9946746322090492
    kappas['gamgam'] = 0.9946746322090492
    kappas['Zgam'] = 0.9946746322090492
    kappas['gg'] = 0.9946746322090492
    kappas['ZZ_0'] = 1.0029048375816612
    kappas['ZZ_240'] = 1.0131674918477072
    kappas['ZZ_365'] = 1.0012681608199012
    kappas['ZZ_500'] = 0.9963212081752236
    kappas['ZZ_550'] = 0.9950642899936526
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.9036900242985877
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.011899331027805937
    # Best scan point row: 145566 out of 203446

elif BP == "BPB_5":
    kappas['lam'] = 5.946907598934937
    kappas['uu'] = 0.9835951935978676
    kappas['dd'] = 0.9835951935978676
    kappas['ss'] = 0.9835951935978676
    kappas['cc'] = 0.9835951935978676
    kappas['bb'] = 0.9835951935978676
    kappas['tt'] = 0.9835951935978676
    kappas['ee'] = 0.9835951935978676
    kappas['mumu'] = 0.9835951935978676
    kappas['tautau'] = 0.9835951935978676
    kappas['ZZ'] = 0.9835951935978676
    kappas['WW'] = 0.9835951935978676
    kappas['gamgam'] = 0.9835951935978676
    kappas['Zgam'] = 0.9835951935978676
    kappas['gg'] = 0.9835951935978676
    kappas['ZZ_0'] = 1.0038164249626607
    kappas['ZZ_240'] = 1.0290312886185762
    kappas['ZZ_365'] = 0.9997951863701144
    kappas['ZZ_500'] = 0.9876407540747085
    kappas['ZZ_550'] = 0.9845525646304032
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 1.007054927274379
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.029236102248461737
    # Best scan point row: 100772 out of 203446

elif BP == "BPB_6":
    kappas['lam'] = 4.968691068740802
    kappas['uu'] = 0.989807571463894
    kappas['dd'] = 0.989807571463894
    kappas['ss'] = 0.989807571463894
    kappas['cc'] = 0.989807571463894
    kappas['bb'] = 0.989807571463894
    kappas['tt'] = 0.989807571463894
    kappas['ee'] = 0.989807571463894
    kappas['mumu'] = 0.989807571463894
    kappas['tautau'] = 0.989807571463894
    kappas['ZZ'] = 0.989807571463894
    kappas['WW'] = 0.989807571463894
    kappas['gamgam'] = 0.989807571463894
    kappas['Zgam'] = 0.989807571463894
    kappas['gg'] = 0.989807571463894
    kappas['ZZ_0'] = 1.0060301951356347
    kappas['ZZ_240'] = 1.026258995085788
    kappas['ZZ_365'] = 1.00280412847311
    kappas['ZZ_500'] = 0.9930531505274581
    kappas['ZZ_550'] = 0.9905756290413416
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8932126509811639
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.02345486661267815
    # Best scan point row: 102477 out of 203446

elif BP == "BPB_7":
    kappas['lam'] = 7.233411757176534
    kappas['uu'] = 0.9812843835313146
    kappas['dd'] = 0.9812843835313146
    kappas['ss'] = 0.9812843835313146
    kappas['cc'] = 0.9812843835313146
    kappas['bb'] = 0.9812843835313146
    kappas['tt'] = 0.9812843835313146
    kappas['ee'] = 0.9812843835313146
    kappas['mumu'] = 0.9812843835313146
    kappas['tautau'] = 0.9812843835313146
    kappas['ZZ'] = 0.9812843835313146
    kappas['WW'] = 0.9812843835313146
    kappas['gamgam'] = 0.9812843835313146
    kappas['Zgam'] = 0.9812843835313146
    kappas['gg'] = 0.9812843835313146
    kappas['ZZ_0'] = 1.0067643947935072
    kappas['ZZ_240'] = 1.038536693835888
    kappas['ZZ_365'] = 1.0016973836517211
    kappas['ZZ_500'] = 0.9863820417625171
    kappas['ZZ_550'] = 0.9824907306746234
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.9559540925085691
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.03683931018416686
    # Best scan point row: 189546 out of 203446

elif BP == "BPB_8":
    kappas['lam'] = 6.988652545078013
    kappas['uu'] = 0.984730069743724
    kappas['dd'] = 0.984730069743724
    kappas['ss'] = 0.984730069743724
    kappas['cc'] = 0.984730069743724
    kappas['bb'] = 0.984730069743724
    kappas['tt'] = 0.984730069743724
    kappas['ee'] = 0.984730069743724
    kappas['mumu'] = 0.984730069743724
    kappas['tautau'] = 0.984730069743724
    kappas['ZZ'] = 0.984730069743724
    kappas['WW'] = 0.984730069743724
    kappas['gamgam'] = 0.984730069743724
    kappas['Zgam'] = 0.984730069743724
    kappas['gg'] = 0.984730069743724
    kappas['ZZ_0'] = 1.0092095907890437
    kappas['ZZ_240'] = 1.0397343285948002
    kappas['ZZ_365'] = 1.004341539334676
    kappas['ZZ_500'] = 0.9896275649084036
    kappas['ZZ_550'] = 0.9858890488343811
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8907358073430713
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.035392789260124236
    # Best scan point row: 201505 out of 203446

elif BP == "BPB_9":
    kappas['lam'] = 8.519243114238716
    kappas['uu'] = 0.979120561462646
    kappas['dd'] = 0.979120561462646
    kappas['ss'] = 0.979120561462646
    kappas['cc'] = 0.979120561462646
    kappas['bb'] = 0.979120561462646
    kappas['tt'] = 0.979120561462646
    kappas['ee'] = 0.979120561462646
    kappas['mumu'] = 0.979120561462646
    kappas['tautau'] = 0.979120561462646
    kappas['ZZ'] = 0.979120561462646
    kappas['WW'] = 0.979120561462646
    kappas['gamgam'] = 0.979120561462646
    kappas['Zgam'] = 0.979120561462646
    kappas['gg'] = 0.979120561462646
    kappas['ZZ_0'] = 1.0098566024458826
    kappas['ZZ_240'] = 1.0481829075424303
    kappas['ZZ_365'] = 1.0037443656609821
    kappas['ZZ_500'] = 0.9852697672342016
    kappas['ZZ_550'] = 0.9805757545100592
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.9222885074404277
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.044438541881448135
    # Best scan point row: 201749 out of 203446

elif BP == "BPB_10":
    kappas['lam'] = 8.915995818716492
    kappas['uu'] = 0.9801233123783776
    kappas['dd'] = 0.9801233123783776
    kappas['ss'] = 0.9801233123783776
    kappas['cc'] = 0.9801233123783776
    kappas['bb'] = 0.9801233123783776
    kappas['tt'] = 0.9801233123783776
    kappas['ee'] = 0.9801233123783776
    kappas['mumu'] = 0.9801233123783776
    kappas['tautau'] = 0.9801233123783776
    kappas['ZZ'] = 0.9801233123783776
    kappas['WW'] = 0.9801233123783776
    kappas['gamgam'] = 0.9801233123783776
    kappas['Zgam'] = 0.9801233123783776
    kappas['gg'] = 0.9801233123783776
    kappas['ZZ_0'] = 1.0124811399164266
    kappas['ZZ_240'] = 1.052829731693784
    kappas['ZZ_365'] = 1.0060463910863675
    kappas['ZZ_500'] = 0.9865969808628936
    kappas['ZZ_550'] = 0.9816552886562737
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8855494644301036
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.04678334060741651
    # Best scan point row: 175316 out of 203446

elif BP == "BPB_11":
    kappas['lam'] = 9.679739818437092
    kappas['uu'] = 0.9773018511992412
    kappas['dd'] = 0.9773018511992412
    kappas['ss'] = 0.9773018511992412
    kappas['cc'] = 0.9773018511992412
    kappas['bb'] = 0.9773018511992412
    kappas['tt'] = 0.9773018511992412
    kappas['ee'] = 0.9773018511992412
    kappas['mumu'] = 0.9773018511992412
    kappas['tautau'] = 0.9773018511992412
    kappas['ZZ'] = 0.9773018511992412
    kappas['WW'] = 0.9773018511992412
    kappas['gamgam'] = 0.9773018511992412
    kappas['Zgam'] = 0.9773018511992412
    kappas['gg'] = 0.9773018511992412
    kappas['ZZ_0'] = 1.012781597595275
    kappas['ZZ_240'] = 1.0570230659699484
    kappas['ZZ_365'] = 1.0057260171072395
    kappas['ZZ_500'] = 0.9844001063528833
    kappas['ZZ_550'] = 0.9789816342366092
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8995841943985058
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.051297048862708916
    # Best scan point row: 157364 out of 203446

elif BP == "BPB_12":
    kappas['lam'] = 10.721334023900692
    kappas['uu'] = 0.9757823329209472
    kappas['dd'] = 0.9757823329209472
    kappas['ss'] = 0.9757823329209472
    kappas['cc'] = 0.9757823329209472
    kappas['bb'] = 0.9757823329209472
    kappas['tt'] = 0.9757823329209472
    kappas['ee'] = 0.9757823329209472
    kappas['mumu'] = 0.9757823329209472
    kappas['tautau'] = 0.9757823329209472
    kappas['ZZ'] = 0.9757823329209472
    kappas['WW'] = 0.9757823329209472
    kappas['gamgam'] = 0.9757823329209472
    kappas['Zgam'] = 0.9757823329209472
    kappas['gg'] = 0.9757823329209472
    kappas['ZZ_0'] = 1.0155197528222313
    kappas['ZZ_240'] = 1.0650703270070094
    kappas['ZZ_365'] = 1.0076174820063466
    kappas['ZZ_500'] = 0.9837323994873268
    kappas['ZZ_550'] = 0.9776636948437147
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8829346284747265
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.05745284500066283
    # Best scan point row: 201134 out of 203446



elif BP == "BPBnew_0":
    kappas['lam'] = 1.0643594459030925
    kappas['kappaSingleHiggs'] = 0.997795157109014
    kappas['uu'] = 0.997795157109014
    kappas['dd'] = 0.997795157109014
    kappas['ss'] = 0.997795157109014
    kappas['cc'] = 0.997795157109014
    kappas['bb'] = 0.997795157109014
    kappas['tt'] = 0.997795157109014
    kappas['ee'] = 0.997795157109014
    kappas['mumu'] = 0.997795157109014
    kappas['tautau'] = 0.997795157109014
    kappas['ZZ'] = 0.997795157109014
    kappas['WW'] = 0.997795157109014
    kappas['gamgam'] = 0.997795157109014
    kappas['Zgam'] = 0.997795157109014
    kappas['gg'] = 0.997795157109014
    kappas['ZZ_0'] = 0.9980563471636651
    kappas['ZZ_0_with_WFR'] = 0.9979539099793131
    kappas['ZZ_0_no_BSM'] = 1.0002630443516598
    kappas['ZZ_0_with_WFR_no_BSM'] = 1.0001608331788296
    kappas['ZZ_240'] = 0.9983849781927755
    kappas['ZZ_240_with_WFR'] = 0.9982825747303763
    kappas['ZZ_240_no_BSM'] = 1.0005909506201627
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.000488772946644
    kappas['ZZ_240_use_HEPfit_C1_values'] = 0.9983408359865786
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 0.9982384279958877
    kappas['ZZ_365'] = 0.9980039274452023
    kappas['ZZ_365_with_WFR'] = 0.9979014848798298
    kappas['ZZ_365_no_BSM'] = 1.0002107402832767
    kappas['ZZ_365_with_WFR_no_BSM'] = 1.0001085237649667
    kappas['ZZ_365_use_HEPfit_C1_values'] = 0.9979765343231651
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9978740889455925
    kappas['ZZ_500'] = 0.997845468994492
    kappas['ZZ_500_with_WFR'] = 0.9977430101595091
    kappas['ZZ_500_no_BSM'] = 1.0000526315023675
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9999503988219267
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9978246489586595
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9977221879856099
    kappas['ZZ_550'] = 0.9978052039758095
    kappas['ZZ_550_with_WFR'] = 0.9977027410058206
    kappas['ZZ_550_no_BSM'] = 1.0000124553540215
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.9999102185658967
    kappas['ZZ_HEPfit_C1'] = 0.9980603677228265
    kappas['WW_HEPfit_C1'] = 0.998028124940936
    kappas['gg_HEPfit_C1'] = 0.9980055543738163
    kappas['gamgam_HEPfit_C1'] = 0.9979507380141333
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.23594154943831647
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.00038105074757321944
    # mS = 342.06248290436656
    # muS = 50.469898637652165
    # lamS = 0.9315179171986576
    # lamSH = 3.782785760532923
    # Best scan point row: 64903 out of 64942

elif BP == "BPBnew_1":
    kappas['lam'] = 2.068362744578383
    kappas['kappaSingleHiggs'] = 0.9929873927786936
    kappas['uu'] = 0.9929873927786936
    kappas['dd'] = 0.9929873927786936
    kappas['ss'] = 0.9929873927786936
    kappas['cc'] = 0.9929873927786936
    kappas['bb'] = 0.9929873927786936
    kappas['tt'] = 0.9929873927786936
    kappas['ee'] = 0.9929873927786936
    kappas['mumu'] = 0.9929873927786936
    kappas['tautau'] = 0.9929873927786936
    kappas['ZZ'] = 0.9929873927786936
    kappas['WW'] = 0.9929873927786936
    kappas['gamgam'] = 0.9929873927786936
    kappas['Zgam'] = 0.9929873927786936
    kappas['gg'] = 0.9929873927786936
    kappas['ZZ_0'] = 0.997350978068708
    kappas['ZZ_0_with_WFR'] = 0.9948186386808753
    kappas['ZZ_0_no_BSM'] = 1.0043575996114238
    kappas['ZZ_0_with_WFR_no_BSM'] = 1.0018429708839018
    kappas['ZZ_240'] = 1.0027961251968998
    kappas['ZZ_240_with_WFR'] = 1.0002775710382483
    kappas['ZZ_240_no_BSM'] = 1.0097649643122548
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.007263835131983
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.0020663412245816
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 0.9995459482322366
    kappas['ZZ_365'] = 0.9964798410496472
    kappas['ZZ_365_with_WFR'] = 0.9939452822115468
    kappas['ZZ_365_no_BSM'] = 1.0034925450948515
    kappas['ZZ_365_with_WFR_no_BSM'] = 1.0009757431992066
    kappas['ZZ_365_use_HEPfit_C1_values'] = 0.9960243235993206
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9934886026592079
    kappas['ZZ_500'] = 0.9938421357453896
    kappas['ZZ_500_with_WFR'] = 0.9913008328429966
    kappas['ZZ_500_no_BSM'] = 1.0008733212677665
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9983499164310234
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9934950753146791
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9909528823747279
    kappas['ZZ_550'] = 0.9931708333996221
    kappas['ZZ_550_with_WFR'] = 0.9906278083760627
    kappas['ZZ_550_no_BSM'] = 1.0002067380088542
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.9976816472054469
    kappas['ZZ_HEPfit_C1'] = 0.9974177641978249
    kappas['WW_HEPfit_C1'] = 0.9968820560090393
    kappas['gg_HEPfit_C1'] = 0.9965068889233052
    kappas['gamgam_HEPfit_C1'] = 0.9955951802845479
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 2.2589418221529827
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.006316284147252604
    # mS = 549.9854232395771
    # muS = 33.42004172941415
    # lamS = 0.2748339886577788
    # lamSH = 9.959913629017812
    # Best scan point row: 64198 out of 64942

elif BP == "BPBnew_2":
    kappas['lam'] = 3.41660475844658
    kappas['kappaSingleHiggs'] = 0.989084904009899
    kappas['uu'] = 0.989084904009899
    kappas['dd'] = 0.989084904009899
    kappas['ss'] = 0.989084904009899
    kappas['cc'] = 0.989084904009899
    kappas['bb'] = 0.989084904009899
    kappas['tt'] = 0.989084904009899
    kappas['ee'] = 0.989084904009899
    kappas['mumu'] = 0.989084904009899
    kappas['tautau'] = 0.989084904009899
    kappas['ZZ'] = 0.989084904009899
    kappas['WW'] = 0.989084904009899
    kappas['gamgam'] = 0.989084904009899
    kappas['Zgam'] = 0.989084904009899
    kappas['gg'] = 0.989084904009899
    kappas['ZZ_0'] = 0.9989626025611232
    kappas['ZZ_0_with_WFR'] = 0.9907072442063742
    kappas['ZZ_0_no_BSM'] = 1.0098299229552938
    kappas['ZZ_0_with_WFR_no_BSM'] = 1.0016641331819716
    kappas['ZZ_240'] = 1.0112178869639588
    kappas['ZZ_240_with_WFR'] = 1.0030633964626312
    kappas['ZZ_240_no_BSM'] = 1.021954894746366
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.013886763550719
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.0095801547739485
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 1.0014123283246945
    kappas['ZZ_365'] = 0.9969942153974802
    kappas['ZZ_365_with_WFR'] = 0.9887224220899075
    kappas['ZZ_365_no_BSM'] = 1.007882759807032
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.9997010652807844
    kappas['ZZ_365_use_HEPfit_C1_values'] = 0.9959640832595036
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9876836626927872
    kappas['ZZ_500'] = 0.9910208810502599
    kappas['ZZ_500_with_WFR'] = 0.9826988089363543
    kappas['ZZ_500_no_BSM'] = 1.00197434031907
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9937440017756742
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9902334304246955
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9819046843446445
    kappas['ZZ_550'] = 0.9894974356481869
    kappas['ZZ_550_with_WFR'] = 0.9811624419848294
    kappas['ZZ_550_no_BSM'] = 1.0004675742544282
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.992224737416799
    kappas['ZZ_HEPfit_C1'] = 0.9991134207460656
    kappas['WW_HEPfit_C1'] = 0.9979033133307345
    kappas['gg_HEPfit_C1'] = 0.9970553642729904
    kappas['gamgam_HEPfit_C1'] = 0.9949930508984404
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 1.2679457024461793
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.014223671566478524
    # mS = 657.6327267530628
    # muS = 71.0340790902051
    # lamS = 0.0445565655614998
    # lamSH = 14.12634552529827
    # Best scan point row: 36640 out of 64942

elif BP == "BPBnew_3":
    kappas['lam'] = 0.9197317035823376
    kappas['kappaSingleHiggs'] = 0.9999903148002915
    kappas['uu'] = 0.9999903148002915
    kappas['dd'] = 0.9999903148002915
    kappas['ss'] = 0.9999903148002915
    kappas['cc'] = 0.9999903148002915
    kappas['bb'] = 0.9999903148002915
    kappas['tt'] = 0.9999903148002915
    kappas['ee'] = 0.9999903148002915
    kappas['mumu'] = 0.9999903148002915
    kappas['tautau'] = 0.9999903148002915
    kappas['ZZ'] = 0.9999903148002915
    kappas['WW'] = 0.9999903148002915
    kappas['gamgam'] = 0.9999903148002915
    kappas['Zgam'] = 0.9999903148002915
    kappas['gg'] = 0.9999903148002915
    kappas['ZZ_0'] = 0.9996621489534662
    kappas['ZZ_0_with_WFR'] = 0.9997807526876082
    kappas['ZZ_0_no_BSM'] = 0.9996718373794866
    kappas['ZZ_0_with_WFR_no_BSM'] = 0.9997904399643044
    kappas['ZZ_240'] = 0.9992527916406684
    kappas['ZZ_240_with_WFR'] = 0.999371443956654
    kappas['ZZ_240_no_BSM'] = 0.9992624840356441
    kappas['ZZ_240_with_WFR_no_BSM'] = 0.9993811352008924
    kappas['ZZ_240_use_HEPfit_C1_values'] = 0.9993077947066574
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 0.9994264404926564
    kappas['ZZ_365'] = 0.9997274173079311
    kappas['ZZ_365_with_WFR'] = 0.9998460132998105
    kappas['ZZ_365_no_BSM'] = 0.9997371051014378
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.9998556999442177
    kappas['ZZ_365_use_HEPfit_C1_values'] = 0.9997615217195561
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9998801136663039
    kappas['ZZ_500'] = 0.9999246688836588
    kappas['ZZ_500_with_WFR'] = 1.0000432414833036
    kappas['ZZ_500_no_BSM'] = 0.9999343547661074
    kappas['ZZ_500_with_WFR_no_BSM'] = 1.0000529262173328
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9999505807724348
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 1.000069150299852
    kappas['ZZ_550'] = 0.9999747802236914
    kappas['ZZ_550_with_WFR'] = 1.000093346882059
    kappas['ZZ_550_no_BSM'] = 0.9999844656207599
    kappas['ZZ_550_with_WFR_no_BSM'] = 1.0001030311308807
    kappas['ZZ_HEPfit_C1'] = 0.999657142594558
    kappas['WW_HEPfit_C1'] = 0.9996972897016048
    kappas['gg_HEPfit_C1'] = 0.9997253917172588
    kappas['gamgam_HEPfit_C1'] = 0.9997936361810554
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.6351985511608915
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.00047462566726275135
    # mS = 395.1567254150093
    # muS = 383.2625025565322
    # lamS = 0.2972955406315003
    # lamSH = 0.3059915319854975
    # Best scan point row: 64926 out of 64942

elif BP == "BPBnew_4":
    kappas['lam'] = 4.996504503173265
    kappas['kappaSingleHiggs'] = 0.9855862784130798
    kappas['uu'] = 0.9855862784130798
    kappas['dd'] = 0.9855862784130798
    kappas['ss'] = 0.9855862784130798
    kappas['cc'] = 0.9855862784130798
    kappas['bb'] = 0.9855862784130798
    kappas['tt'] = 0.9855862784130798
    kappas['ee'] = 0.9855862784130798
    kappas['mumu'] = 0.9855862784130798
    kappas['tautau'] = 0.9855862784130798
    kappas['ZZ'] = 0.9855862784130798
    kappas['WW'] = 0.9855862784130798
    kappas['gamgam'] = 0.9855862784130798
    kappas['Zgam'] = 0.9855862784130798
    kappas['gg'] = 0.9855862784130798
    kappas['ZZ_0'] = 1.0019207490570103
    kappas['ZZ_0_with_WFR'] = 0.9833434338640956
    kappas['ZZ_0_no_BSM'] = 1.0162050140423442
    kappas['ZZ_0_with_WFR_no_BSM'] = 0.9978936577098141
    kappas['ZZ_240'] = 1.0220500588474906
    kappas['ZZ_240_with_WFR'] = 1.0038453288843006
    kappas['ZZ_240_no_BSM'] = 1.0360568352962107
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.0181025918328026
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.019368987844983
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 1.0011155052803724
    kappas['ZZ_365'] = 0.998673037654399
    kappas['ZZ_365_with_WFR'] = 0.980034161481392
    kappas['ZZ_365_no_BSM'] = 1.0130030993593775
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.9946327969881023
    kappas['ZZ_365_use_HEPfit_C1_values'] = 0.9969717310406786
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9783004415959944
    kappas['ZZ_500'] = 0.9887917912156634
    kappas['ZZ_500_with_WFR'] = 0.9699630549191812
    kappas['ZZ_500_no_BSM'] = 1.0032630011862895
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9847110089168248
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9874862511874791
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9686321375098864
    kappas['ZZ_550'] = 0.9862653990706874
    kappas['ZZ_550_with_WFR'] = 0.9673874916168458
    kappas['ZZ_550_no_BSM'] = 1.0007731414151275
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.9821741200574231
    kappas['ZZ_HEPfit_C1'] = 1.002169418912041
    kappas['WW_HEPfit_C1'] = 1.0001735047977047
    kappas['gg_HEPfit_C1'] = 0.9987739917254068
    kappas['gamgam_HEPfit_C1'] = 0.9953669820180437
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 1.0601795376048193
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.023377021193091596
    # mS = 732.6512311643469
    # muS = 96.53859777723906
    # lamS = 0.0473187114032036
    # lamSH = 17.432022131860588
    # Best scan point row: 58992 out of 64942

elif BP == "BPBnew_5":
    kappas['lam'] = 2.723103795696014
    kappas['kappaSingleHiggs'] = 0.9953205471193108
    kappas['uu'] = 0.9953205471193108
    kappas['dd'] = 0.9953205471193108
    kappas['ss'] = 0.9953205471193108
    kappas['cc'] = 0.9953205471193108
    kappas['bb'] = 0.9953205471193108
    kappas['tt'] = 0.9953205471193108
    kappas['ee'] = 0.9953205471193108
    kappas['mumu'] = 0.9953205471193108
    kappas['tautau'] = 0.9953205471193108
    kappas['ZZ'] = 0.9953205471193108
    kappas['WW'] = 0.9953205471193108
    kappas['gamgam'] = 0.9953205471193108
    kappas['Zgam'] = 0.9953205471193108
    kappas['gg'] = 0.9953205471193108
    kappas['ZZ_0'] = 1.0023612062759581
    kappas['ZZ_0_with_WFR'] = 0.9974242878026494
    kappas['ZZ_0_no_BSM'] = 1.0070188149227264
    kappas['ZZ_0_with_WFR_no_BSM'] = 1.0021048426487125
    kappas['ZZ_240'] = 1.0110853768493215
    kappas['ZZ_240_with_WFR'] = 1.0061912647852609
    kappas['ZZ_240_no_BSM'] = 1.0157029807182376
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.0108312258193952
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.0099177485149242
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 1.0050179504949563
    kappas['ZZ_365'] = 1.0009628550387601
    kappas['ZZ_365_with_WFR'] = 0.9960190054506864
    kappas['ZZ_365_no_BSM'] = 1.0056269402361515
    kappas['ZZ_365_with_WFR_no_BSM'] = 1.0007061331781437
    kappas['ZZ_365_use_HEPfit_C1_values'] = 1.0002313661718918
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9952838830834735
    kappas['ZZ_500'] = 0.9967243292333459
    kappas['ZZ_500_with_WFR'] = 0.9917593511216779
    kappas['ZZ_500_no_BSM'] = 1.001408155672322
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9964665153925997
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9961661342348277
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9911983600914548
    kappas['ZZ_550'] = 0.9956445329587521
    kappas['ZZ_550_with_WFR'] = 0.9906741432288824
    kappas['ZZ_550_no_BSM'] = 1.000333415303133
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.9953864394413149
    kappas['ZZ_HEPfit_C1'] = 1.0024683814180368
    kappas['WW_HEPfit_C1'] = 1.0016085822052458
    kappas['gg_HEPfit_C1'] = 1.0010062833420255
    kappas['gamgam_HEPfit_C1'] = 0.9995420465580885
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.9131418758380707
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.010122521810561391
    # mS = 1950.884865803917
    # muS = 1753.0447950511482
    # lamS = 0.0934388626040527
    # lamSH = 24.21791612687041
    # Best scan point row: 53699 out of 64942

elif BP == "BPBnew_6":
    kappas['lam'] = 6.114019817191308
    kappas['kappaSingleHiggs'] = 0.9833984190189476
    kappas['uu'] = 0.9833984190189476
    kappas['dd'] = 0.9833984190189476
    kappas['ss'] = 0.9833984190189476
    kappas['cc'] = 0.9833984190189476
    kappas['bb'] = 0.9833984190189476
    kappas['tt'] = 0.9833984190189476
    kappas['ee'] = 0.9833984190189476
    kappas['mumu'] = 0.9833984190189476
    kappas['tautau'] = 0.9833984190189476
    kappas['ZZ'] = 0.9833984190189476
    kappas['WW'] = 0.9833984190189476
    kappas['gamgam'] = 0.9833984190189476
    kappas['Zgam'] = 0.9833984190189476
    kappas['gg'] = 0.9833984190189476
    kappas['ZZ_0'] = 1.0042935295971192
    kappas['ZZ_0_with_WFR'] = 0.9760209060779161
    kappas['ZZ_0_no_BSM'] = 1.0206902838534049
    kappas['ZZ_0_with_WFR_no_BSM'] = 0.9928846715823854
    kappas['ZZ_240'] = 1.0299217421676443
    kappas['ZZ_240_with_WFR'] = 1.0023722414852438
    kappas['ZZ_240_no_BSM'] = 1.0459168021175203
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.018799917776919
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.0265160373467856
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 0.9988726097159057
    kappas['ZZ_365'] = 1.0001456555385495
    kappas['ZZ_365_with_WFR'] = 0.971752359298989
    kappas['ZZ_365_no_BSM'] = 1.0166093124965654
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.9886889347844732
    kappas['ZZ_365_use_HEPfit_C1_values'] = 0.9979713177220504
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9695143456939678
    kappas['ZZ_500'] = 0.9875025500457408
    kappas['ZZ_500_with_WFR'] = 0.9587348965471933
    kappas['ZZ_500_no_BSM'] = 1.0041735150405757
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9758974145982058
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9858294566794576
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9570115115124955
    kappas['ZZ_550'] = 0.9842643254168301
    kappas['ZZ_550_with_WFR'] = 0.95539917196885
    kappas['ZZ_550_no_BSM'] = 1.0009892228442583
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.9726205528163946
    kappas['ZZ_HEPfit_C1'] = 1.0046109707347333
    kappas['WW_HEPfit_C1'] = 1.002062464471847
    kappas['gg_HEPfit_C1'] = 1.0002746467002739
    kappas['gamgam_HEPfit_C1'] = 0.9959194420946569
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.9951321170494207
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.02977608662909481
    # mS = 760.8128874200765
    # muS = 31.492025677545943
    # lamS = 0.1762131058100124
    # lamSH = 19.097247074598418
    # Best scan point row: 54430 out of 64942

elif BP == "BPBnew_7":
    kappas['lam'] = 4.878015572616551
    kappas['kappaSingleHiggs'] = 0.98996618183163
    kappas['uu'] = 0.98996618183163
    kappas['dd'] = 0.98996618183163
    kappas['ss'] = 0.98996618183163
    kappas['cc'] = 0.98996618183163
    kappas['bb'] = 0.98996618183163
    kappas['tt'] = 0.98996618183163
    kappas['ee'] = 0.98996618183163
    kappas['mumu'] = 0.98996618183163
    kappas['tautau'] = 0.98996618183163
    kappas['ZZ'] = 0.98996618183163
    kappas['WW'] = 0.98996618183163
    kappas['gamgam'] = 0.98996618183163
    kappas['Zgam'] = 0.98996618183163
    kappas['gg'] = 0.98996618183163
    kappas['ZZ_0'] = 1.0058013280253955
    kappas['ZZ_0_with_WFR'] = 0.988208495287931
    kappas['ZZ_0_no_BSM'] = 1.0157282844316136
    kappas['ZZ_0_with_WFR_no_BSM'] = 0.9983104058838497
    kappas['ZZ_240'] = 1.0252655987178825
    kappas['ZZ_240_with_WFR'] = 1.0080125329656997
    kappas['ZZ_240_no_BSM'] = 1.0350058860948945
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.017917925450115
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.022672297658317
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 1.005374729690044
    kappas['ZZ_365'] = 1.0026622534997187
    kappas['ZZ_365_with_WFR'] = 0.9850133569118349
    kappas['ZZ_365_no_BSM'] = 1.0126199834735015
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.9951477024198278
    kappas['ZZ_365_use_HEPfit_C1_values'] = 1.0010180080433988
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.983339601118943
    kappas['ZZ_500'] = 0.9931138976484806
    kappas['ZZ_500_with_WFR'] = 0.9752922292339586
    kappas['ZZ_500_no_BSM'] = 1.0031664119373698
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.985526543904772
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9918526095545398
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9740078633059068
    kappas['ZZ_550'] = 0.9906731964210413
    kappas['ZZ_550_with_WFR'] = 0.9728068157700536
    kappas['ZZ_550_no_BSM'] = 1.0007502278010347
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.9830670054199819
    kappas['ZZ_HEPfit_C1'] = 1.0060416954162374
    kappas['WW_HEPfit_C1'] = 1.00411248241587
    kappas['gg_HEPfit_C1'] = 1.0027598249045129
    kappas['gamgam_HEPfit_C1'] = 0.9994671780349172
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8946293127882845
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.022603345218163762
    # mS = 1358.7347235071884
    # muS = 1048.030554858611
    # lamS = 0.0340977523387375
    # lamSH = 24.713860960635483
    # Best scan point row: 15775 out of 64942

elif BP == "BPBnew_8":
    kappas['lam'] = 7.24831645311373
    kappas['kappaSingleHiggs'] = 0.9813387077797447
    kappas['uu'] = 0.9813387077797447
    kappas['dd'] = 0.9813387077797447
    kappas['ss'] = 0.9813387077797447
    kappas['cc'] = 0.9813387077797447
    kappas['bb'] = 0.9813387077797447
    kappas['tt'] = 0.9813387077797447
    kappas['ee'] = 0.9813387077797447
    kappas['mumu'] = 0.9813387077797447
    kappas['tautau'] = 0.9813387077797447
    kappas['ZZ'] = 0.9813387077797447
    kappas['WW'] = 0.9813387077797447
    kappas['gamgam'] = 0.9813387077797447
    kappas['Zgam'] = 0.9813387077797447
    kappas['gg'] = 0.9813387077797447
    kappas['ZZ_0'] = 1.0068561409018644
    kappas['ZZ_0_with_WFR'] = 0.9666669837744679
    kappas['ZZ_0_no_BSM'] = 1.0252228406118864
    kappas['ZZ_0_with_WFR_no_BSM'] = 0.9857827559661093
    kappas['ZZ_240'] = 1.038005697427999
    kappas['ZZ_240_with_WFR'] = 0.9990703663610583
    kappas['ZZ_240_no_BSM'] = 1.0558306740824956
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.0175776045989464
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.0338756188548133
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 0.9947786509119781
    kappas['ZZ_365'] = 1.0017988993564473
    kappas['ZZ_365_with_WFR'] = 0.9613983585380317
    kappas['ZZ_365_no_BSM'] = 1.0202566437873852
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.9806168406876011
    kappas['ZZ_365_use_HEPfit_C1_values'] = 0.999146045051592
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9586337091872318
    kappas['ZZ_500'] = 0.9863554683878892
    kappas['ZZ_500_with_WFR'] = 0.9452951280243249
    kappas['ZZ_500_no_BSM'] = 1.0050968582476034
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9648344228452026
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9843085130425684
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9431590628817096
    kappas['ZZ_550'] = 0.982392935048722
    kappas['ZZ_550_with_WFR'] = 0.9411597355823692
    kappas['ZZ_550_no_BSM'] = 1.0012085013992607
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.960783134907137
    kappas['ZZ_HEPfit_C1'] = 1.007242990603724
    kappas['WW_HEPfit_C1'] = 1.0041365074865167
    kappas['gg_HEPfit_C1'] = 1.0019562386402112
    kappas['gamgam_HEPfit_C1'] = 0.996641443137775
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.9526676399017474
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.036206798071551693
    # mS = 796.8225379825861
    # muS = 67.52416688293073
    # lamS = 0.069290944402981
    # lamSH = 20.83305717244286
    # Best scan point row: 32483 out of 64942

elif BP == "BPBnew_9":
    kappas['lam'] = 7.005268951781772
    kappas['kappaSingleHiggs'] = 0.9845763293696326
    kappas['uu'] = 0.9845763293696326
    kappas['dd'] = 0.9845763293696326
    kappas['ss'] = 0.9845763293696326
    kappas['cc'] = 0.9845763293696326
    kappas['bb'] = 0.9845763293696326
    kappas['tt'] = 0.9845763293696326
    kappas['ee'] = 0.9845763293696326
    kappas['mumu'] = 0.9845763293696326
    kappas['tautau'] = 0.9845763293696326
    kappas['ZZ'] = 0.9845763293696326
    kappas['WW'] = 0.9845763293696326
    kappas['gamgam'] = 0.9845763293696326
    kappas['Zgam'] = 0.9845763293696326
    kappas['gg'] = 0.9845763293696326
    kappas['ZZ_0'] = 1.0090825263426086
    kappas['ZZ_0_with_WFR'] = 0.9717328206624107
    kappas['ZZ_0_no_BSM'] = 1.0242533310810935
    kappas['ZZ_0_with_WFR_no_BSM'] = 0.9874776027906961
    kappas['ZZ_240'] = 1.0389737299020732
    kappas['ZZ_240_with_WFR'] = 1.0027380222217415
    kappas['ZZ_240_no_BSM'] = 1.0537142652006573
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.0180033803823565
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.0350083240822536
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 0.9986287401742947
    kappas['ZZ_365'] = 1.0042332536798644
    kappas['ZZ_365_with_WFR'] = 0.96669620749178
    kappas['ZZ_365_no_BSM'] = 1.0194762228993777
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.982521704004408
    kappas['ZZ_365_use_HEPfit_C1_values'] = 1.0016899179708365
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9640538478461486
    kappas['ZZ_500'] = 0.9894315674796945
    kappas['ZZ_500_with_WFR'] = 0.9513106519470225
    kappas['ZZ_500_no_BSM'] = 1.0048990834835407
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9673878734864335
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9874704425963995
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9492707752712461
    kappas['ZZ_550'] = 0.9856353526736547
    kappas['ZZ_550_with_WFR'] = 0.9473616934532783
    kappas['ZZ_550_no_BSM'] = 1.0011615202857402
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.9635048103063099
    kappas['ZZ_HEPfit_C1'] = 1.009453511083623
    kappas['WW_HEPfit_C1'] = 1.0064746008157741
    kappas['gg_HEPfit_C1'] = 1.0043841067146695
    kappas['gamgam_HEPfit_C1'] = 0.9992889855307101
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8913818695182367
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.03474047622220877
    # mS = 1080.1666061800718
    # muS = 651.2200151232414
    # lamS = 0.0288391862473291
    # lamSH = 24.544662205349308
    # Best scan point row: 38210 out of 64942

elif BP == "BPBnew_10":
    kappas['lam'] = 8.535635929341407
    kappas['kappaSingleHiggs'] = 0.9791890510548172
    kappas['uu'] = 0.9791890510548172
    kappas['dd'] = 0.9791890510548172
    kappas['ss'] = 0.9791890510548172
    kappas['cc'] = 0.9791890510548172
    kappas['bb'] = 0.9791890510548172
    kappas['tt'] = 0.9791890510548172
    kappas['ee'] = 0.9791890510548172
    kappas['mumu'] = 0.9791890510548172
    kappas['tautau'] = 0.9791890510548172
    kappas['ZZ'] = 0.9791890510548172
    kappas['WW'] = 0.9791890510548172
    kappas['gamgam'] = 0.9791890510548172
    kappas['Zgam'] = 0.9791890510548172
    kappas['gg'] = 0.9791890510548172
    kappas['ZZ_0'] = 1.0099426717825917
    kappas['ZZ_0_with_WFR'] = 0.9536247610287034
    kappas['ZZ_0_no_BSM'] = 1.030342709091361
    kappas['ZZ_0_with_WFR_no_BSM'] = 0.9752036109128274
    kappas['ZZ_240'] = 1.047284069386053
    kappas['ZZ_240_with_WFR'] = 0.9930860519358344
    kappas['ZZ_240_no_BSM'] = 1.0669703931600802
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.0138253323131496
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.0423453904097424
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 0.9878764586061004
    kappas['ZZ_365'] = 1.0038590916850385
    kappas['ZZ_365_with_WFR'] = 0.9471795291909567
    kappas['ZZ_365_no_BSM'] = 1.0243802877101238
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.9689019343611447
    kappas['ZZ_365_use_HEPfit_C1_values'] = 1.00066539208013
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9437940514045278
    kappas['ZZ_500'] = 0.9852427749569556
    kappas['ZZ_500_with_WFR'] = 0.9274261750482214
    kappas['ZZ_500_no_BSM'] = 1.0061437389832766
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9496005518400565
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9827707676155628
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9247996357262337
    kappas['ZZ_550'] = 0.9804564412461152
    kappas['ZZ_550_with_WFR'] = 0.9223398602146006
    kappas['ZZ_550_no_BSM'] = 1.0014573036686898
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.944633640958787
    kappas['ZZ_HEPfit_C1'] = 1.0104077792273614
    kappas['WW_HEPfit_C1'] = 1.0066718653035986
    kappas['gg_HEPfit_C1'] = 1.0040484546292014
    kappas['gamgam_HEPfit_C1'] = 0.9976485945278565
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.9183849500445748
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.0434249777010145
    # mS = 823.9940050307168
    # muS = 31.96901574957845
    # lamS = 0.1115402288081102
    # lamSH = 22.405449876348875
    # Best scan point row: 11799 out of 64942

elif BP == "BPBnew_11":
    kappas['lam'] = 8.84021000223677
    kappas['kappaSingleHiggs'] = 0.98016935808828
    kappas['uu'] = 0.98016935808828
    kappas['dd'] = 0.98016935808828
    kappas['ss'] = 0.98016935808828
    kappas['cc'] = 0.98016935808828
    kappas['bb'] = 0.98016935808828
    kappas['tt'] = 0.98016935808828
    kappas['ee'] = 0.98016935808828
    kappas['mumu'] = 0.98016935808828
    kappas['tautau'] = 0.98016935808828
    kappas['ZZ'] = 0.98016935808828
    kappas['WW'] = 0.98016935808828
    kappas['gamgam'] = 0.98016935808828
    kappas['Zgam'] = 0.98016935808828
    kappas['gg'] = 0.98016935808828
    kappas['ZZ_0'] = 1.0121436653601905
    kappas['ZZ_0_with_WFR'] = 0.9516860488231159
    kappas['ZZ_0_no_BSM'] = 1.0315503299171598
    kappas['ZZ_0_with_WFR_no_BSM'] = 0.9723001693654045
    kappas['ZZ_240'] = 1.0508850592226122
    kappas['ZZ_240_with_WFR'] = 0.9927894761192357
    kappas['ZZ_240_no_BSM'] = 1.0695890292634613
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.0125671472631068
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.0457639725170231
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 0.9873671163302827
    kappas['ZZ_365'] = 1.005827276974337
    kappas['ZZ_365_with_WFR'] = 0.9449656328678852
    kappas['ZZ_365_no_BSM'] = 1.0253534975456267
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.9657232166230875
    kappas['ZZ_365_use_HEPfit_C1_values'] = 1.0025108045249735
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9414347823323199
    kappas['ZZ_500'] = 0.9864897863100432
    kappas['ZZ_500_with_WFR'] = 0.9243557944264902
    kappas['ZZ_500_no_BSM'] = 1.0063912670117299
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9455659249958555
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9839209948358528
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9216138346805388
    kappas['ZZ_550'] = 0.9815158354283612
    kappas['ZZ_550_with_WFR'] = 0.9190456307455179
    kappas['ZZ_550_no_BSM'] = 1.001516160139253
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.9403755394606279
    kappas['ZZ_HEPfit_C1'] = 1.012626515155082
    kappas['WW_HEPfit_C1'] = 1.0087478620512107
    kappas['gg_HEPfit_C1'] = 1.0060239073656863
    kappas['gamgam_HEPfit_C1'] = 0.9993776789520167
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8854815723247201
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.04505778224827517
    # mS = 957.2657014098172
    # muS = 409.7368992474435
    # lamS = 0.0048392293567689
    # lamSH = 24.7363770404759
    # Best scan point row: 18404 out of 64942

elif BP == "BPBnew_12":
    kappas['lam'] = 9.584476423981522
    kappas['kappaSingleHiggs'] = 0.9775885324481944
    kappas['uu'] = 0.9775885324481944
    kappas['dd'] = 0.9775885324481944
    kappas['ss'] = 0.9775885324481944
    kappas['cc'] = 0.9775885324481944
    kappas['bb'] = 0.9775885324481944
    kappas['tt'] = 0.9775885324481944
    kappas['ee'] = 0.9775885324481944
    kappas['mumu'] = 0.9775885324481944
    kappas['tautau'] = 0.9775885324481944
    kappas['ZZ'] = 0.9775885324481944
    kappas['WW'] = 0.9775885324481944
    kappas['gamgam'] = 0.9775885324481944
    kappas['Zgam'] = 0.9775885324481944
    kappas['gg'] = 0.9775885324481944
    kappas['ZZ_0'] = 1.0125995016223126
    kappas['ZZ_0_with_WFR'] = 0.9410238790750765
    kappas['ZZ_0_no_BSM'] = 1.0344953773649097
    kappas['ZZ_0_with_WFR_no_BSM'] = 0.96454594296649
    kappas['ZZ_240'] = 1.054926326372454
    kappas['ZZ_240_with_WFR'] = 0.9864267557084154
    kappas['ZZ_240_no_BSM'] = 1.0759611931558186
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.0088908164321058
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.0493393941447517
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 0.980449567498412
    kappas['ZZ_365'] = 1.0056845752943755
    kappas['ZZ_365_with_WFR'] = 0.9335789496816949
    kappas['ZZ_365_no_BSM'] = 1.0277277850134439
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.9572839653897832
    kappas['ZZ_365_use_HEPfit_C1_values'] = 1.0020521845258776
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9296648701638843
    kappas['ZZ_500'] = 0.984488579510937
    kappas['ZZ_500_with_WFR'] = 0.9107062937584274
    kappas['ZZ_500_no_BSM'] = 1.0069958779911037
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.93499138423561
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9816698510986933
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.9076584637736151
    kappas['ZZ_550'] = 0.979030008975994
    kappas['ZZ_550_with_WFR'] = 0.9048027126281636
    kappas['ZZ_550_no_BSM'] = 1.0016599690409644
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.9292421018673735
    kappas['ZZ_HEPfit_C1'] = 1.013127938226676
    kappas['WW_HEPfit_C1'] = 1.0088824226793993
    kappas['gg_HEPfit_C1'] = 1.0058999002359363
    kappas['gamgam_HEPfit_C1'] = 0.9986195468615153
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.896505452488693
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.04924175107807849
    # mS = 855.3699274942333
    # muS = 106.25539388488514
    # lamS = 0.0154150319505119
    # lamSH = 23.80750558965753
    # Best scan point row: 63349 out of 64942

elif BP == "BPBnew_13":
    kappas['lam'] = 10.34814810189343
    kappas['kappaSingleHiggs'] = 0.9763251458223264
    kappas['uu'] = 0.9763251458223264
    kappas['dd'] = 0.9763251458223264
    kappas['ss'] = 0.9763251458223264
    kappas['cc'] = 0.9763251458223264
    kappas['bb'] = 0.9763251458223264
    kappas['tt'] = 0.9763251458223264
    kappas['ee'] = 0.9763251458223264
    kappas['mumu'] = 0.9763251458223264
    kappas['tautau'] = 0.9763251458223264
    kappas['ZZ'] = 0.9763251458223264
    kappas['WW'] = 0.9763251458223264
    kappas['gamgam'] = 0.9763251458223264
    kappas['Zgam'] = 0.9763251458223264
    kappas['gg'] = 0.9763251458223264
    kappas['ZZ_0'] = 1.014432956827298
    kappas['ZZ_0_with_WFR'] = 0.9304926865939384
    kappas['ZZ_0_no_BSM'] = 1.0375085215325808
    kappas['ZZ_0_with_WFR_no_BSM'] = 0.9555973776440329
    kappas['ZZ_240'] = 1.0603636372572889
    kappas['ZZ_240_with_WFR'] = 0.9803639421790961
    kappas['ZZ_240_no_BSM'] = 1.082460508089258
    kappas['ZZ_240_with_WFR_no_BSM'] = 1.0042226682764561
    kappas['ZZ_240_use_HEPfit_C1_values'] = 1.054309636386219
    kappas['ZZ_240_with_WFR_HEPfit_C1_values'] = 0.9738127259818861
    kappas['ZZ_365'] = 1.006914292508797
    kappas['ZZ_365_with_WFR'] = 0.9222899806275258
    kappas['ZZ_365_no_BSM'] = 1.0301582892030905
    kappas['ZZ_365_with_WFR_no_BSM'] = 0.9476120074805242
    kappas['ZZ_365_use_HEPfit_C1_values'] = 1.0029629782925416
    kappas['ZZ_365_with_WFR_HEPfit_C1_values'] = 0.9179744831600037
    kappas['ZZ_500'] = 0.9838394406533161
    kappas['ZZ_500_with_WFR'] = 0.8970409471659923
    kappas['ZZ_500_no_BSM'] = 1.0076158758874223
    kappas['ZZ_500_with_WFR_no_BSM'] = 0.9230558863079784
    kappas['ZZ_500_use_HEPfit_C1_values'] = 0.9807675352832226
    kappas['ZZ_500_with_WFR_HEPfit_C1_values'] = 0.8936707302877038
    kappas['ZZ_550'] = 0.977889856144331
    kappas['ZZ_550_with_WFR'] = 0.8905116431902566
    kappas['ZZ_550_no_BSM'] = 1.001807506013669
    kappas['ZZ_550_with_WFR_no_BSM'] = 0.9167118931336923
    kappas['ZZ_HEPfit_C1'] = 1.0150073501656864
    kappas['WW_HEPfit_C1'] = 1.0103918906980969
    kappas['gg_HEPfit_C1'] = 1.0071484841457836
    kappas['gamgam_HEPfit_C1'] = 0.9992278105336794
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8854559992909945
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.053449344748491834
    # mS = 861.096892426842
    # muS = 23.85086023360161
    # lamS = 0.0280805001781014
    # lamSH = 24.486714079360222
    # Best scan point row: 64883 out of 64942

else:
    raise ValueError("Could not determine benchmark point!")



if no_BSM or no_BSM_WFR_kala2_input_all:
    kappas['ZZ_0']   = kappas['ZZ_0_no_BSM']
    kappas['ZZ_240'] = kappas['ZZ_240_no_BSM']
    # kappas['ZZ_125'] = kappas['ZZ_125_no_BSM']
    kappas['ZZ_365'] = kappas['ZZ_365_no_BSM']
    kappas['ZZ_500'] = kappas['ZZ_500_no_BSM']
    kappas['ZZ_550'] = kappas['ZZ_550_no_BSM']

if use_HEPfit_C1_values_WFR_kala2_input_all or \
    use_HEPfit_C1_values_decayrates_WFR_kala2_input_all:
    kappas['ZZ_240'] = kappas['ZZ_240_use_HEPfit_C1_values']
    kappas['ZZ_365'] = kappas['ZZ_365_use_HEPfit_C1_values']
    kappas['ZZ_500'] = kappas['ZZ_500_use_HEPfit_C1_values']

if use_HEPfit_C1_values_decayrates_WFR_kala2_input_all:
    kappas['ZZ']   = kappas['ZZ_HEPfit_C1']
    kappas['ZZ_0'] = kappas['ZZ_HEPfit_C1'] # Used for the Zh cross-section at HL-LHC
    kappas['WW']   = kappas['WW_HEPfit_C1']
    kappas['gg']   = kappas['gg_HEPfit_C1']
    kappas['gamgam'] = kappas['gamgam_HEPfit_C1']


M_PI = 3.14159265358979323846
GF = 1.1663787e-5
mHl = 125.1
sqrt = np.sqrt


# Expression for the Higgs self-energy diagram
dZH = -(9.0/16.0)*( GF*mHl*mHl/sqrt(2.0)/M_PI/M_PI )*( 2.0*M_PI/3.0/sqrt(3.0) - 1.0 )

# Resummations
dZH1 = dZH / (1.0 - dZH)
dZH2 = dZH * (1 + 3.0 * dZH) / (1.0 - dZH) / (1.0 - dZH)

# HEPfit flags
cLHd6 = 1
cLH3d62 = 1



# e+e- cross-sections
def smeft_mueeZH(lmbd, sqrt_s):
    mu = 1.0

    if sqrt_s == 0.240:
        C1 = 0.017
    elif sqrt_s == 0.365:
        C1 = 0.0057
    elif sqrt_s == 0.500:
        C1 = 0.00099
    else:
        raise ValueError("sqrt_s for the e+e- collider must be 240, 365, or 500 GeV")

    deltaG_hhhRatio = lmbd - 1

    mu = mu + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio
    
    mu = mu + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return mu

def smeft_mueeHvv(lmbd, sqrt_s):
    mu = 1.0

    if sqrt_s == 0.240:
        C1 = 0.0064
    elif sqrt_s == 0.365:
        C1 = 0.0062
    elif sqrt_s == 0.500:
        C1 = 0.0061
    else:
        raise ValueError("sqrt_s for the e+e- collider must be 240, 365, or 500 GeV")

    deltaG_hhhRatio = lmbd - 1

    mu = mu + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    mu = mu + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return mu

# pp cross-sections
def smeft_muggH(lmbd, sqrt_s):
    mu = 1.0

    C1 = 0.0066 # It seems to be independent of energy 

    deltaG_hhhRatio = lmbd - 1

    mu = mu + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    mu = mu + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return mu

def smeft_muVBF(lmbd, sqrt_s):
    mu = 1.0

    if sqrt_s == 7.0:
        C1 = 0.0065
    elif sqrt_s == 8.0:
        C1 = 0.0065
    elif sqrt_s == 13.0:
        C1 = 0.0064
    elif sqrt_s == 14.0:
        C1 = 0.0064
    else:
        raise ValueError("sqrt_s for pp collider must be 7, 8, 13 or 14 TeV")

    deltaG_hhhRatio = lmbd - 1

    mu = mu + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    mu = mu + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return mu

def smeft_muZH(lmbd, sqrt_s):
    mu = 1.0

    if sqrt_s == 7.0:
        C1 = 0.0123
    elif sqrt_s == 8.0:
        C1 = 0.0122
    elif sqrt_s == 13.0:
        C1 = 0.0119
    elif sqrt_s == 14.0:
        C1 = 0.0118
    else:
        raise ValueError("sqrt_s for pp collider must be 7, 8, 13 or 14 TeV")

    deltaG_hhhRatio = lmbd - 1

    mu = mu + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    mu = mu + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return mu

def smeft_muWH(lmbd, sqrt_s):
    mu = 1.0

    if sqrt_s == 7.0:
        C1 = 0.0106
    elif sqrt_s == 8.0:
        C1 = 0.0105
    elif sqrt_s == 13.0:
        C1 = 0.0103
    elif sqrt_s == 14.0:
        C1 = 0.0103
    else:
        raise ValueError("sqrt_s for pp collider must be 7, 8, 13 or 14 TeV")

    deltaG_hhhRatio = lmbd - 1

    mu = mu + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    mu = mu + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return mu

def smeft_muttH(lmbd, sqrt_s):
    mu = 1.0

    if sqrt_s == 7.0:
        C1 = 0.0387
    elif sqrt_s == 8.0:
        C1 = 0.0378
    elif sqrt_s == 13.0:
        C1 = 0.0351
    elif sqrt_s == 14.0:
        C1 = 0.0347
    else:
        raise ValueError("sqrt_s for pp collider must be 7, 8, 13 or 14 TeV")

    deltaG_hhhRatio = lmbd - 1

    mu = mu + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    mu = mu + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return mu


# Higgs branching ratios
def smeft_deltaGammaHgagaRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0049

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

def smeft_deltaGammaHZgaRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

def smeft_deltaGammaHZZ4lRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0083

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

def smeft_deltaGammaHZZ4fRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0083

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

def smeft_deltaGammaHZZRatio(lmbd):
    return smeft_deltaGammaHZZ4fRatio(lmbd)

def smeft_deltaGammaHWW2l2vRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0073

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

def smeft_deltaGammaHWW4fRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0073

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

def smeft_deltaGammaHWWRatio(lmbd):
    return smeft_deltaGammaHWW4fRatio(lmbd)

def smeft_deltaGammaHmumuRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

def smeft_deltaGammaHtautauRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

def smeft_deltaGammaHbbRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

def smeft_deltaGammaHccRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

def smeft_deltaGammaHggRatio(lmbd):
    dwidth = 0.0

    C1 = 0.0066

    deltaG_hhhRatio = lmbd - 1

    dwidth = dwidth + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    dwidth = dwidth + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return dwidth

# Obs: all ZZ branching ratios have the same C1 value. Same with WW
# Todo: ask Henning what to do with the other couplings (WW, ZZ, Zga, gaga)
# Todo: check if all couplings are correctly assigned to the XS and BR

if smeft_formula:
    # Implements the Zh cross-section using the kappa_lambda dependent expression from HEPfit,
    # plus the external-leg correction (~C_Hbox), taken from the coupling modifier to fermions.
    # No BSM contributions to the ZH cross-section are included.
    kappas['ZZ_240'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.240)) + (kappas["uu"]-1)
    kappas['ZZ_365'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.365)) + (kappas["uu"]-1)
    kappas['ZZ_500'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.500)) + (kappas["uu"]-1)
    
    kappas['ZZ_0'] = kappas["ZZ"]

if smeft_formula_sqrt:
    # Implements the Zh cross-section using the kappa_lambda dependent expression from HEPfit,
    # plus the external-leg correction (~C_Hbox), taken from the coupling modifier to fermions.
    # No BSM contributions to the ZH cross-section are included.
    # Cross terms are removed by including dkappaf**2 inside of the square root
    kappas['ZZ_240'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.240) + (kappas["uu"]-1)**2)
    kappas['ZZ_365'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.365) + (kappas["uu"]-1)**2)
    kappas['ZZ_500'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.500) + (kappas["uu"]-1)**2)
    
    kappas['ZZ_0'] = kappas["ZZ"]

if smeft_formula_no_cross:
    # Implements the Zh cross-section using the kappa_lambda dependent expression from HEPfit,
    # plus the external-leg correction (~C_Hbox), taken from the coupling modifier to fermions.
    # No BSM contributions to the ZH cross-section are included.
    # Cross terms are removed by including 2*dkappaf inside of the square root
    kappas['ZZ_240'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.240) + 2*(kappas["uu"]-1))
    kappas['ZZ_365'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.365) + 2*(kappas["uu"]-1))
    kappas['ZZ_500'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.500) + 2*(kappas["uu"]-1))
    
    kappas['ZZ_0'] = kappas["ZZ"]

if smeft_formula_external_leg:
    # Implements the Zh cross-section using the kappa_lambda dependent expression from HEPfit,
    # No BSM contributions to the ZH cross-section are included.
    kappas['ZZ_240'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.240))
    kappas['ZZ_365'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.365))
    kappas['ZZ_500'] = sqrt(smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.500))
    
    kappas['ZZ_0'] = kappas["ZZ"]

if smeft_formula_all:
    # Implements all XS and BR using the kappa_lambda dependent expression from HEPfit,
    # plus the external-leg correction (~C_Hbox), taken from the coupling modifier to fermions.
    # No BSM contributions to the ZH cross-section are included.
    # Cross terms are removed by including dkappaf**2 inside of the square root
    kappas['ZZ_240'] = sqrt( smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.240) + 2*(kappas["uu"]-1) )
    kappas['ZZ_365'] = sqrt( smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.365) + 2*(kappas["uu"]-1) )
    kappas['ZZ_500'] = sqrt( smeft_mueeZH(lmbd=kappas["lam"], sqrt_s=0.500) + 2*(kappas["uu"]-1) )

    kappas['WW_240'] = sqrt( smeft_mueeHvv(lmbd=kappas["lam"], sqrt_s=0.240) + 2*(kappas["uu"]-1) )
    kappas['WW_365'] = sqrt( smeft_mueeHvv(lmbd=kappas["lam"], sqrt_s=0.365) + 2*(kappas["uu"]-1) )
    kappas['WW_500'] = sqrt( smeft_mueeHvv(lmbd=kappas["lam"], sqrt_s=0.500) + 2*(kappas["uu"]-1) )

    kappas['bb']     = sqrt( 1.0 + smeft_deltaGammaHbbRatio(lmbd=kappas["lam"])     + 2*(kappas["uu"]-1) )
    kappas['cc']     = sqrt( 1.0 + smeft_deltaGammaHccRatio(lmbd=kappas["lam"])     + 2*(kappas["uu"]-1) )
    kappas['gg']     = sqrt( 1.0 + smeft_deltaGammaHggRatio(lmbd=kappas["lam"])     + 2*(kappas["uu"]-1) )
    kappas['WW']     = sqrt( 1.0 + smeft_deltaGammaHWWRatio(lmbd=kappas["lam"])     + 2*(kappas["uu"]-1) )
    kappas['ZZ']     = sqrt( 1.0 + smeft_deltaGammaHZZRatio(lmbd=kappas["lam"])     + 2*(kappas["uu"]-1) )
    kappas['tautau'] = sqrt( 1.0 + smeft_deltaGammaHtautauRatio(lmbd=kappas["lam"]) + 2*(kappas["uu"]-1) )
    kappas['mumu']   = sqrt( 1.0 + smeft_deltaGammaHmumuRatio(lmbd=kappas["lam"])   + 2*(kappas["uu"]-1) )
    kappas['gamgam'] = sqrt( 1.0 + smeft_deltaGammaHgagaRatio(lmbd=kappas["lam"])   + 2*(kappas["uu"]-1) )
    kappas['Zgam']   = sqrt( 1.0 + smeft_deltaGammaHZgaRatio(lmbd=kappas["lam"])    + 2*(kappas["uu"]-1) )
    
    kappas['ZZ_0'] = kappas["ZZ"]
    kappas['ss'] = kappas['cc'] # No information from HEPfit, but C1=0 just as for cc and bb
    kappas['dd'] = kappas['cc'] 
    kappas['uu'] = kappas['cc'] 
    kappas['ee'] = kappas['cc'] 

    kappas["ggH_HLLHC"] = sqrt( smeft_muggH(lmbd=kappas["lam"], sqrt_s=14.0) + 2*(kappas["uu"]-1) )
    kappas["VBF_HLLHC"] = sqrt( smeft_muVBF(lmbd=kappas["lam"], sqrt_s=14.0) + 2*(kappas["uu"]-1) )
    kappas["ZH_HLLHC"]  = sqrt( smeft_muZH (lmbd=kappas["lam"], sqrt_s=14.0) + 2*(kappas["uu"]-1) )
    kappas["WH_HLLHC"]  = sqrt( smeft_muWH (lmbd=kappas["lam"], sqrt_s=14.0) + 2*(kappas["uu"]-1) )
    kappas["ttH_HLLHC"] = sqrt( smeft_muttH(lmbd=kappas["lam"], sqrt_s=14.0) + 2*(kappas["uu"]-1) )

else:
    # Need to weigh the kappas to get the scaling factor for VBF
    wgt_W_VBF = 10.
    wgt_Z_VBF = 1.
    kappas["VBF"]     = sqrt( (wgt_W_VBF*kappas["WW"]**2 + wgt_Z_VBF*kappas["ZZ"]**2    ) / (wgt_W_VBF + wgt_Z_VBF) )
    kappas["VBF_0"]   = sqrt( (wgt_W_VBF*kappas["WW"]**2 + wgt_Z_VBF*kappas["ZZ_0"]**2  ) / (wgt_W_VBF + wgt_Z_VBF) )
    # kappas["VBF_125"] = sqrt( (wgt_W_VBF*kappas["WW"]**2 + wgt_Z_VBF*kappas["ZZ_125"]**2) / (wgt_W_VBF + wgt_Z_VBF) )
    kappas["VBF_240"] = sqrt( (wgt_W_VBF*kappas["WW"]**2 + wgt_Z_VBF*kappas["ZZ_240"]**2) / (wgt_W_VBF + wgt_Z_VBF) )
    kappas["VBF_365"] = sqrt( (wgt_W_VBF*kappas["WW"]**2 + wgt_Z_VBF*kappas["ZZ_365"]**2) / (wgt_W_VBF + wgt_Z_VBF) )

    kappas["WW_240"] = kappas["WW"]
    kappas["WW_365"] = kappas["WW"]
    kappas["WW_500"] = kappas["WW"]

    kappas["ggH_HLLHC"] = kappas["gg"]
    kappas["VBF_HLLHC"] = kappas["VBF"]
    kappas["ZH_HLLHC"]  = kappas["ZZ_0"]
    kappas["WH_HLLHC"]  = kappas["WW"]
    kappas["ttH_HLLHC"] = kappas["tt"]

# Johannes' formula
Mh = 125.1
vev = 246.21965
def ZZh_hextleg(kala):
    dZh = -(Mh**2*(-9 + 2*np.sqrt(3)*np.pi))/(32*np.pi**2*vev**2)
    return (kala**2-1)*dZh

if WFR_kala2_input:
    # Adds the external-leg correction (the contribution proportional to kappa_lambda**2) to 
    # the ZH cross-section coupling modifier
    kappas['ZZ_0']   = sqrt( kappas["ZZ_0"]**2   + ZZh_hextleg( kappas["lam"] ) )
    kappas['ZZ_240'] = sqrt( kappas['ZZ_240']**2 + ZZh_hextleg( kappas["lam"] ) )
    kappas['ZZ_365'] = sqrt( kappas['ZZ_365']**2 + ZZh_hextleg( kappas["lam"] ) )
    kappas['ZZ_500'] = sqrt( kappas['ZZ_500']**2 + ZZh_hextleg( kappas["lam"] ) )
    # kappas['ZZ_0'] =   kappas['ZZ_0_with_WFR']
    # kappas['ZZ_240'] = kappas['ZZ_240_with_WFR']
    # kappas['ZZ_365'] = kappas['ZZ_365_with_WFR']
    # kappas['ZZ_500'] = kappas['ZZ_500_with_WFR']

if WFR_kala2_input_all or \
    use_HEPfit_C1_values_WFR_kala2_input_all or \
    use_HEPfit_C1_values_decayrates_WFR_kala2_input_all or \
    no_BSM_WFR_kala2_input_all:
    # Adds the external-leg correction (the contribution proportional to kappa_lambda**2) to 
    # the all Higgs cross-sections and decay rates
    coupling_list = [
        'ZZ_0', 'ZZ_240', 'ZZ_365', 'ZZ_500', 'ZZ_550',
        'WW_240', 'WW_365', 'WW_500',
        'tt', 'bb', 'cc', 'ss', 'dd', 'uu', 'tautau', 'mumu', 'ee',
        'gg', 'WW', 'ZZ', 'gamgam', 'Zgam',
        'VBF_HLLHC', 'ZH_HLLHC', 'WH_HLLHC', 'ttH_HLLHC', "ggH_HLLHC", 
    ]
    for coup in coupling_list:
        kappas[coup] = sqrt( kappas[coup]**2 + ZZh_hextleg( kappas["lam"] ) )


BrHinv = 0.
BrHexo = 0.

kappas2 = {}
for kappa in kappas.keys():
    kappas2[kappa] = kappas[kappa]**2

if no_quad:
    for kappa in ['ZZ_0', 'ZZ_240', 'ZZ_365', 'ZZ_500', 'ZZ_550', ]:
        kappas2[kappa] = 2*kappas[kappa] - 1
        # Only linear correction to the Z->ZH cross sections are included




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
               kappas2["ZZ"]*BR_H_to_ZZ     + \
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
             "# Z2SSM Benchmark Point:\n"


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

output_file_flag_map = {
    no_BSM: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_BSM.conf",
    no_quad: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_quad.conf",
    smeft_formula: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_smeft_formula.conf",
    smeft_formula_sqrt: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_smeft_formula_sqrt.conf",
    smeft_formula_no_cross: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_smeft_formula_no_cross.conf",
    smeft_formula_external_leg: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_smeft_formula_external_leg.conf",
    smeft_formula_all: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_smeft_formula_all.conf",
    WFR_kala2_input: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_WFR_kala2_input.conf",
    WFR_kala2_input_all: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_WFR_kala2_input_all.conf",
    use_HEPfit_C1_values_WFR_kala2_input_all: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_use_HEPfit_C1_values_WFR_kala2_input_all.conf",
    use_HEPfit_C1_values_decayrates_WFR_kala2_input_all: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_use_HEPfit_C1_values_decayrates_WFR_kala2_input_all.conf",
    no_BSM_WFR_kala2_input_all: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_BSM_WFR_kala2_input_all.conf",
}

for condition, filename in output_file_flag_map.items():
    if condition:
        output_file_FCCee240 = file_dir + filename
        break


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
                columns[8] = str(kappas2["WW_240"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW_240"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

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

if (scenario == "Z2SSM_FCCee240_FCCee365" 
    or scenario == "Z2SSM_FCCee240_FCCee365_HLLHClambda"):
    # Open the FCCee_365 input file in read mode and output file in write mode
    input_file_FCCee365 =  file_dir + "ObservablesHiggs_FCCee_365.conf"
    output_file_FCCee365 = file_dir + "ObservablesHiggs_FCCee_365_kappa_scaled.conf"

    output_file_flag_map = {
        no_BSM: "ObservablesHiggs_FCCee_365_kappa_scaled_no_BSM.conf",
        no_quad: "ObservablesHiggs_FCCee_365_kappa_scaled_no_quad.conf",
        smeft_formula: "ObservablesHiggs_FCCee_365_kappa_scaled_smeft_formula.conf",
        smeft_formula_sqrt: "ObservablesHiggs_FCCee_365_kappa_scaled_smeft_formula_sqrt.conf",
        smeft_formula_no_cross: "ObservablesHiggs_FCCee_365_kappa_scaled_smeft_formula_no_cross.conf",
        smeft_formula_external_leg: "ObservablesHiggs_FCCee_365_kappa_scaled_smeft_formula_external_leg.conf",
        smeft_formula_all: "ObservablesHiggs_FCCee_365_kappa_scaled_smeft_formula_all.conf",
        WFR_kala2_input: "ObservablesHiggs_FCCee_365_kappa_scaled_WFR_kala2_input.conf",
        WFR_kala2_input_all: "ObservablesHiggs_FCCee_365_kappa_scaled_WFR_kala2_input_all.conf",
        use_HEPfit_C1_values_WFR_kala2_input_all: "ObservablesHiggs_FCCee_365_kappa_scaled_use_HEPfit_C1_values_WFR_kala2_input_all.conf",
        use_HEPfit_C1_values_decayrates_WFR_kala2_input_all: "ObservablesHiggs_FCCee_365_kappa_scaled_use_HEPfit_C1_values_decayrates_WFR_kala2_input_all.conf",
        no_BSM_WFR_kala2_input_all: "ObservablesHiggs_FCCee_365_kappa_scaled_no_BSM_WFR_kala2_input_all.conf",
    }

    for condition, filename in output_file_flag_map.items():
        if condition:
            output_file_FCCee365 = file_dir + filename
            break


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
                    columns[8] = str(kappas2["WW_365"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW_365"]*kappas2["bb"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHcc_")):
                    columns[8] = str(kappas2["ZZ_365"]*kappas2["cc"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_365"]*kappas2["cc"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvcc_")):
                    columns[8] = str(kappas2["WW_365"]*kappas2["cc"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW_365"]*kappas2["cc"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHgg_")):
                    columns[8] = str(kappas2["ZZ_365"]*kappas2["gg"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_365"]*kappas2["gg"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvgg_")):
                    columns[8] = str(kappas2["WW_365"]*kappas2["gg"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW_365"]*kappas2["gg"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHWW_")):
                    columns[8] = str(kappas2["ZZ_365"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_365"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvWW_")):
                    columns[8] = str(kappas2["WW_365"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW_365"]*kappas2["WW"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHZZ_")):
                    columns[8] = str(kappas2["ZZ_365"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_365"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvZZ_")):
                    columns[8] = str(kappas2["WW_365"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW_365"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHtautau_")):
                    columns[8] = str(kappas2["ZZ_365"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_365"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvtautau_")):
                    columns[8] = str(kappas2["WW_365"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW_365"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHgaga_")):
                    columns[8] = str(kappas2["ZZ_365"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_365"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvgaga_")):
                    columns[8] = str(kappas2["WW_365"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW_365"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])


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

output_file_flag_map = {
    no_BSM: "ObservablesHiggs_HLLHC_SM_kappa_scaled_no_BSM.conf",
    no_quad: "ObservablesHiggs_HLLHC_SM_kappa_scaled_no_quad.conf",
    smeft_formula: "ObservablesHiggs_HLLHC_SM_kappa_scaled_smeft_formula.conf",
    smeft_formula_sqrt: "ObservablesHiggs_HLLHC_SM_kappa_scaled_smeft_formula_sqrt.conf",
    smeft_formula_no_cross: "ObservablesHiggs_HLLHC_SM_kappa_scaled_smeft_formula_no_cross.conf",
    smeft_formula_external_leg: "ObservablesHiggs_HLLHC_SM_kappa_scaled_smeft_formula_external_leg.conf",
    smeft_formula_all: "ObservablesHiggs_HLLHC_SM_kappa_scaled_smeft_formula_all.conf",
    WFR_kala2_input: "ObservablesHiggs_HLLHC_SM_kappa_scaled_WFR_kala2_input.conf",
    WFR_kala2_input_all: "ObservablesHiggs_HLLHC_SM_kappa_scaled_WFR_kala2_input_all.conf",
    use_HEPfit_C1_values_WFR_kala2_input_all: "ObservablesHiggs_HLLHC_SM_kappa_scaled_use_HEPfit_C1_values_WFR_kala2_input_all.conf",
    use_HEPfit_C1_values_decayrates_WFR_kala2_input_all: "ObservablesHiggs_HLLHC_SM_kappa_scaled_use_HEPfit_C1_values_decayrates_WFR_kala2_input_all.conf",
    no_BSM_WFR_kala2_input_all: "ObservablesHiggs_HLLHC_SM_kappa_scaled_no_BSM_WFR_kala2_input_all.conf",
}

for condition, filename in output_file_flag_map.items():
    if condition:
        output_file_HLLHC = file_dir + filename
        break


with open(input_file_HLLHC, 'r') as infile, open(output_file_HLLHC, 'w') as outfile:
    for line in infile:
        if line.startswith("Observable"):
            # Split the line into columns by whitespace
            columns = line.split()

            # ggF
            if (columns[1].startswith("muggHgagaHL")):
                columns[8] = str(kappas2["ggH_HLLHC"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ggH_HLLHC"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHZZ4lHL")):
                columns[8] = str(kappas2["ggH_HLLHC"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ggH_HLLHC"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHWW2l2vHL")):
                columns[8] = str(kappas2["ggH_HLLHC"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ggH_HLLHC"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHtautauHL")):
                columns[8] = str(kappas2["ggH_HLLHC"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ggH_HLLHC"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHbbHL")):
                columns[8] = str(kappas2["ggH_HLLHC"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ggH_HLLHC"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHmumuHL")):
                columns[8] = str(kappas2["ggH_HLLHC"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ggH_HLLHC"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muggHZgaHL")):
                columns[8] = str(kappas2["ggH_HLLHC"]*kappas2["Zgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ggH_HLLHC"]*kappas2["Zgam"]*float(columns[9])/kappas2["H"])


            # VBF
            elif (columns[1].startswith("muVBFgagaHL")):
                columns[8] = str(kappas2["VBF_HLLHC"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_HLLHC"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muVBFZZ4lHL")):
                columns[8] = str(kappas2["VBF_HLLHC"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_HLLHC"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muVBFWW2l2vHL")):
                columns[8] = str(kappas2["VBF_HLLHC"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_HLLHC"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muVBFtautauHL")):
                columns[8] = str(kappas2["VBF_HLLHC"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_HLLHC"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muVBFmumuHL")):
                columns[8] = str(kappas2["VBF_HLLHC"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_HLLHC"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muVBFZgaHL")):
                columns[8] = str(kappas2["VBF_HLLHC"]*kappas2["Zgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["VBF_HLLHC"]*kappas2["Zgam"]*float(columns[9])/kappas2["H"])



            # WH
            elif (columns[1].startswith("muWHgagaHL")):
                columns[8] = str(kappas2["WH_HLLHC"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WH_HLLHC"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muWHZZ4lHL")):
                columns[8] = str(kappas2["WH_HLLHC"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WH_HLLHC"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muWHWW2l2vHL")):
                columns[8] = str(kappas2["WH_HLLHC"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WH_HLLHC"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muWHbbHL")):
                columns[8] = str(kappas2["WH_HLLHC"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WH_HLLHC"]*kappas2["bb"]*float(columns[9])/kappas2["H"])




            # ZH
            elif (columns[1].startswith("muZHgagaHL")):
                columns[8] = str(kappas2["ZH_HLLHC"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZH_HLLHC"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muZHZZ4lHL")):
                columns[8] = str(kappas2["ZH_HLLHC"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZH_HLLHC"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muZHWW2l2vHL")):
                columns[8] = str(kappas2["ZH_HLLHC"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZH_HLLHC"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muZHbbHL")):
                columns[8] = str(kappas2["ZH_HLLHC"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZH_HLLHC"]*kappas2["bb"]*float(columns[9])/kappas2["H"])




            # ttH
            elif (columns[1].startswith("muttHgaga")):
                columns[8] = str(kappas2["ttH_HLLHC"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ttH_HLLHC"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muttHZZ4lHL")):
                columns[8] = str(kappas2["ttH_HLLHC"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ttH_HLLHC"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muttHWW2l2vHL")):
                columns[8] = str(kappas2["ttH_HLLHC"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ttH_HLLHC"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muttHbbHL")):
                columns[8] = str(kappas2["ttH_HLLHC"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ttH_HLLHC"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("muttHtautauHL")):
                columns[8] = str(kappas2["ttH_HLLHC"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ttH_HLLHC"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

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



# import numpy as np
from scipy.interpolate import interp1d
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

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

# Overwrites the main Higgs config file. Implies that the file must already exist!
if scenario == "Z2SSM_FCCee240_FCCee365_HLLHClambda":
    if higgsconf is None:
        if not realistic_HL_LHC_k_lambda_uncertainties:
            input_file = file_dir + "ObservablesHiggs"
        else:
            input_file = file_dir + "ObservablesHiggs_scaled_realistic_HL_LHC"

        flag_map = {
            no_BSM: "_no_BSM",
            no_quad: "_no_quad",
            smeft_formula: "_smeft_formula",
            smeft_formula_sqrt: "_smeft_formula_sqrt",
            smeft_formula_no_cross: "_smeft_formula_no_cross",
            smeft_formula_external_leg: "_smeft_formula_external_leg",
            smeft_formula_all: "_smeft_formula_all",
            WFR_kala2_input: "_WFR_kala2_input",
            WFR_kala2_input_all: "_WFR_kala2_input_all",
            use_HEPfit_C1_values_WFR_kala2_input_all: "_use_HEPfit_C1_values_WFR_kala2_input_all",
            use_HEPfit_C1_values_decayrates_WFR_kala2_input_all: "_use_HEPfit_C1_values_decayrates_WFR_kala2_input_all",
            no_BSM_WFR_kala2_input_all: "_no_BSM_WFR_kala2_input_all",
        }

        for condition, flag in flag_map.items():
            if condition:
                input_file = input_file + flag
                break

    else:
        input_file = file_dir + higgsconf

    output_file = input_file + "_temp.conf"
    input_file  = input_file  + ".conf"
    

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
                if (columns[2].startswith("deltalHHH")):
                    columns[8] = str(kappas['lam']-1)
                    if not realistic_HL_LHC_k_lambda_uncertainties:
                        columns[9] = str(kappas['lam']*0.5)
                    else:
                        columns[0] = "AsyGausObservable"
                        columns[9]  = str(uncertanties_low(kappas['lam']))
                        columns[10] = str(uncertanties_high(kappas['lam']))

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

    subprocess.run(["mv", output_file, input_file])



# # No EWPO predictions for Z2SSM at the moment!!
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
# if modify_all_ewpos:
#     input_files.append(file_dir + "ObservablesEW_Current_SM_noLFU.conf")

output_files = [# "ObservablesEW_Current_SM_noLFU_kappa_scaled.conf",
               file_dir + "ObservablesEW_HLLHC_kappa_scaled.conf",
               file_dir + "ObservablesEW_FCCee_WW_SM_kappa_scaled.conf",
               file_dir + "ObservablesEW_FCCee_Zpole_SM_kappa_scaled.conf",
              ]
# if modify_all_ewpos:
#     output_files.append(file_dir + "ObservablesEW_Current_SM_noLFU_kappa_scaled.conf")

for input_file, output_file in zip(input_files, output_files):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
                # No EWPO predictions for Z2SSM at the moment!!
                # if (columns[2].startswith("GammaZ")):
                #     columns[8] = str(GammaZ)

                # elif (columns[2].startswith("Mw")):
                #     columns[8] = str(Mw)

                # Rejoin the columns and write to the output file
                outfile.write(" ".join(columns) + "\n")
            else:
                # Write unmodified lines to the output file
                outfile.write(line)

    with open(output_file, 'a') as outfile:
        outfile.write(final_text)

    print(f"Modified content saved to {output_file}.")
