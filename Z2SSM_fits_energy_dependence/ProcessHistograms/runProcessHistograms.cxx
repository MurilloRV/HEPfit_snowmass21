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
    bool drawGlobalModes = false;

    std::string model_spec = "fits";


    std::string working_dir = "../Fits_HLLHC_FCCee/different_BPs/";


    std::vector<std::string> scenarios;
    std::vector<std::string> plot_titles;

    std::vector<float> KappaLambdas;
    std::vector<float> base_KappaLambdas = {
        -0.2508742207313748, // BPO_0
        -0.3647055096736148, // BPO_1
        -0.283207588738505, // BPO_2
        -0.2265153925052781, // BPO_3
        0.8270343237975535, // BPO_4
        0.8918170746898771, // BPB_0
        3.4771963023861323, // BPB_1
        0.9196804937486558, // BPB_2
        4.703937706690645, // BPB_3
        3.013431564284278, // BPB_4
        5.946907598934937, // BPB_5
        4.968691068740802, // BPB_6
        7.233411757176534, // BPB_7
        6.988652545078013, // BPB_8
        8.519243114238716, // BPB_9
        8.915995818716492, // BPB_10
        9.679739818437092, // BPB_11
        10.721334023900692, // BPB_12
    };

    const int n_scenarios_base = 3;
    const int num_BPO = 5;
    const int num_BPB = 13;
    const int n_scenarios = n_scenarios_base * (num_BPO + num_BPB);
    const std::string base_paths[] = {
        "Z2SSM_FCCee240",
        "Z2SSM_FCCee240_FCCee365",
        "Z2SSM_FCCee240_FCCee365_HLLHClambda",
    };

    const std::string base_titles[] = {
        "Z2SSM central values, FCC-ee_{240}",
        "Z2SSM central values, FCC-ee_{240+365}",
        "Z2SSM central values, FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    };

    for (int bp = 0; bp < num_BPO; ++bp) {
        for (int i=0; i<n_scenarios_base; ++i) {
            // std::cout << base_paths[i] << std::endl;
            // std::cout << base_titles[i] << std::endl;
            scenarios.push_back("BPO_" + std::to_string(bp) + "/" + base_paths[i]);
            plot_titles.push_back(base_titles[i]);
            // std::cout << base_KappaLambdas[i] << std::endl;
            KappaLambdas.push_back(base_KappaLambdas[bp]);
        }
    }

    for (int bp = 0; bp < num_BPB; ++bp) {
        for (int i=0; i<n_scenarios_base; ++i) {
            scenarios.push_back("BPB_" + std::to_string(bp) + "/" + base_paths[i]);
            plot_titles.push_back(base_titles[i]);
            KappaLambdas.push_back(base_KappaLambdas[bp + num_BPO]);
        }
    }

    ProcessHistograms Modify_Histos = ProcessHistograms(cindex,
                                                        printLogo,
                                                        nSmooth,
                                                        histogram2Dtype,
                                                        noLegend,
                                                        nBins1D,
                                                        nBins2D,
                                                        drawGlobalModes);

    

    for (int i=0; i<n_scenarios; i++)
    {
        std::string results_dir = working_dir + scenarios[i] + "/results_" + model_spec + "/";
        std::string obs_dir = results_dir + "Observables/";
        std::string root_filepath = results_dir + "MCout.root";
        std::cout << root_filepath << std::endl;

        std::string stats_filepath = obs_dir + "Statistics.txt";


        // try {
            Modify_Histos.Get_Global_Modes(stats_filepath);
            Modify_Histos.Print_1D_Histos(root_filepath, obs_dir, plot_titles[i], KappaLambdas[i]);
        //}

    }


    // delete HEPfit_red;
    // delete HEPfit_green;
    // HEPfit_red = NULL;
    // HEPfit_green = NULL;
    
    return 0;
}
