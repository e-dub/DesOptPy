# -*- coding: utf-8 -*-
"""
Cylinder head test function for design optimization

Source:  Dakota User's Guide §20.4

xOpt = [2.122, 1.769]
fOpt = -2.461
"""
from DesOptPy import OptimizationProblem
import numpy as np


class CylinderHead:
    x = [1, 1]

    def SysEq(self):
        print(self.x)
        exhaustOffset = 1.34
        exhaustDia = 1.556
        intakeOffset = 3.25
        warranty = 100000 + 15000 * (4 - self.x[1])
        cycleTime = 45 + 4.5 * pow(4 - self.x[1], 1.5)
        wallThickness = (
            intakeOffset - exhaustOffset - (self.x[0] + exhaustDia) / 2
        )
        horsePower = 250.0 + 200.0 * (self.x[0] / 1.833 - 1.0)
        maxStress = 750 + pow(np.fabs(wallThickness), -2.5)
        self.f = -1 * (horsePower / 250 + warranty / 100000)
        self.g1 = maxStress / 1500.0 - 1.0
        self.g2 = 1.0 - warranty / 100000.0
        self.g3 = cycleTime / 60.0 - 1.0


OptCylinderHead = OptimizationProblem(CylinderHead)
OptCylinderHead.Primal = 'SysEq'
OptCylinderHead.x = 'x'
OptCylinderHead.x0 = [1.8, 1.0]
OptCylinderHead.xL = [1.5, 0.0]
OptCylinderHead.xU = [2.164, 4.0]
OptCylinderHead.f = 'f'
OptCylinderHead.g = ['g1', 'g2', 'g3']
OptCylinderHead.gLimit = [0] * 3
OptCylinderHead.Alg = 'SCIPY_SLSQP'
OptCylinderHead.optimize()
OptCylinderHead.plotConvergence()
OptCylinderHead.plotBeforeAfter()
