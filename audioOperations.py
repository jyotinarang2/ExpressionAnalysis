import os
import sys

import pandas as pd
import essentia

from music21 import *
from essentia.standard import *
import matplotlib
import matplotlib.pyplot as plt

from scipy.fftpack import fft
from scipy.signal import get_window

import numpy as np
import warnings
warnings.filterwarnings('ignore')
import IPython.display as ipd
import libfmp

#Libraries for plotting on top on spectrogram
from libfmp.b import color_argument_to_dict
from matplotlib import patches

import pandas as pd
import csv
import madmom
import scipy.io
import PyQt5

#Load audio using MonoLoader
def load_mono_audio_using_essentia(audio_path):
    audio = essentia.standard.MonoLoader(filename=audio_path)()
    return audio

#Load audio using stereo option
def load_stereo_audio_file_using_essentia(audio_path):
    audio, srm, _, _, brm, cm = AudioLoader(filename=audio_path)()
    return audio, srm, brm, cm

def compute_magnitude_spectrum_for_audio_file(audio_file_path, N, H):
    magnitude_spectrum = []
    spectrum = Spectrum()
    loader = essentia.standard.MonoLoader(filename=audio_file_path)
    # and then we actually perform the loading:
    audio = loader()
    w = Windowing(type = 'blackmanharris62')
    fft = FFT() # this gives us a complex FFT
    for frame in FrameGenerator(audio, frameSize=N, hopSize=H, startFromZero=True):      
        mag_spec = spectrum(w(frame))
        magnitude_spectrum.append(np.array(mag_spec))
    return np.array(magnitude_spectrum)