
import numpy as np
import math as m 
import sys
import RungeKuttaFehlberg as RKF

W=np.array([0,1,0]);
h=1/4;
tol=05e-15;
tEnd=1.0;

def F1A(Y):
    M=np.array([[1, 1,],
                [-1, 1]]);
    res=np.ones(3); 
    res[1:3]=M.dot(Y[1:3]);
    return res;

def F1B(Y):
    M=np.array([[-1, -1,],
                [1, -1]]);
    res=np.ones(3); 
    res[1:3]=M.dot(Y[1:3]);
    return res;

def do_RKF_on(f,dim,h,tol):
    rkf54 = RKF.RungeKuttaFehlberg54(f,dim,h,tol)

    W=np.array([0,1,0]);
    while(W[0]<tEnd):
        W , E = rkf54.safeStep(W);
        #print(W[0])
    rkf54.setStepLength(tEnd-W[0]);
    return rkf54.step(W)

def oppg1Ach6_3():
    W,E = do_RKF_on(F1A,3,h,tol);
    
    y1Eksakt = lambda num: m.e**(num)*m.cos(num) 
    y2Eksakt = lambda num: -m.e**(num)*m.sin(num) 
    eksaktSvar=[y1Eksakt(1), y2Eksakt(1)]
    printRes("Oppg 1a kapittel 6.3",W,E,eksaktSvar)

def oppg1Bch6_3():
    W,E = do_RKF_on(F1B,3,h,tol);
    
    y1Eksakt = lambda num: m.e**(num)*m.cos(-num) 
    y2Eksakt = lambda num: m.e**(-num)*m.sin(num) 

    eksaktSvar=[y1Eksakt(1), y2Eksakt(1)]
    printRes("Oppg 1b kapittel 6.3",W,E,eksaktSvar)


def tidPerToleranse():
    import time
    import matplotlib.pyplot as plt

    times=[]
    tols=[]

    for tol in np.linspace(1e-10,1e-15,500):
      time1 = time.time()
      W,E = do_RKF_on(F1B,3,h,tol);
      time2 = time.time()
      times.append([time2-time1])
      tols.append(tol) 
    
    fig= plt.figure()
    fig.set_size_inches(18.5, 10.5)
    plt.plot(tols,times)
    #plt.plot(times,tols)
    #print(tols)
    
    
def printRes(headline,W,E,eksaktSvar):
    print(headline)
    print(" Tilnærma svar:          ", W[1:]);
    print(" Eksakt svar:            ", eksaktSvar)
    print(" Global feil ved t=1:    ", W[1:]-eksaktSvar)
    print(" Akkumulert feil ved t=1:", E)
    print()

if __name__ == "__main__":
    oppg1Ach6_3()
    oppg1Bch6_3()
    #tidPerToleranse()

