#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import mplDeprecation
from matplotlib.widgets import Button, TextBox
import scipy.integrate as ode
from math import pi
import warnings

print("-----------------------------------------------------")
print("Euler's method for the non-linear ODE")
print("     dy/dt = cos(y*t), 0 < t < 2*pi,")
print("     y(0) = 0.")
print("-----------------------------------------------------")
print("This demo program solves the non-linear ODE using Euler's method. For comparison the exact solution is plotted in the figure (not really exact, a highly accurate method from SciPy is used). Use the program as follows:")
print("1. Choose a step size, type in the textbox.")
print("2. Press \"Initialize\" to initialize Euler's method.")
print("3. Press \"Step once\" to perform one iteration, continue until the final time is reached. Pay attention to the difference between the exact and approximate solutions.")
print("4. Press \"Reset\" to reset the solver and try another step size. Quit the program by closing the figure window.")
print("-----------------------------------------------------")

# Hide warning "Toggling axes navigation from the keyboard is deprecated..." when typing in textbox. 
warnings.filterwarnings("ignore",category=mplDeprecation)

# RHS function
def f(t,y):
    return np.cos(y*t)

# Global variable to keep track of current iteration
iter_no = 0

# Set ODE parameters
maxintervals = 50
tspan = (0,2*pi)
y0 = 0

# Setup the figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_navigate(False)
plt.title('Euler\'s method')

# Adjust the subplots region to leave some space for the sliders and buttons
fig.subplots_adjust(left=0.10, bottom=0.20)

# Draw the initial plot. The 'line' variable is used for modifying the interval line later.
# Plot exact solution using SciPys RK45
SOL = ode.solve_ivp(f, tspan, np.array([y0]), method='RK45', rtol=1e-10, atol=1e-10)
ax.plot(SOL.t,SOL.y[0],label='Exact solution',color='blue')
[line] = ax.plot(tspan[0],y0,'r*-',label='Approximate solution');
plt.xlabel('$t$')
plt.ylabel('$y$')
ax.legend()
ax.set_xlim([0,7])
ax.set_ylim([0, 1.5])

# Define textbox and buttons
reset_button_ax = fig.add_axes([0.60, 0.03, 0.1, 0.04])
reset_button = Button(reset_button_ax, 'Reset', hovercolor='0.975')

textbox_ax = fig.add_axes([0.20, 0.03, 0.1, 0.04])
textbox = TextBox(textbox_ax, "Step size: ", initial='', color='.95', hovercolor='1', label_pad=0.01)

step_button_ax = fig.add_axes([0.35, 0.03, 0.2, 0.04])
step_button = Button(step_button_ax, 'Step once', hovercolor='0.975', color='0.85')

def reset_button_on_clicked(mouse_event):
    global iter_no
    iter_no = 0
    line.set_xdata([tspan[0]])
    line.set_ydata([y0])
    textbox.set_val('')
    textbox.set_active(True)
    plt.draw()

reset_button.on_clicked(reset_button_on_clicked)

def step_button_on_clicked(mouse_event):
    global iter_no

    # read textbox
    if iter_no == 0:
        try:
            h = float(textbox.text)
        except ValueError:
            print("Input '{:s}' could not be interpreted as a step size (float). Try again.".format(textbox.text))    
            return

        if not h > 0 or h > 2*pi:
            print("Step size error. Choose step size on the interval 0 < h < 2*pi. Current h: {:f}".format(h))
            return        

        # deactivate the textbox
        textbox.set_active(False)
    else:
        h = float(textbox.text)

    # Eulers method
    tvec, yvec = line.get_data()
    told = tvec[-1]
    yold = yvec[-1]

    h = float(textbox.text)

    ynew = yold + h*f(told,yold)
    
    tvec = np.append(tvec,told + h)
    yvec = np.append(yvec,ynew)

    # Correct the final step
    if tvec[-1] > tspan[1]:
        h = tspan[1] - told
        ynew = yold + h*f(told,yold)
        tvec[-1] = tspan[1]
        yvec[-1] = ynew
        err = abs(ynew - SOL.y[0][-1])
        print("Final time reached. With step size {:f} the error is {:e}.".format(float(textbox.text),err))

    iter_no += 1
    line.set_xdata(tvec)
    line.set_ydata(yvec)
    plt.draw()

step_button.on_clicked(step_button_on_clicked)

plt.show()
