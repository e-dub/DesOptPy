#TODO Noramlizatoin of f not working
from DesOptPy import OptimizationProblem
from scipy.optimize import rosen, rosen_der
import numpy as np


class Rosenbrock:
    def calc(self, x):
        self.obj = rosen(x)

    def calcSens(self, x):
        self.objNabla = rosen_der(x)


ProbRosenbrockSens = OptimizationProblem(Rosenbrock)
ProbRosenbrockSens.RunFolder = True
nx = 100
ProbRosenbrockSens.x0 = np.ones(nx,)*+0
ProbRosenbrockSens.xL = np.ones(nx,)*-5
ProbRosenbrockSens.xU = np.ones(nx,)*+5
ProbRosenbrockSens.xNorm = [True]*nx
ProbRosenbrockSens.xType = ["continuous"]*nx
ProbRosenbrockSens.f = ["obj"]
ProbRosenbrockSens.fNorm = [False]
ProbRosenbrockSens.Alg = "NLPQLP"
ProbRosenbrockSens.Primal = "calc"
ProbRosenbrockSens.Sensitivity = "calcSens"
ProbRosenbrockSens.fNabla = ["objNabla"]
ProbRosenbrockSens.TablesPlots = True
ProbRosenbrockSens.optimize()
