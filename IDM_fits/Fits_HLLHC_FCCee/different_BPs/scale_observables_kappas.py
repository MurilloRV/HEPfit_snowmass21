# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

import subprocess
import argparse
import numpy as np
import yaml
import os, sys

sys.path.append(os.path.abspath("/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/THDM_EWPOs/"))
import ewpo

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scenario", help = "Name of the scenario (e.g. IDM_FCCee240)", type=str)
parser.add_argument("-b", "--bp", help = "Which benchmark point to use", type=str)
parser.add_argument("--realistic", help = "Use realistic, asymmetric uncertainties for the on-shell kappa_lambda measurement at HL-LHC", action="store_true")
parser.add_argument("--ewpos_all", help = "Modify also the EWPO central values for current observables", action="store_true")
parser.add_argument("--with_Af", help = "Use BSM predictions for sin2theta_eff to evaluate A_f and A_FB_f asymmetries and use these in the fit inputs", action="store_true")
parser.add_argument("--EWPO_2L", help = "Use 2-loop IDM predictions for EWPO, instead of 1-loop ones", action="store_true")
parser.add_argument("--shifted_sin2thetaEff", help = "Shift the sin2thetaEff value using the HEPfit prediction for the SM", action="store_true")
parser.add_argument("--no_1L_BSM_sqrt_s", help = "Do not include momentum dependent BSM 1L corrections to Z->ZH", action="store_true")
parser.add_argument("--no_1L_BSM", help = "Do not include ANY BSM 1L corrections to Z->ZH", action="store_true")
parser.add_argument("--pure_1L_BSM", help = "Only includes strictly 1L BSM contributions, no SM-like diagrams with insertions of kappa_lambda", action="store_true")
parser.add_argument("--no_quad", help = "Do not include quadratic momentum dependent BSM 1L corrections to Z->ZH", action="store_true")
parser.add_argument("--smeft_formula", help = "Use the HEPfit SMEFT expression for the Zh cross-section, plus vertex corrections", action="store_true")
parser.add_argument("--smeft_formula_sqrt", help = "Use the HEPfit SMEFT expression for the Zh cross-section, with dkappaf**2 inside the square root", action="store_true")
parser.add_argument("--smeft_formula_no_cross", help = "Use the HEPfit SMEFT expression for the Zh cross-section, without cross terms", action="store_true")
parser.add_argument("--smeft_formula_external_leg", help = "Use the HEPfit SMEFT expression for the Zh cross-section, without vertex corrections", action="store_true")
parser.add_argument("--smeft_formula_all", help = "Use the HEPfit SMEFT expression for all XS and BR, including 2*dkappaf in the square root to stand in for C_Hbox (as \"_no_cross\")", action="store_true")
parser.add_argument("--WFR_kala2_input", help = "Include the WFR contribution, proportional to kappa_lambda**2, into the IDM ZH cross-section prediction", action="store_true")
parser.add_argument("--WFR_kala2_input_all", help = "Include the WFR contribution, proportional to kappa_lambda**2, into the IDM predictions for all the XS and BR", action="store_true")
parser.add_argument("--use_HEPfit_C1_values_WFR_kala2_input_all", help = "Use the HEPfit C1 values, instead of the IDM values. Activates WFR_kala2_input_all as well", action="store_true")
parser.add_argument("--use_HEPfit_C1_values_decayrates_WFR_kala2_input_all", help = "Use the HEPfit C1 values, also for the Higgs decay rates, instead of the Z2SSM values. Activates WFR_kala2_input_all as well", action="store_true")
parser.add_argument("--use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all", help = "Include higher-order contributions to the ZZh vertex, beyond the 1L BSM contribution", action="store_true")
parser.add_argument("--higgsconf", help = "Name of the ObsevablesHiggs configuration file", type=str, default=None)


args = parser.parse_args()
scenario                                            = args.scenario
BP                                                  = args.bp
realistic_HL_LHC_k_lambda_uncertainties             = args.realistic
modify_all_ewpos                                    = args.ewpos_all
with_Af                                             = args.with_Af
EWPO_2L                                             = args.EWPO_2L
shifted_sin2thetaEff                                = args.shifted_sin2thetaEff
no_1L_BSM_sqrt_s                                    = args.no_1L_BSM_sqrt_s
no_1L_BSM                                           = args.no_1L_BSM
pure_1L_BSM                                         = args.pure_1L_BSM
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
use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all  = args.use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all
higgsconf                                           = args.higgsconf

exclusive_flag_count = sum([
    no_1L_BSM_sqrt_s, 
    no_1L_BSM, 
    pure_1L_BSM,
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
    use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all,
])

# These flags are mutually exclusive, and can only be used one at a time
if exclusive_flag_count > 1:
    raise ValueError("""You can only use at most one of the following options:
        --ewpos_all,
        --no_1L_BSM_sqrt_s,
        --no_1L_BSM,
        --pure_1L_BSM,
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
        --use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all,
        """)

# Use of these flags is not currently possible without use of the realistic HL-LHC kappa_lambda uncertainties
elif exclusive_flag_count == 1 and not realistic_HL_LHC_k_lambda_uncertainties:
    raise ValueError("""The following options are only be currently used along with the --realistic option:
        --ewpos_all,
        --with_Af,
        --EWPO_2L,
        --shifted_sin2thetaEff,
        --no_1L_BSM_sqrt_s,
        --no_1L_BSM,
        --pure_1L_BSM,
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
        --use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all,
        """)



# file_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/Z2SSM_BenchmarkPoint_fits_HLLHC_ILC_250"
file_dir = f"{BP}/{scenario}/"


kappas={}

# Definition of IDM benchmark point:

# Main benchmark points, for which data is stored in yaml files
BP_Names = [f"BPB_{i}" for i in range(19)] + \
           [f"BPO_{i}" for i in range(2)] + \
           ["BP_lambda1"]

if BP in BP_Names:
    with open(f"./yaml_files_BPs/{BP}.yaml", 'r') as f:
        try:
            data_loaded = yaml.safe_load(f)
            for key in data_loaded['kappas']:
                kappas[key] = float(data_loaded['kappas'][key])

            EWPOs = data_loaded['EWPOs']
            Mw1L           = float(EWPOs['Mw1L'])
            sin2thetaEff1L = float(EWPOs['sin2thetaEff1L'])
            GammaZ1L       = float(EWPOs['GammaZ1L'])

            Mw2L           = float(EWPOs['Mw2L'])
            sin2thetaEff2L = float(EWPOs['sin2thetaEff2L'])
            GammaZ2L       = float(EWPOs['GammaZ2L'])

            model_pars = data_loaded['model_pars']
            mH = float(model_pars['mH'])
            mA = float(model_pars['mA'])
            mHp = float(model_pars['mHp'])
            lam1 = float(model_pars['lam1'])
            lam2 = float(model_pars['lam2'])
            lam3 = float(model_pars['lam3'])
            lam4 = float(model_pars['lam4'])
            lam5 = float(model_pars['lam5'])

        except yaml.YAMLError as exc:
            print(exc)

elif BP == "BP_0":
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


elif BP == "BP_new_0":
    kappas['uu'] = 0.9869872109932658
    kappas['dd'] = 0.9869872109932658
    kappas['ss'] = 0.9869872109932658
    kappas['cc'] = 0.9869872109932658
    kappas['bb'] = 0.9869872109932658
    kappas['tt'] = 0.9869872109932658
    kappas['ee'] = 0.9869872109932658
    kappas['mumu'] = 0.9869872109932658
    kappas['tautau'] = 0.9869872109932658
    kappas['ZZ_0'] = 0.9927730841276848
    kappas['ZZ_240'] = 0.9952371395622289
    kappas['ZZ_365'] = 0.9956317949997474
    kappas['ZZ_500'] = 0.999337958611399
    kappas['ZZ_550'] = 1.0006435883204592
    kappas['ZZ'] = 0.9896307057302142
    kappas['WW'] = 0.9896307057302142
    kappas['lam'] = 1.251996176990656
    kappas['gamgam'] = 0.9516431530275777
    kappas['Zgam'] = 0.9820251080944254
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.08286101234223403
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.0003946554375184874
    Mw = 80.37300109869199
    sin2thetaEff = 0.2314077810445216
    GammaZ = 2.495083123130063
    # Best scan point row: 6 out of 52

elif BP == "BP_new_1":
    kappas['uu'] = 0.9754368705981494
    kappas['dd'] = 0.9754368705981494
    kappas['ss'] = 0.9754368705981494
    kappas['cc'] = 0.9754368705981494
    kappas['bb'] = 0.9754368705981494
    kappas['tt'] = 0.9754368705981494
    kappas['ee'] = 0.9754368705981494
    kappas['mumu'] = 0.9754368705981494
    kappas['tautau'] = 0.9754368705981494
    kappas['ZZ_0'] = 0.98263626637054
    kappas['ZZ_240'] = 0.9855086896240941
    kappas['ZZ_365'] = 0.985313243531471
    kappas['ZZ_500'] = 0.9886415167590338
    kappas['ZZ_550'] = 0.9901721152161438
    kappas['ZZ'] = 0.9789103657001667
    kappas['WW'] = 0.9789103657001667
    kappas['lam'] = 1.336509415441691
    kappas['gamgam'] = 0.951843349855176
    kappas['Zgam'] = 0.9821089391490216
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.013487123493544072
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.0001954460926231194
    Mw = 80.37345634500961
    sin2thetaEff = 0.2314051330861581
    GammaZ = 2.495109828484497
    # Best scan point row: 40 out of 52

elif BP == "BP_new_2":
    kappas['uu'] = 0.9879068661201466
    kappas['dd'] = 0.9879068661201466
    kappas['ss'] = 0.9879068661201466
    kappas['cc'] = 0.9879068661201466
    kappas['bb'] = 0.9879068661201466
    kappas['tt'] = 0.9879068661201466
    kappas['ee'] = 0.9879068661201466
    kappas['mumu'] = 0.9879068661201466
    kappas['tautau'] = 0.9879068661201466
    kappas['ZZ_0'] = 1.0044841249903689
    kappas['ZZ_240'] = 1.013624931733064
    kappas['ZZ_365'] = 1.0061588405902715
    kappas['ZZ_500'] = 1.0054005676500877
    kappas['ZZ_550'] = 1.006066615721484
    kappas['ZZ'] = 0.9930708880201714
    kappas['WW'] = 0.9930708880201714
    kappas['lam'] = 2.55763062802754
    kappas['gamgam'] = 0.9505666520154421
    kappas['Zgam'] = 0.9816697920411275
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.5479727377036528
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.007466091142792397
    Mw = 80.37956135515566
    sin2thetaEff = 0.2313713438269027
    GammaZ = 2.495451770467056
    # Best scan point row: 52 out of 52

elif BP == "BP_new_3":
    kappas['uu'] = 0.9881747344745595
    kappas['dd'] = 0.9881747344745595
    kappas['ss'] = 0.9881747344745595
    kappas['cc'] = 0.9881747344745595
    kappas['bb'] = 0.9881747344745595
    kappas['tt'] = 0.9881747344745595
    kappas['ee'] = 0.9881747344745595
    kappas['mumu'] = 0.9881747344745595
    kappas['tautau'] = 0.9881747344745595
    kappas['ZZ_0'] = 1.0074114610219205
    kappas['ZZ_240'] = 1.0172598666184485
    kappas['ZZ_365'] = 1.0088851116279154
    kappas['ZZ_500'] = 1.0076338585646742
    kappas['ZZ_550'] = 1.008095595249646
    kappas['ZZ'] = 0.9956228983887574
    kappas['WW'] = 0.9956228983887574
    kappas['lam'] = 2.702656543464968
    kappas['gamgam'] = 0.9510241156863131
    kappas['Zgam'] = 0.981841354476324
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.48521551038995864
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.008374754990533084
    Mw = 80.37100942625534
    sin2thetaEff = 0.2314176589787162
    GammaZ = 2.4949832431401444
    # Best scan point row: 22 out of 51

elif BP == "BP_new_4":
    kappas['uu'] = 0.9814567142090073
    kappas['dd'] = 0.9814567142090073
    kappas['ss'] = 0.9814567142090073
    kappas['cc'] = 0.9814567142090073
    kappas['bb'] = 0.9814567142090073
    kappas['tt'] = 0.9814567142090073
    kappas['ee'] = 0.9814567142090073
    kappas['mumu'] = 0.9814567142090073
    kappas['tautau'] = 0.9814567142090073
    kappas['ZZ_0'] = 1.0131428507613656
    kappas['ZZ_240'] = 1.0340795808639291
    kappas['ZZ_365'] = 1.012907760808646
    kappas['ZZ_500'] = 1.0062211755787205
    kappas['ZZ_550'] = 1.0051789628938332
    kappas['ZZ'] = 0.9894014416689983
    kappas['WW'] = 0.9894014416689983
    kappas['lam'] = 4.874507355735764
    kappas['gamgam'] = 0.9502971694743096
    kappas['Zgam'] = 0.9815832221698187
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.62124649184556
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.021171820055283064
    Mw = 80.38274913236829
    sin2thetaEff = 0.2313539033748779
    GammaZ = 2.495631185446592
    # Best scan point row: 9 out of 51

elif BP == "BP_new_5":
    kappas['uu'] = 0.9948392829018028
    kappas['dd'] = 0.9948392829018028
    kappas['ss'] = 0.9948392829018028
    kappas['cc'] = 0.9948392829018028
    kappas['bb'] = 0.9948392829018028
    kappas['tt'] = 0.9948392829018028
    kappas['ee'] = 0.9948392829018028
    kappas['mumu'] = 0.9948392829018028
    kappas['tautau'] = 0.9948392829018028
    kappas['ZZ_0'] = 1.0051386882808055
    kappas['ZZ_240'] = 1.008298413604481
    kappas['ZZ_365'] = 1.0075069616615753
    kappas['ZZ_500'] = 1.010013675655837
    kappas['ZZ_550'] = 1.0116839881599824
    kappas['ZZ'] = 1.0013445805817487
    kappas['WW'] = 1.0013445805817487
    kappas['lam'] = 1.40834708223538
    kappas['gamgam'] = 0.9530234064245932
    kappas['Zgam'] = 0.9825544621615534
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.09537388477219058
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.000791451942905752
    Mw = 80.35960929534941
    sin2thetaEff = 0.2314801469992004
    GammaZ = 2.4943570296591533
    # Best scan point row: 31 out of 51

elif BP == "BP_new_6":
    kappas['uu'] = 0.9834419885721146
    kappas['dd'] = 0.9834419885721146
    kappas['ss'] = 0.9834419885721146
    kappas['cc'] = 0.9834419885721146
    kappas['bb'] = 0.9834419885721146
    kappas['tt'] = 0.9834419885721146
    kappas['ee'] = 0.9834419885721146
    kappas['mumu'] = 0.9834419885721146
    kappas['tautau'] = 0.9834419885721146
    kappas['ZZ_0'] = 1.017625243299268
    kappas['ZZ_240'] = 1.0383293329401886
    kappas['ZZ_365'] = 1.017328563064984
    kappas['ZZ_500'] = 1.0106365761100995
    kappas['ZZ_550'] = 1.0095652870157676
    kappas['ZZ'] = 0.9948095676884501
    kappas['WW'] = 0.9948095676884501
    kappas['lam'] = 4.836238671915516
    kappas['gamgam'] = 0.9508797089917917
    kappas['Zgam'] = 0.9817993759028473
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.5479033488001338
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.021000769875204606
    Mw = 80.37965470044583
    sin2thetaEff = 0.2313706760453281
    GammaZ = 2.495461121722893
    # Best scan point row: 43 out of 69

elif BP == "BP_new_7":
    kappas['uu'] = 0.979082493652984
    kappas['dd'] = 0.979082493652984
    kappas['ss'] = 0.979082493652984
    kappas['cc'] = 0.979082493652984
    kappas['bb'] = 0.979082493652984
    kappas['tt'] = 0.979082493652984
    kappas['ee'] = 0.979082493652984
    kappas['mumu'] = 0.979082493652984
    kappas['tautau'] = 0.979082493652984
    kappas['ZZ_0'] = 1.0213383561776428
    kappas['ZZ_240'] = 1.050299422231679
    kappas['ZZ_365'] = 1.019780486878427
    kappas['ZZ_500'] = 1.009128991056699
    kappas['ZZ_550'] = 1.0070348168241405
    kappas['ZZ'] = 0.9901254303627953
    kappas['WW'] = 0.9901254303627953
    kappas['lam'] = 6.453926326795824
    kappas['gamgam'] = 0.9504313971645049
    kappas['Zgam'] = 0.9816368373063304
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.6067452467482002
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.030518935353252008
    Mw = 80.38292732438012
    sin2thetaEff = 0.2313528864621709
    GammaZ = 2.495642324521779
    # Best scan point row: 45 out of 69

elif BP == "BP_new_8":
    kappas['uu'] = 0.975174002704635
    kappas['dd'] = 0.975174002704635
    kappas['ss'] = 0.975174002704635
    kappas['cc'] = 0.975174002704635
    kappas['bb'] = 0.975174002704635
    kappas['tt'] = 0.975174002704635
    kappas['ee'] = 0.975174002704635
    kappas['mumu'] = 0.975174002704635
    kappas['tautau'] = 0.975174002704635
    kappas['ZZ_0'] = 1.0244912605528027
    kappas['ZZ_240'] = 1.0610103816981897
    kappas['ZZ_365'] = 1.02178158014904
    kappas['ZZ_500'] = 1.0075205445278583
    kappas['ZZ_550'] = 1.0045036391944444
    kappas['ZZ'] = 0.9857145478973057
    kappas['WW'] = 0.9857145478973057
    kappas['lam'] = 7.934713697992164
    kappas['gamgam'] = 0.9500567164562701
    kappas['Zgam'] = 0.98150006781032
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.6429856764904281
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.03922880154914976
    Mw = 80.36434030781206
    sin2thetaEff = 0.2314532507692058
    GammaZ = 2.494618642957178
    # Best scan point row: 15 out of 69

elif BP == "BP_new_9":
    kappas['uu'] = 0.9900882501802496
    kappas['dd'] = 0.9900882501802496
    kappas['ss'] = 0.9900882501802496
    kappas['cc'] = 0.9900882501802496
    kappas['bb'] = 0.9900882501802496
    kappas['tt'] = 0.9900882501802496
    kappas['ee'] = 0.9900882501802496
    kappas['mumu'] = 0.9900882501802496
    kappas['tautau'] = 0.9900882501802496
    kappas['ZZ_0'] = 1.0091530851058754
    kappas['ZZ_240'] = 1.0177092996110788
    kappas['ZZ_365'] = 1.0107357645626283
    kappas['ZZ_500'] = 1.0100165617149708
    kappas['ZZ_550'] = 1.0106109047258678
    kappas['ZZ'] = 0.9991019636209117
    kappas['WW'] = 0.9991019636209117
    kappas['lam'] = 2.456447833753604
    kappas['gamgam'] = 0.9516675062121578
    kappas['Zgam'] = 0.9820778769653792
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.3937781392601184
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.006973535048450552
    Mw = 80.3668996543769
    sin2thetaEff = 0.2314399457534867
    GammaZ = 2.494757487723553
    # Best scan point row: 17 out of 69

elif BP == "BP_new_10":
    kappas['uu'] = 0.9825493013667561
    kappas['dd'] = 0.9825493013667561
    kappas['ss'] = 0.9825493013667561
    kappas['cc'] = 0.9825493013667561
    kappas['bb'] = 0.9825493013667561
    kappas['tt'] = 0.9825493013667561
    kappas['ee'] = 0.9825493013667561
    kappas['mumu'] = 0.9825493013667561
    kappas['tautau'] = 0.9825493013667561
    kappas['ZZ_0'] = 1.0120952032126092
    kappas['ZZ_240'] = 1.0307365191082503
    kappas['ZZ_365'] = 1.0122270497488346
    kappas['ZZ_500'] = 1.0066643155374064
    kappas['ZZ_550'] = 1.0059201246191558
    kappas['ZZ'] = 0.9909743590442306
    kappas['WW'] = 0.9909743590442306
    kappas['lam'] = 4.423626318095999
    kappas['gamgam'] = 0.9503584022996147
    kappas['Zgam'] = 0.9816042695935586
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.6021979682939236
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.018509469359415665
    Mw = 80.36276077114606
    sin2thetaEff = 0.2314619655614417
    GammaZ = 2.494531061576091
    # Best scan point row: 50 out of 69

else:
    raise ValueError("Could not determine benchmark point!")


ewpo.working_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/THDM_EWPOs"

large_mass = 100_000
sl_SM_value_1L = ewpo.sl1L_vec(large_mass, large_mass, large_mass, 0.0, test=True)
sl_SM_value_2L = ewpo.sl2L_vec(large_mass, large_mass, large_mass, 0.0, test=True)  # 1L and 2L values seem to be very close.

sl_value_HEPfit = 0.2314833512991618

def sin2thetaEff1L_shift_calc(loop_order = 1,):
    if loop_order == 1:
        delta_sin2thetaEff_BSM = ewpo.sl1L_vec(mH, mA, mHp, lam3+lam4+lam5, test=True) - sl_SM_value_2L
    elif loop_order == 2:
        delta_sin2thetaEff_BSM = ewpo.sl1L_vec(mH, mA, mHp, lam3+lam4+lam5, test=True) - sl_SM_value_2L

    sin2thetaEff_shifted = sl_value_HEPfit + delta_sin2thetaEff_BSM

    return sin2thetaEff_shifted

if shifted_sin2thetaEff:
    sin2thetaEff1L = sin2thetaEff1L_shift_calc(loop_order=1)
    sin2thetaEff2L = sin2thetaEff1L_shift_calc(loop_order=2)

if EWPO_2L:
    Mw = Mw2L
    sin2thetaEff = sin2thetaEff2L
    GammaZ = GammaZ2L
else:
    Mw = Mw1L
    sin2thetaEff = sin2thetaEff1L
    GammaZ = GammaZ1L


def A_f(f, sin2thetaEff):
    if f in ['u', 'c', 't']:
        T3 = 0.5
        Q = 2.0/3.0
    elif f in ['d', 's', 'b']:
        T3 = -0.5
        Q = -1.0/3.0
    elif f in ['e', 'mu', 'tau']:
        T3 = -0.5
        Q = -1.0
    else:
        raise ValueError("Invalid fermion type for A_f calculation")

    gV = T3 - 2*Q*sin2thetaEff
    gA = T3

    return 2*gV*gA/(gV**2 + gA**2)

def sin2thetaEff_from_Af(f, Af):
    if f in ['u', 'c', 't']:
        Q = 2.0/3.0
    elif f in ['d', 's', 'b']:
        Q = -1.0/3.0
    elif f in ['e', 'mu', 'tau']:
        Q = -1.0
    else:
        raise ValueError("Invalid fermion type for A_f calculation")

    return ( np.sqrt(1 - Af**2) - (1 - Af)) / (4*np.abs(Q)*Af)

# def A_f_test(f, sin2thetaEff):
#     if f in ['u', 'c', 't']:
#         Q = 2.0/3.0
#         A_f_SM = 0.6679249978345343  # from HEPfit

#     elif f in ['d', 's', 'b']:
#         Q = -1.0/3.0
#         A_f_SM = 0.9347523361749206  # from HEPfit

#     elif f in ['e', 'mu', 'tau']:
#         Q = -1.0
#         A_f_SM = 0.1473249852597804  # from HEPfit
#     else:
#         raise ValueError("Invalid fermion type for A_f calculation")

#     sin2thetaEff_SM = sin2thetaEff_from_Af(f, A_f_SM)
#     delta_sin2thetaEff = sin2thetaEff - sin2thetaEff_SM

#     gV_over_gA_SM = (1 - 4*np.abs(Q)*sin2thetaEff_SM)

#     delta_A_f = (2*(1 - gV_over_gA_SM**2)/(1 + gV_over_gA_SM**2)**2) * (-4*np.abs(Q)*delta_sin2thetaEff)

#     A_f_value = A_f_SM + delta_A_f

#     return A_f_value

# def A_FB_f_test(f, sin2thetaEff):
#     A_f_value = A_f_test(f, sin2thetaEff)
#     A_e_value = A_f_test('e', sin2thetaEff)
#     A_FB_value = 3/4 * A_e_value * A_f_value 
#     return A_FB_value

def A_FB_f(f, sin2thetaEff):
    A_f_value = A_f(f, sin2thetaEff)
    A_e_value = A_f('e', sin2thetaEff)
    A_FB_value = 3/4 * A_e_value * A_f_value 
    return A_FB_value




if no_1L_BSM_sqrt_s:
    kappas['ZZ_0'] = kappas['ZZ_0_no_1L_BSM_sqrt_s']
    kappas['ZZ_240'] = kappas['ZZ_240_no_1L_BSM_sqrt_s']
    # kappas['ZZ_125'] = kappas['ZZ_125_no_1L_BSM_sqrt_s']
    kappas['ZZ_365'] = kappas['ZZ_365_no_1L_BSM_sqrt_s']
    kappas['ZZ_500'] = kappas['ZZ_500_no_1L_BSM_sqrt_s']
    kappas['ZZ_550'] = kappas['ZZ_550_no_1L_BSM_sqrt_s']

if no_1L_BSM:
    kappas['ZZ_0'] = kappas['ZZ_0_no_1L_BSM']
    kappas['ZZ_240'] = kappas['ZZ_240_no_1L_BSM']
    # kappas['ZZ_125'] = kappas['ZZ_125_no_1L_BSM']
    kappas['ZZ_365'] = kappas['ZZ_365_no_1L_BSM']
    kappas['ZZ_500'] = kappas['ZZ_500_no_1L_BSM']
    kappas['ZZ_550'] = kappas['ZZ_550_no_1L_BSM']

if pure_1L_BSM:
    kappas['ZZ_0'] = kappas['ZZ_0_pure_1L_BSM']
    kappas['ZZ_240'] = kappas['ZZ_240_pure_1L_BSM']
    # kappas['ZZ_125'] = kappas['ZZ_125_pure_1L_BSM']
    kappas['ZZ_365'] = kappas['ZZ_365_pure_1L_BSM']
    kappas['ZZ_500'] = kappas['ZZ_500_pure_1L_BSM']
    kappas['ZZ_550'] = kappas['ZZ_550_pure_1L_BSM']

if use_HEPfit_C1_values_WFR_kala2_input_all or \
    use_HEPfit_C1_values_decayrates_WFR_kala2_input_all:
    kappas['ZZ_240'] = kappas['ZZ_240_use_HEPfit_C1_values']
    kappas['ZZ_365'] = kappas['ZZ_365_use_HEPfit_C1_values']
    kappas['ZZ_500'] = kappas['ZZ_500_use_HEPfit_C1_values']

if use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all:
    kappas['ZZ_240'] = kappas['ZZ_240_use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all']
    kappas['ZZ_365'] = kappas['ZZ_365_use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all']
    kappas['ZZ_500'] = kappas['ZZ_500_use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all']

if use_HEPfit_C1_values_decayrates_WFR_kala2_input_all or \
    use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all:
    kappas['ZZ']   = kappas['ZZ_HEPfit_C1']
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


# HEPfit expressions:

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

### Still to be checked
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

    if use_HEPfit_C1_values_decayrates_WFR_kala2_input_all or \
        use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all:
        kappas["ggH_HLLHC"] = kappas["ggH_HLLHC_HEPfit_C1"]
        kappas["VBF_HLLHC"] = kappas["VBF_HLLHC_HEPfit_C1"]
        kappas["ZH_HLLHC"]  = kappas["ZH_HLLHC_HEPfit_C1"]
        kappas["WH_HLLHC"]  = kappas["WH_HLLHC_HEPfit_C1"]
        kappas["ttH_HLLHC"] = kappas["ttH_HLLHC_HEPfit_C1"]
    else:
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

if WFR_kala2_input_all or \
    use_HEPfit_C1_values_WFR_kala2_input_all or \
    use_HEPfit_C1_values_decayrates_WFR_kala2_input_all or \
    use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all:
    ###########################################################################################
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
               kappas2["ZZ"]*BR_H_to_ZZ         + \
               kappas2["Zgam"]*BR_H_to_Zga      + \
               kappas2["gamgam"]*BR_H_to_gaga   + \
               kappas2["mumu"]*BR_H_to_mumu     + \
               kappas2["tautau"]*BR_H_to_tautau + \
               kappas2["cc"]*BR_H_to_cc         + \
               kappas2["bb"]*BR_H_to_bb         + \
               kappas2["ss"]*BR_H_to_ss         ## Check this!

kappas2["H"] = kappas2["H"]/(1.0 - BrHinv - BrHexo)
print(f"kappa_H^2 = {kappas2['H']}")



final_text = "#\n" + \
             "#\n" + \
             "# IDM Benchmark Point:\n"


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
    no_1L_BSM_sqrt_s: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_1L_BSM_sqrt_s.conf",
    no_1L_BSM: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_1L_BSM.conf",
    pure_1L_BSM: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_pure_1L_BSM.conf",
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
    use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all.conf",
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

if (scenario == "IDM_FCCee240_FCCee365" 
    or scenario == "IDM_FCCee240_FCCee365_HLLHClambda"):
    # Open the FCCee_365 input file in read mode and output file in write mode
    input_file_FCCee365 =  file_dir + "ObservablesHiggs_FCCee_365.conf"
    output_file_FCCee365 = file_dir + "ObservablesHiggs_FCCee_365_kappa_scaled.conf"

    output_file_flag_map = {
        no_1L_BSM_sqrt_s: "ObservablesHiggs_FCCee_365_kappa_scaled_no_1L_BSM_sqrt_s.conf",
        no_1L_BSM: "ObservablesHiggs_FCCee_365_kappa_scaled_no_1L_BSM.conf",
        pure_1L_BSM: "ObservablesHiggs_FCCee_365_kappa_scaled_pure_1L_BSM.conf",
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
        use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all: "ObservablesHiggs_FCCee_365_kappa_scaled_use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all.conf",
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
    no_1L_BSM_sqrt_s: "ObservablesHiggs_HLLHC_SM_kappa_scaled_no_1L_BSM_sqrt_s.conf",
    no_1L_BSM: "ObservablesHiggs_HLLHC_SM_kappa_scaled_no_1L_BSM.conf",
    pure_1L_BSM: "ObservablesHiggs_HLLHC_SM_kappa_scaled_pure_1L_BSM.conf",
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
    use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all: "ObservablesHiggs_HLLHC_SM_kappa_scaled_use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all.conf",
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
if scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
    if higgsconf is None:
        if not realistic_HL_LHC_k_lambda_uncertainties:
            input_file = file_dir + "ObservablesHiggs"
        else:
            input_file = file_dir + "ObservablesHiggs_scaled_realistic_HL_LHC"

        flag_map = {
            no_1L_BSM_sqrt_s: "_no_1L_BSM_sqrt_s",
            no_1L_BSM: "_no_1L_BSM",
            pure_1L_BSM: "_pure_1L_BSM",
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
            use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all: "_use_HEPfit_C1_values_decayrates_higher_order_ZZh_WFR_kala2_input_all",
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




###########################################################################################
###########################################################################################
#######################################   EWPOs   #########################################
###########################################################################################
###########################################################################################

input_files =  [
            #    file_dir + "ObservablesEW_HLLHC",
            #    file_dir + "ObservablesEW_FCCee_WW_SM",
               file_dir + "ObservablesEW_FCCee_Zpole_SM",
               ]

output_files = [
            #    file_dir + "ObservablesEW_HLLHC_kappa_scaled",
            #    file_dir + "ObservablesEW_FCCee_WW_SM_kappa_scaled",
               file_dir + "ObservablesEW_FCCee_Zpole_SM_kappa_scaled",
              ]

if modify_all_ewpos:
    input_files.append(file_dir + "ObservablesEW_Current_SM_noLFU")
    output_files.append(file_dir + "ObservablesEW_Current_SM_noLFU_kappa_scaled")

if with_Af:
    output_files = [output_file + "_with_Af" for output_file in output_files]
if shifted_sin2thetaEff:
    output_files = [output_file + "_shifted_sin2thetaEff" for output_file in output_files]

input_files.append(file_dir + "ObservablesEW_HLLHC")
input_files.append(file_dir + "ObservablesEW_FCCee_WW_SM",)
output_files.append(file_dir + "ObservablesEW_HLLHC_kappa_scaled")
output_files.append(file_dir + "ObservablesEW_FCCee_WW_SM_kappa_scaled")


if EWPO_2L:
    output_files = [output_file + "_EWPO_2L" for output_file in output_files]

for input_file, output_file in zip(input_files, output_files):
    input_file = input_file  + ".conf"
    output_file = output_file + ".conf"
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
                if (columns[2].startswith("GammaZ")):
                    columns[8] = str(GammaZ)

                elif (columns[2].startswith("Mw")):
                    columns[8] = str(Mw)

                if with_Af:
                    if (columns[2].startswith("Aelectron")):
                        columns[8] = str(A_f('e', sin2thetaEff))
                    elif (columns[2].startswith("Amuon")):
                        columns[8] = str(A_f('mu', sin2thetaEff))
                    elif (columns[2].startswith("Atau")):
                        columns[8] = str(A_f('tau', sin2thetaEff))
                    elif (columns[2].startswith("Abottom")):
                        columns[8] = str(A_f('b', sin2thetaEff))
                    elif (columns[2].startswith("Acharm")):
                        columns[8] = str(A_f('c', sin2thetaEff))
                    elif (columns[2].startswith("As")):
                        columns[8] = str(A_f('s', sin2thetaEff))

                    elif (columns[2].startswith("AFBelectron")):
                        columns[8] = str(A_FB_f('e', sin2thetaEff))
                    elif (columns[2].startswith("AFBmuon")):
                        columns[8] = str(A_FB_f('mu', sin2thetaEff))
                    elif (columns[2].startswith("AFBtau")):
                        columns[8] = str(A_FB_f('tau', sin2thetaEff))
                    elif (columns[2].startswith("AFBbottom")):
                        columns[8] = str(A_FB_f('b', sin2thetaEff))
                    elif (columns[2].startswith("AFBcharm")):
                        columns[8] = str(A_FB_f('c', sin2thetaEff))

                # Rejoin the columns and write to the output file
                outfile.write(" ".join(columns) + "\n")
            else:
                # Write unmodified lines to the output file
                outfile.write(line)

    with open(output_file, 'a') as outfile:
        outfile.write(final_text)

    print(f"Modified content saved to {output_file}.")
