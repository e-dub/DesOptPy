# -*- coding: utf-8 -*-
"""
Styblinski--Tang test function for design optimization

xOpt = -2.9
fOpt = -78.3
"""

from DesOptPy import OptimizationProblem
import numpy as np


class Styblinski:
    def SysEq(self):
        self.f = (
            1.0
            / 2.0
            * (
                self.x ** 4
                - 16.0 * self.x ** 2
                + 5.0 * self.x
                + self.y ** 4
                - 16.0 * self.y ** 2
                + 5.0 * self.y
            )
        )


OptStyblinski = OptimizationProblem(Styblinski)
OptStyblinski.Primal = 'SysEq'
OptStyblinski.x = ['x', 'y']
OptStyblinski.x0 = (
    np.ones(
        2,
    )
    * +0
)
OptStyblinski.xL = (
    np.ones(
        2,
    )
    * -5
)
OptStyblinski.xU = (
    np.ones(
        2,
    )
    * +5
)
OptStyblinski.f = 'f'
OptStyblinski.Alg = 'ALHSO'
OptStyblinski.optimize()
OptStyblinski.plotConvergence()
