# -*- coding: utf-8 -*-
"""
Title:    RosenbrockSens.py
Units:    -
Author:   E.J. Wehrle
Date:     July 5, 2016
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Description:

Rosenbrock test function for design optimization

xOpt = [1, 1]
fOpt = 0

-------------------------------------------------------------------------------
"""
from DesOptPy import DesOpt
from DesOptPy import OptAlgOptions
import numpy as np
from scipy.optimize import rosen, rosen_der


def SysEq(x, gc):
    f = rosen(x)
    return f, []


def SensEq(x, f, g, gc):
    dfdx = rosen_der(x)
    return dfdx, []


x0 = (
    np.ones(
        [
            20,
        ]
    )
    * -1
)
xL = (
    np.ones(
        [
            20,
        ]
    )
    * -5
)
xU = (
    np.ones(
        [
            20,
        ]
    )
    * 5
)
gc = []
Alg = 'NLPQLP'
AlgOptions = OptAlgOptions.setDefault(Alg)
AlgOptions.MAXIT = 1000
SensEqList = [SensEq, '', '']
SensCalcList = ['', 'FD', 'AD']
Output = [[]] * len(SensEqList)
Name = ['AnaSens', 'NumSens', 'AutoDiff']
for ii in range(len(SensEqList)):
    xOpt, fOpt, Output[ii] = DesOpt(
        x0=x0,
        xL=xL,
        xU=xU,
        gc=gc,
        SysEq=SysEq,
        SensCalc=SensCalcList[ii],
        SensEq=SensEqList[ii],
        Alg=Alg,
        AlgOptions=AlgOptions,
        DesVarNorm=True,
        deltax=1e-4,
        ResultReport=False,
        StatusReport=False,
        OptNameAdd='RosenSens' + Name[ii],
    )
for ii in range(len(SensEqList)):
    print(Name[ii] + ':')
    print('nIter: ' + str(Output[ii]['nIter']))
    print('nEval: ' + str(Output[ii]['nEval']))
    print('')
