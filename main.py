import numpy as np
import librosa
from scipy import signal
import IPython.display as ipd
import pandas as pd
from typing import OrderedDict
import matplotlib.pyplot as plt
import argparse

def tempo(y, sr):
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return beat_times

def convert_l_sec_to_frames(L_h_sec, Fs=22050, N=1024, H=512):
    """Convert filter length parameter from seconds to frame indices

    Notebook: C8/C8S1_HPS.ipynb

    Args:
        L_h_sec (float): Filter length (in seconds)
        Fs (scalar): Sample rate (Default value = 22050)
        N (int): Window size (Default value = 1024)
        H (int): Hop size (Default value = 512)

    Returns:
        L_h (int): Filter length (in samples)
    """
    L_h = int(np.ceil(L_h_sec * Fs / H))
    return L_h

def convert_l_hertz_to_bins(L_p_Hz, Fs=22050, N=1024, H=512):
    """Convert filter length parameter from Hertz to frequency bins

    Notebook: C8/C8S1_HPS.ipynb

    Args:
        L_p_Hz (float): Filter length (in Hertz)
        Fs (scalar): Sample rate (Default value = 22050)
        N (int): Window size (Default value = 1024)
        H (int): Hop size (Default value = 512)

    Returns:
        L_p (int): Filter length (in frequency bins)
    """
    L_p = int(np.ceil(L_p_Hz * N / Fs))
    return L_p

def make_integer_odd(n):
    """Convert integer into odd integer

    Notebook: C8/C8S1_HPS.ipynb

    Args:
        n (int): Integer

    Returns:
        n (int): Odd integer
    """
    if n % 2 == 0:
        n += 1
    return n

def hps(x, Fs, N, H, L_h, L_p, L_unit='physical', mask='binary', eps=0.001, detail=False):
    """Harmonic-percussive separation (HPS) algorithm

    Notebook: C8/C8S1_HPS.ipynb

    Args:
        x (np.ndarray): Input signal
        Fs (scalar): Sampling rate of x
        N (int): Frame length
        H (int): Hopsize
        L_h (float): Horizontal median filter length given in seconds or frames
        L_p (float): Percussive median filter length given in Hertz or bins
        L_unit (str): Adjusts unit, either 'pyhsical' or 'indices' (Default value = 'physical')
        mask (str): Either 'binary' or 'soft' (Default value = 'binary')
        eps (float): Parameter used in soft maskig (Default value = 0.001)
        detail (bool): Returns detailed information (Default value = False)

    Returns:
        x_h (np.ndarray): Harmonic signal
        x_p (np.ndarray): Percussive signal
        details (dict): Dictionary containing detailed information; returned if ``detail=True``
    """
    assert L_unit in ['physical', 'indices']
    assert mask in ['binary', 'soft']
    # stft
    X = librosa.stft(x, n_fft=N, hop_length=H, win_length=N, window='hann', center=True, pad_mode='constant')
    # power spectrogram
    Y = np.abs(X) ** 2
    # median filtering
    if L_unit == 'physical':
        L_h = convert_l_sec_to_frames(L_h_sec=L_h, Fs=Fs, N=N, H=H)
        L_p = convert_l_hertz_to_bins(L_p_Hz=L_p, Fs=Fs, N=N, H=H)
    L_h = make_integer_odd(L_h)
    L_p = make_integer_odd(L_p)
    Y_h = signal.medfilt(Y, [1, L_h])
    Y_p = signal.medfilt(Y, [L_p, 1])

    # masking
    if mask == 'binary':
        M_h = np.int8(Y_h >= Y_p)
        M_p = np.int8(Y_h < Y_p)
    if mask == 'soft':
        eps = 0.00001
        M_h = (Y_h + eps / 2) / (Y_h + Y_p + eps)
        M_p = (Y_p + eps / 2) / (Y_h + Y_p + eps)
    X_h = X * M_h
    X_p = X * M_p

    # istft
    x_h = librosa.istft(X_h, hop_length=H, win_length=N, window='hann', center=True, length=x.size)
    x_p = librosa.istft(X_p, hop_length=H, win_length=N, window='hann', center=True, length=x.size)

    if detail:
        return x_h, x_p, dict(Y_h=Y_h, Y_p=Y_p, M_h=M_h, M_p=M_p, X_h=X_h, X_p=X_p)
    else:
        return x_h, x_p

def percussive_onset(y, sr):
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    first = True
    notes = []
    for onset in onset_frames:
        # For all other notes
        if not first:
            note_duration = librosa.frames_to_time(onset, sr=sr)
            notes.append((note_duration, note_duration - prev_note_duration))
            prev_note_duration = note_duration
        # For the first note
        else:
            prev_note_duration = librosa.frames_to_time(onset, sr=sr)
            first = False
    return np.array([*notes])

def harmonic_onset(y, sr, n_fft, hop_length, fmin, fmax, n_mels, lag, max_size):
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft,
                                   hop_length=hop_length,
                                   fmin=fmin,
                                   fmax=fmax,
                                   n_mels=n_mels)
    odf_sf = librosa.onset.onset_strength(S=librosa.power_to_db(S, ref=np.max),
                                      sr=sr,
                                      hop_length=hop_length,
                                      lag=lag, max_size=max_size)
    onset_sf = librosa.onset.onset_detect(onset_envelope=odf_sf,
                                          sr=sr,
                                          hop_length=hop_length,
                                          units='time')
    onset_frames = onset_sf.tolist()
    first = True
    notes = []
    for onset in onset_frames:
      # For all other notes
      if not first:
            notes.append((onset, onset - prev_note_onset))
            prev_note_onset = onset
      # For the first note
      else:
          prev_note_onset = onset
          first = False
    return np.array([*notes])

def loudness(x, sr):
    rms = librosa.feature.rms(y=x)[0]
    loudness = (rms - np.min(rms)) / (np.max(rms) - np.min(rms))
    return loudness

def main(music_path):
    Fs = 22050
    N=1024
    H=256
    L_h_sec=0.2
    L_p_Hz=500
    
    n_fft = 1024
    hop_length = int(librosa.time_to_samples(1./200, sr=Fs))
    lag = 2
    n_mels = 138
    fmin = 27.5
    fmax = 16000.
    max_size = 3
    
    win_len_sec = 0.2
    
    x, Fs = librosa.load(music_path, sr=Fs)
    x_h, x_p = hps(x, Fs, N, H, L_h_sec, L_p_Hz)
    # x_p_onset = percussive_onset(x_p, Fs)
    x_p_onset = harmonic_onset(x_p, Fs, n_fft, hop_length, fmin, fmax, n_mels, lag, max_size)
    x_h_onset = harmonic_onset(x_h, Fs, n_fft, hop_length, fmin, fmax, n_mels, lag, max_size)
    x_loudness = loudness(x, Fs)
    x_h_loudness = loudness(x_h, Fs)
    x_p_loudness = loudness(x_p, Fs)
    np.save('values/x.npy', x)
    np.save('values/x_h.npy', x_h)
    np.save('values/x_p.npy', x_p)
    np.save('values/x_p_onset.npy', x_p_onset)
    np.save('values/x_h_onset.npy', x_h_onset)
    np.save('values/x_loudness.npy', x_loudness)
    np.save('values/x_h_loudness.npy', x_h_loudness)
    np.save('values/x_p_loudness.npy', x_p_loudness)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Music Visualizer')
    parser.add_argument('music_path', type=str, help='Path to the music file')
    music_path = parser.parse_args().music_path
    main(music_path)