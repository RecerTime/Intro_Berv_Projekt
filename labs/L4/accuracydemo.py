#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from matplotlib.cbook import mplDeprecation
import warnings
from math import floor, log, log2, exp
import time

## Internal functions
def _Euler(y0, tspan, h):
    t = np.arange(tspan[0],tspan[1],h)

    y = np.zeros(t.size)
    y[0] = y0

    for tidx in np.arange(1,t.size):
        y[tidx] = y[tidx-1] + h*f(t[tidx-1],y[tidx-1])

    if not tspan[1] == t[-1]:
        hfinal = tspan[1] - t[-1]
        yfinal = y[-1] + hfinal*f(t[-1],y[-1])
        t = np.append(t, tspan[1])
        y = np.append(y, yfinal)

    return t, y

def _Heun(y0, tspan, h):
    t = np.arange(tspan[0],tspan[1],h)

    y = np.zeros(t.size)
    y[0] = y0

    for tidx in np.arange(1,t.size):
        k1 = h*f(t[tidx-1],y[tidx-1])
        k2 = h*f(t[tidx-1] + h,y[tidx-1] + k1)
        y[tidx] = y[tidx-1] + 0.5*(k1 + k2)

    if not tspan[1] == t[-1]:
        hfinal = tspan[1] - t[-1]
        k1 = f(t[-1],y[-1])
        k2 = f(t[-1] + hfinal,y[-1] + hfinal*k1)
        yfinal = y[-1] + 0.5*hfinal*(k1 + k2)

        t = np.append(t, tspan[1])
        y = np.append(y, yfinal)

    return t, y

def _RK4(y0, tspan, h):
    t = np.arange(tspan[0],tspan[1],h)

    y = np.zeros(t.size)
    y[0] = y0

    for tidx in np.arange(1,t.size):
        k1 = h*f(t[tidx-1],y[tidx-1])
        k2 = h*f(t[tidx-1] + 0.5*h,y[tidx-1] + 0.5*k1)
        k3 = h*f(t[tidx-1] + 0.5*h,y[tidx-1] + 0.5*k2)
        k4 = h*f(t[tidx-1] + h,y[tidx-1] + k3)
        y[tidx] = y[tidx-1] + 1/6*(k1 + 2*k2 + 2*k3 + k4)

    if not tspan[1] == t[-1]:
        hfinal = tspan[1] - t[-1]

        k1 = hfinal*f(t[-1],y[-1])
        k2 = hfinal*f(t[-1] + 0.5*hfinal,y[-1] + 0.5*k1)
        k3 = hfinal*f(t[-1] + 0.5*hfinal,y[-1] + 0.5*k2)
        k4 = hfinal*f(t[-1] + hfinal,y[-1] + k3)
        yfinal = y[-1] + 1./6*(k1 + 2*k2 + 2*k3 + k4)

        t = np.append(t, tspan[1])
        y = np.append(y, yfinal)

    return t, y

def polyfit(x,y,poly_order):
    X = np.vander(np.log(x),poly_order+1)
    p = np.linalg.solve(np.matmul(np.transpose(X),X),np.matmul(np.transpose(X),np.log(y)))    
    return p

# RHS function
def f(t,y):
    return t*y + t**3

# Exact solution
def yfunc(t,y0):
    return 3*np.exp((t**2)/2) - t**2 -2;

# Hide warning "Toggling axes navigation from the keyboard is deprecated..." when typing in textbox. 
warnings.filterwarnings("ignore",category=mplDeprecation)


print("---------------------------------------------------------")
print("Euler's method, Heun's method and classical Runge-Kutta method for the linear ODE")
print("     dy/dt = f(t,y), 0 < t < 1,")
print("     f(t,y) = t*y + t^3,")
print("     y(0) = 1.")
print("---------------------------------------------------------")
print("This demo program solves the ODE using Euler's method, Heun's method and classical Runge-Kutta method with multiple step sizes on the interval [1e-5,1e0]. The absolute errors of each method is plotted as a function of step size, the slopes of each curve indicate the orders of accuracy. The program also computes and prints statistics on step size, execution time and number of steps required to obtain a specified error tolerance with each method. Use the program as follows:")
print("1. Study the plot and printed information produced when running the program. Pay attention to the slopes of each curve. Also think about why there seems to be an error limit for the Runge-Kutta method.")
print("2. Choose an error tolerance, type in the text box, and press 'Get statistic'. The program will find the step size required to obtain this accuracy and perform statistical measurements for each method. Study the printed information.")
print("3. Quit the program by closing the figure window.")
print("---------------------------------------------------------")

# Set ODE parameters
y0 = 1
tspan = (0,1)

# Get h-values
hmin, hmax = (1e-5,1)
hvec = hmax*np.power(2.,np.arange(0,floor(log2(hmin/hmax)),-1))

# Solve ODE
err_Euler = np.zeros(hvec.size)
err_Heun = np.zeros(hvec.size)
err_RK4 = np.zeros(hvec.size)

yexact = yfunc(tspan[1], y0)

for idx,h in enumerate(hvec):
    t, y = _Euler(y0, tspan, h)
    err_Euler[idx] = abs(y[-1] - yexact)

    t, y = _Heun(y0, tspan, h)
    err_Heun[idx] = abs(y[-1] - yexact)

    t, y = _RK4(y0, tspan, h)
    err_RK4[idx] = abs(y[-1] - yexact)

# Get slopes
ids = list(range(4,10,1))
line_Euler = polyfit(hvec[ids], err_Euler[ids],1)
line_Heun = polyfit(hvec[ids], err_Heun[ids],1)
line_RK4 = polyfit(hvec[ids], err_RK4[ids],1)

# Plot errors vs. step sizes
fig = plt.figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.15, bottom=0.20)

ax.loglog(hvec,err_Euler,label='Euler')
ax.loglog(hvec,err_Heun,label='Heun')
ax.loglog(hvec,err_RK4,label='Runge-Kutta 4')
plt.grid()
plt.xlim([0.1*hmin,10*hmax])
plt.ylim([1e-16,1e0])
plt.xlabel('Step size')
plt.ylabel('Error')
plt.show(block=False)

# Define textbox and button
textbox_ax = fig.add_axes([0.3, 0.03, 0.1, 0.04])
textbox = TextBox(textbox_ax, "Error tolerance: ", initial='', color='.95', hovercolor='1', label_pad=0.01)

get_stats_button_ax = fig.add_axes([0.45, 0.03, 0.2, 0.04])
get_stats_button = Button(get_stats_button_ax, 'Get statistics', hovercolor='0.975', color='0.85')

print("The slope of each error curve (order of accuracy) is estimated to:")
print("Euler's method: {:f}".format(line_Euler[0]))
print("Heun's method: {:f}".format(line_Heun[0]))
print("Runge-Kutta 4: {:f}".format(line_RK4[0]))
print("---------------------------------------------------------")

errtol = 1e-4

[line_errtol] = ax.loglog([hmin,hmax],[errtol,errtol],'k--',label='Error tolerance')
ax.legend(loc='lower right')
line_errtol.set_visible(False)

# Set button action
def get_stats_button_on_clicked(mouse_event):
    try:
        errtol = float(textbox.text)
    except ValueError:
        print("Input '{:s}' could not be interpreted as an error tolerance (float). Try again.".format(textbox.text))    
        return

    line_errtol.set_visible(True)
    line_errtol.set_ydata([errtol,errtol])
    plt.draw()
    get_stats(errtol)

get_stats_button.on_clicked(get_stats_button_on_clicked)

# Runs measurements and prints statistics for given error tolerance
def get_stats(errtol):
    print("Chosen tolerance {:e}. Running measurements...".format(errtol))

    # Check if errtol is ok
    if errtol < np.min(err_Euler):
        print("Too small error tolerance for Euler's method, takes too long.")
    elif errtol > np.max(err_Euler):
        print("Too large error tolerance for Euler's method, step size can't be larger than the time interval.")
    else:
        ids_Euler = [np.where((errtol > err_Euler))[0][0]-1,np.where((errtol > err_Euler))[0][0]]
        p = polyfit(hvec[ids_Euler],err_Euler[ids_Euler],1)
        h_Euler = exp((log(errtol) - p[1])/p[0])

    if errtol < np.min(err_Heun):
        print("Too small error tolerance for Heun's method, takes too long.")
    elif errtol > np.max(err_Heun):
        print("Too large error tolerance for Heun's method, step size can't be larger than the time interval.")
    else:
        ids_Heun = [np.where((errtol > err_Heun))[0][0]-1,np.where((errtol > err_Heun))[0][0]]
        p = polyfit(hvec[ids_Heun],err_Heun[ids_Heun],1)
        h_Heun = exp((log(errtol) - p[1])/p[0])

    if errtol < np.min(err_RK4):
        print("Too small error tolerance for RK4, takes too long.")
    elif errtol > np.max(err_RK4):
        print("Too large error tolerance for RK4 method, step size can't be larger than the time interval.")
    else:
        ids_RK4 = [np.where((errtol > err_RK4))[0][0]-1,np.where((errtol > err_RK4))[0][0]]
        p = polyfit(hvec[ids_RK4],err_RK4[ids_RK4],1)
        h_RK4 = exp((log(errtol) - p[1])/p[0])

    print("\n{:^12s}\t{:^12s}\t{:^12s}\t{:^12s}\t{:^12s}".format("Method","Step size","Time [s]","Steps","Time [s] per step"))
    print("{:^12s}\t{:^12s}\t{:^12s}\t{:^12s}\t{:^12s}".format("------","---------","--------","-----","-----------------"))

    # Average runtime of reps number of runs
    reps = 40

    if errtol > np.min(err_Euler) and errtol < np.max(err_Euler):
        starttime = time.time()
        for rep in range(0,reps): t, y = _Euler(y0, tspan, h_Euler)
        elaptime = (time.time() - starttime)/reps
        print("{:^12s}\t{:^12e}\t{:^12e}\t{:^12d}\t{:^12e}".format("Euler's",h_Euler,elaptime,t.size-1,elaptime/t.size))

    if errtol > np.min(err_Heun) and errtol < np.max(err_Heun):
        starttime = time.time()
        for rep in range(0,reps): t, y = _Heun(y0, tspan, h_Heun)
        elaptime = (time.time() - starttime)/reps
        print("{:^12s}\t{:^12e}\t{:^12e}\t{:^12d}\t{:^12e}".format("Heun's",h_Heun,elaptime,t.size-1,elaptime/t.size))

    if errtol > np.min(err_RK4) and errtol < np.max(err_RK4):
        starttime = time.time()
        for rep in range(0,reps): t, y = _RK4(y0, tspan, h_RK4)
        elaptime = (time.time() - starttime)/reps
        print("{:^12s}\t{:^12e}\t{:^12e}\t{:^12d}\t{:^12e}".format("Runge-Kutta",h_RK4,elaptime,t.size-1,elaptime/t.size))
    print("---------------------------------------------------------")

plt.show()
