# -*- coding: utf-8 -*-
"""
Ackley test function for design optimiazation

xOpt = [0.0, 0.0]
fOpt = 0.0
"""
from DesOptPy import OptimizationProblem
import numpy as np


class Ackley:
    x = 10

    def SysEq(self):
        a = 20
        b = 0.2
        c = 2 * np.pi
        n = len(self.x)
        s1 = sum(self.x ** 2)
        s2 = sum(np.cos(c * self.x))
        self.f = (
            -a * np.exp(-b * np.sqrt(s1 / n)) - np.exp(s2 / n) + a + np.exp(1)
        )


nx = 10
OptAckley = OptimizationProblem(Ackley)
OptAckley.x = 'x'
OptAckley.x0 = [1] * nx
OptAckley.xL = -5
OptAckley.xU = 5
OptAckley.f = 'f'
OptAckley.Primal = 'SysEq'
OptAckley.optimize()
OptAckley.plotConvergence()
