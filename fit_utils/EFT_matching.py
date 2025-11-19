import numpy as np
from abc import ABC, abstractmethod
from pyCollier import db0, b0, c0, a0
dB0 = np.vectorize(db0)
B0 = np.vectorize(b0)
C0 = np.vectorize(c0)
A0 = np.vectorize(a0)

import matplotlib.pyplot as plt

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
        """
        Obtain the values for the Wilson coefficients divided by the new physics scale squared. To obtain 
        dimensionless coefficients, set dimensionless=True and the desired energy scale in lamNP (in GeV).
        If dimensionless is False, lamNP is ignored, since we do not implement RGE running here.
        Implemented in child classes.
        """
        pass

    def get_kappa_lambda_SMEFT_match(self, lamNP=None):
        WCs = self.get_coefficients(lamNP=lamNP)

        # Coefficients already include the 1/lambda_NP^2 factor
        delta_kappa_lambda = (vev**2) * (
            - 2 * vev**2 / Mh**2 * WCs["CH"]
            + 3 * (WCs["CHbox"] - 1/4 * WCs["CHD"])
        )
        return 1 + delta_kappa_lambda
    

    def get_ZtoZH_SMEFT_match(self, sqrts=0.):
        # From Henning

        WCs = self.get_coefficients()

        p1p2 = 0.5 * (sqrts**2 + MZ**2 - Mh**2)
        b_gmunu = (
            WCs["CHbox"]
            + 3 / 4 * WCs["CHD"]
            + gL * gy / (gL**2 + gy**2) * WCs["CHWB"]
        )
        b_p1p2 = (
            1
            / (gL**2 + gy**2)
            * (
                - 4 * gL**2 / (gL**2 + gy**2) * WCs["CHW"]
                - 4 * gy**2 / (gL**2 + gy**2) * WCs["CHB"]
                - 4 * gL * gy / (gL**2 + gy**2) * WCs["CHWB"]
            )
        )
        b_SMEFT = b_gmunu * vev**2 + b_p1p2 * p1p2
        b_SM = 1
        # print(b_SMEFT, b_gmunu * vev**2, b_p1p2 * p1p2, b_SM)  # Debug print
        return b_SMEFT / b_SM
        # SMEFT_kin = b_SMEFT**2 * ZtoZH_kin(sqrts)
        # SM_kin = b_SM**2 * ZtoZH_kin(sqrts)
        # return SMEFT_kin / SM_kin - 1

    
    def plot_higgs_potential_SMEFT(
        self,
        figsize = (4, 3.5),
        phi_range = (-1.1*vev, 1.1*vev)
    ):


        WCs = self.get_coefficients()

        CH = WCs["CH"]
        # CHbox = WCs["CHbox"]
        # CHD = WCs["CHD"]

        phi = np.linspace(*phi_range, 200)

        mu2 = Mh**2 / 2 + (3/4) * CH * vev**4
        lam = Mh**2 / (2 * vev**2) + 3 * CH * vev**2 / 2
        V_phi_SMEFT = -mu2 * phi**2 + lam * phi**4 - CH * phi**6 # + 0.25 * CHD * vev**2 * phi**4 - CHbox * vev**2 * phi**4

        # V_SM = lamSM * (v_vals**2 - vev**2)**2
        # V_SMEFT = (
        #     lamSM * (v_vals**2 - vev**2)**2
        #     + CH * (v_vals**6 - vev**6)
        #     + 0.25 * CHD * vev**2 * (v_vals**2 - vev**2)**2
        #     - CHbox * vev**2 * (v_vals**2 - vev**2)**2
        # )

        mu2_SM = Mh**2 / 2
        lam_SM = Mh**2 / (2 * vev**2)
        V_phi_SM = -mu2_SM * phi**2 + lam_SM * phi**4

        kappa_lambda = self.get_kappa_lambda_SMEFT_match()[0]
        # print(CH, kappa_lambda)

        plt.figure(figsize=figsize)
        plt.plot(phi, V_phi_SM, label="SM Potential", color="blue")
        plt.plot(phi, V_phi_SMEFT, label="SMEFT Potential", color="red", linestyle="--")
        plt.xlabel(r"Higgs Field Value $|\phi_0|$ [GeV]")
        plt.ylabel(r"Higgs Potential $V(\phi_0)$ [GeV$^4$]")
        plt.title("Higgs Potential in SM and SMEFT\n"+rf"$C_H=${CH:.3g} GeV$^{{-2}}$, $\kappa_\lambda={kappa_lambda:.3g}$", fontsize=10)
        plt.axvline(+vev/np.sqrt(2), color='green', linestyle=':', label=r'$\pm\nu/\sqrt{2}$')
        plt.axvline(-vev/np.sqrt(2), color='green', linestyle=':')
        plt.legend()
        plt.grid()
        # plt.ylim(top=2e9)
        plt.show()

class Z2SSM(BSMModel):
    def __init__(self, muS, lamS, lamSH, mS=None):
        if not np.all( [np.isscalar(par) for par in (muS, lamS, lamSH)] ):
            if len(muS) != len(lamS) or len(muS) != len(lamSH) or (mS is not None and len(muS) != len(mS)):
                raise ValueError("Input parameters must have the same length.")
            else:
                self.N = len(muS)
        else:
            self.N = 1

        self.muS = muS
        self.lamS = lamS
        self.lamSH = lamSH

        if mS is not None:
            self.mS = mS
        else:
            self.mS = np.sqrt(muS**2 + 0.5*lamSH*vev**2)

    # Note: Wilson coefficients already include the 1/lambda_NP^2 factor, with
    # lambda_NP = muS, following [1811.08878]. 
    # UPDATE: Now using mS as NP scale in the denominators, as a test. Z2SSM kala 
    # predictions now matches the SMEFT ones!

    @staticmethod
    def CH(muS, lamS, lamSH, mS):
        # Matching to conventions in [1811.08878]
        kappa = lamSH
        lamphi = 4*3*lamS
        # return - 1 / 12 * hbar * kappa**3 / muS**2
        return - 1 / 12 * hbar * kappa**3 / mS**2

    @staticmethod
    def CHbox(muS, lamS, lamSH, mS):
        # Matching to conventions in [1811.08878]
        kappa = lamSH
        lamphi = 4*3*lamS
        # return - 1 / 24 * hbar * kappa**2 / muS**2
        return - 1 / 24 * hbar * kappa**2 / mS**2

    def get_coefficients(self, lamNP=None, dimensionless=False):
        if lamNP is None:
            lamNP = self.muS

        CH_val    = Z2SSM.CH    (self.muS, self.lamS, self.lamSH, self.mS)
        CHbox_val = Z2SSM.CHbox (self.muS, self.lamS, self.lamSH, self.mS)

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

        lam1 = np.full_like(mH, (Mh/vev)**2)
        lam3 = 2 * (mHp**2 - mu2**2) / vev**2
        lamH = 2 * (mH**2 - mu2**2) / vev**2
        lamA = 2 * (mA**2 - mu2**2) / vev**2
        lam4 = 1 / 2 * (lamH + lamA) - lam3
        lam5 = 1 / 2 * (lamH - lamA)

        return cls(lam1, lam3, lam4, lam5, mu2)

    def get_BSM_masses(self):
        mH  = np.sqrt(self.mu2**2 + 1 / 2 * (self.l3 + self.l4 + self.l5) * vev**2)
        mA  = np.sqrt(self.mu2**2 + 1 / 2 * (self.l3 + self.l4 - self.l5) * vev**2)
        mHp = np.sqrt(self.mu2**2 + 1 / 2 * self.l3 * vev**2)
        return mH, mA, mHp

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


    def get_ZtoZH_IDM(self, sqrts):
        mH, mA, mHp = self.get_BSM_masses()
        S = sqrts**2
        lam3 = self.l3; lam4 = self.l4; lam5 = self.l5

        w = np.arccos(cw)
        res = 1 / 2 * lam3 * (3 + np.cos(4 * w)) + lam4
        
        res = res - (
            1 / 4 * (lam3 + lam4 + lam5) ** 2 * vev**2 * dB0(Mh**2, mH**2, mH**2)
            + 1 / 4 * (lam3 + lam4 - lam5) ** 2 * vev**2 * dB0(Mh**2, mA**2, mA**2)
            + 1 / 2 * lam3**2 * vev**2 * dB0(Mh**2, mHp**2, mHp**2)
        )
        #
        denom = Mh**4 + (MZ**2 - S) ** 2 - 2 * Mh**2 * (MZ**2 + S)
        resb = (
            -(
                (lam3 + lam4 - lam5)
                * (2 * mA**2 * Mh**2 + (MZ**2 - S) ** 2 - Mh**2 * (2 * mH**2 + MZ**2 + S))
                * B0(Mh**2, mA**2, mA**2)
            )
            / 2.0
        )
        resb += (
            (lam3 + lam4 + lam5)
            * (2 * mA**2 * Mh**2 - (MZ**2 - S) ** 2 + Mh**2 * (-2 * mH**2 + MZ**2 + S))
            * B0(Mh**2, mH**2, mH**2)
        ) / 2.0
        resb += +(
            -(lam5 * (mA**2 - mH**2) * (Mh**2 + MZ**2 - S))
            - (lam3 + lam4) * MZ**2 * (Mh**2 - MZ**2 + S)
        ) * B0(MZ**2, mA**2, mH**2)
        resb += (
            (-lam3 - lam4) * (Mh**2 + MZ**2 - S) * S
            - lam5 * (mA**2 - mH**2) * (Mh**2 - MZ**2 + S)
        ) * B0(S, mA**2, mH**2)
        resb += (
            (lam3 + lam4 - lam5)
            * (
                mA**4 * Mh**2
                + mH**2 * Mh**4
                + Mh**2 * (mH**2 - MZ**2) * (mH**2 - S)
                + mA**2 * ((MZ**2 - S) ** 2 - Mh**2 * (2 * mH**2 + MZ**2 + S))
            )
            * C0(Mh**2, MZ**2, S, mA**2, mA**2, mH**2)
        )
        resb += (
            (lam3 + lam4 + lam5)
            * (
                mA**4 * Mh**2
                + Mh**2 * (mH**2 - MZ**2) * (mH**2 - S)
                + mA**2 * Mh**2 * (-2 * mH**2 + Mh**2 - MZ**2 - S)
                + mH**2 * (MZ**2 - S) ** 2
            )
            * C0(S, Mh**2, MZ**2, mA**2, mH**2, mH**2)
        )
        resb += (
            lam3
            * (-((MZ**2 - S) ** 2) + Mh**2 * (MZ**2 + S))
            * B0(Mh**2, mHp**2, mHp**2)
            * np.cos(2 * w) ** 2
            + lam3
            * MZ**2
            * (-(Mh**2) + MZ**2 - S)
            * B0(MZ**2, mHp**2, mHp**2)
            * np.cos(2 * w) ** 2
        )
        resb -= lam3 * (Mh**2 + MZ**2 - S) * S * B0(S, mHp**2, mHp**2) * np.cos(2 * w) ** 2
        resb += (
            2
            * lam3
            * (
                Mh**4 * mHp**2
                + mHp**2 * (MZ**2 - S) ** 2
                + Mh**2 * (MZ**2 * S - 2 * mHp**2 * (MZ**2 + S))
            )
            * C0(Mh**2, MZ**2, S, mHp**2, mHp**2, mHp**2)
            * np.cos(2 * w) ** 2
        )
        #
        resc = (
            (1 / np.sin(w)) ** 2
            * (
                3
                * mHp**2
                * A0(mH**2)
                * (
                    mA**2
                    - mH**2
                    + 8 * MW**2
                    - 4 * (mA**2 + mH**2 - 2 * mHp**2 + 2 * MW**2) * np.cos(2 * w)
                    - 5 * (mA**2 - mH**2) * np.cos(4 * w)
                )
                + 3
                * mHp**2
                * A0(mA**2)
                * (
                    -(mA**2)
                    + mH**2
                    + 8 * MW**2
                    - 4 * (mA**2 + mH**2 - 2 * mHp**2 + 2 * MW**2) * np.cos(2 * w)
                    + 5 * (mA**2 - mH**2) * np.cos(4 * w)
                )
                + 4
                * (
                    3
                    * A0(mHp**2)
                    * (
                        (
                            2 * mA**2 * mHp**2
                            + 2 * mH**2 * mHp**2
                            - 4 * mHp**4
                            - mHp**2 * MW**2
                            - 4 * MW**4
                        )
                        * np.cos(2 * w)
                        + MW**2
                        * (
                            2 * mHp**2
                            + 3 * MW**2
                            + (2 * mHp**2 + MW**2) * np.cos(4 * w)
                            - 3 * mHp**2 * np.cos(6 * w)
                        )
                    )
                    - 4
                    * mHp**2
                    * MW**2
                    * (
                        3 * mA**2
                        + 3 * mH**2
                        + 9 * mHp**2
                        + 5 * MW**2
                        + (12 * mHp**2 - 5 * MW**2) * np.cos(2 * w)
                        + 9 * mHp**2 * np.cos(4 * w)
                    )
                    * np.sin(w) ** 2
                )
            )
        ) / (144.0 * mHp**2 * MW**2)
        resc += (
            (mA**4 + (mHp**2 - MW**2) ** 2 - 2 * mA**2 * (mHp**2 + MW**2))
            * B0(MW**2, mA**2, mHp**2)
            * np.cos(2 * w)
            * (1 / np.sin(w)) ** 2
        ) / (6.0 * MW**2)
        resc += (
            (mH**4 + (mHp**2 - MW**2) ** 2 - 2 * mH**2 * (mHp**2 + MW**2))
            * B0(MW**2, mH**2, mHp**2)
            * np.cos(2 * w)
            * (1 / np.sin(w)) ** 2
        ) / (6.0 * MW**2)
        resc += (
            B0(MZ**2, mHp**2, mHp**2)
            * np.cos(2 * w) ** 2
            * (-2 * mHp**2 - MW**2 + 6 * mHp**2 * np.cos(2 * w))
            * (1 / np.sin(w)) ** 2
        ) / 6.0
        resc -= (
            B0(MZ**2, mA**2, mH**2)
            * (
                -(mA**4)
                + 2 * mA**2 * mH**2
                - mH**4
                + 8 * mA**2 * MW**2
                + 8 * mH**2 * MW**2
                + 8 * MW**4
                + 4
                * (mA**4 + mH**4 - 6 * mH**2 * MW**2 - 2 * mA**2 * (mH**2 + 3 * MW**2))
                * np.cos(2 * w)
                + 5 * (mA**2 - mH**2) ** 2 * np.cos(4 * w)
            )
            * (1 / np.sin(w)) ** 2
        ) / (48.0 * MW**2)
        resc -= (
            MW**2
            * dB0(MZ**2, mHp**2, mHp**2)
            * np.cos(2 * w) ** 2
            * (1 / np.cos(w)) ** 2
            * (-4 * mHp**2 + MZ**2)
        ) / 3.0
        resc += (
            dB0(MZ**2, mA**2, mH**2)
            * (-((mA**2 - mH**2) ** 2) + 2 * (mA**2 + mH**2) * MZ**2 - MZ**4)
        ) / 3.0
        return np.real(res + resb / denom + resc / vev**2) / (16 * np.pi**2)