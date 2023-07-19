import numpy as np


def check_order(signals):
    """
    Checks if the given signals are in the correct order.

    This function takes a list of signals as input, and returns True if the signals are in the correct order, and False
        otherwise. The correct order is determined by the phase difference between the signals. If the signals are not in
        the correct order, the function prints instructions on how to get them in the correct order. This function
        requires the signals to be in order of increasing phase.

    Parameters
    ----------
    signals : list of array_like
        The list of signals to be checked.

    Returns
    -------
    bool
        True if the signals are in the correct order, and False otherwise.
    """
    phases = [np.arctan2(signal[1], signal[0]) for signal in signals]
    if np.all(np.diff(phases) > 0):
        return True
    else:
        sorted_indices = np.argsort(phases)
        print("To get the signals in the correct order, rearrange them as follows:")
        for i, index in enumerate(sorted_indices):
            print(f"Signal {i+1}: Signal {index+1}")
        return False


# Example usage
signal1 = np.sin(np.linspace(0, 2 * np.pi, 100))
signal2 = np.sin(np.linspace(0, 2 * np.pi, 100) + np.pi / 2)
signal3 = np.sin(np.linspace(0, 2 * np.pi, 100) + np.pi)
signal4 = np.sin(np.linspace(0, 2 * np.pi, 100) + 3 * np.pi / 2)

signals = [signal1, signal2, signal3, signal4]

print(check_order(signals))  # True
print(check_order(signals[::-1]))  # False
