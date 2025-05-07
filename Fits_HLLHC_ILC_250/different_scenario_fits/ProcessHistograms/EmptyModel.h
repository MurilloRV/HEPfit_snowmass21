// ***************************************************************
// This file was created using the bat-project script.
// bat-project is part of Bayesian Analysis Toolkit (BAT).
// BAT can be downloaded from http://mpp.mpg.de/bat
// ***************************************************************

#ifndef __BAT__EMPTYMODEL__H
#define __BAT__EMPTYMODEL__H

#include <BAT/BCModel.h>

#include <string>
#include <vector>

// This is a EmptyModel header file.
// Model source code is located in file ProcessHistograms/EmptyModel.cxx

// ---------------------------------------------------------
class EmptyModel : public BCModel
{

public:

    // Constructor
    EmptyModel(const std::string& name);

    // Destructor
    ~EmptyModel();

    // Overload LogLikelihood to implement model
    double LogLikelihood(const std::vector<double>& pars);

    // Overload LogAprioriProbability if not using built-in 1D priors
    // double LogAPrioriProbability(const std::vector<double> & pars);

    // Overload CalculateObservables if using observables
    // void CalculateObservables(const std::vector<double> & pars);

};
// ---------------------------------------------------------

#endif
