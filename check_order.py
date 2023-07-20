import numpy as np
import itertools
import matplotlib.pyplot as plt


def align_signals(time, main_signal, move_signal, period, expected_phase_shift, sampling_time):
    """
    Aligns two given signals and calculates their average absolute difference. IT EXPECTS THE PHASE SHIFT IN UNITS OF 1
        (eg. if signals differ in phase by pi/2, input 0.25)

    This function takes a 1D numpy array of time values, two 1D numpy arrays representing the two input signals,
    the period of the signals, and the expected phase shift between them as input. It returns the aligned portions
    of the two signals and their average absolute difference.

    Parameters
    ----------
    time : array_like
        The time values of the input data.
    main_signal : array_like
        The first input signal.
    move_signal : array_like
        The second input signal.
    period : float
        The period of the signals.
    expected_phase_shift : float
        The expected phase shift between the two signals.

    Returns
    -------
    tuple
        A tuple containing three elements: the aligned portion of the first signal, the aligned portion of the
        second signal, and their average absolute difference.
    """

    # Shift second signal to overlap with first signal
    time_shift = round((expected_phase_shift * period) / sampling_time)
    shifted_signal = np.roll(move_signal, time_shift)

    # Calculate average absolute difference between shifted signals, ignoring rolled values
    avg_abs_diff = np.mean((main_signal[time_shift:] - shifted_signal[time_shift:]) ** 2)

    return main_signal[time_shift:], shifted_signal[time_shift:], avg_abs_diff


def correct_order_checker(signal_list, time, period, sampling_time):
    sinP = signal_list[0]
    cosP = signal_list[1]
    sinN = signal_list[2]
    cosN = signal_list[3]

    # check sinP shifts correctly
    sinp_sinp = np.array([0, 0, 0])
    sinp_cosp = align_signals(time, cosP, sinP, period, 0.25, sampling_time)
    sinp_sinn = align_signals(time, sinN, sinP, period, 0.5, sampling_time)
    sinp_cosn = align_signals(time, cosN, sinP, period, 0.75, sampling_time)
    sinp_start_line = np.array([sinp_sinp[2], sinp_cosp[2], sinp_sinn[2], sinp_cosn[2]])
    print("sinP aligning check: ", sinp_start_line)

    # check cosp shifts correctly
    cosp_sinp = align_signals(time, sinP, cosP, period, 0.75, sampling_time)
    cosp_cosp = np.array([0, 0, 0])
    cosp_sinn = align_signals(time, sinN, cosP, period, 0.25, sampling_time)
    cosp_cosn = align_signals(time, cosN, cosP, period, 0.5, sampling_time)
    cosp_start_line = np.array([cosp_sinp[2], cosp_cosp[2], cosp_sinn[2], cosp_cosn[2]])
    print("cosp aligning check: ", cosp_start_line)

    # check sinn shifts correctly
    sinn_sinp = align_signals(time, sinP, sinN, period, 0.5, sampling_time)
    sinn_cosp = align_signals(time, cosP, sinN, period, 0.75, sampling_time)
    sinn_sinn = np.array([0, 0, 0])
    sinn_cosn = align_signals(time, cosN, sinN, period, 0.25, sampling_time)
    sinn_start_line = np.array([sinn_sinp[2], sinn_cosp[2], sinn_sinn[2], sinn_cosn[2]])
    print("sinn aligning check: ", sinn_start_line)

    # check cosnn shifts correctly
    cosn_sinp = align_signals(time, sinP, cosN, period, 0.25, sampling_time)
    cosn_cosp = align_signals(time, cosP, cosN, period, 0.5, sampling_time)
    cosn_sinn = align_signals(time, sinN, cosN, period, 0.75, sampling_time)
    cosn_cosn = np.array([0, 0, 0])
    cosn_start_line = np.array([cosn_sinp[2], cosn_cosp[2], cosn_sinn[2], cosn_cosn[2]])
    print("cosn aligning check: ", cosn_start_line)

    alignment_matrix = np.vstack((sinp_start_line, cosp_start_line, sinn_start_line, cosn_start_line))
    alignment_matrix = np.where(alignment_matrix > 0.5, 1, 0)
    print("\nAlignment Matrix:\n", alignment_matrix)

    if np.all(alignment_matrix == 0):
        return True
    else:
        return False


def rps_order_checker(rps_data: np.ndarray):
    print("_" * 60, "order checker", "_" * 60)
    time = rps_data[100000:100100, 0]  #  np.linspace(25, 25.01, 100)
    sampling_time = np.mean(np.diff(time))
    sampling_freq = 1 / sampling_time  # Sampling frequency
    sinP = rps_data[100000:100100, 1]  # EDIT THESE INPUTS TO BE SINUSOIDAL SIGNALS TO RUN CHECK ORDER GITHUB
    cosP = rps_data[100000:100100, 3]  # EDIT THESE INPUTS TO BE SINUSOIDAL SIGNALS TO RUN CHECK ORDER GITHUB
    sinN = rps_data[100000:100100, 2]  # EDIT THESE INPUTS TO BE SINUSOIDAL SIGNALS TO RUN CHECK ORDER GITHUB
    cosN = rps_data[100000:100100, 4]  # EDIT THESE INPUTS TO BE SINUSOIDAL SIGNALS TO RUN CHECK ORDER GITHUB
    signals_list = [sinP, cosP, sinN, cosN]
    sinP = signals_list[0]
    cosP = signals_list[1]
    sinN = signals_list[2]
    cosN = signals_list[3]
    signals_list = [sinP, cosP, sinN, cosN]
    signal_names = ["sinP", "cosP", "sinN", "cosN"]
    signals = np.column_stack((sinP, sinN, cosP, cosN))

    fig12, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)
    ax1.plot(time, sinP)
    ax2.plot(time, cosP)
    ax3.plot(time, sinN)
    ax4.plot(time, cosN)
    ax5.plot(time, sinP, label="SinP")
    ax5.plot(time, cosP, label="CosP")
    ax5.plot(time, sinN, label="SinN")
    ax5.plot(time, cosN, label="CosN")
    plt.legend()

    frequencies = calculate_frequencies(time, signals)
    T = 1 / np.mean(frequencies)

    print(f"The frequencies of the signals are {frequencies}, period: {T}")

    main_signal, shifted_signal, error = align_signals(time, cosN, cosP, T, 0.5, sampling_time)
    print("\nPlotting Error: ", error, "\n")

    # fig14, (ax1) = plt.subplots()
    # ax1.plot(time[-len(main_signal) :], main_signal, label="main")
    # ax1.plot(time[-len(shifted_signal) :], shifted_signal, label="shifted")
    # ax1.legend()

    correct_order = []
    for permutation in itertools.permutations(signals_list):
        if correct_order_checker(permutation, time, T, sampling_time):
            correct_perm = [
                signal_names[next(i for i, x in enumerate(signals_list) if np.array_equal(x, signal))]
                for signal in permutation
            ]
            for i in correct_perm:
                correct_order.append(i)
            print("Correct order:", correct_perm)
            break

    print("=" * 120, "\n")

    if correct_order == ["sinP", "cosP", "sinN", "cosN"]:
        rps_pinning_status = [0, 0, 0, 0]
    else:
        rps_pinning_status = [1, 1, 1, 1]
    return rps_pinning_status, correct_order


# %% Toplevel Runner
if __name__ == "__main__":
    # rps_data_np_V = rps_prefilter(df_filepath_V, df_test_V, eol_test_id_V)
    # rps_zero_status = rps_signal_zero_checker(rps_data_np_V)
    # rps_short_status = rps_signal_5V_checker(rps_data_np_V)
    # rps_static_status = rps_signal_static_checker(rps_data_np_V)
    rps_order_status = rps_order_checker(rps_data_np_V)
    print("_" * 60, "Results", "_" * 60)
    # print(rps_zero_status)
    # print(rps_short_status)
    # print(f"Overall Results: {rps_static_status[0]}")
    # print(f"Average Status: {rps_static_status[1]}")
    # print(f"Differential Status: {rps_static_status[2]}")
    # print(f"Non Normal Times: {rps_static_status[3]}")
    # print(f"Differential RMS values: {rps_static_status[4]}")
    print(f"Pinning Status: {rps_order_status[0]}")
    print(f"Current Order of Pinning: {rps_order_status[1]}")
    print("=" * 120, "\n")
    plt.show()
