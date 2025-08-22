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
    // std::string model_spec = "fits_realistic_HL_LHC_smeft_formula_all_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_no_C_HG_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_smeft_formula_no_cross_no_HLLHC_Higgs_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_smeft_formula_external_leg_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_WFR_kala2_input_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_WFR_kala2_input_no_C_HG_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_WFR_kala2_input_no_HLLHC_Higgs_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_WFR_kala2_input_all_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_WFR_kala2_input_all_all_EW_mods_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_use_HEPfit_C1_values_WFR_kala2_input_all_all_EW_mods_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_use_HEPfit_C1_values_WFR_kala2_input_all_small_priors_long";
    std::string model_spec = "fits_realistic_HL_LHC_use_HEPfit_C1_values_decayrates_WFR_kala2_input_all_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_WFR_kala2_input_all_all_EW_mods_small_priors_strict";
    // std::string model_spec = "fits_realistic_HL_LHC_WFR_kala2_input_all_no_HLLHC_Higgs_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_WFR_kala2_input_all_all_EW_mods_no_HLLHC_Higgs_small_priors_long";
    // std::string model_spec = "fits_long";
    // std::string model_spec = "fits_full";
    // std::string model_spec = "fits_realistic_HL_LHC_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_no_quad_long";
    // std::string model_spec = "fits_realistic_HL_LHC_noLoopH3d6Quad_long";
    // std::string model_spec = "fits_realistic_HL_LHC_noLoopH3d6Quad_no_quad_long";
    // std::string model_spec = "fits_realistic_HL_LHC_LoopHd6noWFR_no_quad_long";
    // std::string model_spec = "fits_realistic_HL_LHC_LoopHd6noWFR_long";
    // std::string model_spec = "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_no_HLLHC_Higgs_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_all_EW_mods_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_use_new_NPs_WFR_kala2_input_all_all_EW_mods_no_HLLHC_Higgs_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_small_priors_long";
    // std::string model_spec = "fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_small_priors_strict";
    // std::string model_spec = "fits_realistic_HL_LHC_use_new_NPs_scale1.52_theoerr240_0.00107_theoerr365_0.00105_WFR_kala2_input_all_all_EW_mods_small_priors_strict";
    // std::string model_spec = "fits_realistic_HL_LHC_use_new_NPs_scale1.52_WFR_kala2_input_all_all_EW_mods_no_HLLHC_Higgs_small_priors_long";
    


    std::string working_dir = "../Fits_HLLHC_FCCee/different_BPs/";
    // std::string working_dir = "../Fits_HLLHC_ILC_250_350_500_1000/different_BPs/";


    std::vector<std::string> scenarios;
    std::vector<std::string> plot_titles;

    std::vector<float> KappaLambdas;
    // std::vector<float> base_KappaLambdas = {
    //     1.0643594459030925, // BPB_0
    //     2.068362744578383, // BPB_1
    //     3.41660475844658, // BPB_2
    //     0.9197317035823376, // BPB_3
    //     4.996504503173265, // BPB_4
    //     2.723103795696014, // BPB_5
    //     6.114019817191308, // BPB_6
    //     4.878015572616551, // BPB_7
    //     7.24831645311373, // BPB_8
    //     7.005268951781772, // BPB_9
    //     8.535635929341407, // BPB_10
    //     8.84021000223677, // BPB_11
    //     9.584476423981522, // BPB_12
    //     10.34814810189343, // BPB_13
    // };
        std::vector<float> base_KappaLambdas = {
        1.0643594459030925, // BPB_0
        2.068362744578383, // BPB_1
        3.41660475844658, // BPB_2
        4.996504503173265, // BPB_4
    };

    bool drawKLambdaErrorProjection = false;
    std::vector<float> KappaLambdas_error_low;
    // std::vector<float> base_KappaLambdas_error_low = {1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,};
    std::vector<float> base_KappaLambdas_error_low = {1.,1.,1.,1.,};

    std::vector<float> KappaLambdas_error_high;
    // std::vector<float> base_KappaLambdas_error_high = {-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,};
    std::vector<float> base_KappaLambdas_error_high = {-1.,-1.,-1.,-1.,};

    bool setRangeKLambda = false;
    // std::vector<float> KappaLambdas_range_low = {1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,};
    std::vector<float> KappaLambdas_range_low = {1.,1.,1.,1.,};
    // std::vector<float> KappaLambdas_range_high = {-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,};
    std::vector<float> KappaLambdas_range_high = {-1.,-1.,-1.,-1.,};


    bool only_relevant_plots = true;

    const int n_scenarios_base = 1;

    // const int num_BPO = 2;
    const int num_BPO = 0;
    const int num_BPB = 4;
    // const int num_BPB = 4;

    const int n_scenarios = n_scenarios_base * (num_BPO + num_BPB);
    const std::string base_paths[] = {
        // "Z2SSM_FCCee240",
        "Z2SSM_FCCee240_FCCee365",
        // "Z2SSM_FCCee240_FCCee365_HLLHClambda",
    };
    // const std::string base_paths[] = {
    //     "Z2SSM_ILC_250_350",
    //     "Z2SSM_ILC_250_350_500",
    // };

    // const std::string base_titles[] = {
    //     "Z2SSM central values, FCC-ee_{240}",
    //     "Z2SSM central values, FCC-ee_{240+365}",
    //     "Z2SSM central values, FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
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
    // std::vector<std::string> base_BP_names = {
    //     "BPBnew 0",
    //     "BPBnew 1",
    //     "BPBnew 2",
    //     "BPBnew 3",
    //     "BPBnew 4",
    //     "BPBnew 5",
    //     "BPBnew 6",
    //     "BPBnew 7",
    //     "BPBnew 8",
    //     "BPBnew 9",
    //     "BPBnew 10",
    //     "BPBnew 11",
    //     "BPBnew 12",
    //     "BPBnew 13",
    // };
    // std::vector<std::string> base_BP_names = {
    //     "BPBnew 0",
    //     "BPBnew 1",
    //     "BPBnew 2",
    //     "BPBnew 4",
    // };
    std::vector<std::string> base_BP_names = {
        "BP 0",
        "BP 1",
        "BP 2",
        "BP 3",
    };

    // BP_lambda1
    // std::vector<std::string> base_BP_names = {
    //     // "BP_{#kappa_{#lambda} #approx 1}",
    //     "BP 0",
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

    int BPB_numbers[num_BPB] = {0, 1, 2, 4};
    // int BPB_numbers[num_BPB] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
    int BPB = 0;

    for (int bp = 0; bp < num_BPB; ++bp) {
        for (int i=0; i<n_scenarios_base; ++i) {
            BPB = BPB_numbers[bp];
            std::cout << base_KappaLambdas[bp] << std::endl;
            scenarios.push_back("BPBnew_" + std::to_string(BPB) + "/" + base_paths[i]);
            // scenarios.push_back(std::string("BP_lambda1") + "/" + base_paths[i]);
            // plot_titles.push_back("Z2SSM BP " + std::to_string(BPB) + ", " + base_titles[i]);
            // plot_titles.push_back("Z2SSM BP " + std::to_string(bp+1) + ", " + base_titles[i]);
            plot_titles.push_back("Z2SSM " + base_BP_names[bp] + ", " + base_titles[i]);
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
