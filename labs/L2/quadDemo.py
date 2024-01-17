#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from matplotlib.cbook import mplDeprecation
import warnings
from math import pi

def f(x):
    return np.cos(2*x) + np.sin(x)

def trapetz(fx,h):
    weights = np.full(fx.size,2)
    weights[0] = 1
    weights[-1] = 1
    return h/2*np.dot(fx,weights)

def simpsons(fx,h):    
    weights = np.full(fx.size,2)
    weights[0] = 1
    weights[-1] = 1
    weights[1:fx.size:2] = 4
    return h/3*np.dot(fx,weights)

def plot_trapz(x,ax):
    lines = []
    lines.append(ax.plot(x,f(x), color='red', lw=0.5))

    lines.append(ax.plot(x,np.full(x.shape,0), color='red', lw=0.5, label='Trapezoidal rule'))
    
    for i in range(x.size):
        lines.append(ax.plot([x[i],x[i]],[0,f(x[i])], color='red', lw=0.5))

    return lines
    
def plot_polys(x,ax):
    lines = []
    lines.append(ax.plot(x,np.full(x.shape,0), color='blue', lw=0.5, label='Simpson\'s rule'))
    for i in range(0,x.size,2):
        lines.append(ax.plot([x[i],x[i]],[0,f(x[i])], color='blue', lw=0.5))
        if i < x.size-1:
            lines.append(ax.plot([x[i+1],x[i+1]],[0,f(x[i+1])], color='blue', ls='--', alpha=0.5, lw=0.5))
            xx = x[i:i+3]
            yy = f(x[i:i+3])
            p = np.linalg.solve(np.vander(xx),yy)
            xtmp = np.linspace(x[i],x[i+2])
            ytmp = p[0]*xtmp*xtmp + p[1]*xtmp + p[2]
            lines.append(ax.plot(xtmp,ytmp, color='blue', lw=0.5))

    return lines

# Hide warning "Toggling axes navigation from the keyboard is deprecated..." when typing in textbox. 
warnings.filterwarnings("ignore",category=mplDeprecation)

print("---------------------------------------------------------")
print("Trapezoidal rule and Simpson's method for the integral of")
print("     f(x) = cos(2*x) + sin(x),")
print("on the interval [-pi,2*pi].")
print("---------------------------------------------------------")
print("This demo program solves the integral using the trapezoidal rule and Simpson's method with a chosen number of subintervals. The integrand f(x) is plotted on the interval. The numerical methods are illustrated graphically. Use the program as follows:")
print("1. Study the plot produced when running the program.")
print("2. Choose a number of subintervals by typing in the text box. Press 'Show trapezoid' and/or 'Show Simpson'. The methods are illustrated in the figure and accuracy information is printed. Press 'Hide ...' to the remove the plots and try another number of subintervals. Note that Simpson's method requires an even number of subintervals." )
print("3. Quit the program by closing the figure window.")
print("---------------------------------------------------------")

# Set integral parameters
xl = -pi
xr = 2*pi

# Compute exact integral
Iexact = (0.5*np.sin(2*xr) - np.cos(xr)) - (0.5*np.sin(2*xl) - np.cos(xl))
print("Exact integral: {:.10f}".format(Iexact))

# Setup figure
fig = plt.figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.15, bottom=0.25)

# Plot integrand
xplot = np.linspace(xl,xr,1000,retstep=False)
plt.plot(xplot,f(xplot), color='black', label='Integrand')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()

# --- Define widgets and events ---
# Subintervals textbox
textbox_ax = fig.add_axes([0.5, 0.1, 0.1, 0.04])
textbox = TextBox(textbox_ax, "Number of subintervals: ", initial='', color='.95', hovercolor='1', label_pad=0.01)

# Show trapezoid button
show_traps_button_ax = fig.add_axes([0.15, 0.03, 0.2, 0.04])
show_traps_button = Button(show_traps_button_ax, "Show trapezoid", hovercolor='0.975', color='0.85')

def show_traps_button_on_clicked(mouse_event):
    global lines_traps

    try:
        nsubints = int(textbox.text)
    except ValueError:
        print("Input '{:s}' could not be interpreted as a number of subintervals (integer). Try again.".format(textbox.text))	
        return

    if show_traps_button.label.get_text() == "Show trapezoid":
        if not nsubints > 0:
            print("Number of subintervals must be positive, current value: {:d}. Try again.".format(nsubints))
            return

        show_traps_button.label.set_text("Hide trapezoid")

        # Discretize x-axis and evaluate integrand
        [x,h] = np.linspace(xl, xr, nsubints+1, retstep=True)    

        # Apply trapetz method
        It = trapetz(f(x),h)
        print("Integral approximation using trapezoidal method with {:d} subintervals: {:.10f}, relative error: {:.4e}.".format(nsubints,It,abs((It - Iexact)/It)))

        # Plot method
        lines_traps = plot_trapz(x,ax)
    else:
        # Remove current lines
        for line_tmp in lines_traps:
            line_tmp.pop(0).remove()

        show_traps_button.label.set_text("Show trapezoid")

    ax.legend()
    plt.draw()

show_traps_button.on_clicked(show_traps_button_on_clicked)

# Show Simpsons button
show_simp_button_ax = fig.add_axes([0.40, 0.03, 0.2, 0.04])
show_simp_button = Button(show_simp_button_ax, "Show Simpson", hovercolor='0.975', color='0.85')

def show_simp_button_on_clicked(mouse_event):
    global lines_simp

    try:
        nsubints = int(textbox.text)
    except ValueError:
        print("Input '{:s}' could not be interpreted as a number of subintervals (integer). Try again.".format(textbox.text))	
        return

    if show_simp_button.label.get_text() == "Show Simpson":
        if not nsubints > 0:
            print("Number of subintervals must be positive, current value: {:d}. Try again.".format(nsubints))
            return

        if not nsubints % 2 == 0:
            print("Simpson's method requires an even number of subintervals, current value: {:d}. Try again.".format(nsubints))
            return

        show_simp_button.label.set_text("Hide Simpson")

        # Apply Simpson's method
        [x,h] = np.linspace(xl, xr, nsubints+1, retstep=True)    
        Is = simpsons(f(x),h)

        # Print accuracy
        print("Integral approximation using Simpson's method with {:d} subintervals: {:.10f}, relative error: {:.4e}.".format(nsubints,Is,abs((Is - Iexact)/Is)))

        # Plot method
        lines_simp = plot_polys(x,ax)
    else:
        # Remove current lines
        for line_tmp in lines_simp:
            line_tmp.pop(0).remove()

        show_simp_button.label.set_text("Show Simpson")
        
    ax.legend()
    plt.draw()

show_simp_button.on_clicked(show_simp_button_on_clicked)

plt.show()