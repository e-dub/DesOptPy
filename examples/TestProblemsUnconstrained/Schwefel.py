# -*- coding: utf-8 -*-
"""
Schwefel test function for design optimization

xOpt = 420
fOpt = 0
"""
from DesOptPy import OptimizationProblem
import numpy as np


class Schwefel:
    def SysEq(self):
        n = len(self.x)
        self.f = 418.9829 * n - np.sum(
            self.x * np.sin(np.sqrt(np.abs(self.x)))
        )


OptSchwefel = OptimizationProblem(Schwefel)
OptSchwefel.Primal = 'SysEq'
OptSchwefel.x = 'x'
nx = 20
OptSchwefel.x0 = np.ones(
    nx,
)
OptSchwefel.xL = (
    np.ones(
        nx,
    )
    * -500
)
OptSchwefel.xU = (
    np.ones(
        nx,
    )
    * +500
)
OptSchwefel.Alg = 'ALHSO'
OptSchwefel.f = 'f'
OptSchwefel.optimize()
OptSchwefel.plotConvergence()
