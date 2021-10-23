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
    x = 1
    y = 2

    def SysEq(self):
        exhaustOffset = 1.34
        exhaustDia = 1.556
        intakeOffset = 3.25
        self.warranty = 100000 + 15000 * (4 - self.y)
        self.cycleTime = 45 + 4.5 * pow(4 - self.y, 1.5)
        wallThickness = (
            intakeOffset - exhaustOffset - (self.x + exhaustDia) / 2
        )
        horsePower = 250.0 + 200.0 * (self.x / 1.833 - 1.0)
        self.maxStress = 750 + pow(np.fabs(wallThickness), -2.5)
        self.f = -1 * (horsePower / 250 + self.warranty / 100000)


OptCylinderHead = OptimizationProblem(CylinderHead)
OptCylinderHead.Primal = 'SysEq'
OptCylinderHead.x = ['x', 'y']
OptCylinderHead.xDelta = 1e-6
OptCylinderHead.x0 = [1.8, 1.0]
OptCylinderHead.xL = [1.5, 0.0]
OptCylinderHead.xU = [2.164, 4.0]
OptCylinderHead.f = 'f'
OptCylinderHead.g = ['maxStress', 'warranty', 'cycleTime']
OptCylinderHead.gType = ['upper', 'lower', 'upper']
OptCylinderHead.gLimit = [1500, 100000, 60]
OptCylinderHead.optimize()
OptCylinderHead.plotConvergence()
OptCylinderHead.plotBeforeAfter()
