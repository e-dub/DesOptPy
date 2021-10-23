# -*- coding: utf-8 -*-
"""
Himmelblau test function for design optimization

xOpt = [3.0, 2.0]
xOpt = [-2.805118, 3.131312]
xOpt = [-3.779310, -3.283186]
xOpt = [3.584428, -1.848126]
fOpt = 0.0
"""
from DesOptPy import OptimizationProblem
import numpy as np


class Himmelblau:
    x = np.zeros(
        [
            2,
        ]
    )

    def SysEq(self):
        self.f = (self.x[0] ** 2 + self.x[1] - 11) ** 2 + (
            self.x[0] + self.x[1] ** 2 - 7
        ) ** 2


OptHimmelblau = OptimizationProblem(Himmelblau)
OptHimmelblau.Primal = 'SysEq'
OptHimmelblau.x = 'x'
OptHimmelblau.x0 = (
    np.ones(
        2,
    )
    * +0
)
OptHimmelblau.xL = (
    np.ones(
        2,
    )
    * -5
)
OptHimmelblau.xU = (
    np.ones(
        2,
    )
    * +5
)
OptHimmelblau.f = 'f'
OptHimmelblau.Alg = 'SOLVOPT'
OptHimmelblau.optimize()
OptHimmelblau.plotConvergence()
