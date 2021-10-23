# -*- coding: utf-8 -*-
"""
Description: Simple multi-objective test function for design optimization with use of weighting factors resulting in a Pareto front
"""
from DesOptPy import OptimizationProblem
import numpy as np


class Multobj:
    x = 2

    def SysEq(self):
        self.f1 = self.x
        self.f2 = 100.0 - self.x ** 2
        self.f = -1 * ((gamma[ii] * self.f1) + self.f2)


nPareto = 21
xOpt = [[]] * nPareto
fOpt = [[]] * nPareto
f1 = [[]] * nPareto
f2 = [[]] * nPareto
nEval = [[]] * nPareto
gamma = np.logspace(-1, 1, nPareto)
for ii in range(nPareto):
    OptMultobj = OptimizationProblem(Multobj)
    OptMultobj.Primal = 'SysEq'
    OptMultobj.x = 'x'
    OptMultobj.xL = np.ones((1,)) * 0
    OptMultobj.xU = np.ones((1,)) * 10
    OptMultobj.x0 = np.average((OptMultobj.xL, OptMultobj.xU), 0)
    OptMultobj.f = 'f'
    OptMultobj.optimize()
    xOpt[ii] = OptMultobj.xOpt
    OptMultobj.x0 = xOpt[ii]  # Better start value
    Eval = Multobj()
    Eval.x = xOpt[ii][0]
    Eval.SysEq()
    f1[ii] = Eval.f1
    f2[ii] = Eval.f2
ParetoFront = np.array([f1, f2])
print(ParetoFront)
