from labjack import ljm
from datetime import datetime, timedelta
import random

from collections import deque
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

# Assign the handle/address of device; Open the LabJack device ("T7" device, "COM3" connection, Any identifier)
handle = ljm.openS("ANY", "ANY", "ANY")

# Set the name of the analog input channel to read from (e.g., AIN0)
channel_name = "AIN0"

# Configure AIN0 range to +/- 10V
ljm.eWriteName(handle, "AIN0_RANGE", 10.0)

# Read the voltage from the specified analog input
voltage = ljm.eReadName(handle, channel_name)

print(f"{channel_name} voltage: {voltage:.4f} V")

# Parameters 
x_len = 40
y_range = [-2, 6]

window_size = timedelta(seconds=10)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0,40))
ys = [0] * x_len
ax.set_xlim([0, x_len])
ax.set_ylim(y_range)

line, = ax.plot(xs, ys)

# Format plot
# plt.xticks(rotation=45, ha='right')
# plt.subplots_adjust(bottom=0.30)
plt.title('LabJack Voltage over Time')
plt.ylabel('Voltage (V)')

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read voltage from LabJack
    voltage = round(ljm.eReadName(handle, channel_name), 2)

    current_time = datetime.now()
    current_val = np.sin(i * 0.2)

    xs.append(current_time)
    ys.append(voltage)

    ys = ys[-x_len:]  # Limit y list to set number of items

    # Draw x and y lists
    # ax.clear()
    line.set_ydata(xs, ys)
    # ax.plot(xs, ys)
    ax.set_xlim(current_time - window_size, current_time)
    ax.relim()
    ax.autoscale_view(y=True, x=False)
    return line,

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1, blit=False)
plt.show()