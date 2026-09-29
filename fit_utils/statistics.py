
import numpy as np
import scipy

def confidence_level(nsigma):
    r"""Return the confidence level corresponding to a number of sigmas,
    i.e. the probability contained in the normal distribution between $-n\sigma$
    and $+n\sigma$.

    Example: `confidence_level(1)` returns approximately 0.68."""
    return (scipy.stats.norm.cdf(nsigma)-0.5)*2

def delta_chi2(nsigma, dof):
    r"""Compute the $\Delta\chi^2$ for `dof` degrees of freedom corresponding
    to `nsigma` Gaussian standard deviations.

    Example: For `dof=2` and `nsigma=1`, the result is roughly 2.3."""
    if dof == 1:
        # that's trivial
        return nsigma**2
    chi2_ndof = scipy.stats.chi2(dof)
    cl_nsigma = confidence_level(nsigma)
    return chi2_ndof.ppf(cl_nsigma)

def chi2_prob(chi2, dof):
    r"""Compute the probability the the chi2 value is equal or larger than `chi2'
    for `dof' degrees of freedom"""
    chi2_ndof = scipy.stats.chi2(dof)
    return 1 - chi2_ndof.cdf(chi2)

def chi2_prob_sigma(chi2, dof):
    r"""Compute the probability the the chi2 value is equal or larger than `chi2'
    for `dof' degrees of freedom"""
    chisq_probability = 1 - chi2_prob(chi2, dof)
    print(chisq_probability)
    chi2_1D = scipy.stats.chi2(1)
    return np.sqrt(chi2_1D.ppf(chisq_probability))

# print(delta_chi2(nsigma=1, dof=2))
# print(chi2_prob(6.180074, 2))

# chi2_1D = scipy.stats.chi2(1)
# print(chi2_1D.ppf(0.5))
# chi2_prob_sigma(6.18,2)
# chi2_prob_sigma(10.423363,9)

# chi2_prob_sigma(6.8, 2)
# delta_chi2(1, 9)