# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

import subprocess
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scenario", help = "Name of the scenario (e.g. IDM_FCCee240)", type=str)
parser.add_argument("-b", "--bp", help = "Which benchmark point to use", type=str)
# parser.add_argument("--noHLLHClambda", help = "No on-shell kappa_lambda constraint", action="store_true")
parser.add_argument("--fast", help = "Run faster, using less points and a looser criterium for convergence", action="store_true")
parser.add_argument("--ewpos_all", help = "Modify also the EWPO central values for current observables", action="store_true")
parser.add_argument("--no_1L_BSM_sqrt_s", help = "Do not include momentum dependent BSM 1L corrections to Z->ZH", action="store_true")
parser.add_argument("--no_quad", help = "Do not include quadratic momentum dependent BSM 1L corrections to Z->ZH", action="store_true")


args = parser.parse_args()
scenario = args.scenario
BP = args.bp
# noHLLHClambda = args.noHLLHClambda
fast = args.fast
modify_all_ewpos = args.ewpos_all
no_1L_BSM_sqrt_s = args.no_1L_BSM_sqrt_s
no_quad = args.no_quad


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
    kappas['ZZ_0_no_1L_BSM'] = 1.0023378651272847
    kappas['ZZ_240_no_1L_BSM'] = 1.0177981665211153
    kappas['ZZ_365_no_1L_BSM'] = 0.9998722462932628
    kappas['ZZ_500_no_1L_BSM'] = 0.9924197633264032
    kappas['ZZ_550_no_1L_BSM'] = 0.9905262353724729
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
    kappas['ZZ_0_no_1L_BSM'] = 0.9993516901502957
    kappas['ZZ_240_no_1L_BSM'] = 1.0005654828751926
    kappas['ZZ_365_no_1L_BSM'] = 0.9991581137039593
    kappas['ZZ_500_no_1L_BSM'] = 0.9985730171151438
    kappas['ZZ_550_no_1L_BSM'] = 0.9984243556889322
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
    kappas['ZZ_0_no_1L_BSM'] = 0.9970430932347498
    kappas['ZZ_240_no_1L_BSM'] = 0.9976582557060288
    kappas['ZZ_365_no_1L_BSM'] = 0.996944986727216
    kappas['ZZ_500_no_1L_BSM'] = 0.996648453838091
    kappas['ZZ_550_no_1L_BSM'] = 0.996573110718581
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
    kappas['ZZ_0_no_1L_BSM'] = 0.9983584296416149
    kappas['ZZ_240_no_1L_BSM'] = 0.9989280007074098
    kappas['ZZ_365_no_1L_BSM'] = 0.9982675940808219
    kappas['ZZ_500_no_1L_BSM'] = 0.997993038070682
    kappas['ZZ_550_no_1L_BSM'] = 0.9979232788397744
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
    kappas['ZZ_0_no_1L_BSM'] = 0.9977031653428668
    kappas['ZZ_240_no_1L_BSM'] = 1.0047587501412416
    kappas['ZZ_365_no_1L_BSM'] = 0.9965779361302687
    kappas['ZZ_500_no_1L_BSM'] = 0.9931768623612863
    kappas['ZZ_550_no_1L_BSM'] = 0.9923127170444053
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0017506560443745
    kappas['ZZ_240_no_1L_BSM'] = 1.0083483360548362
    kappas['ZZ_365_no_1L_BSM'] = 1.000698453782578
    kappas['ZZ_500_no_1L_BSM'] = 0.9975181084163243
    kappas['ZZ_550_no_1L_BSM'] = 0.9967100458040468
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
    kappas['ZZ_0_no_1L_BSM'] = 0.9991265995710326
    kappas['ZZ_240_no_1L_BSM'] = 1.0110560618089828
    kappas['ZZ_365_no_1L_BSM'] = 0.9972240812420315
    kappas['ZZ_500_no_1L_BSM'] = 0.9914736038181186
    kappas['ZZ_550_no_1L_BSM'] = 0.9900125216795821
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0042285694053632
    kappas['ZZ_240_no_1L_BSM'] = 1.0160257773760775
    kappas['ZZ_365_no_1L_BSM'] = 1.002347143072169
    kappas['ZZ_500_no_1L_BSM'] = 0.9966604174891006
    kappas['ZZ_550_no_1L_BSM'] = 0.9952155334275394
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0012755439989802
    kappas['ZZ_240_no_1L_BSM'] = 1.0182314260000087
    kappas['ZZ_365_no_1L_BSM'] = 0.9985714090054754
    kappas['ZZ_500_no_1L_BSM'] = 0.9903979964320847
    kappas['ZZ_550_no_1L_BSM'] = 0.9883212945790857
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
    kappas['ZZ_0_no_1L_BSM'] = 1.005223379266794
    kappas['ZZ_240_no_1L_BSM'] = 1.0221370066304132
    kappas['ZZ_365_no_1L_BSM'] = 1.0025259830701059
    kappas['ZZ_500_no_1L_BSM'] = 0.9943729389201723
    kappas['ZZ_550_no_1L_BSM'] = 0.9923014122791617
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0034517459492933
    kappas['ZZ_240_no_1L_BSM'] = 1.0257925851168923
    kappas['ZZ_365_no_1L_BSM'] = 0.9998888145150157
    kappas['ZZ_500_no_1L_BSM'] = 0.9891196374387966
    kappas['ZZ_550_no_1L_BSM'] = 0.9863834033641496
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
    kappas['ZZ_0_no_1L_BSM'] = 1.008659490805412
    kappas['ZZ_240_no_1L_BSM'] = 1.030486135139472
    kappas['ZZ_365_no_1L_BSM'] = 1.0051785634947046
    kappas['ZZ_500_no_1L_BSM'] = 0.994657248872197
    kappas['ZZ_550_no_1L_BSM'] = 0.9919839917257659
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0051009631840995
    kappas['ZZ_240_no_1L_BSM'] = 1.0324231976879572
    kappas['ZZ_365_no_1L_BSM'] = 1.0007435956099358
    kappas['ZZ_500_no_1L_BSM'] = 0.987573186956855
    kappas['ZZ_550_no_1L_BSM'] = 0.9842268476146259
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0113339571975337
    kappas['ZZ_240_no_1L_BSM'] = 1.0381501772434816
    kappas['ZZ_365_no_1L_BSM'] = 1.0070572891353609
    kappas['ZZ_500_no_1L_BSM'] = 0.9941307996681031
    kappas['ZZ_550_no_1L_BSM'] = 0.9908464353480122
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
    kappas['ZZ_0_no_1L_BSM'] = 1.007592375587837
    kappas['ZZ_240_no_1L_BSM'] = 1.0407444761242528
    kappas['ZZ_365_no_1L_BSM'] = 1.0023052572201065
    kappas['ZZ_500_no_1L_BSM'] = 0.9863246202150712
    kappas['ZZ_550_no_1L_BSM'] = 0.9822642576452792
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0131490230128533
    kappas['ZZ_240_no_1L_BSM'] = 1.0460474734001508
    kappas['ZZ_365_no_1L_BSM'] = 1.0079023569344399
    kappas['ZZ_500_no_1L_BSM'] = 0.9920439894355215
    kappas['ZZ_550_no_1L_BSM'] = 0.988014693119591
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0101407780543297
    kappas['ZZ_240_no_1L_BSM'] = 1.048867172999423
    kappas['ZZ_365_no_1L_BSM'] = 1.0039646676203833
    kappas['ZZ_500_no_1L_BSM'] = 0.9852969979971153
    kappas['ZZ_550_no_1L_BSM'] = 0.9805539137896662
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0150385281300451
    kappas['ZZ_240_no_1L_BSM'] = 1.0529931067268972
    kappas['ZZ_365_no_1L_BSM'] = 1.00898550746493
    kappas['ZZ_500_no_1L_BSM'] = 0.990689884158373
    kappas['ZZ_550_no_1L_BSM'] = 0.9860413295330754
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0108193645129049
    kappas['ZZ_240_no_1L_BSM'] = 1.0531482762759274
    kappas['ZZ_365_no_1L_BSM'] = 1.004068722374181
    kappas['ZZ_500_no_1L_BSM'] = 0.9836644957110771
    kappas['ZZ_550_no_1L_BSM'] = 0.9784801868388892
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
    kappas['ZZ_0_no_1L_BSM'] = 1.0167276682828614
    kappas['ZZ_240_no_1L_BSM'] = 1.0619531108004323
    kappas['ZZ_365_no_1L_BSM'] = 1.0095150855519197
    kappas['ZZ_500_no_1L_BSM'] = 0.9877146153382295
    kappas['ZZ_550_no_1L_BSM'] = 0.9821755487020472
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
    kappas['ZZ_0_no_1L_BSM'] = 1.015036927190039
    kappas['ZZ_240_no_1L_BSM'] = 1.0672062026301008
    kappas['ZZ_365_no_1L_BSM'] = 1.006716937507715
    kappas['ZZ_500_no_1L_BSM'] = 0.9815692623941105
    kappas['ZZ_550_no_1L_BSM'] = 0.9751797374511189
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

else:
    raise ValueError("Could not determine benchmark point!")

### For now, no values at precisely 250 and 350 GeV
kappas['ZZ_250'] = kappas['ZZ_240']; kappas['ZZ_250_no_1L_BSM'] = kappas['ZZ_240_no_1L_BSM']; 
kappas['ZZ_350'] = kappas['ZZ_365']; kappas['ZZ_350_no_1L_BSM'] = kappas['ZZ_365_no_1L_BSM']

if no_1L_BSM_sqrt_s:
    kappas['ZZ_0'] = kappas['ZZ_0_no_1L_BSM']
    # kappas['ZZ_125'] = kappas['ZZ_125_no_1L_BSM']
    kappas['ZZ_240'] = kappas['ZZ_240_no_1L_BSM']
    kappas['ZZ_250'] = kappas['ZZ_250_no_1L_BSM']
    kappas['ZZ_350'] = kappas['ZZ_350_no_1L_BSM']
    kappas['ZZ_365'] = kappas['ZZ_365_no_1L_BSM']
    kappas['ZZ_500'] = kappas['ZZ_500_no_1L_BSM']
    kappas['ZZ_550'] = kappas['ZZ_550_no_1L_BSM']

BrHinv = 0.
BrHexo = 0.

kappas2 = {}
for kappa in kappas.keys():
    kappas2[kappa] = kappas[kappa]**2

if no_quad:
    for kappa in ['ZZ_0', 'ZZ_240', 'ZZ_250', 'ZZ_350', 'ZZ_365', 'ZZ_500', 'ZZ_550', ]:
        kappas2[kappa] = 2*kappas[kappa] - 1
        # Only linear correction to the Z->ZH cross sections are included


# Need to weigh the kappas to get the scaling factor for VBF
wgt_W_VBF = 10.
wgt_Z_VBF = 1.
kappas2["VBF"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ"]) / (wgt_W_VBF + wgt_Z_VBF)
kappas2["VBF_0"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_0"]) / (wgt_W_VBF + wgt_Z_VBF)
# kappas2["VBF_125"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_125"]) / (wgt_W_VBF + wgt_Z_VBF)
kappas2["VBF_240"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_240"]) / (wgt_W_VBF + wgt_Z_VBF)
kappas2["VBF_250"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_250"]) / (wgt_W_VBF + wgt_Z_VBF)
kappas2["VBF_350"] = (wgt_W_VBF*kappas2["WW"] + wgt_Z_VBF*kappas2["ZZ_350"]) / (wgt_W_VBF + wgt_Z_VBF)
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
###################################   ILC at 250 GeV   ####################################
###########################################################################################
###########################################################################################

# Open the ILC_250 input file in read mode and output file in write mode
input_file_ILC250 =  file_dir + "ObservablesHiggs_ILC_250_SM.conf"
output_file_ILC250 = file_dir + "ObservablesHiggs_ILC_250_IDM.conf"
if no_1L_BSM_sqrt_s:
    output_file_ILC250 = file_dir + "ObservablesHiggs_ILC_250_IDM_no_1L_BSM_sqrt_s.conf"
elif no_quad:
    output_file_ILC250 = file_dir + "ObservablesHiggs_ILC_250_IDM_no_quad.conf"

with open(input_file_ILC250, 'r') as infile, open(output_file_ILC250, 'w') as outfile:
    for line in infile:
        if line.startswith("Observable"):
            # Split the line into columns by whitespace
            columns = line.split()
            
            if (columns[1].startswith("eeZH_")):
                columns[8] = str(kappas2["ZZ_250"]*float(columns[8]))
                columns[9] = str(kappas2["ZZ_250"]*float(columns[9]))

            elif (columns[1].startswith("eeZHbb_")):
                columns[8] = str(kappas2["ZZ_250"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_250"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeHvvbb_")):
                columns[8] = str(kappas2["WW"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["WW"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHcc_")):
                columns[8] = str(kappas2["ZZ_250"]*kappas2["cc"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_250"]*kappas2["cc"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHgg_")):
                columns[8] = str(kappas2["ZZ_250"]*kappas2["gg"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_250"]*kappas2["gg"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHWW_")):
                columns[8] = str(kappas2["ZZ_250"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_250"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHZZ_")):
                columns[8] = str(kappas2["ZZ_250"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_250"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHtautau_")):
                columns[8] = str(kappas2["ZZ_250"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_250"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHgaga_")):
                columns[8] = str(kappas2["ZZ_250"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_250"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

            elif (columns[1].startswith("eeZHmumu_")):
                columns[8] = str(kappas2["ZZ_250"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                columns[9] = str(kappas2["ZZ_250"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])

            # elif (columns[1].startswith("eeZHZga_")):
            #     columns[8] = str(kappas2["ZZ_250"]*kappas2["Zgam"]*float(columns[8])/kappas2["H"])
            #     columns[9] = str(kappas2["ZZ_250"]*kappas2["Zgam"]*float(columns[9])/kappas2["H"])

            # Rejoin the columns and write to the output file
            outfile.write(" ".join(columns) + "\n")
        else:
            # Write unmodified lines to the output file
            outfile.write(line)

with open(output_file_ILC250, 'a') as outfile:
    outfile.write(final_text)


print(f"Modified content saved to {output_file_ILC250}.")






###########################################################################################
###########################################################################################
###################################   ILC at 350 GeV   ####################################
###########################################################################################
###########################################################################################

if (scenario == "IDM_ILC_250_350" 
    or scenario == "IDM_ILC_250_350_500"
    or scenario == "IDM_ILC_250_350_500_1000"):
    # Open the ILC_350 input file in read mode and output file in write mode
    input_file_ILC350 =  file_dir + "ObservablesHiggs_ILC_350_SM.conf"
    output_file_ILC350 = file_dir + "ObservablesHiggs_ILC_350_IDM.conf"
    if no_1L_BSM_sqrt_s:
        output_file_ILC350 = file_dir + "ObservablesHiggs_ILC_350_IDM_no_1L_BSM_sqrt_s.conf"
    elif no_quad:
        output_file_ILC350 = file_dir + "ObservablesHiggs_ILC_350_IDM_no_quad.conf"


    with open(input_file_ILC350, 'r') as infile, open(output_file_ILC350, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
                if (columns[1].startswith("eeZH_")):
                    columns[8] = str(kappas2["ZZ_350"]*float(columns[8]))
                    columns[9] = str(kappas2["ZZ_350"]*float(columns[9]))


                elif (columns[1].startswith("eeZHbb_")):
                    columns[8] = str(kappas2["ZZ_350"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_350"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvbb_")):
                    columns[8] = str(kappas2["WW"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["bb"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHcc_")):
                    columns[8] = str(kappas2["ZZ_350"]*kappas2["cc"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_350"]*kappas2["cc"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvcc_")):
                    columns[8] = str(kappas2["WW"]*kappas2["cc"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["cc"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHgg_")):
                    columns[8] = str(kappas2["ZZ_350"]*kappas2["gg"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_350"]*kappas2["gg"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvgg_")):
                    columns[8] = str(kappas2["WW"]*kappas2["gg"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["gg"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHWW_")):
                    columns[8] = str(kappas2["ZZ_350"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_350"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvWW_")):
                    columns[8] = str(kappas2["WW"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["WW"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHZZ_")):
                    columns[8] = str(kappas2["ZZ_350"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_350"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvZZ_")):
                    columns[8] = str(kappas2["WW"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHtautau_")):
                    columns[8] = str(kappas2["ZZ_350"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_350"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvtautau_")):
                    columns[8] = str(kappas2["WW"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHgaga_")):
                    columns[8] = str(kappas2["ZZ_350"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_350"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvgaga_")):
                    columns[8] = str(kappas2["WW"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHmumu_")):
                    columns[8] = str(kappas2["ZZ_350"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_350"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvmumu_")):
                    columns[8] = str(kappas2["WW"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])


                # Rejoin the columns and write to the output file
                outfile.write(" ".join(columns) + "\n")
            else:
                # Write unmodified lines to the output file
                outfile.write(line)

    with open(output_file_ILC350, 'a') as outfile:
        outfile.write(final_text)

    print(f"Modified content saved to {output_file_ILC350}.")




###########################################################################################
###########################################################################################
###################################   ILC at 500 GeV   ####################################
###########################################################################################
###########################################################################################

if (scenario == "IDM_ILC_250_350_500"
    or scenario == "IDM_ILC_250_350_500_1000"):
    # Open the ILC_500 input file in read mode and output file in write mode
    input_file_ILC500 =  file_dir + "ObservablesHiggs_ILC_500_SM.conf"
    output_file_ILC500 = file_dir + "ObservablesHiggs_ILC_500_IDM.conf"
    if no_1L_BSM_sqrt_s:
        output_file_ILC500 = file_dir + "ObservablesHiggs_ILC_500_IDM_no_1L_BSM_sqrt_s.conf"
    elif no_quad:
        output_file_ILC500 = file_dir + "ObservablesHiggs_ILC_500_IDM_no_quad.conf"


    with open(input_file_ILC500, 'r') as infile, open(output_file_ILC500, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
                if (columns[1].startswith("eeZH_")):
                    columns[8] = str(kappas2["ZZ_500"]*float(columns[8]))
                    columns[9] = str(kappas2["ZZ_500"]*float(columns[9]))


                elif (columns[1].startswith("eeZHbb_")):
                    columns[8] = str(kappas2["ZZ_500"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_500"]*kappas2["bb"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvbb_")):
                    columns[8] = str(kappas2["WW"]*kappas2["bb"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["bb"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHcc_")):
                    columns[8] = str(kappas2["ZZ_500"]*kappas2["cc"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_500"]*kappas2["cc"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvcc_")):
                    columns[8] = str(kappas2["WW"]*kappas2["cc"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["cc"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHgg_")):
                    columns[8] = str(kappas2["ZZ_500"]*kappas2["gg"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_500"]*kappas2["gg"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvgg_")):
                    columns[8] = str(kappas2["WW"]*kappas2["gg"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["gg"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHWW_")):
                    columns[8] = str(kappas2["ZZ_500"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_500"]*kappas2["WW"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvWW_")):
                    columns[8] = str(kappas2["WW"]*kappas2["WW"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["WW"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHZZ_")):
                    columns[8] = str(kappas2["ZZ_500"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_500"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvZZ_")):
                    columns[8] = str(kappas2["WW"]*kappas2["ZZ"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["ZZ"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHtautau_")):
                    columns[8] = str(kappas2["ZZ_500"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_500"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvtautau_")):
                    columns[8] = str(kappas2["WW"]*kappas2["tautau"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["tautau"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHgaga_")):
                    columns[8] = str(kappas2["ZZ_500"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_500"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvgaga_")):
                    columns[8] = str(kappas2["WW"]*kappas2["gamgam"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["gamgam"]*float(columns[9])/kappas2["H"])


                elif (columns[1].startswith("eeZHmumu_")):
                    columns[8] = str(kappas2["ZZ_500"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["ZZ_500"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])

                elif (columns[1].startswith("eeHvvmumu_")):
                    columns[8] = str(kappas2["WW"]*kappas2["mumu"]*float(columns[8])/kappas2["H"])
                    columns[9] = str(kappas2["WW"]*kappas2["mumu"]*float(columns[9])/kappas2["H"])


                # Rejoin the columns and write to the output file
                outfile.write(" ".join(columns) + "\n")
            else:
                # Write unmodified lines to the output file
                outfile.write(line)

    with open(output_file_ILC500, 'a') as outfile:
        outfile.write(final_text)

    print(f"Modified content saved to {output_file_ILC500}.")




###########################################################################################
###########################################################################################
##################################   ILC at 1000 GeV   ####################################
###########################################################################################
###########################################################################################

### To be implemented!!
if (scenario == "IDM_ILC_250_350_500_1000"):
    raise NotImplementedError("Inputs for ILC at 1000 GeV not yet implemented!")



###########################################################################################
###########################################################################################
######################################   HL-HLC   #########################################
###########################################################################################
###########################################################################################


# Open the HL-LHC input file in read mode and output file in write mode
input_file_HLLHC =  file_dir + "ObservablesHiggs_HLLHC_SM.conf"
output_file_HLLHC = file_dir + "ObservablesHiggs_HLLHC_IDM.conf"
if no_1L_BSM_sqrt_s:
    output_file_HLLHC = file_dir + "ObservablesHiggs_HLLHC_IDM_no_1L_BSM_sqrt_s.conf"
if no_quad:
    output_file_HLLHC = file_dir + "ObservablesHiggs_HLLHC_IDM_no_quad.conf"


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

if BP == "BPB_2":
    kala_uncertainty_low  = 0.135811
    kala_uncertainty_high = 0.135811
elif BP == "BPB_4":
    kala_uncertainty_low  = 0.130138
    kala_uncertainty_high = 0.130138
elif BP == "BPB_6":
    kala_uncertainty_low  = 0.128268
    kala_uncertainty_high = 0.128268
else:
    raise IndexError("No uncertainty at ILC500 for this kappa_lambda has been implemented!")

if (scenario == "IDM_ILC_250_350_500"
    or scenario == "IDM_ILC_250_350_500_1000"):
    # Open the e+e- collider input file in read mode and output file in write mode
    input_file =  file_dir + "ObservablesHiggs_IDM.conf"
    output_file = file_dir + "ObservablesHiggs_IDM_temp.conf"
    

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
                if (columns[2].startswith("deltalHHH")):
                    columns[0] = "AsyGausObservable"
                    columns[6]="MCMC"
                    columns[7]="weight"
                    columns.append(str(kappas['lam']-1))
                    columns.append(str(kala_uncertainty_low))
                    columns.append(str(kala_uncertainty_high))

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
    file_dir + "ObservablesEW_HLLHC.conf",
    file_dir + "ObservablesEW_ILC_250_SM.conf",
]

output_files = [
    file_dir + "ObservablesEW_HLLHC_IDM.conf",
    file_dir + "ObservablesEW_ILC_250_IDM.conf",
]

if (scenario == "IDM_ILC_250_350_500"
    or scenario == "IDM_ILC_250_350_500_1000"):
    input_files.append(file_dir + "ObservablesEW_ILC_tt.conf")
    output_files.append(file_dir + "ObservablesEW_ILC_tt_IDM.conf")

if modify_all_ewpos:
    input_files.append(file_dir + "ObservablesEW_Current_SM_noLFU.conf")
    output_files.append(file_dir + "ObservablesEW_Current_SM_noLFU_IDM.conf")

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

