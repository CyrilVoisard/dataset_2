from scipy.signal import butter, filtfilt


def low_pass_filter(signal, order=8, cutoff=14, sampling_rate=100):
    """
    Applies a low-pass Butterworth filter to the input signal.

    Parameters:
    - signal: array-like, the input signal to filter
    - order: int, the order of the Butterworth filter (default is 8)
    - cutoff: float, the cutoff frequency in Hz (default is 14 Hz)
    - sampling_rate: float, the sampling rate of the signal in Hz (default is 100 Hz)

    Returns:
    - The filtered signal (same shape as input)
    """
    nyquist_freq = sampling_rate / 2.0  # Nyquist frequency in Hz

    # Design the Butterworth low-pass filter
    b, a = butter(N=order, Wn=cutoff / nyquist_freq, btype='low', analog=False)

    # Apply the filter
    return filtfilt(b, a, signal)