# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

import subprocess
import argparse
import numpy as np

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scenario", help = "Name of the scenario (e.g. IDM_FCCee240)", type=str)
parser.add_argument("-b", "--bp", help = "Which benchmark point to use", type=str)
# parser.add_argument("--noHLLHClambda", help = "No on-shell kappa_lambda constraint", action="store_true")
# parser.add_argument("--fast", help = "Run faster, using less points and a looser criterium for convergence", action="store_true")
parser.add_argument("--realistic", help = "Use realistic, asymmetric uncertainties for the on-shell kappa_lambda measurement at HL-LHC", action="store_true")
parser.add_argument("--ewpos_all", help = "Modify also the EWPO central values for current observables", action="store_true")
parser.add_argument("--no_1L_BSM_sqrt_s", help = "Do not include momentum dependent BSM 1L corrections to Z->ZH", action="store_true")
parser.add_argument("--no_1L_BSM", help = "Do not include ANY BSM 1L corrections to Z->ZH", action="store_true")
parser.add_argument("--no_quad", help = "Do not include quadratic momentum dependent BSM 1L corrections to Z->ZH", action="store_true")
parser.add_argument("--smeft_formula", help = "Use the HEPfit SMEFT expression for the Zh cross-section, plus vertex corrections", action="store_true")
parser.add_argument("--smeft_formula_sqrt", help = "Use the HEPfit SMEFT expression for the Zh cross-section, with dkappaf**2 inside the square root", action="store_true")
parser.add_argument("--smeft_formula_no_cross", help = "Use the HEPfit SMEFT expression for the Zh cross-section, without cross terms", action="store_true")
parser.add_argument("--smeft_formula_external_leg", help = "Use the HEPfit SMEFT expression for the Zh cross-section, without vertex corrections", action="store_true")
parser.add_argument("--WFR_kala2_input", help = "Include the WFR contribution, proportional to kappa_lambda**2, into the IDM ZH cross-section prediction", action="store_true")


args = parser.parse_args()
scenario = args.scenario
BP = args.bp
# noHLLHClambda = args.noHLLHClambda
# fast = args.fast
realistic_HL_LHC_k_lambda_uncertainties = args.realistic
modify_all_ewpos = args.ewpos_all
no_1L_BSM_sqrt_s = args.no_1L_BSM_sqrt_s
no_1L_BSM = args.no_1L_BSM
no_quad = args.no_quad
smeft_formula = args.smeft_formula
smeft_formula_sqrt = args.smeft_formula_sqrt
smeft_formula_no_cross = args.smeft_formula_no_cross
smeft_formula_external_leg = args.smeft_formula_external_leg
WFR_kala2_input = args.WFR_kala2_input

if sum([no_1L_BSM_sqrt_s, no_1L_BSM, smeft_formula, smeft_formula_sqrt, smeft_formula_no_cross, smeft_formula_external_leg, WFR_kala2_input]) > 1:
    raise ValueError("You can only use one of the following options: --no_1L_BSM_sqrt_s, --no_1L_BSM, --smeft_formula, --smeft_formula_sqrt, --smeft_formula_no_cross, --smeft_formula_external_leg, --WFR_kala2_input")


# file_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/Z2SSM_BenchmarkPoint_fits_HLLHC_ILC_250"
file_dir = f"{BP}/{scenario}/"


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

elif BP == "BPO_0":
    kappas['uu'] = 0.9818547810617284
    kappas['dd'] = 0.9818547810617284
    kappas['ss'] = 0.9818547810617284
    kappas['cc'] = 0.9818547810617284
    kappas['bb'] = 0.9818547810617284
    kappas['tt'] = 0.9818547810617284
    kappas['ee'] = 0.9818547810617284
    kappas['mumu'] = 0.9818547810617284
    kappas['tautau'] = 0.9818547810617284
    kappas['ZZ_0'] = 1.007141704579298
    kappas['ZZ_240'] = 1.0237693288776533
    kappas['ZZ_365'] = 1.0074536101415776
    kappas['ZZ_500'] = 1.0026988104523176
    kappas['ZZ_550'] = 1.0021232678597285
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0023378651272847
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0177981665211153
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 0.9998722462932628
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9924197633264032
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9905262353724729
    kappas['ZZ_0_no_1L_BSM'] = 1.0123986410355819
    kappas['ZZ_240_no_1L_BSM'] = 1.0278589424294124
    kappas['ZZ_365_no_1L_BSM'] = 1.00993302220156
    kappas['ZZ_500_no_1L_BSM'] = 1.0024805392347005
    kappas['ZZ_550_no_1L_BSM'] = 1.00058701128077
    kappas['ZZ'] = 0.9899392240917029
    kappas['WW'] = 0.9899392240917029
    kappas['lam'] = 4.038636858901748
    kappas['gamgam'] = 0.9514322699531608
    kappas['Zgam'] = 0.9820015140523058
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.6864189906268178
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.016315718736075624
    Mw = 80.35863800163634
    sin2thetaEff = 0.2314855517673455
    GammaZ = 2.49430915768778
    # mu2sq = 22291.2734925729
    # lam1 = 0.2581482588231646
    # lam2 = 0.6860388143201386
    # lam3 = 11.78967577439182
    # lam4 = -6.064347273101494
    # lam5 = -6.132550857269012
    # mH = 99.73728395068352
    # mA = 617.8414041157196
    # mHp = 616.166056870238
    # Best scan point row: 4992 out of 14054

elif BP == "BPO_1":
    kappas['uu'] = 0.9948800104857921
    kappas['dd'] = 0.9948800104857921
    kappas['ss'] = 0.9948800104857921
    kappas['cc'] = 0.9948800104857921
    kappas['bb'] = 0.9948800104857921
    kappas['tt'] = 0.9948800104857921
    kappas['ee'] = 0.9948800104857921
    kappas['mumu'] = 0.9948800104857921
    kappas['tautau'] = 0.9948800104857921
    kappas['ZZ_0'] = 1.0012233525483671
    kappas['ZZ_240'] = 1.0036078092756757
    kappas['ZZ_365'] = 1.0040569863550053
    kappas['ZZ_500'] = 1.0077635634642326
    kappas['ZZ_550'] = 1.009112592294324
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 0.9993516901502957
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0005654828751926
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 0.9991581137039593
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9985730171151438
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9984243556889322
    kappas['ZZ_0_no_1L_BSM'] = 1.000973420886452
    kappas['ZZ_240_no_1L_BSM'] = 1.002187213611349
    kappas['ZZ_365_no_1L_BSM'] = 1.0007798444401157
    kappas['ZZ_500_no_1L_BSM'] = 1.0001947478513
    kappas['ZZ_550_no_1L_BSM'] = 1.0000460864250884
    kappas['ZZ'] = 0.9983782692638437
    kappas['WW'] = 0.9983782692638437
    kappas['lam'] = 1.2385642568656816
    kappas['gamgam'] = 0.9519204100128348
    kappas['Zgam'] = 0.982125765438694
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.12450133724029452
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.00044917707932956574
    Mw = 80.35797476859611
    sin2thetaEff = 0.2314895715713228
    GammaZ = 2.4942679684662425
    # mu2sq = 9607.427332165063
    # lam1 = 0.2581482588231646
    # lam2 = 11.99035402191523
    # lam3 = 3.6853191712398297
    # lam4 = -1.8990667792323688
    # lam5 = -1.97462331598214
    # mH = 62.43009654635279
    # mA = 351.5783127700959
    # mHp = 348.3059515487595
    # Best scan point row: 1473 out of 14054

elif BP == "BPB_0":
    kappas['uu'] = 0.997497286095468
    kappas['dd'] = 0.997497286095468
    kappas['ss'] = 0.997497286095468
    kappas['cc'] = 0.997497286095468
    kappas['bb'] = 0.997497286095468
    kappas['tt'] = 0.997497286095468
    kappas['ee'] = 0.997497286095468
    kappas['mumu'] = 0.997497286095468
    kappas['tautau'] = 0.997497286095468
    kappas['ZZ_0'] = 0.99803003617002
    kappas['ZZ_240'] = 0.9989225157021105
    kappas['ZZ_365'] = 0.9985818760113092
    kappas['ZZ_500'] = 0.9988812072771296
    kappas['ZZ_550'] = 0.9990824850147142
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 0.9970430932347498
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 0.9976582557060288
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 0.996944986727216
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.996648453838091
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.996573110718581
    kappas['ZZ_0_no_1L_BSM'] = 1.0004933395841165
    kappas['ZZ_240_no_1L_BSM'] = 1.0011085020553956
    kappas['ZZ_365_no_1L_BSM'] = 1.0003952330765826
    kappas['ZZ_500_no_1L_BSM'] = 1.0000987001874577
    kappas['ZZ_550_no_1L_BSM'] = 1.0000233570679478
    kappas['ZZ'] = 0.9965497536506333
    kappas['WW'] = 0.9965497536506333
    kappas['lam'] = 1.1209067864736006
    kappas['gamgam'] = 0.9821975068074829
    kappas['Zgam'] = 0.9934043522024448
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.31614353125012806
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.0003406396908013365
    Mw = 80.3914079929351
    sin2thetaEff = 0.2313357603551311
    GammaZ = 2.4962175514601705
    # mu2sq = 301008.8896184936
    # lam1 = 0.2581482588231646
    # lam2 = 0.9785764198605832
    # lam3 = 5.238851526522496
    # lam4 = -3.194931717495754
    # lam5 = -1.8282913886008845
    # mH = 554.5674267479683
    # mA = 646.8257726146429
    # mHp = 678.0923691243299
    # Best scan point row: 5534 out of 14054

elif BP == "BPB_1":
    kappas['uu'] = 0.9969473191210583
    kappas['dd'] = 0.9969473191210583
    kappas['ss'] = 0.9969473191210583
    kappas['cc'] = 0.9969473191210583
    kappas['bb'] = 0.9969473191210583
    kappas['tt'] = 0.9969473191210583
    kappas['ee'] = 0.9969473191210583
    kappas['mumu'] = 0.9969473191210583
    kappas['tautau'] = 0.9969473191210583
    kappas['ZZ_0'] = 0.9989621944276256
    kappas['ZZ_240'] = 1.000023618370414
    kappas['ZZ_365'] = 1.0000413187916326
    kappas['ZZ_500'] = 1.0008988220698813
    kappas['ZZ_550'] = 1.0013781536705735
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 0.9983584296416149
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 0.9989280007074098
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 0.9982675940808219
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.997993038070682
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9979232788397744
    kappas['ZZ_0_no_1L_BSM'] = 1.0004567768123758
    kappas['ZZ_240_no_1L_BSM'] = 1.0010263478781707
    kappas['ZZ_365_no_1L_BSM'] = 1.0003659412515828
    kappas['ZZ_500_no_1L_BSM'] = 1.0000913852414428
    kappas['ZZ_550_no_1L_BSM'] = 1.0000216260105352
    kappas['ZZ'] = 0.9979016528292391
    kappas['WW'] = 0.9979016528292391
    kappas['lam'] = 1.1119460475058272
    kappas['gamgam'] = 0.9745673696771745
    kappas['Zgam'] = 0.9905664142164403
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.749434482912224
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 1.7700421218513895e-05
    Mw = 80.35622948679458
    sin2thetaEff = 0.2315231828248444
    GammaZ = 2.4942665435951
    # mu2sq = 119346.66020899298
    # lam1 = 0.2581482588231646
    # lam2 = 12.555533152461472
    # lam3 = 3.801335777873435
    # lam4 = -1.7697582333643918
    # lam5 = -1.906816826496088
    # mH = 350.8965863789508
    # mA = 488.5974814718127
    # mHp = 484.3273385563024
    # Best scan point row: 7982 out of 14054

elif BP == "BPB_2":
    kappas['uu'] = 0.991329519562304
    kappas['dd'] = 0.991329519562304
    kappas['ss'] = 0.991329519562304
    kappas['cc'] = 0.991329519562304
    kappas['bb'] = 0.991329519562304
    kappas['tt'] = 0.991329519562304
    kappas['ee'] = 0.991329519562304
    kappas['mumu'] = 0.991329519562304
    kappas['tautau'] = 0.991329519562304
    kappas['ZZ_0'] = 1.000248738282997
    kappas['ZZ_240'] = 1.0077713199799205
    kappas['ZZ_365'] = 1.0002131692051668
    kappas['ZZ_500'] = 0.997795877018984
    kappas['ZZ_550'] = 0.9973832902199067
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 0.9977031653428668
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0047587501412416
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 0.9965779361302687
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9931768623612863
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9923127170444053
    kappas['ZZ_0_no_1L_BSM'] = 1.0056583413856384
    kappas['ZZ_240_no_1L_BSM'] = 1.0127139261840128
    kappas['ZZ_365_no_1L_BSM'] = 1.00453311217304
    kappas['ZZ_500_no_1L_BSM'] = 1.0011320384040576
    kappas['ZZ_550_no_1L_BSM'] = 1.0002678930871767
    kappas['ZZ'] = 0.9920448239572286
    kappas['WW'] = 0.9920448239572286
    kappas['lam'] = 2.3867362274064843
    kappas['gamgam'] = 0.974955131015653
    kappas['Zgam'] = 0.9907251332792432
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.972569755753518
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.007558150774753747
    Mw = 80.37905036636042
    sin2thetaEff = 0.2314001454658894
    GammaZ = 2.495528985557726
    # mu2sq = 366592.3210321892
    # lam1 = 0.2581482588231646
    # lam2 = 3.083565601023352
    # lam3 = 11.464952016747336
    # lam4 = -5.679908746895023
    # lam5 = -5.109268798298526
    # mH = 622.1546721068894
    # mA = 834.7582527674188
    # mHp = 845.0553897795384
    # Best scan point row: 12535 out of 14054

elif BP == "BPB_3":
    kappas['uu'] = 0.9927495335076485
    kappas['dd'] = 0.9927495335076485
    kappas['ss'] = 0.9927495335076485
    kappas['cc'] = 0.9927495335076485
    kappas['bb'] = 0.9927495335076485
    kappas['tt'] = 0.9927495335076485
    kappas['ee'] = 0.9927495335076485
    kappas['mumu'] = 0.9927495335076485
    kappas['tautau'] = 0.9927495335076485
    kappas['ZZ_0'] = 1.0025946133580672
    kappas['ZZ_240'] = 1.009502841661128
    kappas['ZZ_365'] = 1.0022646595923244
    kappas['ZZ_500'] = 0.9997291599866133
    kappas['ZZ_550'] = 0.999214728766395
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0017506560443745
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0083483360548362
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.000698453782578
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9975181084163243
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9967100458040468
    kappas['ZZ_0_no_1L_BSM'] = 1.005291117167353
    kappas['ZZ_240_no_1L_BSM'] = 1.0118887971778148
    kappas['ZZ_365_no_1L_BSM'] = 1.0042389149055564
    kappas['ZZ_500_no_1L_BSM'] = 1.0010585695393026
    kappas['ZZ_550_no_1L_BSM'] = 1.000250506927025
    kappas['ZZ'] = 0.9964595388770217
    kappas['WW'] = 0.9964595388770217
    kappas['lam'] = 2.296737570137434
    kappas['gamgam'] = 0.9814976263381598
    kappas['Zgam'] = 0.9931497692470427
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7616860647496536
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.007238182068803667
    Mw = 80.35902874095682
    sin2thetaEff = 0.2315107861005693
    GammaZ = 2.494433653758192
    # mu2sq = 680538.0309082636
    # lam1 = 0.2581482588231646
    # lam2 = 6.805809996002355
    # lam3 = 12.621527658615442
    # lam4 = -6.76485454775504
    # lam5 = -6.815321323186791
    # mH = 807.1427573066131
    # mA = 1031.8198783998162
    # mHp = 1031.078323715462
    # Best scan point row: 13367 out of 14054

elif BP == "BPB_4":
    kappas['uu'] = 0.9884079643889591
    kappas['dd'] = 0.9884079643889591
    kappas['ss'] = 0.9884079643889591
    kappas['cc'] = 0.9884079643889591
    kappas['bb'] = 0.9884079643889591
    kappas['tt'] = 0.9884079643889591
    kappas['ee'] = 0.9884079643889591
    kappas['mumu'] = 0.9884079643889591
    kappas['tautau'] = 0.9884079643889591
    kappas['ZZ_0'] = 1.0025717951997075
    kappas['ZZ_240'] = 1.0150117889437067
    kappas['ZZ_365'] = 1.0018592821116823
    kappas['ZZ_500'] = 0.9971793729362697
    kappas['ZZ_550'] = 0.9962084260225224
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 0.9991265995710326
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0110560618089828
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 0.9972240812420315
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9914736038181186
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9900125216795821
    kappas['ZZ_0_no_1L_BSM'] = 1.0095670269465051
    kappas['ZZ_240_no_1L_BSM'] = 1.0214964891844553
    kappas['ZZ_365_no_1L_BSM'] = 1.0076645086175042
    kappas['ZZ_500_no_1L_BSM'] = 1.001914031193591
    kappas['ZZ_550_no_1L_BSM'] = 1.0004529490550547
    kappas['ZZ'] = 0.9895595726245274
    kappas['WW'] = 0.9895595726245274
    kappas['lam'] = 3.3446699219962595
    kappas['gamgam'] = 0.9730906099071067
    kappas['Zgam'] = 0.9900356683423326
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8761452003718885
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.013152506832024402
    Mw = 80.38071823046351
    sin2thetaEff = 0.2313900188743548
    GammaZ = 2.4956174489103207
    # mu2sq = 392201.4410400964
    # lam1 = 0.2581482588231646
    # lam2 = 10.055587617970035
    # lam3 = 14.191244552064315
    # lam4 = -6.9741239021267765
    # lam5 = -6.407287302610276
    # mH = 645.561117519705
    # mA = 897.3211718373656
    # mHp = 906.844677616692
    # Best scan point row: 9138 out of 14054

elif BP == "BPB_5":
    kappas['uu'] = 0.9900931243271051
    kappas['dd'] = 0.9900931243271051
    kappas['ss'] = 0.9900931243271051
    kappas['cc'] = 0.9900931243271051
    kappas['bb'] = 0.9900931243271051
    kappas['tt'] = 0.9900931243271051
    kappas['ee'] = 0.9900931243271051
    kappas['mumu'] = 0.9900931243271051
    kappas['tautau'] = 0.9900931243271051
    kappas['ZZ_0'] = 1.0056040601626168
    kappas['ZZ_240'] = 1.0177390096162389
    kappas['ZZ_365'] = 1.0045074415993116
    kappas['ZZ_500'] = 0.999519357798253
    kappas['ZZ_550'] = 0.9983919428055029
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0042285694053632
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0160257773760775
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.002347143072169
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9966604174891006
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9952155334275394
    kappas['ZZ_0_no_1L_BSM'] = 1.0094609634783291
    kappas['ZZ_240_no_1L_BSM'] = 1.0212581714490434
    kappas['ZZ_365_no_1L_BSM'] = 1.0075795371451353
    kappas['ZZ_500_no_1L_BSM'] = 1.0018928115620667
    kappas['ZZ_550_no_1L_BSM'] = 1.0004479275005054
    kappas['ZZ'] = 0.994767605927034
    kappas['WW'] = 0.994767605927034
    kappas['lam'] = 3.3186760761499228
    kappas['gamgam'] = 0.9802217711125746
    kappas['Zgam'] = 0.9926780357796698
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7459022968686289
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.013231568016927264
    Mw = 80.35940143464471
    sin2thetaEff = 0.2315081093735147
    GammaZ = 2.4944519389039352
    # mu2sq = 783508.4283221567
    # lam1 = 0.2581482588231646
    # lam2 = 0.0942565704916213
    # lam3 = 16.16826765459465
    # lam4 = -8.553633851863331
    # lam5 = -8.591465219325812
    # mH = 868.2733773090105
    # mA = 1129.047670475533
    # mHp = 1128.539718220238
    # Best scan point row: 11188 out of 14054

elif BP == "BPB_6":
    kappas['uu'] = 0.9854469377667994
    kappas['dd'] = 0.9854469377667994
    kappas['ss'] = 0.9854469377667994
    kappas['cc'] = 0.9854469377667994
    kappas['bb'] = 0.9854469377667994
    kappas['tt'] = 0.9854469377667994
    kappas['ee'] = 0.9854469377667994
    kappas['mumu'] = 0.9854469377667994
    kappas['tautau'] = 0.9854469377667994
    kappas['ZZ_0'] = 1.0055192079358077
    kappas['ZZ_240'] = 1.0230601563636632
    kappas['ZZ_365'] = 1.0041791687182084
    kappas['ZZ_500'] = 0.9972340465022999
    kappas['ZZ_550'] = 0.9957200588363064
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0012755439989802
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0182314260000087
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 0.9985714090054754
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9903979964320847
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9883212945790857
    kappas['ZZ_0_no_1L_BSM'] = 1.0135980463134002
    kappas['ZZ_240_no_1L_BSM'] = 1.0305539283144287
    kappas['ZZ_365_no_1L_BSM'] = 1.0108939113198954
    kappas['ZZ_500_no_1L_BSM'] = 1.0027204987465046
    kappas['ZZ_550_no_1L_BSM'] = 1.0006437968935058
    kappas['ZZ'] = 0.98767749768558
    kappas['WW'] = 0.98767749768558
    kappas['lam'] = 4.332584967850238
    kappas['gamgam'] = 0.9700106601524686
    kappas['Zgam'] = 0.9888951932924951
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.8187710155862721
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.01888098764545476
    Mw = 80.37348693182949
    sin2thetaEff = 0.2314269601851323
    GammaZ = 2.4952102702469863
    # mu2sq = 343218.2711120506
    # lam1 = 0.2581482588231646
    # lam2 = 8.984516382894434
    # lam3 = 15.827215377391914
    # lam4 = -7.704245964494598
    # lam5 = -7.399661731335215
    # mH = 604.2708130665314
    # mA = 902.0760317326942
    # mHp = 907.179002168283
    # Best scan point row: 13296 out of 14054

elif BP == "BPB_7":
    kappas['uu'] = 0.9852208371495629
    kappas['dd'] = 0.9852208371495629
    kappas['ss'] = 0.9852208371495629
    kappas['cc'] = 0.9852208371495629
    kappas['bb'] = 0.9852208371495629
    kappas['tt'] = 0.9852208371495629
    kappas['ee'] = 0.9852208371495629
    kappas['mumu'] = 0.9852208371495629
    kappas['tautau'] = 0.9852208371495629
    kappas['ZZ_0'] = 1.0079531045463617
    kappas['ZZ_240'] = 1.0254512345289055
    kappas['ZZ_365'] = 1.0066194417575949
    kappas['ZZ_500'] = 0.9996973232749794
    kappas['ZZ_550'] = 0.9981907127682461
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.005223379266794
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0221370066304132
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.0025259830701059
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9943729389201723
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9923014122791617
    kappas['ZZ_0_no_1L_BSM'] = 1.0135641595172777
    kappas['ZZ_240_no_1L_BSM'] = 1.030477786880897
    kappas['ZZ_365_no_1L_BSM'] = 1.0108667633205897
    kappas['ZZ_500_no_1L_BSM'] = 1.002713719170656
    kappas['ZZ_550_no_1L_BSM'] = 1.0006421925296456
    kappas['ZZ'] = 0.9916592197495162
    kappas['WW'] = 0.9916592197495162
    kappas['lam'] = 4.324280052220163
    kappas['gamgam'] = 0.9690970559288911
    kappas['Zgam'] = 0.9885564514654552
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7399166728011941
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.01883179277131064
    Mw = 80.35876824202134
    sin2thetaEff = 0.2315037043489978
    GammaZ = 2.494387630161727
    # mu2sq = 310947.4410847936
    # lam1 = 0.2581482588231646
    # lam2 = 7.232954805156705
    # lam3 = 15.427491934399168
    # lam4 = -8.000550406260457
    # lam5 = -8.063169908845332
    # mH = 540.0574501781234
    # mA = 883.4503934836061
    # mHp = 882.3754709592797
    # Best scan point row: 11409 out of 14054

elif BP == "BPB_8":
    kappas['uu'] = 0.9828359716154949
    kappas['dd'] = 0.9828359716154949
    kappas['ss'] = 0.9828359716154949
    kappas['cc'] = 0.9828359716154949
    kappas['bb'] = 0.9828359716154949
    kappas['tt'] = 0.9828359716154949
    kappas['ee'] = 0.9828359716154949
    kappas['mumu'] = 0.9828359716154949
    kappas['tautau'] = 0.9828359716154949
    kappas['ZZ_0'] = 1.0085578410846359
    kappas['ZZ_240'] = 1.031527651086288
    kappas['ZZ_365'] = 1.0064611082906136
    kappas['ZZ_500'] = 0.9970113612942804
    kappas['ZZ_550'] = 0.9948793346159323
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0034517459492933
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0257925851168923
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 0.9998888145150157
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9891196374387966
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9863834033641496
    kappas['ZZ_0_no_1L_BSM'] = 1.0179166006028355
    kappas['ZZ_240_no_1L_BSM'] = 1.0402574397704345
    kappas['ZZ_365_no_1L_BSM'] = 1.014353669168558
    kappas['ZZ_500_no_1L_BSM'] = 1.003584492092339
    kappas['ZZ_550_no_1L_BSM'] = 1.0008482580176918
    kappas['ZZ'] = 0.9855351453464578
    kappas['WW'] = 0.9855351453464578
    kappas['lam'] = 5.390968560325193
    kappas['gamgam'] = 0.9681793366722093
    kappas['Zgam'] = 0.9882174303694794
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7950653452447117
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.02506654279567444
    Mw = 80.37609074924455
    sin2thetaEff = 0.2314114903628951
    GammaZ = 2.495348976439634
    # mu2sq = 328759.637232809
    # lam1 = 0.2581482588231646
    # lam2 = 1.2703870616502186
    # lam3 = 17.59281710875603
    # lam4 = -8.612074406019904
    # lam5 = -8.276027320744518
    # mH = 591.7102422482498
    # mA = 922.9560398389395
    # mHp = 928.4579313154292
    # Best scan point row: 650 out of 14054

elif BP == "BPB_9":
    kappas['uu'] = 0.9839951854420015
    kappas['dd'] = 0.9839951854420015
    kappas['ss'] = 0.9839951854420015
    kappas['cc'] = 0.9839951854420015
    kappas['bb'] = 0.9839951854420015
    kappas['tt'] = 0.9839951854420015
    kappas['ee'] = 0.9839951854420015
    kappas['mumu'] = 0.9839951854420015
    kappas['tautau'] = 0.9839951854420015
    kappas['ZZ_0'] = 1.0114054368277123
    kappas['ZZ_240'] = 1.0337493110809932
    kappas['ZZ_365'] = 1.0091285593961397
    kappas['ZZ_500'] = 0.9996856607596301
    kappas['ZZ_550'] = 0.9975045713248815
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.008659490805412
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.030486135139472
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.0051785634947046
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.994657248872197
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9919839917257659
    kappas['ZZ_0_no_1L_BSM'] = 1.0175042336637314
    kappas['ZZ_240_no_1L_BSM'] = 1.0393308779977914
    kappas['ZZ_365_no_1L_BSM'] = 1.014023306353024
    kappas['ZZ_500_no_1L_BSM'] = 1.0035019917305164
    kappas['ZZ_550_no_1L_BSM'] = 1.0008287345840854
    kappas['ZZ'] = 0.9911552571416806
    kappas['WW'] = 0.9911552571416806
    kappas['lam'] = 5.289906405452073
    kappas['gamgam'] = 0.9717649005806308
    kappas['Zgam'] = 0.9895460934847392
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7295186448626314
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.02462075168485356
    Mw = 80.36227084007066
    sin2thetaEff = 0.2314867657126174
    GammaZ = 2.49458857475883
    # mu2sq = 456183.32654440246
    # lam1 = 0.2581482588231646
    # lam2 = 4.705794417185857
    # lam3 = 18.32819562035909
    # lam4 = -9.631675980898995
    # lam5 = -9.60985163869147
    # mH = 654.5978566947667
    # mA = 1005.5282765389716
    # mHp = 1005.8571745763631
    # Best scan point row: 9586 out of 14054

elif BP == "BPB_10":
    kappas['uu'] = 0.9799021451854892
    kappas['dd'] = 0.9799021451854892
    kappas['ss'] = 0.9799021451854892
    kappas['cc'] = 0.9799021451854892
    kappas['bb'] = 0.9799021451854892
    kappas['tt'] = 0.9799021451854892
    kappas['ee'] = 0.9799021451854892
    kappas['mumu'] = 0.9799021451854892
    kappas['tautau'] = 0.9799021451854892
    kappas['ZZ_0'] = 1.011345435393513
    kappas['ZZ_240'] = 1.0393984974770443
    kappas['ZZ_365'] = 1.0086936891072946
    kappas['ZZ_500'] = 0.9970643338394835
    kappas['ZZ_550'] = 0.9944257606352366
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0051009631840995
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0324231976879572
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.0007435956099358
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.987573186956855
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9842268476146259
    kappas['ZZ_0_no_1L_BSM'] = 1.0219115118957838
    kappas['ZZ_240_no_1L_BSM'] = 1.0492337463996417
    kappas['ZZ_365_no_1L_BSM'] = 1.01755414432162
    kappas['ZZ_500_no_1L_BSM'] = 1.0043837356685394
    kappas['ZZ_550_no_1L_BSM'] = 1.0010373963263104
    kappas['ZZ'] = 0.9831894512883156
    kappas['WW'] = 0.9831894512883156
    kappas['lam'] = 6.370034303736775
    kappas['gamgam'] = 0.9642362524964034
    kappas['Zgam'] = 0.9867567059352143
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7793395772932701
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.030704808369749648
    Mw = 80.37895112068958
    sin2thetaEff = 0.2313927412940867
    GammaZ = 2.495494459006496
    # mu2sq = 243509.8038579712
    # lam1 = 0.2581482588231646
    # lam2 = 5.855907537074902
    # lam3 = 18.318377848566364
    # lam4 = -9.0582123206633
    # lam5 = -8.726365552836324
    # mH = 509.5982532102154
    # mA = 888.0982927643415
    # mHp = 893.7435516366396
    # Best scan point row: 3830 out of 14054

elif BP == "BPB_11":
    kappas['uu'] = 0.9822591209070276
    kappas['dd'] = 0.9822591209070276
    kappas['ss'] = 0.9822591209070276
    kappas['cc'] = 0.9822591209070276
    kappas['bb'] = 0.9822591209070276
    kappas['tt'] = 0.9822591209070276
    kappas['ee'] = 0.9822591209070276
    kappas['mumu'] = 0.9822591209070276
    kappas['tautau'] = 0.9822591209070276
    kappas['ZZ_0'] = 1.014537115551844
    kappas['ZZ_240'] = 1.041873404405887
    kappas['ZZ_365'] = 1.0114703907688232
    kappas['ZZ_500'] = 0.9996254236405407
    kappas['ZZ_550'] = 0.9968339404214662
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0113339571975337
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0381501772434816
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.0070572891353609
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9941307996681031
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9908464353480122
    kappas['ZZ_0_no_1L_BSM'] = 1.02150570534243
    kappas['ZZ_240_no_1L_BSM'] = 1.0483219253883775
    kappas['ZZ_365_no_1L_BSM'] = 1.0172290372802568
    kappas['ZZ_500_no_1L_BSM'] = 1.004302547812999
    kappas['ZZ_550_no_1L_BSM'] = 1.0010181834929082
    kappas['ZZ'] = 0.989828251855104
    kappas['WW'] = 0.989828251855104
    kappas['lam'] = 6.270579956517072
    kappas['gamgam'] = 0.9716394792919597
    kappas['Zgam'] = 0.9895001872696593
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.726069782680232
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.03040301363706388
    Mw = 80.36604187614141
    sin2thetaEff = 0.2314664328547996
    GammaZ = 2.4947970488524804
    # mu2sq = 499504.6283960989
    # lam1 = 0.2581482588231646
    # lam2 = 3.2929848441524787
    # lam3 = 20.27610625737985
    # lam4 = -10.662330869539236
    # lam5 = -10.550442043302542
    # mH = 686.3762338451633
    # mA = 1053.908704375542
    # mHp = 1055.5165265174924
    # Best scan point row: 5888 out of 14054

elif BP == "BPB_12":
    kappas['uu'] = 0.9779510402945
    kappas['dd'] = 0.9779510402945
    kappas['ss'] = 0.9779510402945
    kappas['cc'] = 0.9779510402945
    kappas['bb'] = 0.9779510402945
    kappas['tt'] = 0.9779510402945
    kappas['ee'] = 0.9779510402945
    kappas['mumu'] = 0.9779510402945
    kappas['tautau'] = 0.9779510402945
    kappas['ZZ_0'] = 1.0146601801452706
    kappas['ZZ_240'] = 1.048541169142913
    kappas['ZZ_365'] = 1.0110724336603367
    kappas['ZZ_500'] = 0.996621858253727
    kappas['ZZ_550'] = 0.9932624300476764
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.007592375587837
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0407444761242528
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.0023052572201065
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9863246202150712
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9822642576452792
    kappas['ZZ_0_no_1L_BSM'] = 1.0265868681118053
    kappas['ZZ_240_no_1L_BSM'] = 1.0597389686482208
    kappas['ZZ_365_no_1L_BSM'] = 1.0212997497440748
    kappas['ZZ_500_no_1L_BSM'] = 1.0053191127390393
    kappas['ZZ_550_no_1L_BSM'] = 1.0012587501692474
    kappas['ZZ'] = 0.9810055074760319
    kappas['WW'] = 0.9810055074760319
    kappas['lam'] = 7.515862276796717
    kappas['gamgam'] = 0.964519464620997
    kappas['Zgam'] = 0.9868624932160871
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7718960244295371
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.03746873548257623
    Mw = 80.37475970785388
    sin2thetaEff = 0.2314160806836613
    GammaZ = 2.495265930828681
    # mu2sq = 275231.53458544216
    # lam1 = 0.2581482588231646
    # lam2 = 5.205507553180204
    # lam3 = 20.19341903898416
    # lam4 = -9.783845354056114
    # lam5 = -9.523847591325938
    # mH = 549.6177902208486
    # mA = 937.792384757616
    # mHp = 941.9849384035392
    # Best scan point row: 11025 out of 14054

elif BP == "BPB_13":
    kappas['uu'] = 0.9794009347660855
    kappas['dd'] = 0.9794009347660855
    kappas['ss'] = 0.9794009347660855
    kappas['cc'] = 0.9794009347660855
    kappas['bb'] = 0.9794009347660855
    kappas['tt'] = 0.9794009347660855
    kappas['ee'] = 0.9794009347660855
    kappas['mumu'] = 0.9794009347660855
    kappas['tautau'] = 0.9794009347660855
    kappas['ZZ_0'] = 1.017709648973257
    kappas['ZZ_240'] = 1.0512088704608138
    kappas['ZZ_365'] = 1.0138613710380702
    kappas['ZZ_500'] = 0.9992550710344579
    kappas['ZZ_550'] = 0.995797062535416
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0131490230128533
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0460474734001508
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.0079023569344399
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9920439894355215
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.988014693119591
    kappas['ZZ_0_no_1L_BSM'] = 1.0263834492348105
    kappas['ZZ_240_no_1L_BSM'] = 1.0592818996221078
    kappas['ZZ_365_no_1L_BSM'] = 1.021136783156397
    kappas['ZZ_500_no_1L_BSM'] = 1.0052784156574788
    kappas['ZZ_550_no_1L_BSM'] = 1.0012491193415483
    kappas['ZZ'] = 0.9867655737780427
    kappas['WW'] = 0.9867655737780427
    kappas['lam'] = 7.466008740779396
    kappas['gamgam'] = 0.9687124711983263
    kappas['Zgam'] = 0.988416241175598
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7293169930651524
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.037347499422743624
    Mw = 80.35999526714207
    sin2thetaEff = 0.2314973566725667
    GammaZ = 2.4944567399865565
    # mu2sq = 415269.476372534
    # lam1 = 0.2581482588231646
    # lam2 = 3.201524939000471
    # lam3 = 21.29650257001269
    # lam4 = -10.81401334826784
    # lam5 = -10.84959254835891
    # mH = 635.721494866856
    # mA = 1030.4798769217216
    # mHp = 1029.9564544013654
    # Best scan point row: 4572 out of 14054

elif BP == "BPB_14":
    kappas['uu'] = 0.9752928757189672
    kappas['dd'] = 0.9752928757189672
    kappas['ss'] = 0.9752928757189672
    kappas['cc'] = 0.9752928757189672
    kappas['bb'] = 0.9752928757189672
    kappas['tt'] = 0.9752928757189672
    kappas['ee'] = 0.9752928757189672
    kappas['mumu'] = 0.9752928757189672
    kappas['tautau'] = 0.9752928757189672
    kappas['ZZ_0'] = 1.018224274903439
    kappas['ZZ_240'] = 1.0577540179842202
    kappas['ZZ_365'] = 1.0139224973656134
    kappas['ZZ_500'] = 0.9969466588006025
    kappas['ZZ_550'] = 0.9929800438002488
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0101407780543297
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.048867172999423
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.0039646676203833
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9852969979971153
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9805539137896662
    kappas['ZZ_0_no_1L_BSM'] = 1.0310572644927858
    kappas['ZZ_240_no_1L_BSM'] = 1.069783659437879
    kappas['ZZ_365_no_1L_BSM'] = 1.0248811540588394
    kappas['ZZ_500_no_1L_BSM'] = 1.0062134844355712
    kappas['ZZ_550_no_1L_BSM'] = 1.0014704002281223
    kappas['ZZ'] = 0.979083513561544
    kappas['WW'] = 0.979083513561544
    kappas['lam'] = 8.611459058586306
    kappas['gamgam'] = 0.9617556329224429
    kappas['Zgam'] = 0.9858388012191261
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7589345667791059
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.043831520618606845
    Mw = 80.37845879589715
    sin2thetaEff = 0.2313933968857054
    GammaZ = 2.495460078702212
    # mu2sq = 219743.3620017332
    # lam1 = 0.2581482588231646
    # lam2 = 3.3790952472128284
    # lam3 = 21.01272584601004
    # lam4 = -10.340505742608803
    # lam5 = -10.050507081176848
    # mH = 488.4554874347217
    # mA = 920.81044239123
    # mHp = 925.5713516896838
    # Best scan point row: 12586 out of 14054

elif BP == "BPB_15":
    kappas['uu'] = 0.9758076122035252
    kappas['dd'] = 0.9758076122035252
    kappas['ss'] = 0.9758076122035252
    kappas['cc'] = 0.9758076122035252
    kappas['bb'] = 0.9758076122035252
    kappas['tt'] = 0.9758076122035252
    kappas['ee'] = 0.9758076122035252
    kappas['mumu'] = 0.9758076122035252
    kappas['tautau'] = 0.9758076122035252
    kappas['ZZ_0'] = 1.020837921149283
    kappas['ZZ_240'] = 1.059551441355437
    kappas['ZZ_365'] = 1.0165553852124465
    kappas['ZZ_500'] = 0.9998571224979024
    kappas['ZZ_550'] = 0.9959414417602217
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0150385281300451
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0529931067268972
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.00898550746493
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.990689884158373
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9860413295330754
    kappas['ZZ_0_no_1L_BSM'] = 1.030438293775238
    kappas['ZZ_240_no_1L_BSM'] = 1.0683928723720901
    kappas['ZZ_365_no_1L_BSM'] = 1.0243852731101233
    kappas['ZZ_500_no_1L_BSM'] = 1.006089649803566
    kappas['ZZ_550_no_1L_BSM'] = 1.0014410951782684
    kappas['ZZ'] = 0.984600234354807
    kappas['WW'] = 0.984600234354807
    kappas['lam'] = 8.459762817722257
    kappas['gamgam'] = 0.9626061555176816
    kappas['Zgam'] = 0.9861539099506105
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7219985807961474
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.04299605614299051
    Mw = 80.36644727286449
    sin2thetaEff = 0.2314571267403946
    GammaZ = 2.494792723813611
    # mu2sq = 238528.5838429659
    # lam1 = 0.2581482588231646
    # lam2 = 3.7425572765487054
    # lam3 = 20.954896960207243
    # lam4 = -10.782914159041637
    # lam5 = -10.714218892253037
    # mH = 471.2666888161372
    # mA = 933.6125221178388
    # mHp = 934.727038427817
    # Best scan point row: 13599 out of 14054

elif BP == "BPB_16":
    kappas['uu'] = 0.972110709527596
    kappas['dd'] = 0.972110709527596
    kappas['ss'] = 0.972110709527596
    kappas['cc'] = 0.972110709527596
    kappas['bb'] = 0.972110709527596
    kappas['tt'] = 0.972110709527596
    kappas['ee'] = 0.972110709527596
    kappas['mumu'] = 0.972110709527596
    kappas['tautau'] = 0.972110709527596
    kappas['ZZ_0'] = 1.020726628196106
    kappas['ZZ_240'] = 1.0640655366197775
    kappas['ZZ_365'] = 1.016340787857924
    kappas['ZZ_500'] = 0.9980976220606489
    kappas['ZZ_550'] = 0.9939143794605771
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0108193645129049
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0531482762759274
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.004068722374181
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9836644957110771
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9784801868388892
    kappas['ZZ_0_no_1L_BSM'] = 1.0339463616528175
    kappas['ZZ_240_no_1L_BSM'] = 1.0762752734158403
    kappas['ZZ_365_no_1L_BSM'] = 1.027195719514094
    kappas['ZZ_500_no_1L_BSM'] = 1.00679149285099
    kappas['ZZ_550_no_1L_BSM'] = 1.001607183978802
    kappas['ZZ'] = 0.9768730028600872
    kappas['WW'] = 0.9768730028600872
    kappas['lam'] = 9.319513844125106
    kappas['gamgam'] = 0.9553893338375414
    kappas['Zgam'] = 0.9834792434465481
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7449363773395835
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.04772474876185351
    Mw = 80.37347683058418
    sin2thetaEff = 0.2314133073810362
    GammaZ = 2.495158402457192
    # mu2sq = 94462.8593624575
    # lam1 = 0.2581482588231646
    # lam2 = 6.386752548813656
    # lam3 = 20.283034437385734
    # lam4 = -10.123788867795252
    # lam5 = -9.98167381888814
    # mH = 315.9832662863707
    # mA = 839.6282370810434
    # mHp = 842.1896319192272
    # Best scan point row: 4560 out of 14054

elif BP == "BPB_17":
    kappas['uu'] = 0.9723983817965866
    kappas['dd'] = 0.9723983817965866
    kappas['ss'] = 0.9723983817965866
    kappas['cc'] = 0.9723983817965866
    kappas['bb'] = 0.9723983817965866
    kappas['tt'] = 0.9723983817965866
    kappas['ee'] = 0.9723983817965866
    kappas['mumu'] = 0.9723983817965866
    kappas['tautau'] = 0.9723983817965866
    kappas['ZZ_0'] = 1.0246178844400475
    kappas['ZZ_240'] = 1.0707166397756804
    kappas['ZZ_365'] = 1.0194447352171014
    kappas['ZZ_500'] = 0.9994909949726744
    kappas['ZZ_550'] = 0.994801503186093
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.0167276682828614
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0619531108004323
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.0095150855519197
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9877146153382295
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9821755487020472
    kappas['ZZ_0_no_1L_BSM'] = 1.0362692817666839
    kappas['ZZ_240_no_1L_BSM'] = 1.0814947242842547
    kappas['ZZ_365_no_1L_BSM'] = 1.0290566990357422
    kappas['ZZ_500_no_1L_BSM'] = 1.007256228822052
    kappas['ZZ_550_no_1L_BSM'] = 1.0017171621858696
    kappas['ZZ'] = 0.9804583865161776
    kappas['WW'] = 0.9804583865161776
    kappas['lam'] = 9.888810967739037
    kappas['gamgam'] = 0.9590465290403257
    kappas['Zgam'] = 0.9848353795963092
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7250331000061386
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.051271904558578996
    Mw = 80.37022469814376
    sin2thetaEff = 0.2314338179390905
    GammaZ = 2.494990352551212
    # mu2sq = 169690.6853041085
    # lam1 = 0.2581482588231646
    # lam2 = 1.6804473744590598
    # lam3 = 21.85772724295569
    # lam4 = -11.112820389422977
    # lam5 = -10.999690554344296
    # mH = 402.4520679308004
    # mA = 910.3923240118976
    # mHp = 912.2737427684896
    # Best scan point row: 3450 out of 14054

elif BP == "BPB_18":
    kappas['uu'] = 0.9679274507368065
    kappas['dd'] = 0.9679274507368065
    kappas['ss'] = 0.9679274507368065
    kappas['cc'] = 0.9679274507368065
    kappas['bb'] = 0.9679274507368065
    kappas['tt'] = 0.9679274507368065
    kappas['ee'] = 0.9679274507368065
    kappas['mumu'] = 0.9679274507368065
    kappas['tautau'] = 0.9679274507368065
    kappas['ZZ_0'] = 1.0273230857099533
    kappas['ZZ_240'] = 1.0806368505032622
    kappas['ZZ_365'] = 1.021686858342519
    kappas['ZZ_500'] = 0.999005167283247
    kappas['ZZ_550'] = 0.9937629124341144
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 1.015036927190039
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 1.0672062026301008
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 1.006716937507715
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9815692623941105
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9751797374511189
    kappas['ZZ_0_no_1L_BSM'] = 1.041838001911517
    kappas['ZZ_240_no_1L_BSM'] = 1.0940072773515788
    kappas['ZZ_365_no_1L_BSM'] = 1.033518012229193
    kappas['ZZ_500_no_1L_BSM'] = 1.0083703371155885
    kappas['ZZ_550_no_1L_BSM'] = 1.0019808121725968
    kappas['ZZ'] = 0.973198925278522
    kappas['WW'] = 0.973198925278522
    kappas['lam'] = 11.2535829810942
    kappas['gamgam'] = 0.9520472670797051
    kappas['Zgam'] = 0.9822414834898094
    # abs(kappas['ZZ_365'] - kappas['ZZ_240'])/(kappas['ZZ_240'] - 1) = 0.7310552407842171
    # abs(kappas['ZZ_365'] - kappas['ZZ_240']) = 0.05894999216074326
    Mw = 80.36926541455969
    sin2thetaEff = 0.2314314564151143
    GammaZ = 2.494908930791839
    # mu2sq = 48119.38479409877
    # lam1 = 0.2581482588231646
    # lam2 = 1.272373906403079
    # lam3 = 21.66915772112876
    # lam4 = -10.87209304362929
    # lam5 = -10.807713458049989
    # mH = 218.62433153740363
    # mA = 838.4537394598697
    # mHp = 839.6166690507159
    # Best scan point row: 13465 out of 14054


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

elif BP == "BP_lambda1":
    kappas['uu'] = 0.9984178113049657
    kappas['dd'] = 0.9984178113049657
    kappas['ss'] = 0.9984178113049657
    kappas['cc'] = 0.9984178113049657
    kappas['bb'] = 0.9984178113049657
    kappas['tt'] = 0.9984178113049657
    kappas['ee'] = 0.9984178113049657
    kappas['mumu'] = 0.9984178113049657
    kappas['tautau'] = 0.9984178113049657
    kappas['ZZ_0'] = 0.9991982973881574
    kappas['ZZ_240'] = 0.9998186516447237
    kappas['ZZ_365'] = 0.999375887226692
    kappas['ZZ_500'] = 0.9993603116685574
    kappas['ZZ_550'] = 0.9994021868768549
    kappas['ZZ_0_no_1L_BSM_sqrt_s'] = 0.9987890035121672
    kappas['ZZ_240_no_1L_BSM_sqrt_s'] = 0.9992979176548258
    kappas['ZZ_365_no_1L_BSM_sqrt_s'] = 0.9987078415565833
    kappas['ZZ_500_no_1L_BSM_sqrt_s'] = 0.9984625246068588
    kappas['ZZ_550_no_1L_BSM_sqrt_s'] = 0.9984001944406656
    kappas['ZZ_0_no_1L_BSM'] = 1.0004081320028646
    kappas['ZZ_240_no_1L_BSM'] = 1.0009170461455232
    kappas['ZZ_365_no_1L_BSM'] = 1.0003269700472808
    kappas['ZZ_500_no_1L_BSM'] = 1.0000816530975563
    kappas['ZZ_550_no_1L_BSM'] = 1.000019322931363
    kappas['ZZ'] = 0.9983808715093025
    kappas['WW'] = 0.9983808715093025
    kappas['lam'] = 1.1000242642433875
    kappas['gamgam'] = 0.9919985602913337
    kappas['Zgam'] = 0.9970379541928285
    Mw = 80.37399739650569
    sin2thetaEff = 0.23143603210752
    GammaZ = 2.4952832270640632
    # mu2sq = 1178328.7790218268
    # lam1 = 0.2581482588231646
    # lam2 = 6.213490704240298
    # lam3 = 7.168734944920202
    # lam4 = -4.512312447314827
    # lam5 = -3.143066513977466
    # mH = 1078.6925406996102
    # mA = 1163.668005251082
    # mHp = 1181.366957648721
    # Best scan point row: 4804 out of 14054

else:
    raise ValueError("Could not determine benchmark point!")



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


M_PI = 3.14159265358979323846
GF = 1.1663787e-5
mHl = 125.1
sqrt = np.sqrt

def smeft_sigma_Zh(lmbd, sqrt_s):
    mu = 1

    if sqrt_s == 240:
        C1 = 0.017
    elif sqrt_s == 365:
        C1 = 0.0057
    elif sqrt_s == 500:
        C1 = 0.00099
    else:
        raise ValueError("sqrt_s must be 240, 365, or 500 GeV")

    # Expression for the Higgs self-energy diagram
    dZH = -(9.0/16.0)*( GF*mHl*mHl/sqrt(2.0)/M_PI/M_PI )*( 2.0*M_PI/3.0/sqrt(3.0) - 1.0 )
    
    # Resummations
    dZH1 = dZH / (1.0 - dZH)
    dZH2 = dZH * (1 + 3.0 * dZH) / (1.0 - dZH) / (1.0 - dZH)

    # HEPfit flags
    cLHd6 = 1
    cLH3d62 = 1

    deltaG_hhhRatio = lmbd - 1

    mu = mu + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    mu = mu + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return mu

if smeft_formula:
    # Implements the Zh cross-section using the kappa_lambda dependent expression from HEPfit,
    # plus the external-leg correction (C_HD), taken from the coupling modifier to fermions.
    # No BSM contributions to the ZH cross-section are included.
    kappas['ZZ_240'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=240)) + (kappas["uu"]-1)
    kappas['ZZ_365'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=365)) + (kappas["uu"]-1)
    kappas['ZZ_500'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=500)) + (kappas["uu"]-1)
    
    kappas['ZZ_0'] = kappas["ZZ"]

if smeft_formula_sqrt:
    # Implements the Zh cross-section using the kappa_lambda dependent expression from HEPfit,
    # plus the external-leg correction (C_HD), taken from the coupling modifier to fermions.
    # No BSM contributions to the ZH cross-section are included.
    # Cross terms are removed by including dkappaf**2 inside of the square root
    kappas['ZZ_240'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=240) + (kappas["uu"]-1)**2)
    kappas['ZZ_365'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=365) + (kappas["uu"]-1)**2)
    kappas['ZZ_500'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=500) + (kappas["uu"]-1)**2)
    
    kappas['ZZ_0'] = kappas["ZZ"]

if smeft_formula_no_cross:
    # Implements the Zh cross-section using the kappa_lambda dependent expression from HEPfit,
    # plus the external-leg correction (C_HD), taken from the coupling modifier to fermions.
    # No BSM contributions to the ZH cross-section are included.
    # Cross terms are removed by including 2*dkappaf inside of the square root
    kappas['ZZ_240'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=240) + 2*(kappas["uu"]-1))
    kappas['ZZ_365'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=365) + 2*(kappas["uu"]-1))
    kappas['ZZ_500'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=500) + 2*(kappas["uu"]-1))
    
    kappas['ZZ_0'] = kappas["ZZ"]

if smeft_formula_external_leg:
    # Implements the Zh cross-section using the kappa_lambda dependent expression from HEPfit,
    # No BSM contributions to the ZH cross-section are included.
    kappas['ZZ_240'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=240))
    kappas['ZZ_365'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=365))
    kappas['ZZ_500'] = sqrt(smeft_sigma_Zh(lmbd=kappas["lam"], sqrt_s=500))
    
    kappas['ZZ_0'] = kappas["ZZ"]


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
    no_quad: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_no_quad.conf",
    smeft_formula: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_smeft_formula.conf",
    smeft_formula_sqrt: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_smeft_formula_sqrt.conf",
    smeft_formula_no_cross: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_smeft_formula_no_cross.conf",
    smeft_formula_external_leg: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_smeft_formula_external_leg.conf",
    WFR_kala2_input: "ObservablesHiggs_FCCee_240_SM_kappa_scaled_WFR_kala2_input.conf",
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

if (scenario == "IDM_FCCee240_FCCee365" 
    or scenario == "IDM_FCCee240_FCCee365_HLLHClambda"):
    # Open the FCCee_365 input file in read mode and output file in write mode
    input_file_FCCee365 =  file_dir + "ObservablesHiggs_FCCee_365.conf"
    output_file_FCCee365 = file_dir + "ObservablesHiggs_FCCee_365_kappa_scaled.conf"

    output_file_flag_map = {
        no_1L_BSM_sqrt_s: "ObservablesHiggs_FCCee_365_kappa_scaled_no_1L_BSM_sqrt_s.conf",
        no_1L_BSM: "ObservablesHiggs_FCCee_365_kappa_scaled_no_1L_BSM.conf",
        no_quad: "ObservablesHiggs_FCCee_365_kappa_scaled_no_quad.conf",
        smeft_formula: "ObservablesHiggs_FCCee_365_kappa_scaled_smeft_formula.conf",
        smeft_formula_sqrt: "ObservablesHiggs_FCCee_365_kappa_scaled_smeft_formula_sqrt.conf",
        smeft_formula_no_cross: "ObservablesHiggs_FCCee_365_kappa_scaled_smeft_formula_no_cross.conf",
        smeft_formula_external_leg: "ObservablesHiggs_FCCee_365_kappa_scaled_smeft_formula_external_leg.conf",
        WFR_kala2_input: "ObservablesHiggs_FCCee_365_kappa_scaled_WFR_kala2_input.conf",
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

output_file_flag_map = {
    no_1L_BSM_sqrt_s: "ObservablesHiggs_HLLHC_SM_kappa_scaled_no_1L_BSM_sqrt_s.conf",
    no_1L_BSM: "ObservablesHiggs_HLLHC_SM_kappa_scaled_no_1L_BSM.conf",
    no_quad: "ObservablesHiggs_HLLHC_SM_kappa_scaled_no_quad.conf",
    smeft_formula: "ObservablesHiggs_HLLHC_SM_kappa_scaled_smeft_formula.conf",
    smeft_formula_sqrt: "ObservablesHiggs_HLLHC_SM_kappa_scaled_smeft_formula_sqrt.conf",
    smeft_formula_no_cross: "ObservablesHiggs_HLLHC_SM_kappa_scaled_smeft_formula_no_cross.conf",
    smeft_formula_external_leg: "ObservablesHiggs_HLLHC_SM_kappa_scaled_smeft_formula_external_leg.conf",
    WFR_kala2_input: "ObservablesHiggs_HLLHC_SM_kappa_scaled_WFR_kala2_input.conf",
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

if scenario == "IDM_FCCee240_FCCee365_HLLHClambda":
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






# if fast:

#     input_file =  file_dir + "MonteCarlo.conf"
#     output_file = file_dir + "MonteCarlo_fast.conf"

#     with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
#         for line in infile:
#             if line.startswith("Iterations"):
#                 columns = line.split()
#                 columns[1] = str(50000)
#                 outfile.write(" ".join(columns) + "\n")

#             elif line.startswith("RValueForConvergence"):
#                 columns = line.split()
#                 columns[1] = str(1.03)
#                 outfile.write(" ".join(columns) + "\n")

#             else:
#                 # Write unmodified lines to the output file
#                 outfile.write(line)

#     with open(output_file, 'a') as outfile:
#         outfile.write(final_text)

#     print(f"Modified content saved to {output_file}.")

#     subprocess.run(["mv", output_file, input_file])

