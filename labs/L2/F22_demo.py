import numpy as np
from scipy import integrate
from tabulate import tabulate # kräver paketet tabulate för printning av demo för F2.2 och F2.3
import matplotlib.pyplot as plt


# Riemann vänster
def riemann(f,a,b,N):
    h=(b-a)/(N-1)
    xi=np.linspace(a,b,N)
    fxi=f(xi)
    return h*sum(fxi[:-1]) # om Riemann höger, ha istället: h*sum(fxi[1:])

# Trapets version 1
def trapets1(f,a,b,N):
    h=(b-a)/(N-1)
    xi=np.linspace(a,b,N)
    fxi=f(xi)
    return h*sum((fxi[:-1]+fxi[1:])/2)

# Trapets version 2
def trapets2(f,a,b,N):
    h=(b-a)/(N-1)
    xi=np.linspace(a,b,N)
    fxi=f(xi)
    return h*(fxi[0]+fxi[-1])/2+h*sum(fxi[1:-1])

# Simpsons version 1
def simpson1(f,a,b,N):
    if (N%2==0):
        raise RuntimeError("N måste vara udda")
    h=(b-a)/(N-1)
    xi=np.linspace(a,b,N)
    fxi=f(xi)
    S=0
    for j in range((N-1)//2):
        S+=h/3*(fxi[2*j] + 4*fxi[2*j+1] + fxi[2*j+2])
    return S

# Simpsons version 2
def simpson2(f,a,b,N):
    if (N%2==0):
        raise RuntimeError("N måste vara udda")
    h=(b-a)/(N-1)
    xi=np.linspace(a,b,N)
    fxi=f(xi)
    return h/3*(fxi[0] + fxi[-1] + sum(4*fxi[1:-1:2]) + sum(2*fxi[2:-2:2]))

# Simpsons version 3
def simpson3(f,a,b,N):
    if (N%2==0):
        raise RuntimeError("N måste vara udda")
    h=(b-a)/(N-1)
    xi=np.linspace(a,b,N)
    fxi=f(xi)
    return 2*h*(sum(fxi[:-2:2]+4*fxi[1:-1:2]+fxi[2::2]))/6


def get_approximations(f,a,b,I,p_min,p_max):
    Ns=2**np.arange(p_min,p_max)+1
    R=np.zeros(p_max-p_min)
    T=np.zeros(p_max-p_min)
    S=np.zeros(p_max-p_min)
    for ii, N in enumerate(Ns):
        R[ii]=riemann(f,a,b,N)
        T[ii]=trapets1(f,a,b,N)
        S[ii]=simpson1(f,a,b,N)
    return Ns,R,T,S

def print_statistics_F22(f,a,b,I,p_min,p_max,eq):
    Ns,R,T,S=get_approximations(f,a,b,I,p_min,p_max)

    if eq==1:
        print(f"\nIntegralen av f(x)=3x^2 i intervallet [a,b]=[{a},{b}]")
    else:
        print(f"\nIntegralen av f(x)=sin((pi*x)^2)+2x+1 i intervallet [a,b]=[{a},{b}]")

    print(f"\nVärden I(h) för olika metoder, h=(b-a)/(N-1)= 1/{Ns[0]-1}, 1/{Ns[1]-1}, ...,  1/{Ns[-1]-1}")
    V=[[Ns[ii]-1, R[ii], T[ii], S[ii]] for ii in range(p_max-p_min)]
    print(tabulate(V, headers=['1/h','Riemann', 'Trapets', 'Simpson'], floatfmt=(".0f", ".10f", ".10f", ".10f")))


def demo_scipy():
    xi=np.array([0,0.125,0.25,0.375,0.5])
    yi=np.array([1.00,1.13,1.28,1.45,1.65])
    T=integrate.trapezoid(yi,xi)
    S=integrate.simpson(yi,xi)
    print(' ')
    print('Demo att använda SciPy integrering')
    print(f'Integrering av data med Trapets: {T}')
    print(f'Integrering av data med simpson: {S}')

def f1(x):
    return 3*x**2

def f2(x):
    return np.sin((np.pi*x)**2)+2*x+1


def F22_1():
    # Exempel 1, f1(x)=3x^2 F(x)=x^3+C I=7
    (a,b,p_min,p_max,I,eq)=(1,2,3,18,7,1)
    print_statistics_F22(f1,a,b,I,p_min,p_max,eq)
def F22_2():
    # Exempel 2, f2(x)=sin((pi*x)^2)+2x+1, Integralen approximerad nedan med hög precision
    (a,b,p_min,p_max,I,eq)=(0,1,3,18,2.2459426787260857285430684656189996584112396431725709320270040155,2)
    print_statistics_F22(f2,a,b,I,p_min,p_max,eq)
def F22_3():
    # # Använd SciPys inbyggda funktion
    demo_scipy()

if __name__=='__main__':
    F22_1()
    F22_2()
    F22_3()
    
    