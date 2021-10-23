# -*- coding: utf-8 -*-
"""
Testbook test function for design optimization

Source:  https://dakota.sandia.gov//sites/default/files/docs/6.1/html-ref/textbook.html

Unconstrained:
xOpt = [0.1, 0.1]
fOpt = 0.0

Constrained:
xOpt = [0.5, 0.5]
fOpt = 0.125"""
from DesOptPy import OptimizationProblem
import numpy as np


class Textbook:
    x = [5, 0]

    def SysEq(self):
        self.f = (self.x[0] - 1.0) ** 4 + (self.x[1] - 1.0) ** 4
        self.g1 = self.x[0] ** 2 - self.x[1] / 2.0
        self.g2 = self.x[1] ** 2 - self.x[0] / 2.0


OptTextbook = OptimizationProblem(Textbook)
OptTextbook.Primal = 'SysEq'
OptTextbook.x = 'x'
OptTextbook.xL = [0.5, -2.9]
OptTextbook.xU = [5.8, 2.9]
OptTextbook.x0 = OptTextbook.xU
OptTextbook.f = 'f'
OptTextbook.optimize()
OptTextbook.plotConvergence()

OptTextbook = OptimizationProblem(Textbook)
OptTextbook.Primal = 'SysEq'
OptTextbook.x = 'x'
OptTextbook.xL = [0.5, -2.9]
OptTextbook.xU = [5.8, 2.9]
OptTextbook.x0 = OptTextbook.xU
OptTextbook.f = 'f'
OptTextbook.g = ['g1', 'g2']
OptTextbook.gLimit = [0, 0]
OptTextbook.optimize()
OptTextbook.plotConvergence()
OptTextbook.plotBeforeAfter()
