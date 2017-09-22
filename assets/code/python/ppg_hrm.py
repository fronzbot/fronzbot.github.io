'''
ppg_hrm.py

Author: Kevin Fronczak
Date: September 22, 2017
Description: Measure heart-rate from phone camera video
'''
import os
import numpy as np
import matplotlib.pylot as plt
import imageio

# Variables to set by user
filename = 'ppg-resting'
videofile = '{}/{}.mp4'.format(os.getcwd(), filename)
fps = 30 # frames-per-second from video
PLOT = True # should eacch graph be plotted?
SAVE = True # should each graph be saved (will only be saved if PLOT is set to true)

# Set up plotting
plt.style.use('fivethirtyeight')

# Pull video into array
video = imageio.get_reader(videofile, 'ffmpeg')

# Iterate over video and extract red/blue/green channels
colors = {'red': [], 'green': [], 'blue': []}
for frame in video:
    # Average all pixels
    lumped_pixel = np.mean(frame, axis=(0,1))
    colors['red'].append(lumped_pixel[0])
    colors['green'].append(lumped_pixel[1])
    colors['blue'].append(lumped_pixel[2])

# Normalize red/green/blue channels to 255
for key in colors:
    colors[key] = np.divide(colors[key], 255)
    
# Convert frames to time
x = np.arange(len(colors['red'])) / fps

# Perform simple high-pass filter on data
colors['red_filt'] = list()
colors['red_filt'] = np.append(colors['red_filt'], colors['red'][0])
tau = 0.25 # HPF time constant in seconds
fsample = fps # Sample rate
alpha = tau / (tau + 2/fsample)
for index, frame in enumerate(colors['red']):
    if index > 0:
        y_prev = colors['red_filt'][index - 1]
        x_curr = colors['red'][index]
        x_prev = colors['red'][index - 1]
        colors['red_filt'] = np.append(colors['red_filt'], alpha * (y_prev + x_curr - x_prev))

# Want to truncate data since beginning of series will be wonky
x_filt = x[50:-1]
colors['red_filt'] = colors['red_filt'][50:-1]

# Take FFT to get frequency information
red_fft = np.absolute(np.fft.fft(colors['red_filt']))
N = len(colors['red_filt'])
freqs = np.arange(0,fsample/2,fsample/N)

# Truncate to fs/2
red_fft = red_fft[0:len(freqs)]

# Get heartrate from FFT
max_val = 0
max_index = 0
for index, fft_val in enumerate(red_fft):
    if fft_val > max_val:
        max_val = fft_val
        max_index = index

heartrate = freqs[max_index] * 60        
print('Estimated Heartate: {} bpm'.format(heartrate))


# Plotting
if PLOT:
    plt.figure(figsize=(16,9))
    plt.plot(x, colors['red'], color='#fc4f30')
    plt.xlabel('Time [s]')
    plt.ylabel('Normalized Pixel Color')
    plt.title('Time-Series Red Channel Pixel Data')
    fig1 = plt.gcf()
    plt.show()
    if SAVE:
        plt.draw()
        fig1.savefig('./{}_time_series.png'.format(filename), dpi=200)
    
    # Plot the highpass data
    plt.figure(figsize=(16,9))
    plt.plot(x_filt, colors['red_filt'], color='#fc4f30')
    plt.xlabel('Time [s]')
    plt.ylabel('Normalized Pixel Color')
    plt.title('Filtered Red Channel Pixel Data')
    fig2 = plt.gcf()
    plt.show()
    if SAVE:
        plt.draw()
        fig2.savefig('./{}_filtered.png'.format(filename), dpi=200)
    
    # Plot the FFT
    plt.figure(figsize=(16,9))
    plt.semilogx(freqs, red_fft, color='#fc4f30')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('FFT Energy')
    plt.title('Spectrum of Filtered Red Channel with HR = {} bpm'.format(round(heartrate,1)))
    fig3 = plt.gcf()
    plt.show()
    if SAVE:
        plt.draw()
        fig3.savefig('./{}_fft.png'.format(filename), dpi=200)


