from curses import echo

import numpy as np
import sys
import os
from copy import deepcopy
import json
import argparse

sys.path.append(os.path.abspath("/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/"))

from fit_utils.parser import read_fit_results_pars, find_tex_label_par


def find_1sigma_WCs(wilson_coefficients):
    working_dir = "."
    BPs = ["SM_fit", ]
    model_specs = {"." : ["fits_small_priors_strict", ]}
    scenarios = model_specs.keys()
    model = "SM"

    parameters, _, _, results = read_fit_results_pars(
        BPs,
        model_specs,
        working_dir,
        scenarios,
        model,
    )

    wc_ranges = {}
    print()

    for wc in wilson_coefficients:
        for BP in BPs:
            for scenario in scenarios:
                for model_spec in model_specs[scenario]:
                    if (wc + "_corr") not in parameters[BP][scenario][model_spec]:
                        print(f"  {wc} not found in fit results for {BP}, {scenario}, {model_spec}")
                        continue
                    wc_index = parameters[BP][scenario][model_spec].index(wc + "_corr")
                    wc_value = results[BP][scenario][model_spec][:,0][wc_index]
                    wc_error = results[BP][scenario][model_spec][:,1][wc_index]

                    wc_ranges[wc+ "_low"] = wc_value - wc_error
                    wc_ranges[wc+ "_high"] = wc_value + wc_error

    # Print latex table with the results:
    WC_labels = [ find_tex_label_par(None, wc) for wc in wilson_coefficients ]
    print("Wilson coefficient & 1 sigma range \\\\")
    print("\\hline")
    for wc, wc_label in zip(wilson_coefficients, WC_labels):
        if wc + "_low" in wc_ranges and wc + "_high" in wc_ranges:
            print(f"{wc_label} & [{wc_ranges[wc + '_low']:.3g}, {wc_ranges[wc + '_high']:.3g}] \\\\")
        else:
            print(f"{wc_label} & N/A \\\\")
    return wc_ranges

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", 
        "--wilson_coefficients", 
        help="Which Wilson coefficients to analyze", 
        nargs="*", 
        default=["CH", "CHbox", "CHD", "CHW", "CHG", "CHB", "CHWB", "CHe_11", "CHL1_11", "CHL3_11"],
    )

    args = parser.parse_args()
    wilson_coefficients = args.wilson_coefficients 

    wc_ranges = find_1sigma_WCs(wilson_coefficients)
    print(json.dumps(wc_ranges))