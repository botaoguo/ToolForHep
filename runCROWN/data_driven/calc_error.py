import numpy as np

# 2023 m2m
# mt_W < 60 scale   590.615716972202 / 23756.522021737022, 0.02486120301750372
# 2023 e2m
# mt_W < 60 scale   577.4399063748431 / 23182.047615069707, 0.02490892590521093

input = [942.7040165795081, 32314.31469321367, 49.29317040812837, 188.88499048485457]

def error_propagation_division(x, y, sigma_x, sigma_y):
    # Calculate the value of the division
    value = x / y
    
    # Calculate the fractional uncertainties
    frac_uncertainty_x = sigma_x / abs(x)
    frac_uncertainty_y = sigma_y / abs(y)
    
    # Calculate the combined uncertainty
    combined_uncertainty = np.sqrt(frac_uncertainty_x**2 + frac_uncertainty_y**2)
    
    # Calculate the error of the division
    error_division = abs(value) * combined_uncertainty
    
    return error_division

# Example values
x = input[0]
y = input[1]
sigma_x = input[2]
sigma_y = input[3]

# Calculate the error of x/y
error = error_propagation_division(x, y, sigma_x, sigma_y)
print("x: {}".format(x))
print("x_err: {}".format(sigma_x))
print("y: {}".format(y))
print("y_err: {}".format(sigma_y))
print("x/y: {}".format(x/y))
print("Error of x/y: {}".format(error))
