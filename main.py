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
def produce1DFFT(signal, n, fs, fftShift):
    signalFFT = np.fft.fft(a=signal, n=n)

    frequency = np.linspace(start=0,
                            stop=fs - (fs / n),
                            num=n)

    if fftShift:
        signalFFT = np.fft.fftshift(signalFFT)

        frequency = np.linspace(start=int(-fs / 2),
                            stop=(fs / 2) - (fs / n),
                            num=n)

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
    signalFFT = np.zeros([fftSamples, signal.shape[1]],dtype=np.complex_)

    fftShift = False
    freqAxis = produce1DFFT(signal=signal[:, i], 
                            n=fftSamples, 
                            fs=fs, 
                            fftShift=fftShift)[1]

    print(len(freqAxis))

    for i in range(signal.shape[1]):
        signalFFT[:, i] = produce1DFFT(signal=signal[:, i], 
                                       n=fftSamples, 
                                       fs=fs,
                                       fftShift=fftShift)[0]

    # Animation Figure
    fig, ax = plt.subplots(nrows=2,ncols=1)
    ax[0].set_ylim([-amplitude, amplitude])
    ax[0].set_xlim([0, pulseWidth])
    ax[1].set_ylim([0, 20])
    
    timeDomainPlot, = ax[0].plot(time, 
                    signal[:, 0], 
                    label=str(round(freqSweep[0] / fs, 2)) + r"$f_{s}$", 
                    zorder=10)
    timeDomainPlot.set_marker("o")
    timeDomainPlot.set_color('b')
    timeDomainPlot.set_markeredgecolor('b')

    leg = ax[0].legend(loc=1)
    leg.set_title("Frequency")
    leg.set_zorder(20)

    freqDomainPlot, = ax[1].plot(freqAxis,
                      np.abs(signalFFT[:, 0]))                        
    freqDomainPlot.set_marker("o")
    freqDomainPlot.set_color('b')
    freqDomainPlot.set_markeredgecolor('b')

    def animate(i):
        timeDomainPlot.set_ydata(signal[:, i])
        leg.get_texts()[0].set_text(
                           str(round(freqSweep[i] / fs, 2)) + r'$f_{s}$')
        leg.set_zorder(20)

        freqDomainPlot.set_ydata(np.abs(signalFFT[:, i]))

        return timeDomainPlot, leg, freqDomainPlot

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
