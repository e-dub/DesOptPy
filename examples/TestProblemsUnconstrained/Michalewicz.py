# -*- coding: utf-8 -*-
"""
Michalewicz test function for design optimization

xOpt = 0
fOpt = 0.0
"""
from DesOptPy import OptimizationProblem
import numpy as np


class Michalewicz:
    x = np.zeros(
        [
            2,
        ]
    )

    def SysEq(self):
        michalewicz_m = 2
        n = len(self.x)
        j = np.arange(1.0, n + 1)
        self.f = -np.sum(
            np.sin(self.x)
            * np.sin(j * self.x ** 2 / np.pi) ** (2.0 * michalewicz_m)
        )


OptMichalewicz = OptimizationProblem(Michalewicz)
OptMichalewicz.Primal = 'SysEq'
OptMichalewicz.x = 'x'
OptMichalewicz.x0 = (
    np.ones(
        2,
    )
    * +0
)
OptMichalewicz.xL = (
    np.ones(
        2,
    )
    * -5
)
OptMichalewicz.xU = (
    np.ones(
        2,
    )
    * +5
)
OptMichalewicz.f = 'f'
OptMichalewicz.Alg = 'PSQP'
OptMichalewicz.optimize()
OptMichalewicz.plotConvergence()
