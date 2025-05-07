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
    bool printLogo = false;
    // bool printLogo = false;
    bool drawGlobalModes = false;

    // std::string model_spec = "fits";
    // std::string model_spec = "fits_realistic_HL_LHC_realistic_HL_LHC_full";
    
    // std::string model_spec = "fits_realistic_HL_LHC_realistic_HL_LHC_long";
    // std::string model_spec = "fits_realistic_HL_LHC_all_EW_mods_long";
    // std::string model_spec = "fits_realistic_HL_LHC_no_1L_BSM_sqrt_s_long";
    // std::string model_spec = "fits_realistic_HL_LHC_no_1L_BSM_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_smeft_formula_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_smeft_formula_sqrt_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_smeft_formula_external_leg_small_priors_long";
    std::string model_spec = "fits_realistic_HL_LHC_WFR_kala2_input_small_priors_long";
    // std::string model_spec = "fits_long";
    // std::string model_spec = "fits_full";
    // std::string model_spec = "fits_realistic_HL_LHC_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_no_quad_long";
    // std::string model_spec = "fits_realistic_HL_LHC_noLoopH3d6Quad_long";
    // std::string model_spec = "fits_realistic_HL_LHC_noLoopH3d6Quad_no_quad_long";
    // std::string model_spec = "fits_realistic_HL_LHC_LoopHd6noWFR_no_quad_long";
    // std::string model_spec = "fits_realistic_HL_LHC_LoopHd6noWFR_long";
    


    std::string working_dir = "../Fits_HLLHC_FCCee/different_BPs/";
    // std::string working_dir = "../Fits_HLLHC_ILC_250_350_500_1000/different_BPs/";


    std::vector<std::string> scenarios;
    std::vector<std::string> plot_titles;

    std::vector<float> KappaLambdas;
    std::vector<float> base_KappaLambdas = {
        // 4.038636858901748, // BPO_0
        // 1.2385642568656816, // BPO_1
        // 1.1209067864736006, // BPB_0
        // 1.3186016358896624, // BPB_1
        2.3867362274064843, // BPB_2
        // 2.296737570137434, // BPB_3
        3.3446699219962595, // BPB_4
        // 3.3186760761499228, // BPB_5
        4.332584967850238, // BPB_6
        // 4.324280052220163, // BPB_7
        // 5.390968560325193, // BPB_8
        // 5.289906405452073, // BPB_9
        // 6.370034303736775, // BPB_10
        // 6.270579956517072, // BPB_11
        // 7.515862276796717, // BPB_12
        // 7.466008740779396, // BPB_13
        // 8.611459058586306, // BPB_14
        // 8.459762817722257, // BPB_15
        // 9.319513844125106, // BPB_16
        // 9.888810967739037, // BPB_17
        // 11.2535829810942, // BPB_18
    }; 

    // BP_lambda1
    // std::vector<float> base_KappaLambdas = {
    //     1.1000242642433875,
    // };

    bool drawKLambdaErrorProjection = false;
    std::vector<float> KappaLambdas_error_low;
    std::vector<float> base_KappaLambdas_error_low = {
        0.4795908317769697,
        0.7513582390395568,
        1.206292483925119,
    };

    std::vector<float> KappaLambdas_error_high;
    std::vector<float> base_KappaLambdas_error_high = {
        1.3170937786156036,
        0.8707328534211176,
        0.5486815452684013,
    };

    bool setRangeKLambda = false;
    std::vector<float> KappaLambdas_range_low = {
        -1.0,
        1.0,
        -0.5,
        2.5,
        1.0,
        2.5,
    };

    std::vector<float> KappaLambdas_range_high = {
        9.0,
        5.0,
        10.5,
        6.0,
        12.0,
        7.0,
    };
    // std::vector<float> KappaLambdas_range_high;
    // std::vector<float> base_KappaLambdas_range_low = {
    //     1.0,
    //     2.8,
    //     2.8,
    // };

    // std::vector<float> KappaLambdas_range_low;
    // std::vector<float> base_KappaLambdas_range_high = {
    //     5.0,
    //     7.0,
    //     7.0,
    // };


    bool only_relevant_plots = true;

    const int n_scenarios_base = 1;

    // const int num_BPO = 2;
    const int num_BPO = 0;
    // const int num_BPB = 19;
    const int num_BPB = 3;
    // const int num_BPB = 1;

    const int n_scenarios = n_scenarios_base * (num_BPO + num_BPB);
    const std::string base_paths[] = {
        // "IDM_FCCee240",
        "IDM_FCCee240_FCCee365",
        // "IDM_FCCee240_FCCee365_HLLHClambda",
    };
    // const std::string base_paths[] = {
    //     "IDM_ILC_250_350",
    //     "IDM_ILC_250_350_500",
    // };

    // const std::string base_titles[] = {
    //     "IDM central values, FCC-ee_{240}",
    //     "IDM central values, FCC-ee_{240+365}",
    //     "IDM central values, FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    // };

    const std::string base_titles[] = {
        // "FCC-ee_{240}",
        "FCC-ee_{240} + FCC-ee_{365}",
        // "FCC-ee_{240} + FCC-ee_{365} + #kappa_{#lambda} at HL-LHC",
    };

    // const std::string base_titles[] = {
    //     "ILC_{250} + ILC_{350}",
    //     "ILC_{250} + ILC_{350} + ILC_{500}",
    // };

    // const std::string base_titles[] = {
    //     "ILC_{250+350} (P_{e^{-}} , P_{e^{+}}) = (#mp80%, #pm30%)",
    //     "ILC_{250+350+500} (P_{e^{-}} , P_{e^{+}}) = (#mp80%, #pm30%)",
    // };

    std::vector<std::string> BP_names;
    std::vector<std::string> base_BP_names = {
        "BP 1",
        "BP 2",
        "BP 3",
    };

    // BP_lambda1
    // std::vector<std::string> base_BP_names = {
    //     "BP_{#kappa_{#lambda} #approx 1}",
    // };


    // for (int bp = 0; bp < num_BPO; ++bp) {
    //     for (int i=0; i<n_scenarios_base; ++i) {
    //         // std::cout << base_paths[i] << std::endl;
    //         // std::cout << base_titles[i] << std::endl;
    //         scenarios.push_back("BPO_" + std::to_string(bp) + "/" + base_paths[i]);
    //         plot_titles.push_back(base_titles[i]);
    //         // std::cout << base_KappaLambdas[i] << std::endl;
    //         KappaLambdas.push_back(base_KappaLambdas[bp]);
    //     }
    // }

    int BPB_numbers[3] = {2, 4, 6};
    int BPB = 0;

    for (int bp = 0; bp < num_BPB; ++bp) {
        for (int i=0; i<n_scenarios_base; ++i) {
            BPB = BPB_numbers[bp];
            std::cout << base_KappaLambdas[bp] << std::endl;
            scenarios.push_back("BPB_" + std::to_string(BPB) + "/" + base_paths[i]);
            // scenarios.push_back(std::string("BP_lambda1") + "/" + base_paths[i]);
            // plot_titles.push_back("IDM BP " + std::to_string(BPB) + ", " + base_titles[i]);
            plot_titles.push_back("IDM BP " + std::to_string(bp+1) + ", " + base_titles[i]);
            // plot_titles.push_back("IDM " + base_BP_names[bp] + ", " + base_titles[i]);
            KappaLambdas.push_back(base_KappaLambdas[bp + num_BPO]);
            KappaLambdas_error_low.push_back(base_KappaLambdas_error_low[bp + num_BPO]);
            KappaLambdas_error_high.push_back(base_KappaLambdas_error_high[bp + num_BPO]);
            BP_names.push_back(base_BP_names[bp + num_BPO]);
            // KappaLambdas_range_low.push_back(base_KappaLambdas_range_low[bp + num_BPO]);
            // KappaLambdas_range_high.push_back(base_KappaLambdas_range_high[bp + num_BPO]);
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
        Modify_Histos.Print_1D_Histos(
            root_filepath, 
            obs_dir, 
            plot_titles[i], 
            KappaLambdas[i],
            KappaLambdas_error_low[i],
            KappaLambdas_error_high[i],
            KappaLambdas_range_low[i],
            KappaLambdas_range_high[i],
            BP_names[i]
        );

        // Modify_Histos.Print_1D_Histos(
        //     root_filepath, 
        //     obs_dir, 
        //     plot_titles[i], 
        //     KappaLambdas[i]
        // );

    }


    // delete HEPfit_red;
    // delete HEPfit_green;
    // HEPfit_red = NULL;
    // HEPfit_green = NULL;
    
    return 0;
}
