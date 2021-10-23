# -*- coding: utf-8 -*-
"""
Eggholder test function for design optimization

xOpt = []
fOpt = 0.0
"""
from DesOptPy import OptimizationProblem
import numpy as np


class Eggholder:
    z = [1, 1]

    def SysEq(self):
        x = self.z[0]
        y = self.z[1]
        self.f = -(y + 47.0) * np.sin(
            np.sqrt(abs(y + x / 2.0 + 47.0))
        ) - x * np.sin(np.sqrt(abs(x - (y + 47.0))))


OptEggholder = OptimizationProblem(Eggholder)
OptEggholder.x = 'z'
OptEggholder.x0 = [0] * 2
OptEggholder.xL = -5
OptEggholder.xU = 5
OptEggholder.f = 'f'
OptEggholder.fNorm = False
OptEggholder.Alg = 'SLSQP'
OptEggholder.Primal = 'SysEq'
OptEggholder.optimize()
OptEggholder.plotConvergence()
