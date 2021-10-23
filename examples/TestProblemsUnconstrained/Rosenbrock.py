"""
f*=0
x*=1
"""
from DesOptPy import OptimizationProblem
import numpy as np
from scipy.optimize import rosen, rosen_der


class Rosenbrock:
    def calc(self):
        self.obj = rosen(self.x)

    def calcSens(self):
        self.objNabla = rosen_der(self.x)


ProbRosenbrockSens = OptimizationProblem(Rosenbrock)
ProbRosenbrockSens.Primal = 'calc'
ProbRosenbrockSens.Sensitivity = 'calcSens'
nx = 10
ProbRosenbrockSens.x = 'x'
ProbRosenbrockSens.x0 = (
    np.ones(
        nx,
    )
    * 3
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
ProbRosenbrockSens.f = ['obj']
ProbRosenbrockSens.fNabla = ['objNabla']
ProbRosenbrockSens.Alg = 'SLSQP'
ProbRosenbrockSens.optimize()
ProbRosenbrockSens.plotConvergence()
