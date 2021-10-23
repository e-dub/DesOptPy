# -*- coding: utf-8 -*-
"""
Griewank test function for design optimization

xOpt = []
fOpt = 0.0
"""
from DesOptPy import OptimizationProblem
import numpy as np


class Griewank:
    x = [1, 1]

    def SysEq(self):
        fr = 4000
        n = len(self.x)
        j = np.arange(1.0, n + 1)
        s = np.sum(self.x ** 2)
        p = np.prod(np.cos(self.x / np.sqrt(j)))
        self.f = s / fr - p + 1


OptGriewank = OptimizationProblem(Griewank)
OptGriewank.x = 'x'
OptGriewank.x0 = [0] * 2
OptGriewank.xL = -5
OptGriewank.xU = 5
OptGriewank.f = 'f'
OptGriewank.Primal = 'SysEq'
OptGriewank.optimize()
OptGriewank.plotConvergence()
