# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 10:54:43 2023

@author: Ashish Bahuguna
         Dept. of Earthqukae Engineeiring IIT Roorkee
"""
import numpy as np
from scipy.signal import butter, filtfilt
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd 
import os
from SignalProcess import _initialProcess, get_list_files, create_path_list, _fft_Filtered, _fft, _bandPassFilter
#filepath = 'E:/AshishBahuguna/GMPE/veocty_weak motion/'
#pathName ='E:/AshishBahuguna/GMPE/veocty_weak motion/CHN'

# instrument constants to convert the raw data into units engineering 
sample_rate = 100
dt = 1/sample_rate
VoltPerCount = 0.000001586 
VoltsPerUnit = 0.008 # volt/m/s
# change accordingly
filepath = 'E:/AshishBahuguna/GMPE/veocty_weak motion1/' 

# instrument constants to convert the raw data into units engineering 
sample_rate = 100
dt = 1/sample_rate
VoltPerCount = 0.000001586 
VoltsPerUnit = 0.008 # volt/m/s

#get the filename and path list
dir_list = get_list_files(filepath)
file_path_list = create_path_list(dir_list, filepath)

#create raw  
for pathName in file_path_list:
    df = _initialProcess(pathName, VoltPerCount, VoltsPerUnit, dt)
    
    
    #FFT of original data
    frequencies1, fft_original = _fft(df,sample_rate)
    
    #Filtering of Data
    lowcut = 0.8 #low cut  freqency
    highcut = 15 #high pass frequency
    filter_order = 2 # other filter_order = butter, cheby1, cheby2, ellip, bessel
    filtered_signal, signal, time= _bandPassFilter(df,lowcut, highcut, filter_order)
    
    #FFT of filtered data
    frequencies2, fft_filt = _fft_Filtered(filtered_signal, sample_rate)
    
   # print('==============================================================\n')
    print('\n==================Processing complete=======================')
    print('\n==================input used in this======================== \n')
    print('lowcut frequency = ',  lowcut)
    print('highcut frequency = ',  highcut)
    print('filter_order = ',  filter_order)
    print('Sample Rate = ', sample_rate)
    print('VoltPerCount = ', 0.000001586)
    print('VoltsPerUnit = ', 0.008)
    print('\nStation Name = ',pathName[-3:])
    #plot original time series
    plt.figure(figsize=(8, 8))
    plt.subplot(3, 2, 1)
    plt.plot(df['time'], df['Amplitude'], color='blue')
    plt.xlabel('time (s)')
    plt.ylabel('Amplitude (m/s)')
    plt.xlim([38, 50])
    plt.title(pathName [-3:]+ ' original Velocity')
    plt.grid(True)
    #plt.show()
    
    plt.subplot(3, 2, 2)
    plt.plot(frequencies1, fft_original, label='Original')
    plt.xlabel('Frequeny (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 50)
    plt.ylim(0,20)
    plt.title(pathName [-3:]+ ' original Velocity FFT')
    plt.grid(True)
    
    plt.subplot(3, 2, 3)
    plt.plot(time,filtered_signal, label='filtered')
    plt.xlabel('time (s)')
    plt.ylabel('Amplitude (m/s)')
    plt.xlim([38, 50])
    plt.title(pathName [-3:]+ ' filtered Velocity')
    plt.grid(True)
    
    plt.subplot(3, 2, 4)
    plt.plot(frequencies2, fft_filt, label='Filtered')
    plt.xlabel('Frequeny (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 10)
    plt.ylim(0,20)
    plt.title('Filtered FFT of ' + pathName[-3:])
    plt.grid(True)
    
    plt.subplot(3, 2, 5)
    plt.plot(time, signal, label='Original Signal')
    plt.plot(time, filtered_signal, label='Filtered Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Original and Filtered Signals')
    plt.xlim(25,75)
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 2, 6)
    plt.plot(frequencies1, fft_original, label='Original')
    plt.plot(frequencies2, fft_filt, label='Filtered')
    plt.xlabel('Frequeny (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 10)
    plt.ylim(0,20)
    plt.title('Original and Filtered FFT of ' + pathName[-3:])
    plt.legend()
    plt.grid(True)
    
    
    plt.tight_layout()
    plt.grid(True)
    plt.show()

