# Short script to scale the expected values and uncertainties for the 
# XS*BR Higgs Observables, according to the kappa-framework

import subprocess
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scenario", help = "Name of the scenario (e.g. Z2SSM_FCCee240)", type=str)
parser.add_argument("-b", "--bp", help = "Which benchmark point to use", type=str)
# parser.add_argument("--noHLLHClambda", help = "No on-shell kappa_lambda constraint", action="store_true")
parser.add_argument("--fast", help = "Run faster, using less points and a looser criterium for convergence", action="store_true")




args = parser.parse_args()
scenario = args.scenario
BP = args.bp
# noHLLHClambda = args.noHLLHClambda
fast = args.fast


# file_dir = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_ILC_250/Z2SSM_BenchmarkPoint_fits_HLLHC_ILC_250"
file_dir = f"{BP}/{scenario}/"


kappas={}
# Definition of Z2SSM benchmark point:
# kappas['gg'] = 1.0

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
             "# Z2SSM Benchmark Point:\n"

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

if (scenario == "Z2SSM_FCCee240_FCCee365" 
    or scenario == "Z2SSM_FCCee240_FCCee365_HLLHClambda"):
    # Open the FCCee_365 input file in read mode and output file in write mode
    input_file_FCCee365 =  file_dir + "ObservablesHiggs_FCCee_365.conf"
    output_file_FCCee365 = file_dir + "ObservablesHiggs_FCCee_365_kappa_scaled.conf"


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

if scenario == "Z2SSM_FCCee240_FCCee365_HLLHClambda":
    # Open the e+e- collider input file in read mode and output file in write mode
    input_file =  file_dir + "ObservablesHiggs.conf"
    output_file = file_dir + "ObservablesHiggs_scaled.conf"

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

input_files =  [# "ObservablesEW_Current_SM_noLFU.conf",
               file_dir + "ObservablesEW_HLLHC.conf",
               file_dir + "ObservablesEW_FCCee_WW_SM.conf",
               file_dir + "ObservablesEW_FCCee_Zpole_SM.conf",
               ]

output_files = [# "ObservablesEW_Current_SM_noLFU_kappa_scaled.conf",
               file_dir + "ObservablesEW_HLLHC_kappa_scaled.conf",
               file_dir + "ObservablesEW_FCCee_WW_SM_kappa_scaled.conf",
               file_dir + "ObservablesEW_FCCee_Zpole_SM_kappa_scaled.conf",
              ]

for input_file, output_file in zip(input_files, output_files):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
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






if fast:

    input_file =  file_dir + "MonteCarlo.conf"
    output_file = file_dir + "MonteCarlo_fast.conf"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("Iterations"):
                columns = line.split()
                columns[1] = str(50000)
                outfile.write(" ".join(columns) + "\n")

            elif line.startswith("RValueForConvergence"):
                columns = line.split()
                columns[1] = str(1.02)
                outfile.write(" ".join(columns) + "\n")

            else:
                # Write unmodified lines to the output file
                outfile.write(line)

    with open(output_file, 'a') as outfile:
        outfile.write(final_text)

    print(f"Modified content saved to {output_file}.")

    subprocess.run(["mv", output_file, input_file])

