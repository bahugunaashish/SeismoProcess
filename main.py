# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 10:54:43 2023

@author: Ashish Bahuguna
         Dept. of Earthqukae Engineeiring IIT Roorkee
"""
import numpy as np
from scipy.signal import butter, filtfilt
from scipy import signal
from scipy.fft import fft
from scipy.signal import welch
import matplotlib.pyplot as plt
import pandas as pd 
import os
from SignalProcess import _initialProcess, get_list_files, Conversion_Acc, velocity_to_acceleration, create_path_list, _fft_Filtered, _fft, _bandPassFilter

#filepath = 'E:/AshishBahuguna/GMPE/veocty_weak motion/'
#pathName ='E:/AshishBahuguna/GMPE/veocty_weak motion/CHN'

# instrument constants to convert the raw data into units engineering 
# sample_rate = 100
# dt = 1/sample_rate
# VoltPerCount = 0.000001586 
# VoltsPerUnit = 0.008 # volt/m/s
# change accordingly
filepath = 'E:/AshishBahuguna/GMPE/veocty_weak motion1/' 

# instrument constants to convert the raw data into units engineering 
sample_rate = 100
dt = 1/sample_rate
VoltPerCount = 0.000001586 
VoltsPerUnit = 0.005 # volt/m/s

#get the filename and path list
dir_list = get_list_files(filepath)
file_path_list = create_path_list(dir_list, filepath)

#create raw  
for pathName in file_path_list:
    df = _initialProcess(pathName, VoltPerCount, VoltsPerUnit, dt)
       
    #FFT of original data
    frequencies1, fft_original = _fft(df,sample_rate)
    
    #Filtering of Data
    lowcut = 0.01 #low cut  freqency
    highcut = 20 #high pass frequency
    filter_order = 4 # other filter_order = butter, cheby1, cheby2, ellip, bessel
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
    fig1 = plt.figure(figsize=(8, 8))
    plt.subplot(3, 2, 1)
    plt.plot(df['time'], df['Amplitude'], color='blue', linewidth = '0.3')
    plt.xlabel('time (s)')
    plt.ylabel('Amplitude (m/s)')
    #plt.xlim([0, 50])
    plt.title(pathName [-3:]+ ' original Velocity')
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    #plt.show()
    
    plt.subplot(3, 2, 2)
    plt.plot(frequencies1, fft_original, color='blue',label='Original', linewidth = '0.2')
    plt.xlabel('Frequeny (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 50)
    plt.ylim(0,50)
    # Set the y-axis to log scale
    #plt.yscale('log')
    plt.title(pathName [-3:]+ ' original Velocity FFT')
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    plt.subplot(3, 2, 3)
    plt.plot(time,filtered_signal, color ='red', label='filtered',linewidth = '0.3')
    plt.xlabel('time (s)')
    plt.ylabel('Amplitude (cm/s)')
    #plt.xlim([0, 50])
    plt.title(pathName [-3:]+ ' filtered Velocity')
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    plt.subplot(3, 2, 4)
    plt.plot(frequencies2, fft_filt, color ='red', label='Filtered',linewidth = '0.2')
    plt.xlabel('Frequeny (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 50)
    plt.ylim(0,50)
    plt.title('Filtered FFT of ' + pathName[-3:])
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    plt.subplot(3, 2, 5)
    plt.plot(time, signal, color = 'blue',  label='Original Signal',linewidth = '0.3')
    plt.plot(time, filtered_signal, color ='red', label='Filtered Signal', linewidth = '0.3')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Original and Filtered Signals')
    #plt.xlim(0,75)
    plt.legend()
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    plt.subplot(3, 2, 6)
    plt.plot(frequencies1, fft_original, color = 'blue', label='Original', marker = '')
    plt.plot(frequencies2, fft_filt, color ='red', marker = '',label='Filtered', linewidth = '0.3')
    plt.xlabel('Frequeny (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 50)
    plt.ylim(0, 50)
    plt.title('Original and Filtered FFT of ' + pathName[-3:])
    plt.legend()
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    
    plt.tight_layout()
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    plt.show()

    acceleration = velocity_to_acceleration (filtered_signal, 0.01) # 0.01 is time step
    frequencies2, fft_filt = _fft_Filtered(acceleration, sample_rate)
    
    fig2 = plt.figure(figsize=(12, 3))
    plt.subplot(1,3,1)
    plt.plot(time,filtered_signal, color ='red', label='filtered',linewidth = '0.3')
    plt.xlabel('time (s)')
    plt.ylabel('Amplitude (cm/s)')
    #plt.xlim([38, 50])
    plt.title(pathName [-3:]+ ' Velocity')
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    plt.subplot(1,3,2)
    plt.plot(time, acceleration, color ='magenta', label='filtered',linewidth = '0.3')
    plt.xlabel('time (s)')
    plt.ylabel('Amplitude (cm/s/s)')
    #plt.xlim([0, 50])
    #plt.ylim(0, 20)
    plt.title(pathName [-3:]+ ' Acceleration')
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    plt.subplot(1,3,3)
    plt.plot(frequencies2, fft_filt, color ='black',label='Filtered',linewidth = '0.3')
    plt.xlabel('Frequeny (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 50)
    plt.ylim(0,2500)
    plt.title('Acceleration FFT of ' + pathName[-3:])
    #plt.legend()
    plt.tight_layout()
    plt.grid(True, linestyle='--', linewidth = 0.5, color='gray', alpha=0.5)
    fig1.savefig('Veocity_Acc_accFFT'+ pathName [-3:]+'.png', dpi = 500)
    fig2.savefig('processedData'+ pathName [-3:]+'.png', dpi = 500)
     
    #==========================================================================
    displacement, velocity = Conversion_Acc(acceleration, dt)
    fig3 = plt.figure(figsize=(12,3))
    
    
    plt.subplot(1,3,1)
    plt.plot(time, acceleration, color ='magenta', label='filtered',linewidth = '0.3')
    plt.xlabel('time (s)')
    plt.ylabel('Amplitude (cm/s/s)')
    #plt.xlim([0, 50])
    #plt.ylim(0, 20)
    plt.title(pathName [-3:]+ ' Acceleration')
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    plt.subplot(1,3,2)
    plt.plot(time, velocity, color ='red', label='converted_velo',linewidth = '0.3')
    plt.xlabel('time (s)')
    plt.ylabel('Amplitude (cm/s)')
    #plt.xlim([38, 50])
    plt.title(pathName [-3:]+ ' Velocity')
    plt.grid(True,linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    plt.subplot(1,3,3)
    plt.plot(time, displacement, color ='black',label='converted_dis',linewidth = '0.3')
    plt.xlabel('t (s)')
    plt.ylabel('Amplitude')
    #plt.xlim(0, 50)
    #plt.ylim(0,2500)
    plt.title('Displacment (cm) ' + pathName[-3:])
    #plt.legend()
    plt.tight_layout()
    plt.grid(True, linestyle='--', linewidth = 0.5, color='gray', alpha=0.5)
    fig1.savefig('Veocity_Acc_accFFT'+ pathName [-3:]+'.png', dpi = 500)
    fig2.savefig('processedData'+ pathName [-3:]+'.png', dpi = 500)
    fig3.savefig('conversion'+ pathName [-3:]+'.png', dpi = 500)
