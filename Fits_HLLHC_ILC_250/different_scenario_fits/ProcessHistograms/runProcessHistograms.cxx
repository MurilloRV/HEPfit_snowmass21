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

#include "EmptyModel.h"


void Modify_1D_Hist(BCH1D bch1d, const char* filename, int gIdx, int rIdx, int nSmooth, bool noLegend, int cindex)
{

    TCanvas * c;
    cindex++;
    c = new TCanvas(TString::Format("c_bch1d_%d",cindex));

    bch1d.GetHistogram()->Scale(1./bch1d.GetHistogram()->Integral("width"));
    
    bch1d.SetBandType(BCH1D::kSmallestInterval);
    bch1d.SetBandColor(0, gIdx);
    bch1d.SetBandColor(1, rIdx);
    bch1d.SetBandColor(2, kOrange - 3);
    bch1d.SetNBands(3);
    bch1d.SetNSmooth(nSmooth);
    bch1d.SetDrawGlobalMode(true);
    bch1d.SetDrawMean(true, true);
    bch1d.SetDrawLegend(!noLegend);
    if (noLegend) gStyle->SetOptStat("emr");
    bch1d.SetNLegendColumns(1);
    bch1d.SetStats(true);
    
    bch1d.Draw();

    c->Print(filename);

    delete c;
    c = NULL;

}

int main()
{
    // // open log file
    // BCLog::OpenLog("log.txt", BCLog::detail, BCLog::detail);

    // // create new EmptyModel object
    // EmptyModel m("Name_Me");

    // // set precision
    // m.SetPrecision(BCEngineMCMC::kMedium);

    // BCLog::OutSummary("Test model created");

    // //////////////////////////////
    // // perform your analysis here

    // // Normalize the posterior by integrating it over the full parameter space
    // // m.Normalize();

    // // Write Markov Chain to a ROOT file as a TTree
    // // m.WriteMarkovChain(m.GetSafeName() + "_mcmc.root", "RECREATE");

    // // run MCMC, marginalizing posterior
    // m.MarginalizeAll(BCIntegrate::kMargMetropolis);

    // // run mode finding; by default using Minuit
    // m.FindMode(m.GetBestFitParameters());

    // // draw all marginalized distributions into a PDF file
    // m.PrintAllMarginalized(m.GetSafeName() + "_plots.pdf");

    // // print summary plots
    // // m.PrintParameterPlot(m.GetSafeName() + "_parameters.pdf");
    // // m.PrintCorrelationPlot(m.GetSafeName() + "_correlation.pdf");
    // // m.PrintCorrelationMatrix(m.GetSafeName() + "_correlationMatrix.pdf");
    // // m.PrintKnowledgeUpdatePlots(m.GetSafeName() + "_update.pdf");

    // // print results of the analysis into a text file
    // m.PrintSummary();

    // // close log file
    // BCLog::OutSummary("Exiting");
    // BCLog::CloseLog();

    int cindex=0;

    std::map<std::string, BCH1D> Histo1D;
    int nBins1D = 100;
    int gIdx = TColor::GetFreeColorIndex();
    int rIdx = TColor::GetFreeColorIndex() + 1;

    TColor * HEPfit_green = new TColor(gIdx, 0.0, 0.56, 0.57, "HEPfit_green");
    TColor * HEPfit_red = new TColor(rIdx, 0.57, 0.01, 0.00, "HEPfit_red");
    int nSmooth = 0;
    int histogram2Dtype = 1001;
    bool noLegend = false;

    const char * filepath = "../SM_noHLLHClambda/results_SQUARED/MCout.root";
    TFile in_file(filepath);
    // in_file.ls();

    const char * HistName = "deltalHHH_HLLHC_bch_bch";
    auto histo = in_file.Get<TH1D>(HistName);

    //TH1D * histo ;
    BCH1D bchisto = BCH1D(histo);
    Histo1D[HistName] = bchisto;

    const char * filename = "test.pdf";
    Modify_1D_Hist(Histo1D[HistName], filename, gIdx, rIdx, nSmooth, noLegend, cindex);


    delete HEPfit_red;
    delete HEPfit_green;
    HEPfit_red = NULL;
    HEPfit_green = NULL;
    
    return 0;
}
