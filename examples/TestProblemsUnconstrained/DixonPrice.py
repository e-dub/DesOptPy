# -*- coding: utf-8 -*-
"""
Dixon Price test function for design optimization

xOpt =
fOpt = 0.0
"""
from DesOptPy import OptimizationProblem
import numpy as np


class DixenPrice:
    x = 10

    def SysEq(self):
        n = len(self.x)
        j = np.arange(2, n + 1)
        x2 = 2 * self.x ** 2
        self.f = np.sum(j * (x2[1:] - self.x[:-1]) ** 2) + (self.x[0] - 1) ** 2


nx = 2
OptDixenPrice = OptimizationProblem(DixenPrice)
OptDixenPrice.x = 'x'
OptDixenPrice.x0 = [0] * nx
OptDixenPrice.xL = -10
OptDixenPrice.xU = +10
OptDixenPrice.f = 'f'
OptDixenPrice.Alg = 'SLSQP'
OptDixenPrice.Primal = 'SysEq'
OptDixenPrice.optimize()
OptDixenPrice.plotConvergence()
