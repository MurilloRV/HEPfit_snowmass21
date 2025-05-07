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
        bool drawGlobalModes = false);

    // Destructor
    ~ProcessHistograms();

    void Get_Global_Modes(std::string filepath);

    void Modify_1D_Hist(BCH1D bch1d, std::string filename, std::string title, std::string hist_title);

    void Print_1D_Histos(std::string filepath, std::string plot_dir, std::string title, float k_lambda);
    


    void setKappaLambda(float KappaLambda)
    {
        this->KappaLambda = KappaLambda;
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

    float KappaLambda;
    bool drawKappaLambdaLine;

    bool drawGlobalModes;

    std::map<std::string, float> Global_Modes;



};
// ---------------------------------------------------------

#endif
