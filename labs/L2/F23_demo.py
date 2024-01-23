from F22_demo import *

def print_statistics_F23a(f,a,b,I,p_min,p_max,eq):
    Ns,R,T,S=get_approximations(f,a,b,I,p_min,p_max)

    if eq==1:
        print(f"\nIntegralen av f(x)=3x^2 i intervallet [a,b]=[{a},{b}]")
    elif eq==2:
        print(f"\nIntegralen av f(x)=sin((pi*x)^2)+2x+1 i intervallet [a,b]=[{a},{b}]")
    else:
        print(f"\nIntegralen av f(x)=x^(2/3) i intervallet [a,b]=[{a},{b}]")

    print(f"\nRiemann R(h), ER(h), ER(2h)/ER(h), C=ER(h)/h, h=(b-a)/(N-1)= 1/{Ns[0]-1}, 1/{Ns[1]-1}, ...,  1/{Ns[-1]-1}")
    D=[[Ns[ii]-1, R[ii], I-R[ii], (I-R[ii-1])/(I-R[ii]), (I-R[ii])*(Ns[ii]-1)] if ii>0 else [Ns[ii]-1, R[ii], I-R[ii], 0, (I-R[ii])*(Ns[ii]-1)] for ii in range(p_max-p_min)]
    print(tabulate(D, headers=['1/h','R(h)', 'ER(h)=I-R(h)', 'ER(2h)/ER(h)', 'C'], floatfmt=(".0f", ".10f", ".10f", ".10f", ".10f")))

    print(f"\nTrapets T(h), ET(h), ET(2h)/ET(h), C=ER(h)/h^2, h=(b-a)/(N-1)= 1/{Ns[0]-1}, 1/{Ns[1]-1}, ...,  1/{Ns[-1]-1}")
    if eq in [1,2]:
        D=[[Ns[ii]-1, T[ii], I-T[ii], (I-T[ii-1])/(I-T[ii]), (I-T[ii])*(Ns[ii]-1)**2] if ii>0 else [Ns[ii]-1, T[ii], I-T[ii], 0, (I-T[ii])*(Ns[ii]-1)**2] for ii in range(p_max-p_min)]
    else:
        D=[[Ns[ii]-1, T[ii], I-T[ii], (I-T[ii-1])/(I-T[ii]), (I-T[ii])*(Ns[ii]-1)**np.log2(3.16)] if ii>0 else [Ns[ii]-1, T[ii], I-T[ii], 0, (I-T[ii])*(Ns[ii]-1)**np.log2(3.16)] for ii in range(p_max-p_min)]
    print(tabulate(D, headers=['1/h','T(h)', 'ET(h)=I-T(h)', 'ET(2h)/ET(h)', 'C'], floatfmt=(".0f", ".10f", ".10f", ".10f", ".10f")))

    if eq==1:
        print(f"\nSimpsons I(h), ES(h), h=(b-a)/(N-1)= 1/{Ns[0]-1}, 1/{Ns[1]-1}, ...,  1/{Ns[-1]-1}")
        D=[[Ns[ii]-1, S[ii], I-S[ii]] for ii in range(p_max-p_min)]
        print(tabulate(D, headers=['1/h','S(h)', 'ES(h)=I-S(h)'], floatfmt=(".0f", ".10f", ".10f")))
    elif eq==2:
        print(f"\nSimpson S(h), ES(h), ES(2h)/ES(h), C=ER(h)/h^2, h=(b-a)/(N-1)= 1/{Ns[0]-1}, 1/{Ns[1]-1}, ...,  1/{Ns[-1]-1}")
        D=[[Ns[ii]-1, S[ii], I-S[ii], (I-S[ii-1])/(I-S[ii]), (I-S[ii])*(Ns[ii]-1)**4] if ii>0 else [Ns[ii]-1, S[ii], I-S[ii], 0, (I-S[ii])*(Ns[ii]-1)**4] for ii in range(p_max-p_min)]
        print(tabulate(D, headers=['1/h','S(h)', 'ES(h)=I-T(h)', 'ES(2h)/ES(h)', 'C'], floatfmt=(".0f", ".10f", ".10f", ".10f", ".10f")))
    else:
        print(f"\nSimpson S(h), ES(h), ES(2h)/ES(h), C=ER(h)/h^2, h=(b-a)/(N-1)= 1/{Ns[0]-1}, 1/{Ns[1]-1}, ...,  1/{Ns[-1]-1}")
        D=[[Ns[ii]-1, S[ii], I-S[ii], (I-S[ii-1])/(I-S[ii]), (I-S[ii])*(Ns[ii]-1)**np.log2(3.17)] if ii>0 else [Ns[ii]-1, S[ii], I-S[ii], 0, (I-S[ii])*(Ns[ii]-1)**np.log2(3.17)] for ii in range(p_max-p_min)]
        print(tabulate(D, headers=['1/h','S(h)', 'ES(h)=I-T(h)', 'ES(2h)/ES(h)', 'C'], floatfmt=(".0f", ".10f", ".10f", ".10f", ".10f")))

def plot_figures_F23a(f,a,b,I,p_min,p_max,eq):
    Ns,R,T,S=get_approximations(f,a,b,I,p_min,p_max)
    # hs=np.array([1/(Ns[-1-ii]-1) for ii in range(len(Ns))])
    hs=np.array(1/(Ns-1))
    ER=I-R

    if eq==1:
        AER=4.5*hs
        plt.title("f(x)=3x^2")
    elif eq==2:
        AER=0.78*hs
        plt.title("f(x)=sin((pi*x)^2)+2x+1")
    else:
        AER=0.5*hs
        plt.title("f(x)=x^(2/3)")
    plt.loglog(hs,abs(ER),'or',label="log_10|E_R(h)|")
    plt.loglog(hs,abs(AER),'-r',label="log_10(Ch)")
   
    ET=I-T
    if eq==1:
        AET=0.5*hs**2
    elif eq==2:
        AET=1.485*hs**2
    else:
        AET=0.33*hs**2
        AETb=0.14*hs**1.66
    plt.loglog(hs,abs(ET),'ob',label="log_10|E_T(h)|")
    plt.loglog(hs,abs(AET),'-b',label="log_10(Ch^2)")
    if eq==3:
        plt.loglog(hs,abs(AETb),'--b',label="log_10(Ch^1.66)")
    plt.legend()
    plt.xlabel("log_10|h|")
    plt.ylabel("log_10|E(h)|")

    if eq==1:
        plt.savefig("f1error.png")
        plt.show()
    elif eq==2:
        ES=I-S+np.finfo(float).eps
        AES=-41.37*hs**4
        plt.loglog(hs,abs(ES),'og',label="log_10|E_S(h)|")
        plt.loglog(hs,abs(AES),'-g',label="log_10(Ch^4)")
        plt.axhline(y=np.finfo(float).eps,color='r', linestyle='--')
        plt.legend(framealpha=1)
        plt.savefig("f2error.png")
        plt.show()
    else:
        ES=I-S
        AES=5.46*hs**4 # ta första felet och dividera med h^4
        AESb=0.042*hs**1.66 # ta första felet och dividera med h^4
        plt.loglog(hs,ES,'og',label="log_10|E_S(h)|")
        plt.loglog(hs,AES,'-g',label="log_10(Ch^4)")
        plt.loglog(hs,AESb,'--g',label="log_10(Ch^1.66)")
        plt.axhline(y=np.finfo(float).eps,color='r', linestyle='--')
        plt.legend(framealpha=1)
        plt.savefig("f3error.png")
        plt.show()

def f3(x):
    return x**(2/3)

def richardson_trapets(f,a,b,N):
    N2h=(N-1)//2+1
    Nh=N
    T2h=trapets1(f,a,b,N2h)
    Th=trapets1(f,a,b,Nh)
    return (Th-T2h)/3

def richardson_simpson(f,a,b,N):
    N2h=(N-1)//2+1
    Nh=N
    S2h=simpson1(f,a,b,N2h)
    Sh=simpson1(f,a,b,Nh)
    return (Sh-S2h)/15

def print_statistics_F23b(f,a,b,I,p_min,p_max,eq):
    Ns,R,T,S=get_approximations(f,a,b,I,p_min,p_max)
    hs=(b-a)/(Ns[1:]-1)
    ER=I-R[1:]
    RR=R[1:]-R[:-1]
    ET=I-T[1:]
    RT=(T[1:]-T[:-1])/3
    ES=I-S[1:]
    RS=(S[1:]-S[:-1])/15
    print(f"\nFel och feluppskattningar för Riemann, h=(b-a)/(N-1)= 1/{Ns[1]-1}, 1/{Ns[2]-1}, ...,  1/{Ns[-1]-1}")
    V=[[Ns[ii+1]-1, ER[ii], RR[ii], RR[ii]/hs[ii]] for ii in range(p_max-p_min-1)]
    print(tabulate(V, headers=['1/h','Fel', 'Richarson', 'C']))

    p=1
    epsilon=1E-5
    Nmin=int((RR[3]/hs[3]**p/epsilon)**(1/p))
    print(f'Uppskattning N_min för fel mindre än {epsilon}: {Nmin}')

    print(f"\nFel och feluppskattningar för Trapets, h=(b-a)/(N-1)= 1/{Ns[1]-1}, 1/{Ns[2]-1}, ...,  1/{Ns[-1]-1}")
    V=[[Ns[ii+1]-1, ET[ii], RT[ii], RT[ii]/hs[ii]**2] for ii in range(p_max-p_min-1)]
    print(tabulate(V, headers=['1/h','Fel', 'Richarson','C']))

    p=2
    epsilon=1E-5
    Nmin=int((RT[3]/hs[3]**p/epsilon)**(1/p))
    print(f'Uppskattning N_min för fel mindre än {epsilon}: {Nmin}')
    epsilon=1E-10
    Nmin=int((RT[3]/hs[3]**p/epsilon)**(1/p))
    print(f'Uppskattning N_min för fel mindre än {epsilon}: {Nmin}')

    print(f"\nFel och feluppskattningar för Simpsons, h=(b-a)/(N-1)= 1/{Ns[1]-1}, 1/{Ns[2]-1}, ...,  1/{Ns[-1]-1}")
    V=[[Ns[ii+1]-1, ES[ii], RS[ii], RS[ii]/hs[ii]**4] for ii in range(p_max-p_min-1)]
    print(tabulate(V, headers=['1/h','Fel', 'Richarson','C']))

    p=4
    epsilon=1E-10
    Nmin=int(np.abs((RS[3]/hs[3]**p/epsilon))**(1/p))
    print(f'Uppskattning N_min för fel mindre än {epsilon}: {Nmin}')

def F23_1():
    # Exempel 1, f1(x)=3x^2 F(x)=x^3+C [1,2] I=7
    (a,b,p_min,p_max,I,eq)=(1,2,3,18,7,1)
    print_statistics_F23a(f1,a,b,I,p_min,p_max,eq)
    plot_figures_F23a(f1,a,b,I,p_min,p_max,eq)

def F23_2():
    # Exempel 2, f2(x)=sin((pi*x)^2)+2x+1, [0,1] Integralen approximerad nedan med hög precision
    (a,b,p_min,p_max,I,eq)=(0,1,3,18,2.2459426787260857285430684656189996584112396431725709320270040155,2)
    print_statistics_F23a(f2,a,b,I,p_min,p_max,eq)
    plot_figures_F23a(f2,a,b,I,p_min,p_max,eq)

def F23_3():
    # Exempel 3, f3(x)=x^(2/3) [0,1]
    (a,b,p_min,p_max,I,eq)=(0,1,3,18,0.6,3)
    print_statistics_F23a(f3,a,b,I,p_min,p_max,eq)
    plot_figures_F23a(f3,a,b,I,p_min,p_max,eq)

def F23_4():
    # Exempel 2 Richardson feluppskattning samt uppskatta hur stort Nmin behöver vara för olika toleranser
    (a,b,p_min,p_max,I,eq)=(0,1,3,18,2.2459426787260857285430684656189996584112396431725709320270040155,2)
    print_statistics_F23b(f2,a,b,I,p_min,p_max,eq)

if __name__=='__main__':
    F23_1()
    F23_2()
    F23_3()
    F23_4()
    
