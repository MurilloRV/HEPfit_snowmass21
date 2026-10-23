
import numpy as np
sqrt = np.sqrt

from math import floor, log10

def format_sig(x, sig=6):
    if x == 0:
        return "0"

    decimals = max(0, sig - 1 - floor(log10(abs(x))))
    s = f"{x:.{decimals}f}"
    return s.rstrip('0')#.rstrip('.')

###########################################################################################
###########################################################################################
#######################################   EWPOs   #########################################
###########################################################################################
###########################################################################################

file_dir = "./GIMR/"

# Snowmass 2021 projections
# updated_projections = {
#     "Mw"     : [0.25e-3, 0.3e-3],
#     "GammaW" : [1.2e-3, 0.3e-3],

#     "Mz"     : [0.004e-3, 0.1e-3],
#     "GammaZ" : [0.004e-3, 0.025e-3],

#     "Aelectron" : [0.70e-5, 2.00e-5],
#     "Amu"       : [2.30e-5, 2.20e-5],
#     "Atau"      : [0.50e-5, 20.0e-5],
#     "Abottom"   : [2.40e-5, 21.0e-5],
#     "Acharm"    : [20.0e-5, 15.0e-5],

#     "sigmaHadron" : [0.035e-3, 4.0e-3],

#     "Relectron" : [0.004e-3,  0.3e-3],
#     "Rmu"       : [0.003e-3,  0.05e-3],
#     "Rtau"      : [0.003e-3,  0.1e-3],
#     "Rbottom"   : [0.0014e-3, 0.3e-3],
#     "Rcharm"    : [0.015e-3,  1.5e-3],
# }

# Updated projections 
updated_projections = {
    "Mw"     : [0.18e-3, 0.16e-3],
    "GammaW" : [0.27e-3, 0.2e-3],

    "Mz"     : [0.004e-3, 0.1e-3],
    "GammaZ" : [0.004e-3, 0.012e-3],

    "Aelectron" : [13.5e-6],
    "Amuon"       : [32.0e-6],
    "Atau"      : [34.0e-6],
    "Abottom"   : [98.0e-6],
    "Acharm"    : [60.0e-6],

    "sigmaHadron" : [0.030e-3, 0.8e-3],

    "Relectron" : [3.4e-6,  2.3e-6],
    "Rmuon"       : [2.4e-6,  2.3e-6],
    "Rtau"      : [2.7e-6,  2.3e-6],
    "Rbottom"   : [1.2e-6,  1.6e-6],
    "Rcharm"    : [1.4e-6,  2.2e-6],
}

input_files =  [
               file_dir + "ObservablesEW_FCCee_WW_SM",
               file_dir + "ObservablesEW_FCCee_Zpole_SM",
               ]

output_files = [
               file_dir + "ObservablesEW_FCCee_WW_SM_updated_lumi",
               file_dir + "ObservablesEW_FCCee_Zpole_SM_updated_lumi",
              ]


for input_file, output_file in zip(input_files, output_files):
    input_file = input_file  + ".conf"
    output_file = output_file + ".conf"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith("Observable"):
                # Split the line into columns by whitespace
                columns = line.split()
                
                obs = columns[2]
                if (obs in updated_projections.keys()):
                    if len(updated_projections[obs]) == 1:
                        # If only one uncertainty is provided, assume it's the total uncertainty
                        combined_unc = updated_projections[obs][0]
                    else:
                        stat_unc = updated_projections[obs][0]
                        syst_unc = updated_projections[obs][1]
                        combined_unc = sqrt(stat_unc**2 + syst_unc**2)

                    if obs.startswith("R"):
                        # For R observables, what is given is the relative uncertainty
                        columns[9] = format_sig(combined_unc * float(columns[8]))
                    else:
                        columns[9] = format_sig(combined_unc)

                # Rejoin the columns and write to the output file
                outfile.write(" ".join(columns) + "\n")
            else:
                # Write unmodified lines to the output file
                outfile.write(line)

        print(f"Modified content saved to {output_file}.")



###########################################################################################
###########################################################################################
################################   Diboson Observables   ##################################
###########################################################################################
###########################################################################################

# Will scale the inverse covariance matrices by the appropriate luminosity scaling factor, since the uncertainties scale as 1/sqrt(L)
# Some matrices have negative eigenvalues; to avoid any issues, this will be handled by diagonalizing the matrix and setting the negative eigenvalues to zero before scaling and reconstructing the matrix.

luminosity_old  = {
    90:  150,  #ab^-1, unused, but kept for reference
    161: 10,   #ab^-1
    240: 5,    #ab^-1
    365: 1.5,  #ab^-1
}

luminosity_new = {
    90:  205,   #ab^-1, unused, but kept for reference
    161: 19.2,  #ab^-1
    240: 10.8,  #ab^-1
    365: 2.7,   #ab^-1
}

input_files =  [
    file_dir + "ObservablesVV_OO_FCCee_161",
    file_dir + "ObservablesVV_OO_FCCee_240",
    file_dir + "ObservablesVV_OO_FCCee_365",
    file_dir + "aTGC_observables_Current",
    file_dir + "aTGC_observables_HLLHC_Full",
]

# Scaling factors for the observable uncertainties
scaling_factors = [
    np.sqrt(luminosity_old[161] / luminosity_new[161]),
    np.sqrt(luminosity_old[240] / luminosity_new[240]),
    np.sqrt(luminosity_old[365] / luminosity_new[365]),
    1.,
    1.,
]

output_files = [ file + "_updated_lumi" for file in input_files ]


def rewrite_observable_line(
    line, 
    outfile, 
    scaling_factor,
    column_widths=None,
):
    # Split the line into columns by whitespace
    columns = line.split()
    if len(columns) < 8 or columns[6] != "MCMC" or columns[7] != "weight":
        return line  # Skip lines with observables not considered in the MCMC fit

    uncertainty = float(columns[9])
    scaled_uncertainty = uncertainty * scaling_factor
    columns[9] = format_sig(scaled_uncertainty) + " "

    # Rejoin the columns and write to the output file
    if column_widths is None:
        outfile.write(" ".join(columns) + "\n")
    else:
        # Format each column to have the same width as the maximum width for that column
        formatted_columns = [f"{col:<{width+1}}" for col, width in zip(columns, column_widths)]
        outfile.write(" ".join(formatted_columns) + "\n")



def force_positive_definiteness(matrix):
    # Diagonalize the matrix
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    
    # Set negative eigenvalues to zero
    eigenvalues[eigenvalues < 0] = 1e-3 * np.abs(eigenvalues[eigenvalues < 0])  # Set to a small positive value instead of zero to avoid singularity
    
    # Reconstruct the matrix
    positive_definite_matrix = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T
    
    return positive_definite_matrix


for input_file, output_file, scaling_factor in zip(input_files, output_files, scaling_factors):

    input_file += ".conf"
    output_file += ".conf"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:

        for line_idx, line in enumerate(infile):
            if line.startswith("CorrelatedGaussianObservables "):
                columns = line.split()
                n_corr_obs = int(columns[2])
                outfile.write(line)

                obs_lines = [next(infile) for _ in range(n_corr_obs)]

                corr_matrix_lines = [next(infile) for _j in range(n_corr_obs)]
                corr_matrix = [line.split() for line in corr_matrix_lines]
                corr_matrix = np.array(corr_matrix, dtype=float)

                for obs_line in obs_lines:
                    rewrite_observable_line(obs_line, outfile, scaling_factor=scaling_factor)

                for line in corr_matrix_lines:
                    outfile.write(line)

            elif line.startswith("ObservablesWithCovarianceInverse "):
                columns = line.split()
                n_corr_obs = int(columns[2])
                outfile.write(line)

                obs_lines = [next(infile) for _ in range(n_corr_obs)]
                columns = [obs_line.split() for obs_line in obs_lines]
                column_widths = [max(len(r[i]) for r in columns) for i in range(len(columns[0]))]

                inv_cov_matrix_lines = [next(infile) for _j in range(n_corr_obs)]
                inv_cov_matrix = [line.split() for line in inv_cov_matrix_lines]
                inv_cov_matrix = np.array(inv_cov_matrix, dtype=float)

                # Ensure the inverse covariance matrix has no negative eigenvalue
                inv_cov_matrix = force_positive_definiteness(inv_cov_matrix)

                scaled_inv_cov_matrix = inv_cov_matrix / (scaling_factor ** 2)
                inv_cov_matrix_lines_scaled = [" ".join(str(x) for x in row) + "\n" for row in scaled_inv_cov_matrix]
                
                for obs_line in obs_lines:
                    rewrite_observable_line(obs_line, outfile, scaling_factor=1.0, column_widths=column_widths)

                # for line in inv_cov_matrix_lines_scaled:
                for line in inv_cov_matrix_lines_scaled:
                    outfile.write(line)

            elif line.startswith("Observable "):
                columns = line.split()
                rewrite_observable_line(line, outfile, scaling_factor)
            else:
                # Write unmodified lines to the output file
                outfile.write(line)

        print(f"Modified content saved to {output_file}.")


