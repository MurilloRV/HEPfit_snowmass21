import pickle
import numpy as np
import sys
import os
import json
import argparse

sys.path.append(os.path.abspath("/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/"))
import fit_utils.EFT_matching as EFT_matching


def find_matched_WCs(wilson_coefficients):


    BP_input_dir = "/cephfs/user/mrebuzzi/phd/HiggsTools/future_projections/scan_output/IDM_scan_output"
    BP_dicts_filename = f"{BP_input_dir}/Benchmark_Points_outliers_dicts.pkl"
    BP_dicts_lambda1_filename = f"{BP_input_dir}/Benchmark_Points_lambda1_dicts.pkl"

    with open(BP_dicts_filename, 'rb') as f:
        BPs = pickle.load(f)
        bp_model_pars = BPs["model_pars"][2::2]

    with open(BP_dicts_lambda1_filename, 'rb') as f:
        BPs = pickle.load(f)
        bp_model_pars_lambda1 = BPs["model_pars"]

    print("BP model parameters:", bp_model_pars)
    print("BP model parameters (lambda1):", bp_model_pars_lambda1)
    bp_model_pars[0] = bp_model_pars_lambda1 # BP 0 is BP_lambda1

    mu2 = np.sqrt( np.array([bp["mu2sq"] for bp in bp_model_pars]) ); print("\nmu2:", mu2)
    lam1 = np.array([bp["lam1"] for bp in bp_model_pars]); print("\nlam1:", lam1)
    lam2 = np.array([bp["lam2"] for bp in bp_model_pars]); print("\nlam2:", lam2)
    lam3 = np.array([bp["lam3"] for bp in bp_model_pars]); print("\nlam3:", lam3)
    lam4 = np.array([bp["lam4"] for bp in bp_model_pars]); print("\nlam4:", lam4)
    lam5 = np.array([bp["lam5"] for bp in bp_model_pars]); print("\nlam5:", lam5)
    mH = np.array([bp["mH"] for bp in bp_model_pars]); print("\nmH:", mH)
    mA = np.array([bp["mA"] for bp in bp_model_pars]); print("\nmA:", mA)
    mHp = np.array([bp["mHp"] for bp in bp_model_pars]); print("\nmHp:", mHp)

    IDM = EFT_matching.IDM.from_masses(mH=mH, mA=mA, mHp=mHp, mu2=mu2)

    # Set matching scale
    lamNP_match = mHp
    lamNP = 1000 # GeV
    
    # Getting the matched Wilson coefficients at the NP scale
    matched_WCs = IDM.get_coefficients(lamNP_match=lamNP_match, dimensionless=True, lamNP=lamNP)
    print("\nMatched Wilson coefficients at lamNP = mHp:")
    for wc_name, wc_values in matched_WCs.items():
        print(f"{wc_name}: {wc_values}")

    BP_slice = slice(0, 4)

    CH    = matched_WCs["CH"][BP_slice]
    CHbox = matched_WCs["CHbox"][BP_slice]
    CHD   = matched_WCs["CHD"][BP_slice]
    CHW   = matched_WCs["CHW"][BP_slice]
    CHB   = matched_WCs["CHB"][BP_slice]
    CHWB  = matched_WCs["CHWB"][BP_slice]

    matched_kappa_lambdas = IDM.get_kappa_lambda_SMEFT_match(lamNP_match=lamNP_match)[BP_slice]
    print("\nMatched kappa_lambda at lamNP = mHp:")
    print(matched_kappa_lambdas)

    WC_matched_values = {
        "CH": list(CH),
        "CHbox": list(CHbox),
        "CHD": list(CHD),
        "CHW": list(CHW),
        "CHB": list(CHB),
        "CHWB": list(CHWB),
    }

    return WC_matched_values


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", 
        "--wilson_coefficients", 
        help="Which Wilson coefficients to analyze", 
        nargs="*", 
        default=["CH", "CHbox", "CHD", "CHW", "CHB", "CHWB",],
    )

    args = parser.parse_args()
    wilson_coefficients = args.wilson_coefficients 

    WC_matched_values = find_matched_WCs(wilson_coefficients)
    print(json.dumps(WC_matched_values))