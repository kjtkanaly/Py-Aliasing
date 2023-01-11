# ----------------------------------------------------------------------------
# Title:   Visualize Aliasing
# Author:  Kyle Kanaly
# Purpose: Fun
# ----------------------------------------------------------------------------
import math
import numpy as np
import matplotlib.pylab as plt

# ----------------------------------------------------------------------------
def main():
    
    # Parameters
    fs = 20
    ts = 1 / fs
    T = 4
    freqStep = 0.1
    frameRate = 60
    frameDelay = 1 / frameRate

    # Execution
    time = np.linspace(start=0, 
                       stop=(T - ts), 
                       num=(int(T / ts)))
    freqSweep = np.linspace(start=0, 
                            stop=(fs - freqStep), 
                            num=(int(fs / freqStep)))

    signal = np.sin(2 * math.pi * time * freqSweep[0])

    plt.scatter(time, signal)
    plt.show()

    


if __name__ == "__main__":
    main()
