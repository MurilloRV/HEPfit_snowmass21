# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import scipy
import scipy.special as spe
import os
import sys
import matplotlib.pyplot as plt
import subprocess

mwmin=80.355 # MW from PDG +/- 2* uncertainty from PDG
mwmax=80.403 
slmin=0.23121 # slep from the combined LEP and SLD results (hep-ex/0509008) +/- 2* uncertainty  
slmax=0.23185
GamZmin=2.4906
GamZmax=2.4998

working_dir = "."

def checkwithin(testval, minval, maxval):
    if testval > minval and testval < maxval:
        return True
    else: 
        return False

def ewpo1L2L(mH,mA,mHp,l345, test=False):

    if test:
        out_path = f"{working_dir}/output_test.txt"
        out=open(out_path,'w')
        subprocess.call([f"{working_dir}/THDM_EWPOS/IHDM_allEWPOs_test.bin", str(mH), str(mA), str(mHp), str(l345)], stdout=out)
    else:
        out_path = f"{working_dir}/output.txt"
        out=open(out_path,'w')
        subprocess.call([f"{working_dir}/THDM_EWPOS/IHDM_allEWPOs.bin", str(mH), str(mA), str(mHp), str(l345)], stdout=out)

    out.close()

    val=open(out_path,'r')

    for line in val:
        if 'MW1L:' in line:
            valmw1L=float(line.replace('MW1L:',' '))
        if 'sl1L:' in line: 
                valsl1L=float(line.replace('Result for effective leptonic mixing angle sl1L:',' '))
        if 'GammaZ1L:' in line:
            valGamZ1L=float(line.replace('GammaZ1L:',' '))
        if 'MW2L:' in line:
            valmw2L=float(line.replace('MW2L:',' '))
        if 'sl2L:' in line: 
                valsl2L=float(line.replace('Result for effective leptonic mixing angle sl2L:',' '))
        if 'GammaZ2L:' in line:
            valGamZ2L=float(line.replace('GammaZ2L:',' '))

    val.close()

    return [valmw1L, valsl1L, valGamZ1L, valmw2L, valsl2L, valGamZ2L]
	
def ewpo1L(mH,mA,mHp,l345, test=False):

    if test:
        out_path = f"{working_dir}/output_test.txt"
        out=open(out_path,'w')
        subprocess.call([f"{working_dir}/THDM_EWPOS/IHDM_allEWPOs_test.bin", str(mH), str(mA), str(mHp), str(l345)], stdout=out)
    else:
        out_path = f"{working_dir}/output.txt"
        out=open(out_path,'w')
        subprocess.call([f"{working_dir}/THDM_EWPOS/IHDM_allEWPOs.bin", str(mH), str(mA), str(mHp), str(l345)], stdout=out)

    out.close()

    val=open(out_path,'r')

    for line in val:
        if 'MW1L:' in line:
            valmw1L=float(line.replace('MW1L:',' '))
        if 'sl1L:' in line: 
            valsl1L=float(line.replace('Result for effective leptonic mixing angle sl1L:',' '))
        if 'GammaZ1L:' in line:
            valGamZ1L=float(line.replace('GammaZ1L:',' '))

    val.close()

    return [valmw1L, valsl1L, valGamZ1L]
	
def ewpo2L(mH,mA,mHp,l345, test=False):

    if test:
        out_path = f"{working_dir}/output_test.txt"
        out=open(out_path,'w')
        subprocess.call([f"{working_dir}/THDM_EWPOS/IHDM_allEWPOs_test.bin", str(mH), str(mA), str(mHp), str(l345)], stdout=out)
    else:
        out_path = f"{working_dir}/output.txt"
        out=open(out_path,'w')
        subprocess.call([f"{working_dir}/THDM_EWPOS/IHDM_allEWPOs.bin", str(mH), str(mA), str(mHp), str(l345)], stdout=out)

    out.close()

    val=open(out_path,'r')

    for line in val:
        if 'MW2L:' in line:
            valmw2L=float(line.replace('MW2L:',' '))
        if 'sl2L:' in line: 
            valsl2L=float(line.replace('Result for effective leptonic mixing angle sl2L:',' '))
        if 'GammaZ2L:' in line:
            valGamZ2L=float(line.replace('GammaZ2L:',' '))


    val.close()

    return [valmw2L, valsl2L, valGamZ2L]
	
def checkEWPO1L2L(mH,mA,mHp,l345):

	[mW1L, sl1L, GamZ1L, mW2L, sl2L, GamZ2L] = ewpo1L2L(mH,mA,mHp,l345)
	
	return checkwithin(mW1L, mwmin,mwmax)* checkwithin(sl1L, slmin,slmax)* checkwithin(mW2L, mwmin,mwmax) * checkwithin(sl2L, slmin,slmax) * checkwithin(GamZ1L, GamZmin,GamZmax) * checkwithin(GamZ2L, GamZmin,GamZmax)
	
def checkEWPO1L(mH,mA,mHp,l345):

	[mW1L, sl1L, GamZ1L] = ewpo1L(mH,mA,mHp,l345)
	
	return checkwithin(mW1L, mwmin,mwmax)* checkwithin(sl1L, slmin,slmax) * checkwithin(GamZ1L, GamZmin,GamZmax)
	
def checkEWPO2L(mH,mA,mHp,l345):

	[mW2L, sl2L, GamZ2L] = ewpo2L(mH,mA,mHp,l345)
	
	return checkwithin(mW2L, mwmin,mwmax) * checkwithin(sl2L, slmin,slmax) * checkwithin(GamZ2L, GamZmin,GamZmax)
	
@np.vectorize
def MW1L_vec(mH,mA,mHp,l345, test=False):
	return ewpo1L(mH,mA,mHp,l345, test=test)[0]
	
@np.vectorize
def sl1L_vec(mH,mA,mHp,l345, test=False):
	return ewpo1L(mH,mA,mHp,l345, test=test)[1]
	
@np.vectorize
def GamZ1L_vec(mH,mA,mHp,l345, test=False):
	return ewpo1L(mH,mA,mHp,l345, test=test)[2]
	
@np.vectorize
def MW2L_vec(mH,mA,mHp,l345, test=False):
	return ewpo2L(mH,mA,mHp,l345, test=test)[0]
	
@np.vectorize
def sl2L_vec(mH,mA,mHp,l345, test=False):
	return ewpo2L(mH,mA,mHp,l345, test=test)[1]
	
@np.vectorize
def GamZ2L_vec(mH,mA,mHp,l345, test=False):
	return ewpo2L(mH,mA,mHp,l345, test=test)[2]
	
@np.vectorize 
def checkEWPO1L_vec(mH,mA,mHp,l345):
	return checkEWPO1L(mH,mA,mHp,l345)
	
@np.vectorize 
def checkEWPO2L_vec(mH,mA,mHp,l345):
	return checkEWPO2L(mH,mA,mHp,l345)
