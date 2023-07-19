import numpy as np
from scipy.optimize import curve_fit


def check_function(x, y):
    """
    Checks if the given array represents one of several possible functions.

    This function takes a 1D numpy array of x values and a 1D numpy array of y values as input, and returns the name of
    the function that best fits the input data. The possible functions are "tan", "-tan", "sin^2", "cos^2", "-sin^2",
    and "-cos^2".

    Parameters
    ----------
    x : array_like
        The x values of the input array.
    y : array_like
        The y values of the input array.

    Returns
    -------
    str
        The name of the function that best fits the input data.
    """

    def tan_func(x, amplitude, frequency, phase, offset):
        return amplitude * np.tan(frequency * x + phase) + offset

    def sin2_func(x, amplitude, frequency, phase, offset):
        return amplitude * np.sin(frequency * x + phase) ** 2 + offset

    def cos2_func(x, amplitude, frequency, phase, offset):
        return amplitude * np.cos(frequency * x + phase) ** 2 + offset

    # Fit each function to the data and calculate MSE
    mse_values = []

    for func in [tan_func, sin2_func, cos2_func]:
        try:
            popt, _ = curve_fit(func, x, y)
            y_fit = func(x, *popt)
            mse = np.mean((y - y_fit) ** 2)
            mse_values.append(mse)
            mse_values.append(mse)  # same MSE for negative version of function
        except RuntimeError:
            mse_values.append(np.inf)
            mse_values.append(np.inf)

    # Find function with smallest MSE
    function_names = ["tan", "-tan", "sin^2", "-sin^2", "cos^2", "-cos^2"]

    min_index = np.argmin(mse_values)

    return function_names[min_index]


x = np.linspace(-np.pi / 2, np.pi / 2, 100)
y = -np.tan(x)

result = check_function(x, y)

if result == "tan":
    print("The input array represents tan(x).")
elif result == "-tan":
    print("The input array represents -tan(x).")
else:
    print("The input array does not clearly represent either tan(x) or -tan(x).")
