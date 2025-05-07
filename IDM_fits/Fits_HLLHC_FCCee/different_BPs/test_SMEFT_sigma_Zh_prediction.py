import numpy as np


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

    deltaG_hhhRatio = lmbd - 1

    mu = mu + cLHd6*(C1 + 2.0*dZH1)*deltaG_hhhRatio

    mu = mu + cLHd6*cLH3d62*dZH2*deltaG_hhhRatio*deltaG_hhhRatio

    return mu

# Johannes' formula
# def ZZh_hextleg(kala):
#     dZh = -(Mh**2*(-9 + 2*np.sqrt(3)*np.pi))/(32*np.pi**2*vev**2)
#     return (kala**2-1)*dZh

import matplotlib.pyplot as plt

x = range(-5, 11)
k_zh_240 = [np.sqrt(smeft_sigma_Zh(lmbd, 240))-1 for lmbd in x]
k_zh_365 = [np.sqrt(smeft_sigma_Zh(lmbd, 365))-1 for lmbd in x]

plt.plot(k_zh_365, k_zh_240)
plt.xlabel(r'$\kappa_\text{Zh}^{365}-1$')
plt.ylabel(r'$\kappa_\text{Zh}^{240}-1$')
# plt.show()

lmbd = 2.3867362274064843
dkappaf = 0.991329519562304 - 1

print(f"dkappaf = {dkappaf}")
print(f"smeft_formula: k_Zh_240 = {np.sqrt(smeft_sigma_Zh(lmbd=lmbd, sqrt_s=240)) + (dkappaf)}")
print(f"smeft_formula_sqrt: k_Zh_240 = {np.sqrt(smeft_sigma_Zh(lmbd=lmbd, sqrt_s=240) + (dkappaf)**2)}")
print(f"smeft_formula_external_leg: k_Zh_240 = {np.sqrt(smeft_sigma_Zh(lmbd=lmbd, sqrt_s=240))}")