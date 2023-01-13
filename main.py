# ----------------------------------------------------------------------------
# Title:   Visualize Aliasing
# Author:  Kyle Kanaly
# Purpose: Fun
# ----------------------------------------------------------------------------
# Modules
import math
import numpy as np
import matplotlib.pylab as plt
import matplotlib.animation as animation

# ----------------------------------------------------------------------------
# Next Power of 2
def nextpow2(n):
    n = np.abs(n)
    p = 0

    while (np.power(2, p) < n):
        p += 1

    return p

# ----------------------------------------------------------------------------
# Produce 1-Dimensions FFT
def produce1DFFT(signal, n, fs):
    frequency = np.linspace(start=int(-fs / 2),
                            stop=fs / 2,
                            num=n)
    signalFFT = np.fft.fftshift(np.fft.fft(a=signal, n=n))

    return signalFFT, frequency

# ----------------------------------------------------------------------------
def main():
    
    # Waveform Parameters
    fs = 20
    ts = 1 / fs
    pulseWidth = 2.0
    amplitude = 1.2
    freqStep = 0.01
    frameRate = 120
    frameDelay = 1 / frameRate

    time = np.linspace(start=0, 
                       stop=(pulseWidth - ts), 
                       num=(int(pulseWidth / ts)))
    freqSweep = np.linspace(start=0, 
                            stop=(fs - freqStep), 
                            num=(int(fs / freqStep)))

    # Generate the signal frames
    signal = np.zeros([time.shape[0], freqSweep.shape[0]])

    for i, freq in enumerate(freqSweep):
        signal[:,i] = np.sin(2 * math.pi * time * freq)

    # Generate the signal FFT frames
    fftSamples = np.power(2, nextpow2(signal.shape[0]))
    signalFFT = np.zeros([fftSamples, signal.shape[1]])

    freqAxis = produce1DFFT(signal=signal[:, i], n=fftSamples, fs=fs)[1]

    for i in range(signal.shape[1]):
        signalFFT[:, i] = produce1DFFT(signal=signal[:, i], 
                                       n=fftSamples, 
                                       fs=fs)[0]

    # Plot animation
    fig, ax = plt.subplots()
    ax.set_ylim([-amplitude, amplitude])
    ax.set_xlim([0, pulseWidth])
    
    line, = ax.plot(time, 
                    signal[:, 0], 
                    label=str(round(freqSweep[0] / fs, 2)) + r"$f_{s}$", 
                    zorder=10)
    line.set_marker("o")
    line.set_color('b')
    line.set_markeredgecolor('b')

    leg = ax.legend(loc=1)
    leg.set_title("Frequency")
    leg.set_zorder(20)

    def animate(i):
        line.set_ydata(signal[:, i])
        leg.get_texts()[0].set_text(
                           str(round(freqSweep[i] / fs, 2)) + r'$f_{s}$')
        leg.set_zorder(20)

        return line, leg,

    anime = animation.FuncAnimation(fig, 
                                    animate, 
                                    interval=frameDelay*1000, 
                                    blit=True, 
                                    save_count=50,
                                    frames=freqSweep.shape[0])

    plt.show()

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
