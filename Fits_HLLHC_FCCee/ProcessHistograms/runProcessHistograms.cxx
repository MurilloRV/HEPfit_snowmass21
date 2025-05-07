// ***************************************************************
// This file was created using the bat-project script
// for project ProcessHistograms.
// bat-project is part of Bayesian Analysis Toolkit (BAT).
// BAT can be downloaded from http://mpp.mpg.de/bat
// ***************************************************************

#include <BAT/BCLog.h>

#include <BAT/BCParameter.h>
#include <BAT/BCMath.h>
#include <BAT/BCGaussianPrior.h>
#include <BAT/BCTF1Prior.h>

#include <TF1.h>
#include <TH1D.h>
#include <TTree.h>
#include <TROOT.h>
#include <TPaveText.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <fstream>
#include <stdexcept>
#include <iomanip>
#include <limits>
#include <BAT/BCModel.h>
#include <BAT/BCH1D.h>
#include <BAT/BCH2D.h>
#include <TFile.h>
#include <TPrincipal.h>
#include <TColor.h>
#include <map>

#include "ProcessHistograms.h"


int main()
{
    int cindex=0;

    int nBins1D = 100;
    int nBins2D = 100;
    // int gIdx = TColor::GetFreeColorIndex();
    // int rIdx = TColor::GetFreeColorIndex() + 1;

    // TColor * HEPfit_green = new TColor(gIdx, 0.0, 0.56, 0.57, "HEPfit_green");
    // TColor * HEPfit_red = new TColor(rIdx, 0.57, 0.01, 0.00, "HEPfit_red");
    int nSmooth = 0;
    int histogram2Dtype = 1001;
    bool noLegend = false;
    bool printLogo = true;
    // bool printLogo = false;
    bool drawGlobalModes = false;

    // std::string model_spec = "fits";
    // std::string model_spec = "fits_long";
    std::string model_spec = "fits_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_realistic_HL_LHC_full";
    // std::string model_spec = "fits_realistic_HL_LHC_all_EW_mods_long";
    // std::string model_spec = "fits_realistic_HL_LHC_no_1L_BSM_sqrt_s_long";


    // std::string working_dir = "../large_kappa_lambda_fits_noLoopH3d6Quad/";
    // std::string working_dir = "../large_kappa_lambda_fits_HalfmueeZH/";
    std::string working_dir = "../large_kappa_lambda_fits_kappa_framework/";
    // std::string working_dir = "../large_kappa_lambda_fits/";


    std::vector<std::string> scenarios;
    std::vector<std::string> plot_titles;

    std::vector<float> KappaLambdas;

    bool drawKLambdaErrorProjection = false;
    bool setRangeKLambda = false;

    bool only_relevant_plots = true;


    const int n_scenarios_base = 1;
    const int nlambdas = 16;
    const int n_scenarios = n_scenarios_base * (nlambdas);
    const std::string base_paths[] = {
        "FCCee240_FCCee365_noHLLHClambda",
        // "FCCee240_FCCee365_HLLHClambda",
    };

    // const std::string base_titles[] = {
    //     "IDM central values, FCC-ee_{240}",
    //     "IDM central values, FCC-ee_{240+365}",
    //     "IDM central values, FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    // };

    const std::string base_titles[] = {
        "C_{H} fits, FCC-ee_{240+365}",
        // "C_{H} fits, FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    };


    for (int lmbd = -5; lmbd < 11; ++lmbd) {
        for (int i=0; i<n_scenarios_base; ++i) {
            scenarios.push_back("Lambda" + std::to_string(lmbd) + "_" + base_paths[i]);
            plot_titles.push_back(base_titles[i]);
            KappaLambdas.push_back(lmbd);
        }
    }

    // for (int i=0; i<n_scenarios; ++i) {
    //     std::cout << scenarios[i] << std::endl;
    //     std::cout << plot_titles[i] << std::endl;
    //     std::cout << KappaLambdas[i] << std::endl;
    // }


    ProcessHistograms Modify_Histos = ProcessHistograms(cindex,
                                                        printLogo,
                                                        nSmooth,
                                                        histogram2Dtype,
                                                        noLegend,
                                                        nBins1D,
                                                        nBins2D,
                                                        drawGlobalModes,
                                                        setRangeKLambda,
                                                        drawKLambdaErrorProjection,
                                                        only_relevant_plots
                                                        );

    // const int n_scenarios = 1;
    for (int i=0; i<n_scenarios; i++)
    {
        std::string results_dir = working_dir + scenarios[i] + "/results_" + model_spec + "/";
        std::string obs_dir = results_dir + "Observables/";
        std::string root_filepath = results_dir + "MCout.root";
        std::cout << root_filepath << std::endl;

        std::string stats_filepath = obs_dir + "Statistics.txt";

        Modify_Histos.Get_Global_Modes(stats_filepath);
        // Modify_Histos.Print_1D_Histos(
        //     root_filepath, 
        //     obs_dir, 
        //     plot_titles[i], 
        //     KappaLambdas[i],
        //     KappaLambdas_error_low[i],
        //     KappaLambdas_error_high[i],
        //     KappaLambdas_range_low[i],
        //     KappaLambdas_range_high[i],
        //     BP_names[i]
        // );

        Modify_Histos.Print_1D_Histos(
            root_filepath, 
            obs_dir, 
            plot_titles[i], 
            KappaLambdas[i]
        );

    }


    // delete HEPfit_red;
    // delete HEPfit_green;
    // HEPfit_red = NULL;
    // HEPfit_green = NULL;
    
    return 0;
}
