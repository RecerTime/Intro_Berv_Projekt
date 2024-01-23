import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy import integrate

def curve(x,y,x_new):
    return interpolate.pchip_interpolate(x,y,x_new)

def monte_carlo_demo(x,y,xx0,xx1,yy0,yy1):
    print(" ")
    print("Monte Carlo demo")
    print("Gräsmatta grön")
    print("Vattenytan blå x=[0, 15] y=0")
    print("Botten okänd")
    print(" ")
    plt.plot([xx0-1,xx0],[yy0,yy0],color='green',linewidth=5)
    plt.plot([xx1,xx1+1],[yy0,yy0],color='green',linewidth=5)
    plt.plot([xx0,xx1],[yy0,yy0],color='blue',linestyle='dashed',linewidth=2)
    plt.scatter([xx0,xx1],[yy0,yy0])
    plt.xlim(-1, 16)
    plt.xticks([0,5,10,15])
    plt.ylim(-6, 1)
    plt.ion()
    plt.show()
    input("Tryck [enter] för att fortsätta.")
    n_points=5
    xr=np.zeros(n_points)
    yr=np.zeros(n_points)

    for ii in range(n_points):
        xr[ii]=np.random.random()*xx1
        yr[ii]=curve(x,y,xr[ii])
        print(f'{ii+1}: Slumpvärde x och uppmätt y:')
        print((xr[ii],yr[ii]))
        plt.scatter([xr[ii],xr[ii]],[yy0,yr[ii]])
        plt.plot([xr[ii],xr[ii]],[yy0,yr[ii]])
        plt.plot([0,0,15,15],[0,yr[ii],yr[ii],0],color="black",linewidth=0.5)

        print("Uppskattad Area y*15:")
        print(yr[ii]*xx1)
        plt.xlim(xx0-1, xx1+1)
        plt.ylim(yy1-1, yy0+1)
        plt.draw()
        plt.show()
        input("Tryck [enter] för att fortsätta.")
    plt.draw()
    input("Vi beräknar nu arean som ett medelvärde av alla åtta värden")

    print("Medelvärde alla y-värden, y_mean:")
    y_mean=sum(yr)/n_points
    print(y_mean)
    print("Uppskattad Area y_mean*15:")
    print(y_mean*xx1)
    plt.plot([0,0,15,15],[0,y_mean,y_mean,0],color="black",linewidth=2)
    plt.show()
    input("Tryck [enter] för att fortsätta.")
    plt.close()
    input("Vi räknar nu ut Arean med medelvärden för olika antal värden (n, Area)")
    n_vals=25
    areas=np.zeros(n_vals)
    for ii in range(n_vals):
        nn=2**ii
        x_samples=np.random.random(nn)*xx1
        y_samples=curve(x,y,x_samples)
        print((nn,sum(y_samples)/nn*15))
    input("Tryck [enter] för att fortsätta.")

def scipy_demo(x,y,xx0,xx1,yy0,yy1):
    print(" ")
    print("SciPy integrate.quadrature demo")
    print("Gräsmatta grön")
    print("Vattenyan blå x=[0, 15] y=0")
    print("Botten svart")
    print(" ")
    plt.plot([xx0-1,xx0],[yy0,yy0],color='green',linewidth=5)
    plt.plot([xx1,xx1+1],[yy0,yy0],color='green',linewidth=5)
    plt.plot([xx0,xx1],[yy0,yy0],color='blue',linestyle='dashed',linewidth=2)
    plt.scatter([xx0,xx1],[yy0,yy0])
    plt.xlim(-1, 16)
    plt.xticks([0,5,10,15])
    plt.ylim(-6, 1)
    plt.plot(x,y,color='black',linewidth=2)
    plt.ion()
    plt.show()
    input("Tryck [enter] för att räkna ut Arean.")
    def f(xval):
        return curve(x,y,xval)
    print(integrate.quadrature(f,0,15,maxiter=5000))

def F21():
    xy = np.loadtxt('bottom.txt')
    x=xy[:,0]
    y=xy[:,1]
    (xx0,xx1,yy0,yy1)=(0,15,0,-5)
    monte_carlo_demo(x,y,xx0,xx1,yy0,yy1)
    scipy_demo(x,y,xx0,xx1,yy0,yy1)

if __name__=='__main__':
    F21()



