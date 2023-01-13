# ----------------------------------------------------------------------------
# Title:   Visualize Aliasing
# Author:  Kyle Kanaly
# Purpose: Fun
# ----------------------------------------------------------------------------
import math
import numpy as np
import matplotlib.pylab as plt
import matplotlib.animation as animation

# ----------------------------------------------------------------------------
def main():
    
    # Parameters
    fs = 20
    ts = 1 / fs
    T = 4
    amplitude = 1.2
    freqStep = 0.01
    frameRate = 120
    frameDelay = 1 / frameRate

    # Execution
    time = np.linspace(start=0, 
                       stop=(T - ts), 
                       num=(int(T / ts)))
    freqSweep = np.linspace(start=0, 
                            stop=(fs - freqStep), 
                            num=(int(fs / freqStep)))

    # signal = np.sin(2 * math.pi * time * freqSweep[0])
    signal = np.sin(2 * math.pi * time * 2)

    fig, ax = plt.subplots()
    ax.set_ylim([-amplitude, amplitude])
    ax.set_xlim([0, T])
    
    line, = ax.plot(time, signal, label=str(freqSweep[0]), zorder=10)
    line.set_marker("o")
    line.set_color('b')
    line.set_markeredgecolor('b')

    leg = ax.legend(loc=1)
    leg.set_title("Frequency")
    leg.set_zorder(20)

    def animate(i):
        print(len(leg.get_texts()))

        signal = np.sin(2 * math.pi * time * freqSweep[i])
        line.set_ydata(signal)
        leg.get_texts()[0].set_text(str(round(freqSweep[i], 2)))
        leg.set_zorder(20)

        return line, leg,

    anime = animation.FuncAnimation(
            fig, animate, interval=frameDelay*1000, blit=True, save_count=50)

    plt.show()

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
