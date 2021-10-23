from DesOptPy import OptimizationProblem
from scipy.optimize import rosen, rosen_der
import numpy as np


class Rosenbrock:
    def calc(self):
        self.obj = rosen(self.x)

    def calcSens(self):
        self.objNabla = rosen_der(self.x)


ProbRosenbrockSens = OptimizationProblem(Rosenbrock)
ProbRosenbrockSens.RunFolder = True
nx = 20
ProbRosenbrockSens.x = 'x'
ProbRosenbrockSens.x0 = (
    np.ones(
        nx,
    )
    * +2
)
ProbRosenbrockSens.xL = (
    np.ones(
        nx,
    )
    * -5
)
ProbRosenbrockSens.xU = (
    np.ones(
        nx,
    )
    * +5
)
ProbRosenbrockSens.xNorm = [True] * nx
ProbRosenbrockSens.xType = ['continuous'] * nx
ProbRosenbrockSens.f = ['obj']
ProbRosenbrockSens.fNorm = [False]
ProbRosenbrockSens.Alg = 'NLPQLP'
ProbRosenbrockSens.Primal = 'calc'
ProbRosenbrockSens.Sensitivity = 'calcSens'
ProbRosenbrockSens.fNabla = ['objNabla']
ProbRosenbrockSens.TablesPlots = True
ProbRosenbrockSens.optimize()
ProbRosenbrockSens.plotConvergence()
ProbRosenbrockSens.plotBeforeAfter()
