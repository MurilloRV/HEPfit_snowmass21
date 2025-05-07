// ***************************************************************
// This file was created using the bat-project script.
// bat-project is part of Bayesian Analysis Toolkit (BAT).
// BAT can be downloaded from http://mpp.mpg.de/bat
// ***************************************************************

#ifndef __BAT__PROCESSHISTOGRAMS__H
#define __BAT__PROCESSHISTOGRAMS__H

#include <BAT/BCModel.h>

#include <string>
#include <vector>
#include <TColor.h>
#include <TAxis.h>


// This is a ProcessHistograms header file.
// Model source code is located in file ProcessHistograms/ProcessHistograms.cxx

// ---------------------------------------------------------
class ProcessHistograms
{

public:

    // Constructor
    ProcessHistograms(
        unsigned int cindex = 0,
        bool printLogo = false,
        int nSmooth = 0,
        int histogram2Dtype = 1001,
        bool noLegend = true,
        unsigned int nBins1D = 100,
        unsigned int nBins2D = 100,
        bool drawGlobalModes = false,
        bool setRangeKLambda = false,
        bool drawKLambdaErrorProjection = false,
        bool only_relevant_plots = false);

    // Destructor
    ~ProcessHistograms();

    void Get_Global_Modes(std::string filepath);

    static Double_t ShiftX(Double_t x, Double_t xmin, Double_t xmax, Double_t xmin_new, Double_t xmax_new);
    void ShiftAxis(TAxis *a, Double_t (*Shift)(Double_t, Double_t, Double_t, Double_t, Double_t), Double_t xmin, Double_t xmax, Double_t xmin_new, Double_t xmax_new);
    void ShiftXaxis(TH1 *h, Double_t (*Shift)(Double_t, Double_t, Double_t, Double_t, Double_t), Double_t xmin, Double_t xmax, Double_t xmin_new, Double_t xmax_new);

    void Modify_1D_Hist(BCH1D bch1d, std::string filename, std::string title, std::string hist_title, std::string BP_name);

    void Print_1D_Histos(
        std::string filepath, 
        std::string plot_dir, 
        std::string title, 
        Double_t k_lambda, 
        Double_t k_lambda_err_low=-1.0,
        Double_t k_lambda_err_high=-1.0,
        Double_t k_lambda_range_low=1.0,
        Double_t k_lambda_range_high=-1.0,
        std::string BP_name = "BP"
    );
    


    void setKappaLambda(Double_t KappaLambda, Double_t KappaLambda_err_low, Double_t KappaLambda_err_high, Double_t KappaLambda_range_low, Double_t KappaLambda_range_high)
    {
        this->KappaLambda = KappaLambda;
        this->KappaLambda_err_low = KappaLambda_err_low;
        this->KappaLambda_err_high = KappaLambda_err_high;
        this->KappaLambda_range_low = KappaLambda_range_low;
        this->KappaLambda_range_high = KappaLambda_range_high;
    };

    void setdrawKappaLambdaLine(bool drawKappaLambdaLine)
    {
        this->drawKappaLambdaLine = drawKappaLambdaLine;
    };

private:

    // std::map<std::string, BCH1D> Histo1D; ///< A map between pointers to objects of type BCH1D (<a href="https://www.mppmu.mpg.de/bat/?page=home" target=blank>BAT</a>) and their given names.
    // std::map<std::string, BCH2D> Histo2D; ///< A map between pointers to objects of type BCH2D (<a href="https://www.mppmu.mpg.de/bat/?page=home" target=blank>BAT</a>) and their given names.
    unsigned int cindex;///< An index to distinguish between succesive canvases used to draw histograms.
    bool printLogo; ///< A flag that is set to true for printing the logo on the histogram pdf.
    int nSmooth; ///< The number of times a 1D  histogram should be smoothed.
    int histogram2Dtype; ///< Type of 2D Histogram 1001 -> box pixel, 101 -> filled, 1 -> contour.
    bool noLegend; ///< A flag to toggle the histogram legends.
    int gIdx;
    int rIdx;
    unsigned int nBins1D; ///< The number of bins in a 1D histogram.
    unsigned int nBins2D; ///< The number of bins in a 2D histogram.
    TColor * HEPfit_green; /// < The colour green for HEPfit.
    TColor * HEPfit_red; /// < The colour red for HEPfit.

    Double_t KappaLambda;
    Double_t KappaLambda_err_low;
    Double_t KappaLambda_err_high;
    Double_t KappaLambda_range_low;
    Double_t KappaLambda_range_high;
    bool drawKappaLambdaLine;

    bool drawGlobalModes;
    bool setRangeKLambda;
    bool drawKLambdaErrorProjection;
    
    bool only_relevant_plots;

    std::map<std::string, Double_t> Global_Modes;



};
// ---------------------------------------------------------

#endif
