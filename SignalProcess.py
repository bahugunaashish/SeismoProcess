# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------

Created on Thu Jun  1 14:27:01 2023

@author: Ashish Bahuguna
         Dept. of Earthqukae Engineeiring IIT Roorkee

this function process the raw data of seismogram velocity data
-------------------------------------------------------------------------------
"""
import numpy as np
from scipy.signal import butter, filtfilt
from scipy import signal
from scipy.fft import fft
from scipy.signal import welch
import matplotlib.pyplot as plt
import pandas as pd 
import os


def _initialProcess(pathName, VoltPerCount, VoltsPerUnit, dt):
    """
    Parameters
    ----------
    pathName : string
        path of the file.
    VoltPerCount : float
        .
    VoltsPerUnit : float
        .
    dt : float
        time step.

    Returns
    -------
    df : dataframe
        dataframe obtained from seismogram data.

    """
    df = pd.read_csv(pathName, comment='#', header=None, names=['Amplitude'])
    print(df)
    df['Amplitude'] = pd.to_numeric(df['Amplitude'], errors='coerce')
    df.dropna(inplace=True)

    df['Amplitude'] = df['Amplitude'] * VoltPerCount / VoltsPerUnit

    endtime = len(df) * dt
    step = np.arange(0., endtime, dt).tolist()
    df['time'] = step

    # plt.plot(df['time'], df['Amplitude'], color='blue')
    # plt.xlabel('time (s)')
    # plt.ylabel('Amplitude (m/s)')
    # plt.xlim([38, 50])
    # plt.title(pathName)
    # plt.show()
    return df

# Function 
def get_list_files(filepath):
    """
    

    Parameters
    ----------
    filepath : string ['E:/AshishBahuguna/GMPE/veocty_weak motion/']
        contain the path of the directory contains 
        all files of seismogram data.

    Returns list of files containing in filepath directory
     
    -------
    dir_list : list
        list of files containing in filepath directory.
        as ['AYR', 'CHN', 'RAJ', 'SRT']

    """
    dir_list = os.listdir(filepath)
    return dir_list

def create_path_list(dir_list, filepath):
    """
    Parameters
    ----------
    dir_list : list
        list of files containing in filepath directory.
        as ['AYR', 'CHN', 'RAJ', 'SRT']
    filepath : string ['E:/AshishBahuguna/GMPE/veocty_weak motion/']
        contain the path of the directory contains 
        all files of seismogram data.

    Returns list of files containing in filepath directory
    -------
    file_path_list : list
        list of files path.
        as 
        ['E:/AshishBahuguna/GMPE/veocty_weak motion/AYR',
         'E:/AshishBahuguna/GMPE/veocty_weak motion/CHN',
         'E:/AshishBahuguna/GMPE/veocty_weak motion/RAJ',
         'E:/AshishBahuguna/GMPE/veocty_weak motion/SRT']

    """
    file_path_list = []
    for fname in dir_list:
        _path = filepath + fname
        file_path_list.append(_path)
    return file_path_list


def _fft(df, sample_rate):
    
    window = np.hamming(len(df['Amplitude']))
    windowed_data = df['Amplitude'] * window
    fft = np.fft.fft(windowed_data)
    sample_rate = 100 # Specify the sample rate of your seismogram data
    frequencies = np.fft.fftfreq(len(df['Amplitude']), 1/sample_rate)
    return frequencies, np.abs(fft)

def _fft_Filtered(signal, sample_rate):
    
    window = np.hamming(len(signal))
    windowed_data = signal * window
    fft = np.fft.fft(windowed_data)
    sample_rate = 100 # Specify the sample rate of your seismogram data
    frequencies = np.fft.fftfreq(len(signal), 1/sample_rate) 
    
    return frequencies, np.abs(fft)

# TODO: low pass filter not completed
def _lowPassFilter (df):
    signal = df['Amplitude']
    # Apply a low-pass filter
    cutoff_freq = 5  # Cutoff frequency in Hz
    nyquist_freq = 0.5 * len(t)  # Nyquist frequency
    normalized_cutoff_freq = cutoff_freq / nyquist_freq
    b, a = butter(4, normalized_cutoff_freq, btype='low', analog=False)
    filtered_signal = filtfilt(b, a, signal)
    
   
def _bandPassFilter(df, lowcut, highcut, filter_order):
    # Generate or load the earthquake signal data
    signal = df['Amplitude'].values  # Your earthquake signal data

    # Define the filter parameters
    sampling_rate = 100  # Specify the sampling rate of the signal
    nyquist_freq = 0.5 * sampling_rate
    low = lowcut / nyquist_freq
    high = highcut / nyquist_freq

    # Design the bandpass filter
    b, a = butter(filter_order, [low, high], btype='band')

    # Apply the bandpass filter to the signal
    filtered_signal = filtfilt(b, a, signal)

    # Plot the original and filtered signals
    time = np.arange(len(signal)) / sampling_rate
    
    return filtered_signal,signal,time 
# convert velocity to acceleartion time history
def velocity_to_acceleration(velocity, dt):
    #dt = 1.0  # Time step (assumed to be 1 second here)
    acceleration = np.gradient(velocity, dt, edge_order=2)
    return acceleration


# convert  acceleartion to velocity and dispalcement time history
def Conversion_Acc(acceleration, timestep):
    velocity = np.cumsum(acceleration) * timestep  # Integrate acceleration to get velocity
    displacement = np.cumsum(velocity) * timestep  # Integrate velocity to get displacement
    return displacement,velocity
