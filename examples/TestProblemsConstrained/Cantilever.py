"""
xOpt = [ 2.35342485  3.32421007]
fOpt = 7.82327859
"""
from DesOptPy import OptimizationProblem
import numpy as np
import time


class Cantilever:
    e = 2.9e7
    r = 40000.0
    fx = 500.0
    fy = 1000.0
    w = 1.8
    t = 1.0
    L = 100.0
    D0 = 2.2535
    area = None
    stress = None

    def calc(self):
        # time.sleep(1)
        self.area = self.w * self.t
        self.stress = (
            600 * self.fy / self.w / self.t ** 2
            + 600 * self.fx / self.w ** 2 / self.t
        )
        D1 = 4.0 * pow(self.L, 3) / self.e / self.area
        D2 = pow(self.fy / self.t ** 2, 2) + pow(self.fx / self.w ** 2, 2)
        D3 = D1 / np.sqrt(D2) / self.D0
        self.D4 = D1 * np.sqrt(D2) / self.D0


Prob1 = OptimizationProblem(Cantilever)
Prob1.RemoveRunFolder = False
Prob1.Monitoring = True
Prob1.Primal = 'calc'
Prob1.x = ['w', 't']
Prob1.x0 = [1.8, 1.0]
Prob1.xL = [1.0, 1.0]
Prob1.xU = [4.0, 4.0]
Prob1.f = ['area']
Prob1.g = ['stress', 'D4']
Prob1.gLimit = [40000, 1]
Prob1.gNorm = [True, False]
Prob1.Alg = 'NLPQLP'
Prob1.optimize()
Prob1.plotConvergence()
Prob1.plotBeforeAfter()


Prob2 = OptimizationProblem(Cantilever)
Prob2.Primal = 'calc'
Prob2.x = ['w']
Prob2.x0 = [1.8]
Prob2.xL = [1.0]
Prob2.xU = [100.0]
Prob2.f = ['area']
Prob2.g = ['stress', 'D4']
Prob2.gType = ['upper', 'upper']
Prob2.gNorm = [True, False]
Prob2.gLimit = [40000, 1]
Prob2.Alg = 'NLPQLP'
Prob2.optimize()
Prob2.plotConvergence()
Prob2.plotBeforeAfter()

Prob3 = OptimizationProblem(Cantilever)
Prob3.Primal = 'calc'
Prob3.x = ['t']
Prob3.x0 = [1.8]
Prob3.xL = [1.0]
Prob3.xU = [100.0]
Prob3.xNorm = [True]
Prob3.xType = ['continuous']
Prob3.f = ['area']
Prob3.g = ['stress', 'D4']
Prob3.gType = ['upper', 'upper']
Prob3.gNorm = [True, False]
Prob3.gLimit = [40000, 1]
Prob3.Alg = 'NLPQLP'
Prob3.optimize()
Prob3.plotConvergence()
Prob3.plotBeforeAfter()
