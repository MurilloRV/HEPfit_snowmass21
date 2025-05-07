// ***************************************************************
// This file was created using the bat-project script.
// bat-project is part of Bayesian Analysis Toolkit (BAT).
// BAT can be downloaded from http://mpp.mpg.de/bat
// ***************************************************************

#include "ProcessHistograms.h"
#include <BAT/BCH1D.h>
#include <BAT/BCH2D.h>
#include <TF1.h>
#include <TH1D.h>
#include <TTree.h>
#include <TROOT.h>
#include <TPaveText.h>
#include <TText.h>
#include <TColor.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TPad.h>
#include <TLine.h>
#include <TFile.h>
#include <TKey.h>
#include <TLegendEntry.h>
#include <iomanip>

#include <boost/algorithm/string/predicate.hpp>
#include <algorithm>


// #include <BAT/BCMath.h>

// ---------------------------------------------------------

ProcessHistograms::ProcessHistograms(
        unsigned int cindex,
        bool printLogo,
        int nSmooth,
        int histogram2Dtype,
        bool noLegend,
        unsigned int nBins1D,
        unsigned int nBins2D,
        bool drawGlobalModes) {
            
    this->cindex = cindex;
    this->printLogo = printLogo;
    this->nSmooth = nSmooth;
    this->histogram2Dtype = histogram2Dtype;
    this->noLegend = noLegend;
    this->nBins1D = nBins1D;
    this->nBins2D = nBins2D;
    this->gIdx = TColor::GetFreeColorIndex(),
    this->rIdx = TColor::GetFreeColorIndex() + 1,
    this->HEPfit_green = new TColor(gIdx, 0.0, 0.56, 0.57, "HEPfit_green");
    this->HEPfit_red = new TColor(rIdx, 0.57, 0.01, 0.00, "HEPfit_red");
    this->drawGlobalModes = drawGlobalModes;

}


// ---------------------------------------------------------
ProcessHistograms::~ProcessHistograms()
{
    delete HEPfit_red;
    delete HEPfit_green;
    HEPfit_red = NULL;
    HEPfit_green = NULL;
}


void ProcessHistograms::Get_Global_Modes(std::string filepath)
{
    std::ifstream infile(filepath.c_str());
    if (!infile) throw std::runtime_error("\nERROR: " + filepath + " does not exist.");
    
    int lines_to_skip = 6;
    bool found_data = false;
    std::string line;
    while (std::getline(infile, line)) { // Read file line by line
        if (lines_to_skip!=0) {
            if ((line.compare("Value of the observables at the global mode:")==0) || found_data) {
                found_data = true;
                lines_to_skip--;
            }
            continue;
        }

        // std::cout << line << std::endl;


        std::istringstream ss(line);   // Create a string stream for the line
        std::string word;

        std::string obs, ignore, global_mode_str;
        if (ss >> obs >> ignore >> global_mode_str){

            char charToRemove = '|'; // Use std::remove to "remove" the character, then erase the extra part 
            obs.erase(std::remove(obs.begin(), obs.end(), charToRemove), obs.end());

            float global_mode = std::stof(global_mode_str);
            Global_Modes[obs] = global_mode;
            // std::cout << obs << Global_Modes[obs] << std::endl;
        }
        else break;
    }

    infile.close();

}



void ProcessHistograms::Modify_1D_Hist(BCH1D bch1d, 
                                       std::string filename, 
                                       std::string title,
                                       std::string hist_title)
{
    TCanvas * c;
    cindex++;
    c = new TCanvas(TString::Format("c_bch1d_%d",cindex));
    TPad * pad1 = new TPad("pad1", "pad1", 0.0, 0.9, 1.0, 1.0);
    TPad * pad2 = new TPad("pad2", "pad2", 0.0, 0.0, 1.0, 0.9);
    pad1->Draw();
    pad2->Draw();

    pad1->cd();
    TPaveText *t = new TPaveText(0., 0., 1., 1., "NDC");
    t->AddText(title.c_str());
    t->SetTextAlign(22);
    t->SetTextSize(0.5);
    t->SetBorderSize(0);
    t->SetFillColor(gStyle->GetTitleFillColor());
    t->Draw();


    pad2->cd();
    bch1d.GetHistogram()->Scale(1./bch1d.GetHistogram()->Integral("width"));
    // bch1d.GetHistogram()->SetTitle(title.c_str());
    // gStyle->SetOptTitle(1);

    if (drawGlobalModes) bch1d.SetGlobalMode(Global_Modes[hist_title]);
    
    bch1d.SetROOToptions("HIST");
    bch1d.SetBandType(BCH1D::kSmallestInterval);
    bch1d.SetBandColor(0, gIdx);
    bch1d.SetBandColor(1, rIdx);
    bch1d.SetBandColor(2, kOrange - 3);
    bch1d.SetNBands(3);
    bch1d.SetNSmooth(nSmooth);
    bch1d.SetDrawGlobalMode(drawGlobalModes);
    bch1d.SetDrawMean(true, true);
    bch1d.SetDrawLegend(!noLegend);
    gStyle->SetOptStat("emr");
    bch1d.SetNLegendColumns(1);
    bch1d.SetStats(true);
    

    if (drawKappaLambdaLine) {
        TLine *l = new TLine(KappaLambda-1, 0., KappaLambda-1, 1.1*bch1d.GetHistogram()->GetMaximum());
        l->SetLineStyle(7);
        l->SetLineWidth(5);
        // l->SetLineColor(kMagenta+3);


        std::stringstream stream;
        stream << std::fixed << std::setprecision(2) << KappaLambda;
        std::string KappaLambda_str = stream.str();
        TLegendEntry* leg = bch1d.AddLegendEntry(l, "True model value (#kappa_{#lambda}="+KappaLambda_str+")", "L");
        leg->SetLineStyle(l->GetLineStyle());
        leg->SetLineWidth(l->GetLineWidth());
        leg->SetLineColor(l->GetLineColor());

        bch1d.Draw();
        l->Draw("same");

    } else bch1d.Draw();



    if (printLogo) {
        double xRange = (bch1d.GetHistogram()->GetXaxis()->GetXmax() - bch1d.GetHistogram()->GetXaxis()->GetXmin())*3./4.;
        double yRange = (bch1d.GetHistogram()->GetMaximum() - bch1d.GetHistogram()->GetMinimum());
        
        double xL;
        if (noLegend) xL = bch1d.GetHistogram()->GetXaxis()->GetXmin()+0.0475*xRange;
        else xL = bch1d.GetHistogram()->GetXaxis()->GetXmin() + 0.0375 * xRange;
        double yL = bch1d.GetHistogram()->GetYaxis()->GetXmin() + 0.89 * yRange;

        double xR;
        if (noLegend) xR = xL + 0.21*xRange;
        else xR = xL + 0.18 * xRange;
        double yR = yL + 0.09 * yRange;

        TBox b1 = TBox(xL, yL, xR, yR);
        b1.SetFillColor(gIdx);
        
        TBox b2; 
        b2 = TBox(xL+0.008*xRange, yL+0.008*yRange, xR-0.008*xRange, yR-0.008*yRange);
        b2.SetFillColor(kWhite);
        
        TPaveText b3 = TPaveText(xL+0.014*xRange, yL+0.013*yRange, xL+0.70*(xR-xL), yR-0.013*yRange);
        if (noLegend) b3.SetTextSize(0.056);
        else b3.SetTextSize(0.051);
        b3.SetTextAlign(22);
        b3.SetTextColor(kWhite);
        b3.AddText("HEP");
        b3.SetFillColor(rIdx);
        
        TPaveText * b4; 
        if (noLegend) {
            b4 = new TPaveText(xL+0.72*(xR-xL), yL+0.030*yRange, xR-0.008*xRange, yR-0.013*yRange);
            b4->SetTextSize(0.048);
        } else {
            b4 = new TPaveText(xL + 0.75 * (xR - xL), yL + 0.024 * yRange, xR - 0.008 * xRange, yR - 0.013 * yRange);
            b4->SetTextSize(0.039);
        }
        b4->SetTextAlign(33);
        b4->SetTextColor(rIdx);
        b4->AddText("fit");
        b4->SetFillColor(kWhite);

        b1.Draw("SAME");
        b2.Draw("SAME");
        b3.Draw("SAME");
        b4->Draw("SAME");
        
        c->Print(filename.c_str());
        delete b4;
        b4 = NULL;
    } 
    else c->Print(filename.c_str());

    delete c;
    c = NULL;

    //delete pad1;
    //delete pad2;
    //pad1 = NULL;
    //pad2 = NULL;
}


void ProcessHistograms::Print_1D_Histos(std::string filepath, 
                                        std::string plot_dir, 
                                        std::string title,
                                        float k_lambda)
{
    TFile *in_file = TFile::Open(filepath.c_str());
    // in_file.ls();

    for(auto k : *in_file->GetListOfKeys()) 
    {
        TKey *key = static_cast<TKey*>(k); 
        TClass *cl = gROOT->GetClass(key->GetClassName());
        if (!cl->InheritsFrom("TH1")) continue;
        TH1D *h = (TH1D*)key->ReadObj();

        std::string hist_title = key->GetName();

        if (boost::starts_with(hist_title,"h1") || boost::starts_with(hist_title,"h2")) continue;
        hist_title.erase(hist_title.length()-8);
        std::cout << hist_title << std::endl;

        BCH1D bchisto = BCH1D(h);

        // std::string filename = hist_title + "_mod.pdf";
        std::string filename = hist_title + ".pdf";

        if (hist_title == "deltalHHH_HLLHC") setdrawKappaLambdaLine(true);
        else setdrawKappaLambdaLine(false);

        setKappaLambda(k_lambda);
        Modify_1D_Hist(bchisto, plot_dir+filename, title, hist_title);
    }
}

