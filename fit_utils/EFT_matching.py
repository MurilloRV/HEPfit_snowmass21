import numpy as np
from abc import ABC, abstractmethod

vev = 246.
Mh = 125
MZ = 91.1876
MW = 80.379
cw = MW/MZ
sw = np.sqrt(1-cw**2)
gL = 2*MW/vev
gy = np.sqrt(4*MZ**2/vev**2 - gL**2)
hbar = 1 / (16 * np.pi**2)

full_WC_list = [
    "CW", 
    "CHG", 
    "CHWB", 
    "CHWHB_gaga", 
    "CHWHB_gagaorth", 
    "CHW", 
    "CHB", 
    "CHD", 
    "CHbox", 
    "CHbox", 
    "CH", 
    "CHL1_11", 
    "CHL1_22", 
    "CHL1_33", 
    "CHL3_11", 
    "CHL3_22", 
    "CHL3_33", 
    "CHe_11", 
    "CHe_22", 
    "CHe_33", 
    "CHQ1_11", 
    "CHQ1_33", 
    "CHQ3_11", 
    "CHu_11", 
    "CHd_11", 
    "CHd_33", 
    "CeH_22r", 
    "CeH_33r", 
    "CuH_22r", 
    "CuH_33r", 
    "CdH_33r",
    "CLL_1221",
]


class BSMModel(ABC):
    @abstractmethod
    def get_coefficients(self, lamNP=None, dimensionless=False):
        # Obtain the values for the Wilson coefficients divided by the new physics scale squared. To obtain 
        # dimensionless coefficients, set dimensionless=True and the desired energy scale in lamNP (in GeV).
        pass

    def get_kappa_lambda(self, lamNP=None):
        WCs = self.get_coefficients(lamNP=lamNP)

        # Coefficients already include the 1/lambda_NP^2 factor
        kappa_lambda = 1 + (vev**2) * (
            - 2 * vev**2 / Mh**2 * WCs["CH"]
            + 3 * (WCs["CHbox"] - 1/4 * WCs["CHD"])
        )
        return kappa_lambda

class Z2SSM(BSMModel):
    def __init__(self, muS, lamS, lamSH):
        if len(muS) != len(lamS) or len(muS) != len(lamSH):
            raise ValueError("Input parameters must have the same length.")
        else:
            self.N = len(muS)

        self.muS = muS
        self.lamS = lamS
        self.lamSH = lamSH

    @staticmethod
    def CH(muS, lamS, lamSH):
        # Matching to conventions in [1811.08878]
        kappa = lamSH
        lamphi = 4*3*lamS
        return - 1 / 12 * hbar * kappa**3 / muS**2

    @staticmethod
    def CHbox(muS, lamS, lamSH):
        # Matching to conventions in [1811.08878]
        kappa = lamSH
        lamphi = 4*3*lamS
        return - 1 / 24 * hbar * kappa**2 / muS**2

    def get_coefficients(self, lamNP=None, dimensionless=False):
        if lamNP is None:
            lamNP = self.muS

        CH_val    = Z2SSM.CH    (self.muS, self.lamS, self.lamSH)
        CHbox_val = Z2SSM.CHbox (self.muS, self.lamS, self.lamSH)

        WC_dict = {
            "CH": CH_val, 
            "CHbox": CHbox_val, 
        }

        for WC in full_WC_list:
            if WC not in WC_dict:
                WC_dict[WC] = np.zeros(self.N)

        if dimensionless:
            for key in WC_dict:
                WC_dict[key] = WC_dict[key] * lamNP**2

        return WC_dict

class IDM(BSMModel):
    def __init__(self, l1, l3, l4, l5, mu2):
        if len(l1) != len(l3) or len(l1) != len(l4) or len(l1) != len(l5) or len(l1) != len(mu2):
            raise ValueError("Input parameters must have the same length.")
        else:
            self.N = len(l1)

        self.l1 = l1
        self.l3 = l3
        self.l4 = l4
        self.l5 = l5
        self.mu2 = mu2

    @classmethod
    def from_masses(cls, mH, mA, mHp, mu2):
        if len(mH) != len(mA) or len(mH) != len(mHp) or len(mH) != len(mu2):
            raise ValueError("Input parameters must have the same length.")

        lam1 = Mh**2 / vev**2
        lam3 = 2 * (mHp**2 - mu2**2) / vev**2
        lamH = 2 * (mH**2 - mu2**2) / vev**2
        lamA = 2 * (mA**2 - mu2**2) / vev**2
        lam4 = 1 / 2 * (lamH + lamA) - lam3
        lam5 = 1 / 2 * (lamH - lamA)

        return cls(lam1, lam3, lam4, lam5, mu2)

    @staticmethod
    def CH(l1, l3, l4, l5, mu2):
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
    
    @staticmethod
    def CHbox(l1, l3, l4, l5, mu2):
        return (
            -1 / 6 * hbar * l3**2 / mu2**2
            - 1 / 6 * hbar * l3 * l4 / mu2**2
            + 1 / 12 * hbar * l5**2 / mu2**2
        )

    @staticmethod
    def CHD(l1, l3, l4, l5, mu2):
        return (
            - 1 / 6 * hbar * l4**2 / mu2**2
            + 1 / 6 * hbar * l5**2 / mu2**2
        )

    @staticmethod
    def CHW(l1, l3, l4, l5, mu2):
        return 1 / 48 * hbar * gL**2 * (2 * l3 + l4) / mu2**2

    @staticmethod
    def CHB(l1, l3, l4, l5, mu2):
        return 1 / 48 * hbar * gy**2 * (2 * l3 + l4) / mu2**2
    
    @staticmethod
    def CHWB(l1, l3, l4, l5, mu2):
        return 1 / 24 * hbar * gL * gy * l4 / mu2**2


    def get_coefficients(self, lamNP=None, dimensionless=False):
        if lamNP is None:
            lamNP = self.mu2

        CH_val     = IDM.CH    (self.l1, self.l3, self.l4, self.l5, self.mu2)
        CHbox_val  = IDM.CHbox (self.l1, self.l3, self.l4, self.l5, self.mu2)
        CHD_val    = IDM.CHD   (self.l1, self.l3, self.l4, self.l5, self.mu2)
        CHW_val    = IDM.CHW   (self.l1, self.l3, self.l4, self.l5, self.mu2)
        CHB_val    = IDM.CHB   (self.l1, self.l3, self.l4, self.l5, self.mu2)
        CHWB_val   = IDM.CHWB  (self.l1, self.l3, self.l4, self.l5, self.mu2)

        WC_dict = {
            "CH": CH_val, 
            "CHbox": CHbox_val, 
            "CHD": CHD_val, 
            "CHW": CHW_val, 
            "CHB": CHB_val, 
            "CHWB": CHWB_val
        }
    
        for WC in full_WC_list:
            if WC not in WC_dict:
                WC_dict[WC] = np.zeros(self.N)

        if dimensionless:
            for key in WC_dict:
                WC_dict[key] = WC_dict[key] * lamNP**2

        return WC_dict
