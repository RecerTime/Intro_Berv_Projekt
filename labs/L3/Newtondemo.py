#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Slider, Button
import warnings

# Display info about the program
print("-----------------------------------------------------")
print("The Newton-Raphson method for the non-linear equation")
print("     f(x) = 0, where f(x) = x^2 - 4*sin(x) - 1")
print("-----------------------------------------------------")
print("The function y = f(x) and the line y = 0 are plotted in the figure. We are interested in the solution to the non-linear equation f(x) = 0. To solve the equation we will use the Newton-Raphson method. The method starts with an initial guess and successively improves the solution with each iteration. Use the program as follows:")
print("1. Start by selecting an initial guess by typing in the textbox.")
print("2. Press \"Set initial guess\" to initialize the Newton-Raphson method with the chosen starting guess.")
print("3. Press \"Step once\" to perform one iteration, continue until the solution stops improving. The iteration number, solution value, function value, and estimated error are printed.")
print("4. Press \"Reset\" to reset the solver and try another initial guess. Quit the program by closing the figure window.")

def f(x):
    return x*x - 4*np.sin(x) - 1

def fprime(x):
    return 2*x - 4*np.cos(x)

# Hide warning "Toggling axes navigation from the keyboard is deprecated..." when typing in textbox. 

# Global variable to keep track of current iteration
iter_no = 0

# Setup the figure
xl, xr = -5, 5
fig = plt.figure()
ax = fig.add_subplot(111)
plt.title('Newton-Raphson method')

fig.subplots_adjust(left=0.10, bottom=0.15)

xx = np.linspace(xl,xr,1000);
yy = f(xx)

# Draw the initial plot. 
ax.plot(xx,yy,label='y = f(x)',color='blue')
ax.plot(np.array([xl, xr]),np.array([0, 0]),'--',color='black',label='y = 0');
[dots] = ax.plot([None],[0],'r*',label='Newton-Raphson');
ax.set_xlim([xl, xr])
ax.set_ylim([-10, 30])

# --- Define widgets and events ---
init_tb_ax = fig.add_axes([0.30, 0.03, 0.1, 0.04])
init_tb = TextBox(init_tb_ax, "Initial guess: ", initial='', color='.95', hovercolor='1', label_pad=0.01)

reset_button_ax = fig.add_axes([0.8, 0.03, 0.1, 0.04])
reset_button = Button(reset_button_ax, 'Reset', hovercolor='0.975')
def reset_button_on_clicked(mouse_event):
    global iter_no
    iter_no = 0
    dots.set_xdata(None)
    dots.set_ydata([0])
    step_button.label.set_text('Set initial guess')
    init_tb.set_val('')
    plt.draw()
    
reset_button.on_clicked(reset_button_on_clicked)

step_button_ax = fig.add_axes([0.50, 0.03, 0.2, 0.04])
step_button = Button(step_button_ax, 'Set initial guess', hovercolor='0.975', color='0.85')
def step_button_on_clicked(mouse_event):
    global iter_no
    if iter_no == 0: # first iteration: read from textbox
        try:
            xinit = float(init_tb.text)
        except ValueError:
            print("Input '{:s}' could not be interpreted as a number (float). Try again.".format(init_tb.text))   
            return
        print("\n{:^16s}\t{:^16s}\t{:^16s}\t{:^23s}".format("Iteration","x","f(x)","Estimated Error"))
        print("{:^16d}\t{:^.16f}\t{:^.16f}\t\t-".format(iter_no,xinit,f(xinit)))
        step_button.label.set_text('Step once')
        xvec = np.array([xinit]) # array to store the iterations, for plotting
    else:
        xvec,_ = dots.get_data()
        xold = xvec[-1]
        dx = f(xold)/fprime(xold)
        xnew = xold - dx
        err = abs(dx)
        print("{:^16d}\t{:^.16f}\t{:^.16f}\t{:^.16e}".format(iter_no,xnew,f(xnew),err))
        xvec = np.append(xvec,xnew)
             
    iter_no += 1
    dots.set_xdata(xvec)
    dots.set_ydata(f(xvec))
    plt.draw()
    
step_button.on_clicked(step_button_on_clicked)

ax.legend()
plt.show()


