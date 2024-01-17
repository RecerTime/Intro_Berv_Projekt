#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from matplotlib.cbook import mplDeprecation
import warnings
from math import pi

def f(x):
    return np.cos(2*x) + np.sin(x)

def adaptsimp(xl,xr,tol):
    X = np.array([])
    fl = f(xl)
    fr = f(xr)
    X = np.append(X,xl)
    (xm, fm, Iwhole, X) = adaptsimp_split(xl, xr, fl, fr, X)

    (Iout, X) = adaptsimp_recu(xl, xr, xm, fl, fr, fm, Iwhole, tol, 0, X)
    X = np.append(X,xr)
    X = np.sort(np.unique(X))

    return (Iout, X)

def adaptsimp_split(xl, xr, fl, fr, X):
    xm = (xl+xr)/2
    fm = f(xm)
    X = np.append(X,xm)
    return (xm, fm, (xr-xl)/6*(fl + 4*fm + fr),X)

def adaptsimp_recu(xl, xr, xm, fl, fr, fm, Iwhole, tol, depth, X):
    (xm_l, fm_l, Ileft, X) = adaptsimp_split(xl,xm,fl,fm,X)
    (xm_r, fm_r, Iright, X) = adaptsimp_split(xm,xr,fm,fr,X)
    
    diff = Ileft + Iright - Iwhole
    
    if abs(diff) < 15*tol:
        return (Ileft + Iright + diff/15, X)
    
    Iout_left, Xl = adaptsimp_recu(xl, xm, xm_l, fl, fm, fm_l, Ileft, tol, depth+1, X) 
    Iout_right, Xr = adaptsimp_recu(xm, xr, xm_r, fm, fr, fm_r, Iright, tol, depth+1, X)
              
    return (Iout_left + Iout_right, np.concatenate((Xl,Xr))) 

def plot_polys(x,ax):
    lines = []
    lines.append(ax.plot(x,np.full(x.shape,0), color='blue', lw=0.5, label='Adaptive Simpson\'s rule'))
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
print("Adaptive Simpson's method for the integral of")
print("     f(x) = cos(2*x) + sin(x),")
print("on the interval [-pi,2*pi].")
print("---------------------------------------------------------")
print("This demo program solves the integral using the adaptive Simpson's method for a chosen error tolerance. The integrand f(x) is plotted on the interval. The method is illustrated graphically. Use the program as follows:")
print("1. Study the plot produced when running the program.")
print("2. Choose error tolerance by typing in the text box. Press 'Run adaptive Simpson'. The method is illustrated in the figure and accuracy information is printed. Try a different error tolerance by typing in the text box and pressing 'Run adaptive Simpson' again.")
print("3. Quit the program by closing the figure window.")
print("---------------------------------------------------------")

# Hide warning "Toggling axes navigation from the keyboard is deprecated..." when typing in textbox. 
warnings.filterwarnings("ignore",category=mplDeprecation)

# Set integral parameters
xl = -pi
xr = 2*pi

# Compute exact integral
Iexact = (0.5*np.sin(2*xr) - np.cos(xr)) - (0.5*np.sin(2*xl) - np.cos(xl))
print("Exact integral: {:.4f}".format(Iexact))

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
# Tolerance textbox
textbox_ax = fig.add_axes([0.35, 0.1, 0.1, 0.04])
textbox = TextBox(textbox_ax, "Error tolerance: ", initial='', color='.95', hovercolor='1', label_pad=0.01)

# Adaptive Simpsons button
run_adapt_button_ax = fig.add_axes([0.15, 0.03, 0.3, 0.04])
run_adapt_button = Button(run_adapt_button_ax, 'Run adaptive Simpson', hovercolor='0.975', color='0.85')

lines_simp = []
def run_adapt_button_on_clicked(mouse_event):
    global lines_simp
    try:
        errtol = float(textbox.text)
    except ValueError:
        print("Input '{:s}' could not be interpreted as an error tolerance (float). Try again.".format(textbox.text))
        return

    if errtol < 0:
        print("Error tolerance must be positive, current value: {:e}. Try again.".format(errtol))
        return

    # Remove current lines
    for line_tmp in lines_simp:
        line_tmp.pop(0).remove()

    # Run adaptive Simpsons
    (Ias, x) = adaptsimp(xl,xr,errtol)

    # Print accuracy
    print("Integral approximation using adaptive Simpson's method with local error tolerance {:.2e}: {:.4f}.".format(errtol,Ias))

    # Plot method
    lines_simp = plot_polys(x,ax)
    ax.legend()
    plt.draw()

run_adapt_button.on_clicked(run_adapt_button_on_clicked)

plt.show()