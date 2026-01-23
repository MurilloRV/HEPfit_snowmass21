import numpy as np
from abc import ABC, abstractmethod
from pyCollier import db0, b0, c0, a0
dB0 = np.vectorize(db0)
B0 = np.vectorize(b0)
C0 = np.vectorize(c0)
A0 = np.vectorize(a0)

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation, FuncAnimation
from matplotlib.backends.backend_pdf import PdfPages
import copy, subprocess

vev = 246.
Mh = 125
MZ = 91.1876
MW = 80.379
cw = MW/MZ
sw = np.sqrt(1-cw**2)
gL = 2*MW/vev
gy = np.sqrt(4*MZ**2/vev**2 - gL**2)
hbar = 1 / (16 * np.pi**2)

mtop = 172.5  # GeV
Qren = mtop  # Renormalization scale for loop calculations

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

    def get_kappa_lambda_SMEFT_match(self, lamNP_match=None):
        WCs = self.get_coefficients(lamNP_match=lamNP_match)

        # Coefficients already include the 1/lambda_NP^2 factor
        delta_kappa_lambda = (vev**2) * (
            - 2 * vev**2 / Mh**2 * WCs["CH"]
            + 3 * (WCs["CHbox"] - 1/4 * WCs["CHD"])
        )
        return self.kappa_lambda_SM + delta_kappa_lambda

    @property
    def kappa_lambda_SM(self):
        mtop_temp = 172.5  # GeV
        vev_temp = 246.22  # GeV
        mH_temp = 125.1  # GeV
        pi = 3.141592
        return 1 -48*mtop_temp**4/(16*pi**2*vev_temp**3)/(3*mH_temp**2/vev_temp)

    def get_ZtoZH_SMEFT_match(self, sqrts=0., lamNP_match=None):
        # From Henning

        WCs = self.get_coefficients(lamNP_match=lamNP_match)

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


    # def get_ZtoZH_Z2SSM(self, sqrts=0, lamNP_match=None):
    #     S = sqrts**2
    #     kappalam 
    #     prediags = 3/2 - (3*(2*Mh**4 + (MZ**2 - S)**2 - Mh**2*(3*MZ**2 + S))*B0(Mh**2,Mh**2,Mh**2))/(2.*(Mh**4 + (MZ**2 - S)**2 - 2*Mh**2*(MZ**2 + S))) + (3*Mh**2*(Mh**2 - MZ**2 - S)*B0(MZ**2,Mh**2,MZ**2))/(2.*(Mh**4 + (MZ**2 - S)**2 - 2*Mh**2*(MZ**2 + S))) + (3*(Mh**4 - 2*Mh**2*MZ**2 + (MZ**2 - S)**2)*B0(S,Mh**2,MZ**2))/(2.*(Mh**4 + (MZ**2 - S)**2 - 2*Mh**2*(MZ**2 + S))) - 6*MZ**2*C0(Mh**2,MZ**2,S,Mh**2,Mh**2,MZ**2) + (3*Mh**2*(Mh**4 + (MZ**2 - S)**2 - Mh**2*(2*MZ**2 + S))*C0(S,Mh**2,MZ**2,MZ**2,Mh**2,Mh**2))/(Mh**4 + (MZ**2 - S)**2 - 2*Mh**2*(MZ**2 + S))
    #     return np.real((kappalam-1)*Mh**2/(16*np.pi**2*vev**2)*prediags)

    
    def plot_higgs_potential_SMEFT(
        self,
        figsize = (4, 3.5),
        phi_range = (-1.1*vev, 1.1*vev),
        lamNP_match=None,
        animation=False,
        plot_dir=".",
        y_range=None,
    ):

        WCs = self.get_coefficients(lamNP_match=lamNP_match)
        CH_values = WCs["CH"]
        # CHbox_values = WCs["CHbox"]
        # CHD_values = WCs["CHD"]
        kappa_lambda_values = self.get_kappa_lambda_SMEFT_match(lamNP_match=lamNP_match)

        phi = np.linspace(*phi_range, 200)
        mu2_SM = Mh**2 / 2
        lam_SM = Mh**2 / (2 * vev**2)
        V_phi_SM = -mu2_SM * phi**2 + lam_SM * phi**4

        fig, ax = plt.subplots(1,1,figsize=figsize)

        # create a proxy artist for the SMEFT curves so it appears in the legend
        proxy_smeft = ax.plot([], [], color="red", linestyle="--", label="SMEFT Potential")[0]
        ax.plot([], [], label="SM Potential", color="blue")
        ax.plot([], [], linestyle=':', label=r'$\pm\nu/\sqrt{2}$', color='green')
        
        ax.set_xlabel(r"Higgs Field Value $|\phi_0|$ [GeV]")
        ax.set_ylabel(r"Higgs Potential $V(\phi_0)$ [GeV$^4$]")
        ax.set_title("Higgs Potential in SM and SMEFT", fontsize=10)
        ax.legend(fontsize=8)
        ax.grid()

        fig_template = copy.deepcopy(fig)

        artists = []

        for CH, kappa_lambda in zip(np.atleast_1d(CH_values), np.atleast_1d(kappa_lambda_values)):

            mu2 = Mh**2 / 2 + (3/4) * CH * vev**4
            lam = Mh**2 / (2 * vev**2) + 3 * CH * vev**2 / 2
            V_phi_SMEFT = -mu2 * phi**2 + lam * phi**4 - CH * phi**6 # + 0.25 * CHD * vev**2 * phi**4 - CHbox * vev**2 * phi**4

            line_sm = ax.plot(phi, V_phi_SM, color="blue")  # static background
            line = ax.plot(phi, V_phi_SMEFT, color="red", linestyle="--")
            text = ax.text(
                0.5, 0.7,
                rf"$\kappa_\lambda={kappa_lambda:.3g}$" + "\n" +
                rf"$C_H\cdot\frac{{\nu^2}}{{\Lambda_{{NP}}^2}}={CH*vev**2:.3g}$",
                transform=ax.transAxes,
                fontsize=8,
                va='top',
                ha='center',
                bbox=dict(boxstyle="round", fc="white", ec="0.5", alpha=1.0, pad=0.8),
                clip_on=False,
                zorder=10,
            )
            line.append(text)
            line.append(line_sm[0])
            vev1 = ax.axvline(+vev/np.sqrt(2), color='green', linestyle=':')
            vev2 = ax.axvline(-vev/np.sqrt(2), color='green', linestyle=':')
            line.append(vev1)
            line.append(vev2)
            artists.append(line)
            

        with PdfPages(f"{plot_dir}/Higgs_potential_frames.pdf") as pdf:
            for i, (CH, kappa_lambda) in enumerate(zip(np.atleast_1d(CH_values), np.atleast_1d(kappa_lambda_values))):

                fig_copy = copy.deepcopy(fig_template)
                ax_copy = fig_copy.gca()
                fig_copy.tight_layout()
                    
                mu2 = Mh**2 / 2 + (3/4) * CH * vev**4
                lam = Mh**2 / (2 * vev**2) + 3 * CH * vev**2 / 2
                V_phi_SMEFT = -mu2 * phi**2 + lam * phi**4 - CH * phi**6 # + 0.25 * CHD * vev**2 * phi**4 - CHbox * vev**2 * phi**4

                line_sm = ax_copy.plot(phi, V_phi_SM, color="blue")  # static background
                line = ax_copy.plot(phi, V_phi_SMEFT, color="red", linestyle="--")
                text = ax_copy.text(
                    0.5, 0.7,
                    rf"$\kappa_\lambda={kappa_lambda:.3g}$" + "\n" +
                    rf"$C_H\cdot\frac{{\nu^2}}{{\Lambda_{{NP}}^2}}={CH*vev**2:.3g}$",
                    transform=ax_copy.transAxes,
                    fontsize=8,
                    va='top',
                    ha='center',
                    bbox=dict(boxstyle="round", fc="white", ec="0.5", alpha=1.0, pad=0.8),
                    clip_on=False,
                    zorder=10,
                )
                vev1 = ax_copy.axvline(+vev/np.sqrt(2), color='green', linestyle=':')
                vev2 = ax_copy.axvline(-vev/np.sqrt(2), color='green', linestyle=':')

                if y_range is not None:
                    ax_copy.set_ylim(*y_range)
                pdf.savefig(fig_copy)

                subprocess.run(["mkdir", "-p", f"{plot_dir}/Higgs_potential_frames"])
                fig_copy.savefig(f"{plot_dir}/Higgs_potential_frames/frame_{i}.pdf")


        print(artists)
        ani = ArtistAnimation(fig=fig, artists=artists, interval=400)
        fig.tight_layout()
        if y_range is not None:
            ax.set_ylim(*y_range)

        return fig, ax, ani, artists

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

    @staticmethod
    def CH(muS, lamS, lamSH, mS, lamNP_match):
        # Matching to conventions in [1811.08878]
        kappa = lamSH
        lamphi = 4*3*lamS
        return - 1 / 12 * hbar * kappa**3 / lamNP_match**2

    @staticmethod
    def CHbox(muS, lamS, lamSH, mS, lamNP_match):
        # Matching to conventions in [1811.08878]
        kappa = lamSH
        lamphi = 4*3*lamS
        return - 1 / 24 * hbar * kappa**2 / lamNP_match**2

    def get_coefficients(self, lamNP_match=None, lamNP=None, dimensionless=False):
        if lamNP is None:
            lamNP = self.muS
        if lamNP_match is None:
            lamNP_match = self.muS

        CH_val    = Z2SSM.CH    (self.muS, self.lamS, self.lamSH, self.mS, lamNP_match)
        CHbox_val = Z2SSM.CHbox (self.muS, self.lamS, self.lamSH, self.mS, lamNP_match)

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
    
    @staticmethod
    def f_loop(x, Qren=Qren):
            return (1/4.) * x**2 * (np.log(x/Qren**2) - 3./2)
    
    @staticmethod
    def mt2(h, mt=mtop):
        return mt**2 * ( 1 + (h/vev) )**2
    
    def mS2(self, h, S, muS=None, lamSH=None, lamS=None):
        if muS   is None:  muS   = self.muS
        if lamSH is None:  lamSH = self.lamSH
        if lamS  is None:  lamS  = self.lamS
        return muS**2 + 6*lamS * S**2 + (1/2.)*lamSH * (h+vev)**2


    def V_h_S_func(self, phi, S, mu2=-Mh**2/2, muS=None, lam_H=Mh**2/(vev**2), lamSH=None, lamS=None, loop_order="0L"):
        if muS   is None:  muS   = self.muS
        if lamSH is None:  lamSH = self.lamSH
        if lamS  is None:  lamS  = self.lamS

        V_0L = mu2 * phi**2 + (1/2.)*muS**2 * S**2 + (1/2.)*lam_H * phi**4 + (1/2.)*lamSH * phi**2 * S**2 + (1/2.)*lamS * S**4 

        h = np.sqrt(2) * phi - vev
        V_1L = 1/(16*np.pi**2) * ( -12*Z2SSM.f_loop(Z2SSM.mt2(h)) + Z2SSM.f_loop(self.mS2(h, S, muS, lamSH, lamS)) )

        if loop_order == "0L":
            return V_0L
        elif loop_order == "1L":
            return V_0L + V_1L
        else:
            raise ValueError("loop_order must be '0L' or '1L'.")


    def plot_higgs_potential_Z2SSM(
        self,
        figsize = (4, 3.5),
        phi_range = (-1.1*vev, 1.1*vev),
        S_range = (-500., 500.),
        V_range = None,
        animation_rotate=False,
        plot_dir=".",
        n_frames=10,
        interval=200,
        plot_surface_kwargs={},
        legend_kwargs={"fontsize": 8},
        x_contour=None,
        y_contour=None,
        z_contour=None,
        plot_V_minima=None,
        loop_order=["0L"],
        loop_order_txt="0L",
        x_label_args={"fontsize": 10},
        y_label_args={"fontsize": 10},
        z_label_args={"fontsize": 10},
        plot_h=False,
    ):

        if plot_h:
            x_label_args["xlabel"] = r"$h$ [GeV]"
            y_label_args["ylabel"] = r"$S$ [GeV]"
            z_label_args["zlabel"] = rf"$V(h, S)/\nu^4$"
        else:
            x_label_args["xlabel"] = r"$\Phi_0$ [GeV]"
            y_label_args["ylabel"] = r"$S$ [GeV]"
            z_label_args["zlabel"] = rf"$V(\Phi_0, S)/\nu^4$"
        phi = np.linspace(*phi_range, 200)
        S = np.linspace(*S_range, 200)

        phi, S = np.meshgrid(phi, S)

        # Following conventions in [1911.11507]
        muS   = self.muS
        lamS  = self.lamS
        lamSH = self.lamSH
        mS    = self.mS
        kappa_lambda = self.get_kappa_lambda_SMEFT_match(lamNP_match=self.mS)


        fig = plt.figure(figsize=figsize, constrained_layout=True)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel(**x_label_args)
        ax.set_ylabel(**y_label_args)
        ax.set_zlabel(**z_label_args)
        ax.set_title("Z2SSM Higgs Potential (tree-level)", fontsize=10)
        if x_contour is not None or y_contour is not None or z_contour is not None:
            ax.plot([], [], label="Contours at 0", color=x_contour["colors"], lw=x_contour["linewidths"], alpha=x_contour["alpha"])
        if plot_V_minima is not None:
            ax.scatter([], [], label="$V(\phi_0, S)$ Minima", **plot_V_minima)
        ax.legend(**legend_kwargs)
        ax.grid()

        def clear_ax(ax):
            for c in list(ax.collections):
                c.remove()
            for a in list(ax.artists):
                a.remove()

        def plot_potential(muS, lamSH, lamS, kappa_lambda, mS, update=False):

            if update: clear_ax(ax)

            surface_plots = []
            contour_plots = []
            V_min_plots = []
            for order in loop_order:
                V_phi_S = self.V_h_S_func(phi, S, muS=muS, lamSH=lamSH, lamS=lamS, loop_order=order) / vev**4
                surface_plot = ax.plot_surface(phi, S, V_phi_S, **plot_surface_kwargs[order])

                if x_contour is not None:
                    x_contours_plot = ax.contour(phi, S, V_phi_S, zdir='x', offset=ax.get_xlim()[0], **x_contour)
                else:
                    x_contours_plot = None

                if y_contour is not None:
                    y_contours_plot = ax.contour(phi, S, V_phi_S, zdir='y', offset=ax.get_ylim()[1], **y_contour)
                else:
                    y_contours_plot = None
                    
                if z_contour is not None:
                    z_contours_plot = ax.contour(phi, S, V_phi_S, zdir='z', offset=ax.get_zlim()[0], **z_contour)
                else:
                    z_contours_plot = None

                if plot_V_minima is not None:
                    V_min = self.V_h_S_func(-vev/np.sqrt(2), 0, muS=muS, lamSH=lamSH, lamS=lamS, loop_order=order) / vev**4
                    V_min_plot = ax.scatter([-vev/np.sqrt(2), +vev/np.sqrt(2)], [0,0], [V_min, V_min], **plot_V_minima)
                else:
                    V_min_plot = None

                surface_plots.append(surface_plot)
                contour_plots.append((x_contours_plot, y_contours_plot, z_contours_plot))
                V_min_plots.append(V_min_plot)

            ax.set_title(
                f"Z2SSM Higgs Potential ({loop_order_txt})\n"
                rf"$m_S={mS:.3g}$ GeV, "
                rf"$\mu_S={muS:.3g}$ GeV, "
                rf"$\lambda_{{SH}}={lamSH:.3g}$, "
                rf"$\lambda_S={lamS:.3g}$, "
                rf"$\kappa_\lambda={kappa_lambda:.3g}$",
                fontsize=10
            )

            if V_range is not None:
                ax.set_zlim(*V_range)
            else:
                zmin = np.nanmin(V_phi_S)
                zmax = np.nanmax(V_phi_S)

                # add a margin (e.g. 5%)
                margin = 0.05 * (zmax - zmin if zmax > zmin else 1.0)
                ax.set_zlim(zmin - margin, zmax + margin)

            return surface_plots, contour_plots, V_min_plots

        if np.ndim(muS)!=0:
            def scan_parameter_points(point):
                return plot_potential(muS[point], lamSH[point], lamS[point], kappa_lambda[point], mS[point], update=True)

            anim = FuncAnimation(fig, scan_parameter_points, frames=len(muS), interval=interval, blit=False)

            with PdfPages(f"{plot_dir}/Higgs_potential_{loop_order_txt}_Z2SSM_parameter_points_frames.pdf") as pdf:
                for frame, (muS_point, lamSH_point, lamS_point, kappa_lambda_point, mS_point) in enumerate(zip(muS, lamSH, lamS, kappa_lambda, mS)):
                    plot_potential(muS_point, lamSH_point, lamS_point, kappa_lambda_point, mS_point, update=True)
                    if V_range is not None:
                        ax.set_zlim(*V_range)
                    else:
                        ax.relim()           # recompute data limits from artists
                        ax.autoscale_view()  # update axis limits
                    pdf.savefig(fig)  
                    subprocess.run(["mkdir", "-p", f"{plot_dir}/Higgs_potential_{loop_order_txt}_Z2SSM_parameter_points_frames"])
                    fig.savefig(f"{plot_dir}/Higgs_potential_{loop_order_txt}_Z2SSM_parameter_points_frames/frame_{frame}.pdf")
                    
            return fig, ax, anim
        else:
            plot_potential(muS, lamSH, lamS, kappa_lambda[0], mS)


        if animation_rotate:
            if np.ndim(muS)!=0:
                raise ValueError("The 'animation_rotate' option is only valid for a single parameter point.")
            
            def rotate(angle):
                ax.view_init(elev=30, azim=angle*360/n_frames)

            anim = FuncAnimation(fig, rotate, frames=n_frames+1, interval=interval)

            with PdfPages(f"{plot_dir}/Higgs_potential_{loop_order_txt}_Z2SSM_rotate_frames.pdf") as pdf:
                for frame in range(n_frames):
                    ax.view_init(elev=30, azim=frame*360/n_frames)
                    pdf.savefig(fig)  

                    subprocess.run(["mkdir", "-p", f"{plot_dir}/Higgs_potential_{loop_order_txt}_Z2SSM_rotate_frames"])
                    fig.savefig(f"{plot_dir}/Higgs_potential_{loop_order_txt}_Z2SSM_rotate_frames/frame_{frame}.pdf")

                return fig, ax, anim

        else: 
            return fig, ax, None
        


    def plot_higgs_potential_Z2SSM_projection(
        self,
        figsize = (4, 3.5),
        phi_range = (-1.1*vev, 1.1*vev),
        V_range = None,
        plot_dir=".",
        interval=200,
        plot_kwargs=[{}],
        legend_kwargs={"fontsize": 10},
        loop_order=["0L"],
        loop_order_txt="0L",
        x_label_args={"fontsize": 12},
        y_label_args={"fontsize": 12},
        plot_h=False,
        plot_1L_minima=False,
    ):

        if plot_h:
            x_label_args["xlabel"] = r"$h$ [GeV]"
            y_label_args["ylabel"] = rf"$V(h, S)/\nu^4$"
        else:
            x_label_args["xlabel"] = r"$\Phi_0$ [GeV]"
            y_label_args["ylabel"] = rf"$V(\Phi_0, S)/\nu^4$"

        phi = np.linspace(*phi_range, 200)
        S = np.zeros_like(phi)

        # Following conventions in [1911.11507]
        muS   = self.muS
        lamS  = self.lamS
        lamSH = self.lamSH
        mS    = self.mS
        kappa_lambda = self.get_kappa_lambda_SMEFT_match(lamNP_match=self.mS)

        fig, ax = plt.subplots(1,1,figsize=figsize)
        ax.set_xlabel(**x_label_args)
        ax.set_ylabel(**y_label_args)
        for order in loop_order:
            ax.plot([], [], label=f'Z2SSM potential ({order})', **plot_kwargs[order])

        if "0L" in loop_order:
            ax.plot([], [], linestyle=':', label=r'$V_{\mathrm{0L}}$ Minima $(\pm\nu/\sqrt{2})$', color=plot_kwargs["0L"].get("color", "green"))
        else:
            ax.plot([], [], linestyle=':', label=r'$\pm\nu/\sqrt{2}$', color="green")
        if plot_1L_minima:
            ax.plot([], [], linestyle=':', label=r'$V_{\mathrm{1L}}$ Minima', color=plot_kwargs["1L"].get("color", "green"))


        ax.legend(**legend_kwargs)
        ax.grid(alpha=0.3)
        ax.axhline(0, color='black', lw=1, alpha=0.5)
        ax.axvline(0, color='black', lw=1, alpha=0.5)

        def clear_ax(ax):
            for c in list(ax.collections):
                c.remove()
            for a in list(ax.artists):
                a.remove()
            for a in list(ax.lines):
                a.remove()


        def plot_potential(muS, lamSH, lamS, kappa_lambda, mS, update=False):

            if update: clear_ax(ax)

            plots = []
            V_phi_S = {}
            for order in loop_order:
                V_phi_S[order] = self.V_h_S_func(phi, S, muS=muS, lamSH=lamSH, lamS=lamS, loop_order=order) / vev**4
                plot = ax.plot(phi, V_phi_S[order], **plot_kwargs[order])
                plots.append(plot)

            if "0L" in loop_order:
                vev1 = ax.axvline(+vev/np.sqrt(2), color=plot_kwargs["0L"].get("color", "green"), linestyle=':', lw=2)
                vev2 = ax.axvline(-vev/np.sqrt(2), color=plot_kwargs["0L"].get("color", "green"), linestyle=':', lw=2)
            else:
                vev1 = ax.axvline(+vev/np.sqrt(2), color='green', linestyle=':', lw=2)
                vev2 = ax.axvline(-vev/np.sqrt(2), color='green', linestyle=':', lw=2)
            plots.append(vev1)
            plots.append(vev2)

            if plot_1L_minima:
                min_arg = np.argmin(V_phi_S["1L"])
                phi_min = phi[min_arg]
                min1 = ax.axvline(+phi_min, color='red', linestyle=':', lw=2)
                min2 = ax.axvline(-phi_min, color='red', linestyle=':', lw=2)
                plots.append(min1)
                plots.append(min2)

            ax.set_title(
                "Z2SSM Higgs Potential\n"
                rf"$m_S={mS:.3g}$ GeV, "
                rf"$\mu_S={muS:.3g}$ GeV, "
                rf"$\lambda_{{SH}}={lamSH:.3g}$, "
                rf"$\lambda_S={lamS:.3g}$, "
                rf"$\kappa_\lambda={kappa_lambda:.3g}$",
                fontsize=10
            )

            if V_range is not None:
                ax.set_ylim(*V_range)
            else:
                ax.relim()           # recompute data limits from artists
                ax.autoscale_view()  # update axis limits

            fig.tight_layout()

            return plots

        if np.ndim(muS)!=0:
            def scan_parameter_points(point):
                return plot_potential(muS[point], lamSH[point], lamS[point], kappa_lambda[point], mS[point], update=True)

            anim = FuncAnimation(fig, scan_parameter_points, frames=len(muS), interval=interval, blit=False)

            with PdfPages(f"{plot_dir}/Higgs_potential_projection_{loop_order_txt}_Z2SSM_parameter_points_frames.pdf") as pdf:
                for frame, (muS_point, lamSH_point, lamS_point, kappa_lambda_point, mS_point) in enumerate(zip(muS, lamSH, lamS, kappa_lambda, mS)):
                    plot_potential(muS_point, lamSH_point, lamS_point, kappa_lambda_point, mS_point, update=True)
                    if V_range is not None:
                        ax.set_ylim(*V_range)
                    pdf.savefig(fig)  
                    subprocess.run(["mkdir", "-p", f"{plot_dir}/Higgs_potential_projection_{loop_order_txt}_Z2SSM_parameter_points_frames"])
                    fig.savefig(f"{plot_dir}/Higgs_potential_projection_{loop_order_txt}_Z2SSM_parameter_points_frames/frame_{frame}.pdf")
                    
            return fig, ax, anim
        else:
            plot_potential(muS, lamSH, lamS, kappa_lambda[0], mS)
            return fig, ax, None
        


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
    def CH(l1, l3, l4, l5, mu2, lamNP_match):
        return (
            -1 / 3 * hbar * l3**3 / lamNP_match**2
            - 1 / 2 * hbar * l4 * l3**2 / lamNP_match**2
            + 1 / 6 * hbar * l1 * l4**2 / lamNP_match**2
            - 1 / 2 * hbar * l3 * l4**2 / lamNP_match**2
            - 1 / 6 * hbar * l4**3 / lamNP_match**2
            + 1 / 6 * hbar * l1 * l5**2 / lamNP_match**2
            - 1 / 2 * hbar * l3 * l5**2 / lamNP_match**2
            - 1 / 2 * hbar * l4 * l5**2 / lamNP_match**2
        )
    
    @staticmethod
    def CHbox(l1, l3, l4, l5, mu2, lamNP_match):
        return (
            -1 / 6 * hbar * l3**2 / lamNP_match**2
            - 1 / 6 * hbar * l3 * l4 / lamNP_match**2
            + 1 / 12 * hbar * l5**2 / lamNP_match**2
        )

    @staticmethod
    def CHD(l1, l3, l4, l5, mu2, lamNP_match):
        return (
            - 1 / 6 * hbar * l4**2 / lamNP_match**2
            + 1 / 6 * hbar * l5**2 / lamNP_match**2
        )

    @staticmethod
    def CHW(l1, l3, l4, l5, mu2, lamNP_match):
        return 1 / 48 * hbar * gL**2 * (2 * l3 + l4) / lamNP_match**2

    @staticmethod
    def CHB(l1, l3, l4, l5, mu2, lamNP_match):
        return 1 / 48 * hbar * gy**2 * (2 * l3 + l4) / lamNP_match**2
    
    @staticmethod
    def CHWB(l1, l3, l4, l5, mu2, lamNP_match):
        return 1 / 24 * hbar * gL * gy * l4 / lamNP_match**2

    def get_coefficients(self, lamNP_match=None, lamNP=None, dimensionless=False):
        if lamNP is None:
            lamNP = self.mu2
        if lamNP_match is None:
            lamNP_match = self.mu2

        CH_val     = IDM.CH    (self.l1, self.l3, self.l4, self.l5, self.mu2, lamNP_match)
        CHbox_val  = IDM.CHbox (self.l1, self.l3, self.l4, self.l5, self.mu2, lamNP_match)
        CHD_val    = IDM.CHD   (self.l1, self.l3, self.l4, self.l5, self.mu2, lamNP_match)
        CHW_val    = IDM.CHW   (self.l1, self.l3, self.l4, self.l5, self.mu2, lamNP_match)
        CHB_val    = IDM.CHB   (self.l1, self.l3, self.l4, self.l5, self.mu2, lamNP_match)
        CHWB_val   = IDM.CHWB  (self.l1, self.l3, self.l4, self.l5, self.mu2, lamNP_match)

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


    def get_ZtoZH_IDM(self, sqrts=0.):
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