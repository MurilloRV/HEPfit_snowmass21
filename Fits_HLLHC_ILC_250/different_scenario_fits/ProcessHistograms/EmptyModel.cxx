// ***************************************************************
// This file was created using the bat-project script.
// bat-project is part of Bayesian Analysis Toolkit (BAT).
// BAT can be downloaded from http://mpp.mpg.de/bat
// ***************************************************************

#include "EmptyModel.h"

// #include <BAT/BCMath.h>

// ---------------------------------------------------------
EmptyModel::EmptyModel(const std::string& name)
    : BCModel(name)
{
    // Define parameters here in the constructor.
    // Also define their priors, if using built-in priors.
    // For example:
    // AddParameter("mu", -2, 1, "#mu", "[GeV]");
    // GetParameters.Back().SetPrior(new BCGaussianPrior(-1, 0.25));

    // Define observables here, too. For example:
    // AddObservable("mu_squared", 1, 4, "#mu^{2}", "[GeV^{2}]");
}

// ---------------------------------------------------------
EmptyModel::~EmptyModel()
{
    // destructor
}

// ---------------------------------------------------------
double EmptyModel::LogLikelihood(const std::vector<double>& pars)
{
    // return the log of the conditional probability p(data|pars).
    // This is where you define your model.
    // BCMath contains many functions you will find helpful.

    return 0;
}

// ---------------------------------------------------------
// double EmptyModel::LogAPrioriProbability(const std::vector<double>& pars)
// {
//     // return the log of the prior probability p(pars)
//     // If you use built-in priors, leave this function commented out.
// }

// ---------------------------------------------------------
// void EmptyModel::CalculateObservables(const std::vector<double>& pars)
// {
//     // Calculate and store obvserables. For example:
//     GetObservable(0) = pow(pars[0], 2);
// }
