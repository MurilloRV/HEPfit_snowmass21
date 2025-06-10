import numpy as np
sqrt = np.sqrt

def func(mu_240, mu_365):
    dmu = mu_365 - mu_240

    LambdaNP2 = 1000.**2

    C1_240 = 0.017
    C1_365 = 0.0057
    dC = C1_365 - C1_240

    D1_240 = +121263./LambdaNP2
    D1_365 = +121243./LambdaNP2
    dD = D1_365 - D1_240

    # print(f"dD = {dD}, dC = {dC}")


    M_PI = 3.14159265358979323846
    GF = 1.1663787e-5
    mHl = 125.1
    

    dZH = -(9.0/16.0)*( GF*mHl*mHl/sqrt(2.0)/M_PI/M_PI )*( 2.0*M_PI/3.0/sqrt(3.0) - 1.0 )

    dZH1 = dZH / (1.0 - dZH)
    dZH2 = dZH * (1 + 3.0 * dZH) / (1.0 - dZH) / (1.0 - dZH)

    # print(dZH, dZH1, dZH2)

    a = dZH2
    b = C1_365 + 2*dZH1 - D1_365*dC/dD 
    c = 1 + D1_365*dmu/dD - mu_365

    # print(f"a = {a:.3}, b = {b:.3}, c = {c:.3}")

    dlmbd = (-b-sqrt(b**2 - 4*a*c))/(2*a)
    lmbd = 1 + dlmbd
    # print (f"dlmbd = {dlmbd:.3g}, lmbd = {lmbd:.3}")

    CHBox = 1./dD*(dmu - dC*dlmbd)

    CH = -2.1290888208276963*(dlmbd - CHBox/5.498361921343667)

    return CH, CHBox, lmbd

# mu_240 = 0.97**2
# mu_365 = 0.99**2
# CH, CHBox, lmbd = func(mu_240=mu_240, mu_365=mu_365)
# print(f"CH = {CH:.3g}, CHBox = {CHBox:.3g}, lmbd = {lmbd:.3g}")



CH_file_name = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/large_kappa_lambda_fits/comparison_plots/k_ZH_240_365_predictions.txt"
CHBox_file_name = "/cephfs/user/mrebuzzi/phd/HEPfit/HEPfit_snowmass21/Fits_HLLHC_FCCee/large_kappa_lambda_fits_CHbox/comparison_plots/k_ZH_240_365_predictions.txt"

WCs = ['CH', 'CHbox']
files = [CH_file_name, CHBox_file_name]

lambdas = {}
k_ZH_240 = {}
k_ZH_365 = {}
for WC, file_name in zip(WCs, files):

    lambdas[WC] = []
    k_ZH_240[WC] = {}
    k_ZH_365[WC] = {}

    with open(file_name, "r") as self_consistent_results_file:
        lines = self_consistent_results_file.readlines()
        for n, line in enumerate(lines):
            columns = line.split()

            if WC=='CH':
                lmbd = int(columns[0])
            if WC=='CHbox':
                lmbd = float(columns[0])

            lambdas[WC].append(lmbd)
            if columns[1].startswith("eeZH_FCCee240"):
                k_ZH_240[WC][lmbd] = np.sqrt(float(columns[2]))
            elif columns[1].startswith("eeZH_FCCee365"):
                k_ZH_365[WC][lmbd] = np.sqrt(float(columns[2]))

lambdas = {}
WC_values = {}

lambdas['CH'] = np.array(range(-5, 11))
lambdas['CHbox'] = np.array(np.linspace(0.9, 1.2, 7))


WC_values['CH']    = np.array([ (lmbd - 1) * (-2.1290888208276963) for lmbd in lambdas['CH'] ])
WC_values['CHbox'] = np.array([ (lmbd - 1) * (+5.498361921343667 ) for lmbd in lambdas['CHbox'] ])

analytical_WC_values = {}
analytical_lambdas = {}

for WC in WCs:

    analytical_WC_values[WC] = []
    analytical_lambdas[WC] = []

    for lmbd in lambdas[WC]:
        
        CH, CHbox, analytical_lmbd = func(
            mu_240=k_ZH_240[WC][lmbd]**2, 
            mu_365=k_ZH_365[WC][lmbd]**2, 
        )

        if WC == 'CH':
            analytical_WC_values[WC].append(CH)
            analytical_lambdas[WC].append(analytical_lmbd)
        elif WC == 'CHbox':
            analytical_WC_values[WC].append(CHbox)
            analytical_lambdas[WC].append(analytical_lmbd)

    analytical_WC_values[WC] = np.array(analytical_WC_values[WC])
    analytical_lambdas[WC] = np.array(analytical_lambdas[WC])

    print(f"WC = {WC}")
    print(f"analytical_WC_values = {analytical_WC_values[WC]}")
    print(f"analytical_WC_values - WC_values = {analytical_WC_values[WC] - WC_values[WC]}")
    print(f"analytical_lambdas = {analytical_lambdas[WC]}")
    print(f"analytical_lambdas - lambdas = {analytical_lambdas[WC] - lambdas[WC]}")
    print("\n\n")
