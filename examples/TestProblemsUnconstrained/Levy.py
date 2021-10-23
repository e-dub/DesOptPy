# -*- coding: utf-8 -*-
"""
Levy test function for design optimization

xOpt = 1
fOpt = 0.0
"""
from DesOptPy import OptimizationProblem
import numpy as np


class Levy:
    x = np.zeros(
        [
            2,
        ]
    )

    def SysEq(self):
        n = len(self.x)
        z = 1.0 + (self.x - 1.0) / 4.0
        self.f = (
            np.sin(np.pi * z[0]) ** 2
            + np.sum(
                (z[:-1] - 1.0) ** 2
                * (1.0 + 10.0 * np.sin(np.pi * z[:-1] + 1.0) ** 2)
            )
            + (z[-1] - 1.0) ** 2 * (1.0 + np.sin(2.0 * np.pi * z[-1]) ** 2)
        )


OptLevy = OptimizationProblem(Levy)
OptLevy.Primal = 'SysEq'
OptLevy.x = 'x'
OptLevy.x0 = (
    np.ones(
        2,
    )
    * +0
)
OptLevy.xL = (
    np.ones(
        2,
    )
    * -5
)
OptLevy.xU = (
    np.ones(
        2,
    )
    * +5
)
OptLevy.f = 'f'
OptLevy.optimize()
OptLevy.plotConvergence()
