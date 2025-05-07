
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load the PNG image
image_path = 'Screenshot 2025-01-16 at 10.19.14.png'
img = mpimg.imread(image_path)

# Create a figure and axis
fig, ax = plt.subplots(figsize=(8, 7), dpi=300)

# Display the image as the background
ax.imshow(img, extent=[-4, 9.3, -6.5, 16.5], aspect='auto')  # Adjust extent to set the image coordinates

data_high = {
    "x":[-1.487,-0.986,-0.484,0.029,0.497,0.999,1.512,2.025,2.515,2.994,3.485,3.998,4.499,5.012,5.492,6.016,6.506,6.986,7.498,8.017],
    "y":[-1.091,-0.584,-0.022,0.486,1.02,1.688,2.437,4.922,5.056,5.029,5.109,5.269,5.51,5.831,6.205,6.579,7.033,7.488,7.915,8.423]
}

data_low = {
    "x":[-1.493,-0.987,-0.486,0.004,0.506,1.007,1.508,2.009,2.51,3.011,3.501,4.013,4.503,4.993,5.506,5.996,6.508,6.998,7.51,8.006],
    "y":[-1.893,-1.413,-0.933,-0.453,-0.027,0.453,0.853,1.227,1.493,1.733,1.893,1.92,1.92,2.187,4.56,5.253,5.867,6.48,7.013,7.547]
}


curve_high = interp1d(data_high["x"], data_high["y"], kind='linear', fill_value="extrapolate")
x_high = np.linspace(min(data_high["x"]), max(data_high["x"]), 100)  # Generate 100 points in the x range
y_high = curve_high(x_high)

curve_low = interp1d(data_low["x"], data_low["y"], kind='linear', fill_value="extrapolate")
x_low = np.linspace(min(data_low["x"]), max(data_low["x"]), 100)  # Generate 100 points in the x range
y_low = curve_low(x_low)

# Plot the original points and the interpolated curve
ax.scatter(data_high["x"], data_high["y"], color='tab:blue', label='Upper Limit')
ax.scatter(data_low["x"], data_low["y"], color='tab:orange', label='Lower Limit')
ax.plot(x_high, y_high, color='tab:blue', )
ax.plot(x_low, y_low, color='tab:orange', )
ax.legend()
ax.set_xlabel(r'$\kappa_{\lambda}$')
ax.set_ylabel(r'68\% $\kappa_{\lambda}$ Confidence Level')
ax.set_title('Linear Interpolation')
ax.grid()
# plt.show()
# fig.set_size_inches(40, 8)
fig.savefig("extrapolation.png", dpi=300, bbox_inches='tight', pad_inches=0.1)


def uncertanties_high(lmbd):
    if lmbd < -1.5:
        lmbd = -1.5
    elif lmbd > 8.:
        lmbd = 8.
    sigma = (curve_high(lmbd) - lmbd)/2.
    return sigma

def uncertanties_low(lmbd):
    if lmbd < -1.5:
        lmbd = -1.5
    elif lmbd > 8.:
        lmbd = 8.
    sigma = (lmbd - curve_low(lmbd))/2.
    return sigma

BPs = ["BPB_2", "BPB_4", "BPB_6"]
lambdas_BPs = [
    2.3867362274064843,
    3.3446699219962595,
    4.332584967850238,
]

# uncertainties_BPs = [[uncertanties_low(lmbd), uncertanties_high(lmbd)] for lmbd in lambdas_BPs]
# print(uncertainties_BPs)

print(uncertanties_low(3.332584967850238+1))
print(uncertanties_high(3.332584967850238+1))