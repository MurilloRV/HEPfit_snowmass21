import numpy as np

vev = 246.
Mh = 125
MZ = 91.1876
MW = 80.379
cw = MW/MZ
sw = np.sqrt(1-cw**2)
gL = 2*MW/vev
gy = np.sqrt(4*MZ**2/vev**2 - gL**2)
hbar = 1 / (16 * np.pi**2)

@np.vectorize
def lambdas(mH, mA, mHp, mu2):
    lam1 = Mh**2 / vev**2
    lam3 = 2 * (mHp**2 - mu2**2) / vev**2
    lamH = 2 * (mH**2 - mu2**2) / vev**2
    lamA = 2 * (mA**2 - mu2**2) / vev**2
    lam4 = 1 / 2 * (lamH + lamA) - lam3
    lam5 = 1 / 2 * (lamH - lamA)
    return lam1, lam3, lam4, lam5, mu2


def cHbox(l1, l3, l4, l5, mu2):
    return (
        -1 / 6 * hbar * l3**2 / mu2**2
        - 1 / 6 * hbar * l3 * l4 / mu2**2
        + 1 / 12 * hbar * l5**2 / mu2**2
    )


def cHD(l1, l3, l4, l5, mu2):
    return (
        - 1 / 6 * hbar * l4**2 / mu2**2
        + 1 / 6 * hbar * l5**2 / mu2**2
    )
    
    
def cH(l1, l3, l4, l5, mu2):
    return (
        -1 / 3 * hbar * l3**3 / mu2**2
        - 1 / 2 * hbar * l4 * l3**2 / mu2**2
        + 1 / 6 * hbar * l1 * l4**2 / mu2**2
        - 1 / 2 * hbar * l3 * l4**2 / mu2**2
        - 1 / 6 * hbar * l4**3 / mu2**2
        + 1 / 6 * hbar * l1 * l5**2 / mu2**2
        - 1 / 2 * hbar * l3 * l5**2 / mu2**2
        - 1 / 2 * hbar * l4 * l5**2 / mu2**2
    )


def cHW(l1, l3, l4, l5, mu2):
    return 1 / 48 * hbar * gL**2 * (2 * l3 + l4) / mu2**2


def cHB(l1, l3, l4, l5, mu2):
    return 1 / 48 * hbar * gy**2 * (2 * l3 + l4) / mu2**2


def cHWB(l1, l3, l4, l5, mu2):
    return 1 / 24 * hbar * gL * gy * l4 / mu2**2