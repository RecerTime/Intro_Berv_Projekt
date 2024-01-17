#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

def f(x):
	return np.exp(x)

def fprim(x):
	return np.exp(x)

def forwardDiff(x,h):
	return (f(x+h) - f(x))/h

def centralDiff(x,h):
	return (f(x+h) - f(x-h))/(2*h)

# Compute derivatives at x = 1
x = 1

fprim_exact = fprim(x)

h = 10**np.linspace(-1,-12,200)

fprimF = forwardDiff(x,h)
fprimC = centralDiff(x,h)

errF = np.abs((fprimF - fprim_exact)/fprim_exact)
errC = np.abs((fprimC - fprim_exact)/fprim_exact)

plt.loglog(h,errF,label='Forward difference')
plt.loglog(h,errC,label='Central difference')
plt.xlabel('Step size')
plt.ylabel('Relative error')
plt.grid()
plt.legend()
plt.show()
