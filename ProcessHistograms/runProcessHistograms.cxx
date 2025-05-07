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

    // std::string model_spec = "SQUARED";
    std::string model_spec = "fits";
    // std::string model_spec = "all_uncertainties_SQUARED";
    // std::string model_spec = "fits";
    // std::string model_spec = "crosscheck_1percent_k_lambda_error";
    // std::string model_spec = "crosscheck_1percent_k_lambda_error";


    // std::string working_dir = "../Fits_HLLHC_ILC_250/different_scenario_fits/";
    // std::string working_dir = "../Fits_HLLHC_ILC_250/large_kappa_lambda_fits/";
    // std::string working_dir = "../Fits_HLLHC_FCCee/different_scenario_fits/";
    std::string working_dir = "../Fits_HLLHC_FCCee/large_kappa_lambda_fits/";
    // std::string working_dir = "../Fits_HLLHC_ILC_250/different_scenario_fits/";
    // std::string working_dir = "../Fits_HLLHC_FCCee/different_scenario_fits/";
    // std::string working_dir = "../IDM_fits/Fits_HLLHC_ILC_250/different_scenario_fits/";
    // std::string working_dir = "../IDM_fits/Fits_HLLHC_FCCee/different_scenario_fits/";
    // std::string working_dir = "../IDM_fits/Fits_HLLHC_FCCee/different_BPs/";
    // std::string working_dir = "../Z2SSM_fits_energy_dependence/Fits_HLLHC_ILC_250/different_scenario_fits/";
    // std::string working_dir = "../Z2SSM_fits_energy_dependence/Fits_HLLHC_FCCee/different_scenario_fits/";
    // std::string working_dir = "../Z2SSM_fits_energy_dependence/Fits_HLLHC_FCCee/different_BPs/";
    


    // std::string scenarios[] = {"SM_noHLLHClambda",
    //                            "SM_HLLHClambda",
    //                            "Z2SSM_noHLLHClambda",
    //                            "Z2SSM_HLLHClambda"};

    // std::string scenarios[] = {"Lambda2_noHLLHClambda",
    //                            "Lambda2_HLLHClambda",
    //                            "Lambda3_noHLLHClambda",
    //                            "Lambda3_HLLHClambda",
    //                            "Lambda5_noHLLHClambda",
    //                            "Lambda5_HLLHClambda",
    //                            "Lambda10_noHLLHClambda",
    //                            "Lambda10_HLLHClambda"};
    
    // std::string scenarios[] = {"SM_FCCee240",
    //                            "SM_FCCee240_FCCee365",
    //                            "SM_FCCee240_FCCee365_HLLHClambda",
    //                            "Z2SSM_FCCee240",
    //                            "Z2SSM_FCCee240_FCCee365",
    //                            "Z2SSM_FCCee240_FCCee365_HLLHClambda"};

    // std::string scenarios[] = {"Lambda2_FCCee240_FCCee365_noHLLHClambda",
    //                            "Lambda2_FCCee240_FCCee365_HLLHClambda",
    //                            "Lambda3_FCCee240_FCCee365_noHLLHClambda",
    //                            "Lambda3_FCCee240_FCCee365_HLLHClambda",
    //                            "Lambda5_FCCee240_FCCee365_noHLLHClambda",
    //                            "Lambda5_FCCee240_FCCee365_HLLHClambda",
    //                            "Lambda10_FCCee240_FCCee365_noHLLHClambda",
    //                            "Lambda10_FCCee240_FCCee365_HLLHClambda"};

    std::string scenarios[] = {"Lambda2_FCCee240_FCCee365_noHLLHClambda",
                               "Lambda2_FCCee240_FCCee365_HLLHClambda",
                               "Lambda3_FCCee240_FCCee365_noHLLHClambda",
                               "Lambda3_FCCee240_FCCee365_HLLHClambda",
                               "Lambda5_FCCee240_FCCee365_noHLLHClambda",
                               "Lambda5_FCCee240_FCCee365_HLLHClambda",
                               "Lambda6_FCCee240_FCCee365_noHLLHClambda",
                               "Lambda6_FCCee240_FCCee365_HLLHClambda",
                               "Lambda7_FCCee240_FCCee365_noHLLHClambda",
                               "Lambda7_FCCee240_FCCee365_HLLHClambda",
                               "Lambda8_FCCee240_FCCee365_noHLLHClambda",
                               "Lambda8_FCCee240_FCCee365_HLLHClambda",
                               "Lambda9_FCCee240_FCCee365_noHLLHClambda",
                               "Lambda9_FCCee240_FCCee365_HLLHClambda",
                               "Lambda10_FCCee240_FCCee365_noHLLHClambda",
                               "Lambda10_FCCee240_FCCee365_HLLHClambda"};

    // std::string scenarios[] = {"Z2SSM_HLLHClambda"};

    // std::string scenarios[] = {"Z2SSM_FCCee240_FCCee365_HLLHClambda"};

    // std::string scenarios[] = {"SM_noHLLHClambda",
    //                             "SM_HLLHClambda",
    //                             "IDM_noHLLHClambda",
    //                             "IDM_HLLHClambda"};

    // std::string scenarios[] = {"SM_FCCee240",
    //                            "SM_FCCee240_FCCee365",
    //                            "SM_FCCee240_FCCee365_HLLHClambda",
    //                            "IDM_FCCee240",
    //                            "IDM_FCCee240_FCCee365",
    //                            "IDM_FCCee240_FCCee365_HLLHClambda"};

    // std::string scenarios[] = {"BP_0/IDM_FCCee240",
    //                            "BP_0/IDM_FCCee240_FCCee365",
    //                            "BP_0/IDM_FCCee240_FCCee365_HLLHClambda",
    //                            "BP_1/IDM_FCCee240",
    //                            "BP_1/IDM_FCCee240_FCCee365",
    //                            "BP_1/IDM_FCCee240_FCCee365_HLLHClambda",
    //                            "BP_2/IDM_FCCee240",
    //                            "BP_2/IDM_FCCee240_FCCee365",
    //                            "BP_2/IDM_FCCee240_FCCee365_HLLHClambda",
    //                         //    "BP_3/IDM_FCCee240",
    //                         //    "BP_3/IDM_FCCee240_FCCee365",
    //                         //    "BP_3/IDM_FCCee240_FCCee365_HLLHClambda",
    //                            "BP_4/IDM_FCCee240",
    //                            "BP_4/IDM_FCCee240_FCCee365",
    //                            "BP_4/IDM_FCCee240_FCCee365_HLLHClambda",
    //                         //    "BP_5/IDM_FCCee240",
    //                         //    "BP_5/IDM_FCCee240_FCCee365",
    //                         //    "BP_5/IDM_FCCee240_FCCee365_HLLHClambda",
    //                            "BP_6/IDM_FCCee240",
    //                            "BP_6/IDM_FCCee240_FCCee365",
    //                            "BP_6/IDM_FCCee240_FCCee365_HLLHClambda",
    //                            "BP_7/IDM_FCCee240",
    //                            "BP_7/IDM_FCCee240_FCCee365",
    //                            "BP_7/IDM_FCCee240_FCCee365_HLLHClambda",
    //                            };



    // std::string scenarios[] = {"BP_0/Z2SSM_FCCee240",
    //                            "BP_0/Z2SSM_FCCee240_FCCee365",
    //                            "BP_0/Z2SSM_FCCee240_FCCee365_HLLHClambda",
    //                            "BP_1/Z2SSM_FCCee240",
    //                            "BP_1/Z2SSM_FCCee240_FCCee365",
    //                            "BP_1/Z2SSM_FCCee240_FCCee365_HLLHClambda",
    //                         //    "BP_2/Z2SSM_FCCee240",
    //                         //    "BP_2/Z2SSM_FCCee240_FCCee365",
    //                         //    "BP_2/Z2SSM_FCCee240_FCCee365_HLLHClambda",
    //                            "BP_3/Z2SSM_FCCee240",
    //                            "BP_3/Z2SSM_FCCee240_FCCee365",
    //                            "BP_3/Z2SSM_FCCee240_FCCee365_HLLHClambda",
    //                         //    "BP_4/Z2SSM_FCCee240",
    //                         //    "BP_4/Z2SSM_FCCee240_FCCee365",
    //                         //    "BP_4/Z2SSM_FCCee240_FCCee365_HLLHClambda",
    //                         //    "BP_5/Z2SSM_FCCee240",
    //                         //    "BP_5/Z2SSM_FCCee240_FCCee365",
    //                         //    "BP_5/Z2SSM_FCCee240_FCCee365_HLLHClambda",
    //                            "BP_6/Z2SSM_FCCee240",
    //                            "BP_6/Z2SSM_FCCee240_FCCee365",
    //                            "BP_6/Z2SSM_FCCee240_FCCee365_HLLHClambda",
    //                            "BP_7/Z2SSM_FCCee240",
    //                            "BP_7/Z2SSM_FCCee240_FCCee365",
    //                            "BP_7/Z2SSM_FCCee240_FCCee365_HLLHClambda",
    //                            };



    // std::string plot_titles[] = {"SM central values, ILC_{250}",
    //                              "SM central values, ILC_{250} + #kappa_{#lambda} at HL-LHC",
    //                              "Z2SSM central values, ILC_{250}",
    //                              "Z2SSM central values, ILC_{250} + #kappa_{#lambda} at HL-LHC"};

    // std::string plot_titles[] = {"#kappa_{#lambda} = 2 Cross-check (C_{H} #approx -2.13), ILC_{250}", 
    //                              "#kappa_{#lambda} = 2 Cross-check (C_{H} #approx -2.13), ILC_{250} + #kappa_{#lambda} at HL-LHC",  
    //                              "#kappa_{#lambda} = 3 Cross-check (C_{H} #approx -4.27), ILC_{250}", 
    //                              "#kappa_{#lambda} = 3 Cross-check (C_{H} #approx -4.27), ILC_{250} + #kappa_{#lambda} at HL-LHC",  
    //                              "#kappa_{#lambda} = 5 Cross-check (C_{H} #approx -8.53), ILC_{250}", 
    //                              "#kappa_{#lambda} = 5 Cross-check (C_{H} #approx -8.53), ILC_{250} + #kappa_{#lambda} at HL-LHC",  
    //                              "#kappa_{#lambda} = 10 Cross-check (C_{H} #approx -19.20), ILC_{250}", 
    //                              "#kappa_{#lambda} = 10 Cross-check (C_{H} #approx -19.20), ILC_{250} + #kappa_{#lambda} at HL-LHC"};

    std::string plot_titles[] = {"#kappa_{#lambda} = 2 Cross-check (C_{H} #approx -2.13), ILC_{250}", 
                                 "#kappa_{#lambda} = 2 Cross-check (C_{H} #approx -2.13), ILC_{250} + #kappa_{#lambda} at HL-LHC",  
                                 "#kappa_{#lambda} = 3 Cross-check (C_{H} #approx -4.27), ILC_{250}", 
                                 "#kappa_{#lambda} = 3 Cross-check (C_{H} #approx -4.27), ILC_{250} + #kappa_{#lambda} at HL-LHC",  
                                 "#kappa_{#lambda} = 5 Cross-check (C_{H} #approx -8.53), ILC_{250}", 
                                 "#kappa_{#lambda} = 5 Cross-check (C_{H} #approx -8.53), ILC_{250} + #kappa_{#lambda} at HL-LHC",  
                                 "#kappa_{#lambda} = 6 Cross-check (C_{H} #approx -10.67), ILC_{250}", 
                                 "#kappa_{#lambda} = 6 Cross-check (C_{H} #approx -10.67), ILC_{250} + #kappa_{#lambda} at HL-LHC", 
                                 "#kappa_{#lambda} = 7 Cross-check (C_{H} #approx -12.80), ILC_{250}", 
                                 "#kappa_{#lambda} = 7 Cross-check (C_{H} #approx -12.80), ILC_{250} + #kappa_{#lambda} at HL-LHC", 
                                 "#kappa_{#lambda} = 8 Cross-check (C_{H} #approx -14.93), ILC_{250}", 
                                 "#kappa_{#lambda} = 8 Cross-check (C_{H} #approx -14.93), ILC_{250} + #kappa_{#lambda} at HL-LHC", 
                                 "#kappa_{#lambda} = 9 Cross-check (C_{H} #approx -17.07), ILC_{250}", 
                                 "#kappa_{#lambda} = 9 Cross-check (C_{H} #approx -17.07), ILC_{250} + #kappa_{#lambda} at HL-LHC", 
                                 "#kappa_{#lambda} = 10 Cross-check (C_{H} #approx -19.20), ILC_{250}", 
                                 "#kappa_{#lambda} = 10 Cross-check (C_{H} #approx -19.20), ILC_{250} + #kappa_{#lambda} at HL-LHC"};

    // std::string plot_titles[] = {"SM central values, FCC-ee_{240}",
    //                              "SM central values, FCC-ee_{240} + FCC-ee_{365}",
    //                              "SM central values, FCC-ee_{240} + FCC-ee_{365} + #kappa_{#lambda} at HL-LHC",
    //                              "Z2SSM central values, FCC-ee_{240}",
    //                              "Z2SSM central values, FCC-ee_{240} + FCC-ee_{365}",
    //                              "Z2SSM central values, FCC-ee_{240} + FCC-ee_{365} + #kappa_{#lambda} at HL-LHC"};

    // std::string plot_titles[] = {"#kappa_{#lambda} = 2 Cross-check (C_{H} #approx -2.13), FCC-ee_{240+365}", 
    //                              "#kappa_{#lambda} = 2 Cross-check (C_{H} #approx -2.13), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",  
    //                              "#kappa_{#lambda} = 3 Cross-check (C_{H} #approx -4.27), FCC-ee_{240+365}", 
    //                              "#kappa_{#lambda} = 3 Cross-check (C_{H} #approx -4.27), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",  
    //                              "#kappa_{#lambda} = 5 Cross-check (C_{H} #approx -8.53), FCC-ee_{240+365}", 
    //                              "#kappa_{#lambda} = 5 Cross-check (C_{H} #approx -8.53), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",  
    //                              "#kappa_{#lambda} = 10 Cross-check (C_{H} #approx -19.20), FCC-ee_{240+365}", 
    //                              "#kappa_{#lambda} = 10 Cross-check (C_{H} #approx -19.20), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC"};

    // std::string plot_titles[] = {"Z2SSM Cross-check with 1% #kappa_{#lambda} uncertainty (ILC_{250})"};

    // std::string plot_titles[] = {"Z2SSM Cross-check with 1% #kappa_{#lambda} uncertainty (FCC-ee_{240+365})"};

    // std::string plot_titles[] = {"SM central values, ILC_{250}",
    //                              "SM central values, ILC_{250} + #kappa_{#lambda} at HL-LHC",
    //                              "IDM central values, ILC_{250}",
    //                              "IDM central values, ILC_{250} + #kappa_{#lambda} at HL-LHC"};

    // std::string plot_titles[] = {"SM central values, FCC-ee_{240}",
    //                              "SM central values, FCC-ee_{240} + FCC-ee_{365}",
    //                              "SM central values, FCC-ee_{240} + FCC-ee_{365} + #kappa_{#lambda} at HL-LHC",
    //                              "IDM central values, FCC-ee_{240}",
    //                              "IDM central values, FCC-ee_{240} + FCC-ee_{365}",
    //                              "IDM central values, FCC-ee_{240} + FCC-ee_{365} + #kappa_{#lambda} at HL-LHC"};


    // std::string plot_titles[] = {"IDM central values (BP 0), FCC-ee_{240}",
    //                              "IDM central values (BP 0), FCC-ee_{240+365}",
    //                              "IDM central values (BP 0), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    //                              "IDM central values (BP 1), FCC-ee_{240}",
    //                              "IDM central values (BP 1), FCC-ee_{240+365}",
    //                              "IDM central values (BP 1), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    //                              "IDM central values (BP 2), FCC-ee_{240}",
    //                              "IDM central values (BP 2), FCC-ee_{240+365}",
    //                              "IDM central values (BP 2), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    //                             //  "IDM central values (BP 3), FCC-ee_{240}",
    //                             //  "IDM central values (BP 3), FCC-ee_{240+365}",
    //                             //  "IDM central values (BP 3), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    //                              "IDM central values (BP 4), FCC-ee_{240}",
    //                              "IDM central values (BP 4), FCC-ee_{240+365}",
    //                              "IDM central values (BP 4), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    //                             //  "IDM central values (BP 5), FCC-ee_{240}",
    //                             //  "IDM central values (BP 5), FCC-ee_{240+365}",
    //                             //  "IDM central values (BP 5), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    //                              "IDM central values (BP 6), FCC-ee_{240}",
    //                              "IDM central values (BP 6), FCC-ee_{240+365}",
    //                              "IDM central values (BP 6), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    //                              "IDM central values (BP 7), FCC-ee_{240}",
    //                              "IDM central values (BP 7), FCC-ee_{240+365}",
    //                              "IDM central values (BP 7), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
    //                              };


        // std::string plot_titles[] = {"Z2SSM central values (BP 0), FCC-ee_{240}",
        //                          "Z2SSM central values (BP 0), FCC-ee_{240+365}",
        //                          "Z2SSM central values (BP 0), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
        //                          "Z2SSM central values (BP 1), FCC-ee_{240}",
        //                          "Z2SSM central values (BP 1), FCC-ee_{240+365}",
        //                          "Z2SSM central values (BP 1), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
        //                         //  "Z2SSM central values (BP 2), FCC-ee_{240}",
        //                         //  "Z2SSM central values (BP 2), FCC-ee_{240+365}",
        //                         //  "Z2SSM central values (BP 2), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
        //                          "Z2SSM central values (BP 3), FCC-ee_{240}",
        //                          "Z2SSM central values (BP 3), FCC-ee_{240+365}",
        //                          "Z2SSM central values (BP 3), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
        //                         //  "Z2SSM central values (BP 4), FCC-ee_{240}",
        //                         //  "Z2SSM central values (BP 4), FCC-ee_{240+365}",
        //                         //  "Z2SSM central values (BP 4), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
        //                         //  "Z2SSM central values (BP 5), FCC-ee_{240}",
        //                         //  "Z2SSM central values (BP 5), FCC-ee_{240+365}",
        //                         //  "Z2SSM central values (BP 5), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
        //                          "Z2SSM central values (BP 6), FCC-ee_{240}",
        //                          "Z2SSM central values (BP 6), FCC-ee_{240+365}",
        //                          "Z2SSM central values (BP 6), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
        //                          "Z2SSM central values (BP 7), FCC-ee_{240}",
        //                          "Z2SSM central values (BP 7), FCC-ee_{240+365}",
        //                          "Z2SSM central values (BP 7), FCC-ee_{240+365} + #kappa_{#lambda} at HL-LHC",
        //                          };





    // float KappaLambda_Z2SSM = 2.482538926; 
    // float KappaLambda_IDM = 1.854610413951624; 



    // float KappaLambdas[] = {1.0,
    //                         1.0,
    //                         KappaLambda_Z2SSM,
    //                         KappaLambda_Z2SSM};

    // float KappaLambdas[] = {2.0,
    //                         2.0,
    //                         3.0,
    //                         3.0,
    //                         5.0,
    //                         5.0,
    //                         10.0,
    //                         10.0};

    float KappaLambdas[] = {2.0,
                            2.0,
                            3.0,
                            3.0,
                            5.0,
                            5.0,
                            6.0,
                            6.0,
                            7.0,
                            7.0,
                            8.0,
                            8.0,
                            9.0,
                            9.0,
                            10.0,
                            10.0};

    // float KappaLambdas[] = {1.0,
    //                         1.0,
    //                         1.0,
    //                         KappaLambda_Z2SSM,
    //                         KappaLambda_Z2SSM,
    //                         KappaLambda_Z2SSM};

    // float KappaLambdas[] = {KappaLambda_Z2SSM};

    // float KappaLambdas[] = {1.0,
    //                         1.0,
    //                         KappaLambda_IDM,
    //                         KappaLambda_IDM};

    // float KappaLambdas[] = {1.0,
    //                         1.0,
    //                         1.0,
    //                         KappaLambda_IDM,
    //                         KappaLambda_IDM,
    //                         KappaLambda_IDM};

    // float KappaLambdas[] = {1.6885444220830157,
    //                         1.6885444220830157,
    //                         1.6885444220830157,
    //                         1.5026696187124242,
    //                         1.5026696187124242,
    //                         1.5026696187124242,
    //                         2.003326933459748,
    //                         2.003326933459748,
    //                         2.003326933459748,
    //                         // 2.003326933459748,
    //                         // 2.003326933459748,
    //                         // 2.003326933459748,
    //                         1.5027312712751126,
    //                         1.5027312712751126,
    //                         1.5027312712751126,
    //                         // 1.5027312712751126,
    //                         // 1.5027312712751126,
    //                         // 1.5027312712751126,
    //                         1.186487087345143,
    //                         1.186487087345143,
    //                         1.186487087345143,
    //                         1.2096708258013975,
    //                         1.2096708258013975,
    //                         1.2096708258013975
    //                         };

    // float KappaLambdas[] = {2.8901885159873064,
    //                         2.8901885159873064,
    //                         2.8901885159873064,
    //                         1.500069302100464,
    //                         1.500069302100464,
    //                         1.500069302100464,
    //                         // 10.76349876455617,
    //                         // 10.76349876455617,
    //                         // 10.76349876455617,
    //                         2.0000017431283923,
    //                         2.0000017431283923,
    //                         2.0000017431283923,
    //                         // 10.76349876455617,
    //                         // 10.76349876455617,
    //                         // 10.76349876455617,
    //                         // 1.500069302100464,
    //                         // 1.500069302100464,
    //                         // 1.500069302100464,
    //                         1.138105762218659,
    //                         1.138105762218659,
    //                         1.138105762218659,
    //                         0.066878038392428,
    //                         0.066878038392428,
    //                         0.066878038392428,
    //                         };


    ProcessHistograms Modify_Histos = ProcessHistograms(cindex,
                                                        printLogo,
                                                        nSmooth,
                                                        histogram2Dtype,
                                                        noLegend,
                                                        nBins1D,
                                                        nBins2D,
                                                        drawGlobalModes);

    // const int n_scenarios = 1;
    // const int n_scenarios = 4;
    // const int n_scenarios = 8;
    const int n_scenarios = 16;
    // const int n_scenarios = 6;
    // const int n_scenarios = 18;
    // const int n_scenarios = 15;
    for (int i=0; i<n_scenarios; i++)
    {
        std::string results_dir = working_dir + scenarios[i] + "/results_" + model_spec + "/";
        std::string obs_dir = results_dir + "Observables/";
        std::string root_filepath = results_dir + "MCout.root";
        std::cout << root_filepath << std::endl;

        std::string stats_filepath = obs_dir + "Statistics.txt";

        Modify_Histos.Get_Global_Modes(stats_filepath);

        Modify_Histos.Print_1D_Histos(root_filepath, obs_dir, plot_titles[i], KappaLambdas[i]);

    }


    // delete HEPfit_red;
    // delete HEPfit_green;
    // HEPfit_red = NULL;
    // HEPfit_green = NULL;
    
    return 0;
}
