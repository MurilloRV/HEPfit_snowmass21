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
#include <TLegend.h>
#include <TLegendEntry.h>
#include <TAxis.h>
#include <TGaxis.h>
#include <TArrayD.h>
#include <TGraphAsymmErrors.h>
#include <iomanip>
#include <stdexcept>

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
        bool drawGlobalModes,
        bool setRangeKLambda,
        bool drawKLambdaErrorProjection,
        bool only_relevant_plots) {

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
    this->setRangeKLambda = setRangeKLambda;
    this->drawKLambdaErrorProjection = drawKLambdaErrorProjection;
    this->only_relevant_plots = only_relevant_plots;

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
    std::ifstream infile;
    try {
        infile = std::ifstream(filepath.c_str());
        if (!infile) throw std::runtime_error("\nERROR: " + filepath + " does not exist.");
    }
    catch(const std::runtime_error &e) {
        std::cout << e.what() << std::endl;
        return;
    }

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

            Double_t global_mode = std::stof(global_mode_str);
            Global_Modes[obs] = global_mode;
            // std::cout << obs << Global_Modes[obs] << std::endl;
        }
        else break;
    }

    infile.close();

}

Double_t ProcessHistograms::ShiftX(Double_t x, Double_t xmin, Double_t xmax, Double_t xmin_new, Double_t xmax_new)
{
    Double_t shifted_x;
    shifted_x = (xmax_new - xmin_new)/(xmax - xmin)*(x - xmin) + xmin_new ;
    return shifted_x;
}

void ProcessHistograms::ShiftAxis(TAxis *a, Double_t (*Shift)(Double_t, Double_t, Double_t, Double_t, Double_t), Double_t xmin, Double_t xmax, Double_t xmin_new, Double_t xmax_new)
{
  if (!a) return; // just a precaution
  if (a->GetXbins()->GetSize())
    {
      // an axis with variable bins
      // note: bins must remain in increasing order, hence the "Scale"
      // function must be strictly (monotonically) increasing
      TArrayD X(*(a->GetXbins()));
      for(Int_t i = 0; i < X.GetSize(); i++) X[i] = Shift(X[i], xmin, xmax, xmin_new, xmax_new);
      a->Set((X.GetSize() - 1), X.GetArray()); // new Xbins
    }
  else
    {
      // an axis with fix bins
      // note: we modify Xmin and Xmax only, hence the "Shift" function
      // must be linear (and Xmax must remain greater than Xmin)
      a->Set( a->GetNbins(),
              Shift(a->GetXmin(), xmin, xmax, xmin_new, xmax_new), // new Xmin
              Shift(a->GetXmax(), xmin, xmax, xmin_new, xmax_new)); // new Xmax
    }
  return;
}

void ProcessHistograms::ShiftXaxis(TH1 *h, Double_t (*Shift)(Double_t, Double_t, Double_t, Double_t, Double_t), Double_t xmin, Double_t xmax, Double_t xmin_new, Double_t xmax_new)
{
  if (!h) return; // just a precaution
  ShiftAxis(h->GetXaxis(), Shift, xmin, xmax, xmin_new, xmax_new);
  return;
}



void ProcessHistograms::Modify_1D_Hist(BCH1D bch1d,
                                       std::string filename,
                                       std::string title,
                                       std::string hist_title,
                                       std::string BP_name)
{
    TCanvas * c;
    cindex++;
    c = new TCanvas(TString::Format("c_bch1d_%d",cindex), TString::Format("c_bch1d_%d",cindex), 800, 600);
    TPad * pad1 = new TPad("pad1", "pad1", 0.0, 0.90, 1.0, 1.0);
    TPad * pad2 = new TPad("pad2", "pad2", 0.0, 0.0 , 1.0, 0.92);
    pad1->Draw();
    pad1->SetBottomMargin(0.0);
    pad2->Draw();
    pad2->SetBottomMargin(0.15);
    pad2->SetTopMargin(0.02);


    pad1->cd();
    TPaveText *t = new TPaveText(0., 0., 1., 1., "NDC");
    t->AddText(title.c_str());
    t->SetTextAlign(22);
    t->SetTextSize(0.5);
    t->SetBorderSize(0);
    t->SetFillColor(gStyle->GetTitleFillColor());
    t->Draw("same");


    pad2->cd();
    bch1d.GetHistogram()->Scale(1./bch1d.GetHistogram()->Integral("width"));
    // bch1d.GetHistogram()->SetTitle(title.c_str());
    // gStyle->SetOptTitle(1);

    if (drawGlobalModes) bch1d.SetGlobalMode(Global_Modes[hist_title]);

    const std::string draw_args = "HISTsame";
    bch1d.SetROOToptions(draw_args);
    bch1d.SetBandType(BCH1D::kSmallestInterval);
    bch1d.SetBandColor(0, gIdx);
    bch1d.SetBandColor(1, rIdx);
    bch1d.SetBandColor(2, kOrange - 3);
    bch1d.SetNBands(3);
    bch1d.SetNSmooth(nSmooth);
    bch1d.SetDrawGlobalMode(drawGlobalModes);
    bch1d.SetDrawMean(true, true);
    // bch1d.SetDrawLegend(!noLegend);
    bch1d.SetDrawLegend(false);
    // gStyle->SetOptStat("emr");
    // gStyle->SetOptStat(0);
    bch1d.SetNLegendColumns(1);
    bch1d.SetStats(false);


    TLine *kappa_line = NULL;
    TGraphAsymmErrors *kappa_errors = NULL;
    TH1D * ghosthist = NULL;
    if (hist_title == "deltalHHH_HLLHC") {

        ghosthist = new TH1D("", "", 100, KappaLambda_range_low - 1, KappaLambda_range_high - 1);
        gStyle->SetOptStat(0);
        ghosthist->GetYaxis()->SetLabelSize(0.055);
        ghosthist->GetYaxis()->SetTitleSize(0.055);
        ghosthist->GetXaxis()->SetLabelOffset(999);  // Hide labels
        ghosthist->GetXaxis()->SetTitleOffset(999);  // Hide title
        ghosthist->SetMaximum(bch1d.GetHistogram()->GetMaximum()*1.);
        ghosthist->GetYaxis()->SetRangeUser(0, bch1d.GetHistogram()->GetMaximum()*1.);
        std::cout << bch1d.GetHistogram()->GetMaximum() << std::endl;
        ghosthist->Draw("");

        bch1d.GetHistogram()->GetXaxis()->SetRangeUser(KappaLambda_range_low - 1, KappaLambda_range_high - 1);

        if (drawKappaLambdaLine) {
            kappa_line = new TLine(KappaLambda-1, 0., KappaLambda-1, 1.35*bch1d.GetHistogram()->GetMaximum());
            kappa_line->SetLineStyle(7);
            kappa_line->SetLineWidth(5);
            // kappa_line->SetLineColor(kMagenta+3);


            std::stringstream stream;
            stream << std::fixed << std::setprecision(2) << KappaLambda;
            std::string KappaLambda_str = stream.str();
            TLegendEntry* leg_line = bch1d.AddLegendEntry(kappa_line, "Model value (#kappa_{#lambda}="+KappaLambda_str+")", "L");
            leg_line->SetLineStyle(kappa_line->GetLineStyle());
            leg_line->SetLineWidth(kappa_line->GetLineWidth());
            leg_line->SetLineColor(kappa_line->GetLineColor());
        }

        if (drawKLambdaErrorProjection) {
            const int n = 1;
            Double_t x[n] = {KappaLambda-1};
            Double_t y[n] = {1.15*bch1d.GetHistogram()->GetMaximum()};
            Double_t exl[n] = {KappaLambda_err_low};
            Double_t eyl[n] = {0.0};
            Double_t exh[n] = {KappaLambda_err_high};
            Double_t eyh[n] = {0.0};
            kappa_errors = new TGraphAsymmErrors(n,x,y,exl,exh,eyl,eyh);
            kappa_errors->SetMarkerColor(kGreen+2);
            kappa_errors->SetMarkerStyle(21);
            kappa_errors->SetMarkerSize(1.5);
            kappa_errors->SetLineColor(kGreen+2);
            kappa_errors->SetLineWidth(3);
            gStyle->SetEndErrorSize(10);
            // kappa_errors->SetError(0.5);
            TLegendEntry* leg_gr = bch1d.AddLegendEntry(kappa_errors, "Projected uncertainty at HL-LHC", "LP");
            leg_gr->SetLineStyle(kappa_line->GetLineStyle());
            leg_gr->SetLineWidth(kappa_line->GetLineWidth());
            leg_gr->SetLineColor(kappa_line->GetLineColor());
        }
    }

    bch1d.Draw();
    
    if (kappa_line) kappa_line->Draw("same");
    if (kappa_errors) kappa_errors->Draw("SAMELP");
    gPad->Modified();
    gPad->Update();
    


    // h->GetXaxis()->SetTitle("(#kappa_{#lambda} - 1)");
    // bch1d.GetHistogram()->GetXaxis()->SetTitle("#kappa_{#lambda}");


    bool noLegend_old = true;
    double xL, yL, xRange, yRange;
    double x_min = bch1d.GetHistogram()->GetXaxis()->GetXmin();
    double x_max = bch1d.GetHistogram()->GetXaxis()->GetXmax();
    TGaxis* custom_axis = NULL;
    if (hist_title == "deltalHHH_HLLHC") {

        bch1d.GetHistogram()->GetXaxis()->SetLabelOffset(999);  // Hide labels
        bch1d.GetHistogram()->GetXaxis()->SetTitleOffset(999);  // Hide title
        bch1d.GetHistogram()->GetXaxis()->SetTickLength(0);    // Hide tick marks

        x_min = KappaLambda_range_low - 1;  //bch1d.GetHistogram()->GetXaxis()->GetXmin();
        x_max = KappaLambda_range_high - 1;  //bch1d.GetHistogram()->GetXaxis()->GetXmax();
        double shift = -1.0;  // Amount to shift the axis labels

        // Draw a custom X-axis with shifted labels
        custom_axis = new TGaxis(
            x_min, 0,       // Starting point (x, y)
            x_max, 0,       // Ending point (x, y)
            x_min - shift,  // Minimum of shifted axis
            x_max - shift,  // Maximum of shifted axis
            510, ""       // Number of divisions, and remove default labels
        );
        custom_axis->SetLabelSize(0.055); // Adjust label size
        custom_axis->SetLabelFont(42);
        custom_axis->SetTitle("#kappa_{#lambda}");
        custom_axis->SetTitleSize(0.06);
        bch1d.GetHistogram()->ResetStats();

        custom_axis->Draw("SAME"); 
    }

    std::cout << bch1d.GetHistogram()->GetMaximum() << std::endl;
    TLegend legend = bch1d.GetLegend();
    if (!noLegend) { legend.Draw("SAME"); }
    double ymin = gPad->GetUymin();
    double ymax = gPad->GetUymax();
    std::cout << "ymax" << ymax << std::endl;
    // std::cout << ymin << std::endl;
    // std::cout << ymax << std::endl;
    if (gPad->GetLogy()) {
        ymin = pow(10, ymin);
        ymax = pow(10, ymax);
    }
    bch1d.GetHistogram()->GetYaxis()->SetRangeUser(ymin, ymax * (1.15 + legend.GetTextSize()*legend.GetNRows()) * 1.05);
    if (hist_title == "deltalHHH_HLLHC") ghosthist->GetYaxis()->SetRangeUser(ymin, ymax * (1.15 + legend.GetTextSize()*legend.GetNRows()) * 1.05);
    gPad->Update();
    legend.SetX1NDC(0.55);   // Bottom-left x-coordinate
    legend.SetY1NDC(0.83);   // Bottom-left y-coordinate
    legend.SetX2NDC(0.895);  // Top-right x-coordinate
    legend.SetY2NDC(0.965);   // Top-right y-coordinate
    legend.SetTextSize(0.027);
    // legend.Update();
    gPad->Modified();



    TBox b1, b2;
    TPaveText b3;
    TPaveText * b4 = NULL;
    if (printLogo) {

        xRange = (x_max - x_min)*3./4.;
        yRange = (bch1d.GetHistogram()->GetMaximum() - bch1d.GetHistogram()->GetMinimum());

        std::cout << bch1d.GetHistogram()->GetMaximum() << std::endl;
        // std::cout << yRange << std::endl;

        
        if (noLegend_old) xL = x_min + 0.0475*xRange;
        else xL = x_min + 0.0375 * xRange;
        yL = bch1d.GetHistogram()->GetYaxis()->GetXmin() + 0.89 * yRange;
        // std::cout << yL << std::endl;

        double xR;
        if (noLegend_old) xR = xL + 0.21*xRange;
        else xR = xL + 0.18 * xRange;
        double yR = yL + 0.09 * yRange;
        // std::cout << yR << std::endl;

        b1 = TBox(xL, yL, xR, yR);
        b1.SetFillColor(gIdx);

        b2 = TBox(xL+0.008*xRange, yL+0.008*yRange, xR-0.008*xRange, yR-0.008*yRange);
        b2.SetFillColor(kWhite);

        b3 = TPaveText(xL+0.014*xRange, yL+0.013*yRange, xL+0.70*(xR-xL), yR-0.013*yRange);
        if (noLegend_old) b3.SetTextSize(0.056);
        else b3.SetTextSize(0.051);
        b3.SetTextAlign(22);
        b3.SetTextColor(kWhite);
        b3.AddText("HEP");
        b3.SetFillColor(rIdx);

        if (noLegend_old) {
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


        // if (hist_title == "deltalHHH_HLLHC") {
        //     bch1d.GetHistogram()->GetXaxis()->SetRangeUser(KappaLambda_range_low - 1, KappaLambda_range_high - 1);
        //     gPad->Update();
        // }

        b1.Draw("SAME");
        b2.Draw("SAME");
        b3.Draw("SAME");
        b4->Draw("SAME");
        gPad->Modified();
        gPad->Update();
    }

    c->Print(filename.c_str());
   
    if (custom_axis) delete custom_axis;
    custom_axis = NULL;

    if (b4) delete b4;
    b4 = NULL;

    if (c) delete c;
    c = NULL;

    //delete pad1;
    //delete pad2;
    //pad1 = NULL;
    //pad2 = NULL;
}


void ProcessHistograms::Print_1D_Histos(std::string filepath,
                                        std::string plot_dir,
                                        std::string title,
                                        Double_t k_lambda,
                                        Double_t k_lambda_err_low,
                                        Double_t k_lambda_err_high,
                                        Double_t k_lambda_range_low,
                                        Double_t k_lambda_range_high,
                                        std::string BP_name)
{
    
    TFile *in_file = nullptr;
    try { 
        in_file = TFile::Open(filepath.c_str()); 
        if (!in_file) throw std::runtime_error("\nERROR: " + filepath + " does not exist.");
    }
    catch(const std::runtime_error &e) {
        std::cout << e.what() << std::endl;
        return;
    }
    // in_file.ls();

    for(auto k : *in_file->GetListOfKeys())
    {
        TKey *key = static_cast<TKey*>(k);
        TClass *cl = gROOT->GetClass(key->GetClassName());
        if (!cl->InheritsFrom("TH1")) continue;
        TH1D *h = (TH1D*)key->ReadObj();

        // Double_t mean = h->GetMean();
        // Double_t std_dev = h->GetStdDev();
        // std::cout << mean << std::endl;
        // std::cout << std_dev << std::endl;

        std::string hist_title = key->GetName();

        if (boost::starts_with(hist_title,"h1") || boost::starts_with(hist_title,"h2")) continue;
        if (boost::ends_with(hist_title,"_bch_bch")) {
            hist_title.erase(hist_title.length()-8);
        } else {
            hist_title.erase(hist_title.length());
        }
        // std::cout << hist_title << std::endl;

        if (only_relevant_plots) {
            if (!(hist_title == "deltalHHH_HLLHC" || hist_title == "CH_corr" || hist_title == "CHbox_corr" || hist_title == "CHD_corr")) continue;
        }

        h->GetXaxis()->SetLabelSize(0.055);
        h->GetXaxis()->SetTitleSize(0.055);
        h->GetYaxis()->SetLabelSize(0.055);
        h->GetYaxis()->SetTitleSize(0.055);
        h->SetTitle("");


        // for (int i = 1; i <= h->GetNbinsX(); ++i) {
        //     double label_value = h->GetXaxis()->GetBinCenter(i) + 10.0;  // Shift labels by +10
        //     TString label = Form("%.1f", label_value);  // Format as a string
        //     h->GetXaxis()->SetBinLabel(i, label);
        // }

        if (hist_title == "deltalHHH_HLLHC") {

            if (setRangeKLambda) {

                // std::cout << h->GetXaxis()->GetBinCenter(h->GetMaximumBin()) << std::endl;
                if (k_lambda_range_low > k_lambda_range_high) {
                    throw std::invalid_argument("Please specify a valid range for the kappa_lambda distribution!");
                }
                // std::cout << h->GetXaxis()->GetXmin() << std::endl; 
                // std::cout << h->GetXaxis()->GetXmax() << std::endl; 
                // std::cout << k_lambda_range_low-1 << std::endl; 
                // std::cout << k_lambda_range_high-1 << std::endl; 
                // h->GetXaxis()->SetCanExtend(kTRUE);
                
                // ShiftXaxis(h, 
                //         ShiftX,
                //         h->GetXaxis()->GetXmin(),
                //         h->GetXaxis()->GetXmax(),
                //         k_lambda_range_low-1,
                //         k_lambda_range_high-1
                // );
                // h->GetXaxis()->SetLimits(k_lambda_range_low-1, k_lambda_range_high-1);
                
                
            } else {
                k_lambda_range_low  = h->GetXaxis()->GetXmin() + 1;
                k_lambda_range_high = h->GetXaxis()->GetXmax() + 1;
            }

            if (drawKLambdaErrorProjection && (k_lambda_err_low<0.0 || k_lambda_err_high<0.0 )) {
                throw std::invalid_argument("Please specify valid kappa_lambda uncertainties!");

            }

            setKappaLambda(
                k_lambda, 
                k_lambda_err_low, 
                k_lambda_err_high,
                k_lambda_range_low,
                k_lambda_range_high
            );
            // h->Print("all");
        }

        BCH1D bchisto = BCH1D(h);

        // std::string filename = hist_title + "_mod.pdf";
        std::string filename = hist_title + "_mod.pdf";

        if (hist_title == "deltalHHH_HLLHC") setdrawKappaLambdaLine(true);
        else setdrawKappaLambdaLine(false);

        // std::cout << h->GetXaxis()->GetBinCenter(h->GetMaximumBin()) << std::endl;
        Modify_1D_Hist(bchisto, plot_dir+filename, title, hist_title, BP_name);
    }
}

