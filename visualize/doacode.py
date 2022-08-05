# Matlab plot of Doa

### library for matlab
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
### library for doa
from tuning import Tuning
import usb.core
import usb.util

x_vals = [] # time
y_vals = [] # doa

titleFont = {
    'fontsize': 14,
    'fontweight': 'bold'
}

subFont = {
    'fontsize': 10,
    'fontweight': 'light'
}


# function that gets doa from the mic
def getDoa():
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

    if dev:
        Mic_tuning = Tuning(dev)
        print(Mic_tuning.direction)

    return(Mic_tuning.direction)

index = count()

#### graph design setup
# plt.style.use('fivethirtyeight') # template

# animates the graph 
def animate(i):

    doa = getDoa()
    x_vals.append(next(index))
    y_vals.append(doa)

    plt.plot(x_vals, y_vals, color = "#f54293", linewidth = 3)


    

#### graph design setup
# graph title 
plt.title('Direction of Arrival', fontdict = titleFont)

# labels
plt.xlabel('Time', fontdict = subFont)
plt.ylabel('Angle', fontdict = subFont)
# ticks
plt.ylim = ([0, 360])
plt.minorticks_on()
plt.tick_params(axis = 'both', direction = 'inout', length = 5, labelsize = 12, grid_alpha = 0.5)
plt.grid()

  
ani = FuncAnimation(plt.gcf(), animate, interval = 1000)
plt.show()
plt.cla() # clears the previous line  
