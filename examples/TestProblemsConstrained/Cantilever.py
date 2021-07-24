# -*- coding: utf-8 -*-
"""
Title:    Cantilever.py
Units:    -
Author:   E.J. Wehrle
Date:     November 30, 2014
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Description:

Cantilever test function for design optimization

Source:  Dakota User's Guide §21.6

xOpt = [ 2.35342485  3.32421007]
fOpt = 7.82327859
-------------------------------------------------------------------------------
"""
from DesOptPy import DesOpt
from DesOptPy import OptAlgOptions
import numpy as np


def SysEq(x, gc):
    e = 2.9e7
    r = 40000.
    fx = 500.
    fy = 1000.
    w = x[0]
    t = x[1]
    area = w*t
    f = area
    D0 = 2.2535
    L = 100.
    w_sq = w*w
    t_sq = t*t
    r_sq = r*r
    x_sq = fx*fx
    y_sq = fy*fy
    stress = 600.*fy/w/t_sq + 600.*fx/w_sq/t
    D1 = 4.*pow(L,3)/e/area
    D2 = pow(fy/t_sq, 2)+pow(fx/w_sq, 2)
    D3 = D1/np.sqrt(D2)/D0
    D4 = D1*np.sqrt(D2)/D0
    g1 = stress/r - 1.
    g2 = D4 - 1.
    return f, [g1, g2]


xL = np.array([1.0, 1.0])
xU = np.array([4.0, 4.0])
gc = np.array([0.0, 0.0])
x0 = np.array([1.8, 1.0])

Alg = "IPOPT"
AlgOptions = OptAlgOptions.setDefault(Alg)
AlgOptions.MAXIT = 1000
xOpt, fOpt, Output = DesOpt(x0=x0, xL=xL, xU=xU, gc=gc, SysEq=SysEq, Alg=Alg,
                            AlgOptions=AlgOptions, deltax=1e-2,
                            DesVarNorm=True, Debug=False, ResultReport=True,
                            StatusReport=True, OptNameAdd="Cantilever"+Alg)
