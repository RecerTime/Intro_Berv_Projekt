#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from matplotlib.cbook import mplDeprecation
import warnings
from math import copysign

# Display info about the program
print("-----------------------------------------------------")
print("The program applies the bisection method to the non-linear equation")
print("     f(x) = 0, where f(x) = x^2 - 4*sin(x) - 1")
print("-----------------------------------------------------")
print("The function y = f(x) and the line y = 0 are plotted in the figure. We are interested in the solution to the non-linear equation f(x) = 0. To solve the equation we will use the bisection method. The method starts with an interval in which one root lies and successively halves the interval with each iteration. Use the program as follows:")
print("1. Start by selecting an initial interval. Set the left and right interval points by typing in the textboxes.")
print("2. Press \"Set initial interval\" to initialize the bisection method with the chosen starting interval.")
print("3. Press \"Step once\" to perform one iteration, continue until the solution stops improving. The iteration number, the current interval, the function value at the center of the current interval, and the estimated error are printed.")
print("4. Press \"Reset\" to reset the solver and try another initial interval. Quit the program by closing the figure window.")

def f(x):
    return x*x - 4*np.sin(x) - 1

def sign(x):
    return copysign(1,x)

# Hide warning "Toggling axes navigation from the keyboard is deprecated..." when typing in textbox. 
warnings.filterwarnings("ignore",category=mplDeprecation)

# Global variable to keep track of current iteration
iter_no = 0

# Setup the figure
xl, xr = -5, 5
fig = plt.figure()
ax = fig.add_subplot(111)
plt.title('Bisection method')

fig.subplots_adjust(left=0.10, bottom=0.15)
plt.xlabel('x')
plt.ylabel('y')

# Draw the initial plot. The 'line' variable is used for modifying the interval line later
xx = np.linspace(xl,xr,1000);
y = f(xx)
ax.plot(xx,y,label='y = f(x)',color='blue')
ax.plot(np.array([xl, xr]),np.array([0, 0]),'--',color='black',label='y = 0');
[line] = ax.plot([None,None],[0,0],'r*-',label='Bisection method');
ax.set_xlim([xl, xr])
ax.set_ylim([-10, 30])

# --- Define widgets and events ---

# Left and right textboxes
left_tb_ax = fig.add_axes([0.10, 0.01, 0.1, 0.04])
left_tb = TextBox(left_tb_ax, "Left: ", initial='', color='.95', hovercolor='1', label_pad=0.01)

right_tb_ax = fig.add_axes([0.30, 0.01, 0.1, 0.04])
right_tb = TextBox(right_tb_ax, "Right: ", initial='', color='.95', hovercolor='1', label_pad=0.01)

# Reset button
reset_button_ax = fig.add_axes([0.8, 0.01, 0.1, 0.04])
reset_button = Button(reset_button_ax, 'Reset', hovercolor='0.975')

def reset_button_on_clicked(mouse_event):
    global iter_no
    iter_no = 0
    line.set_xdata([None,None])
    line.set_ydata([0,0])
    step_button.label.set_text('Set initial interval')
    left_tb.set_val('')
    right_tb.set_val('')
    plt.draw()
    
reset_button.on_clicked(reset_button_on_clicked)
    
# Step button
step_button_ax = fig.add_axes([0.5, 0.01, 0.25, 0.04])
step_button = Button(step_button_ax, 'Set initial interval', hovercolor='0.975', color='0.85')

def step_button_on_clicked(mouse_event):
    global iter_no
    if iter_no == 0: # first iteration: read from textboxes
        try:
            a = float(left_tb.text)
        except ValueError:
            print("Input '{:s}' could not be interpreted as a number (float). Try again.".format(left_tb.text))   
            return

        try:
            b = float(right_tb.text)
        except ValueError:
            print("Input '{:s}' could not be interpreted as a number (float). Try again.".format(right_tb.text))   
            return

        if sign(f(a)) == sign(f(b)):
            print("\nThe interval [xl,xr] = [{:f},{:f}] won't work, the signs of f(x) must be different at the interval endpoints. Here f(xl) = {:f} and f(xr) = {:f} => same sign! Try again.".format(a,b,f(a),f(b)))
            return
        else:                
            print("\n{:^12s}\t{:^12s}\t{:^12s}\t{:^12s}\t{:^19s}".format("Iteration","xl","xr","f(xmid)","Estimated Error"))
            step_button.label.set_text('Step once')
    else:
        xint,_ = line.get_data()
        a,b = xint
        c = (a+b)/2
        if sign(f(a)) == sign(f(c)):
            a = c
        else:
            b = c
             
    err = abs(b-a)
    iter_no += 1
    x = (a+b)/2
    print("{:^12d}\t{:^.12f}\t{:^.12f}\t{:^.12f}\t{:^.12e}".format(iter_no,a,b,f(x),err))
    line.set_xdata([a,b])
    
    plt.draw()
    
step_button.on_clicked(step_button_on_clicked)

ax.legend()
plt.show()


