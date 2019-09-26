
import numpy as np
import math as m 
import sys
import RungeKuttaFehlberg as RKF


W=np.array([0,1,0]);
h=1/4;
tol=05e-10;
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

def oppg1Ach6_3():
    rkf54 = RKF.RungeKuttaFehlberg54(F1A,3,h,tol)

    W=np.array([0,1,0]);
    while(W[0]<tEnd):
        W , E = rkf54.safeStep(W);
    rkf54.setStepLength(tEnd-W[0]);
    W,E = rkf54.step(W);

    print(W,E);

def oppg1Bch6_3():
    rkf54 = RKF.RungeKuttaFehlberg54(F1B,3,h,tol)

    W=np.array([0,1,0]);
    while(W[0]<tEnd):
        W , E = rkf54.safeStep(W);
    rkf54.setStepLength(tEnd-W[0]);
    W,E = rkf54.step(W);

    print(W,E);

if __name__ == "__main__":
    oppg1Ach6_3()
    oppg1Bch6_3()
