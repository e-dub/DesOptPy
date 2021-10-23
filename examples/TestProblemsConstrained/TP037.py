# -*- coding: utf-8 -*-
"""
Test function for design optimization

f* = -3456.
x* = 24.0, 12.0, 12.0
"""
from DesOptPy import OptimizationProblem
import numpy as np


class TP037:
    x = [1, 1]

    def SysEq(self):
        print(self.x)
        self.f = -self.x[0] * self.x[1] * self.x[2]
        self.g = (
            np.ones(
                [
                    2,
                ]
            )
            * 0.0
        )
        self.g[0] = self.x[0] + 2.0 * self.x[1] + 2.0 * self.x[2] - 72.0
        self.g[1] = -self.x[0] - 2.0 * self.x[1] - 2.0 * self.x[2]


OptTP037 = OptimizationProblem(TP037)
OptTP037.Primal = 'SysEq'
OptTP037.x = 'x'
OptTP037.x0 = [20] * 3
OptTP037.xL = [0] * 3
OptTP037.xU = [40] * 3
OptTP037.f = 'f'
OptTP037.g = ['g']
OptTP037.gLimit = [0] * 2
OptTP037.optimize()
OptTP037.plotConvergence()
OptTP037.plotBeforeAfter()
