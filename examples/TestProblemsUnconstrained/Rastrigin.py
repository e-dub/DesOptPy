# -*- coding: utf-8 -*-
"""
Rastrigin test function for design optimization

xOpt = 0
fOpt = 0.0
"""
from DesOptPy import OptimizationProblem
import numpy as np


class Rastrigin:
    x = np.zeros(
        [
            2,
        ]
    )

    def SysEq(self):
        n = len(self.x)
        self.f = 10 * n + np.sum(
            self.x ** 2 - 10 * np.cos(2.0 * np.pi * self.x)
        )


OptRastrigin = OptimizationProblem(Rastrigin)
OptRastrigin.Primal = 'SysEq'
OptRastrigin.x = 'x'
OptRastrigin.x0 = (
    np.ones(
        2,
    )
    * +2
)
OptRastrigin.xL = (
    np.ones(
        2,
    )
    * -5
)
OptRastrigin.xU = (
    np.ones(
        2,
    )
    * +5
)
OptRastrigin.f = 'f'
OptRastrigin.optimize()
OptRastrigin.plotConvergence()
