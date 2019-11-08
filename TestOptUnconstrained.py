import numpy as np
from DesOptPy import OptimizationSetup
from TestModelsUnconstrained import Ackley, Michalewicz, Styblinski, Rosenbrock

#
#ProbAckley = OptimizationSetup(Ackley)
#ProbMichalewicz = OptimizationSetup(Michalewicz)
#
ProbStyblinski = OptimizationSetup(Styblinski)
ProbStyblinski.x = ["z", "y"]
ProbStyblinski.x0 = [0, 0]
ProbStyblinski.xL = [-5, -5]
ProbStyblinski.xU = [+5, +5]
ProbStyblinski.xNorm = [True, True]
ProbStyblinski.xType = ["continuous", "continuous"]
ProbStyblinski.f = ["v"]
ProbStyblinski.fNorm = [False]
ProbStyblinski.Alg = "NLPQLP"
ProbStyblinski.Primal = "calc"
ProbStyblinski.optimize()


ProbRosenbrock = OptimizationSetup(Rosenbrock)
ProbRosenbrock.RemoveRunFolder = False
nx = 10
ProbRosenbrock.x0 = [+0]*nx
ProbRosenbrock.xL = [-5]*nx
ProbRosenbrock.xU = [+5]*nx
ProbRosenbrock.xNorm = [True]*nx
ProbRosenbrock.xType = ["continuous"]*nx
ProbRosenbrock.f = ["obj"]
ProbRosenbrock.fNorm = [False]
ProbRosenbrock.Alg = "NLPQLP"
ProbRosenbrock.Primal = "calc"
ProbRosenbrock.optimize()


ProbRosenbrockNumpy = OptimizationSetup(Rosenbrock)
ProbRosenbrockNumpy.RunFolder = True
nx = 15
ProbRosenbrockNumpy.x0 = np.ones(nx,)*+0
ProbRosenbrockNumpy.RemoveRunFolder = False
ProbRosenbrockNumpy.SaveEvaluations = True
ProbRosenbrockNumpy.xL = np.ones(nx,)*-5
ProbRosenbrockNumpy.xU = np.ones(nx,)*+5
ProbRosenbrockNumpy.xNorm = [True]*nx
ProbRosenbrockNumpy.xDelta = 1e-8
ProbRosenbrockNumpy.xType = ["continuous"]*nx
ProbRosenbrockNumpy.f = ["obj"]
ProbRosenbrockNumpy.fNorm = [False]
ProbRosenbrockNumpy.Alg = "NLPQLP"
ProbRosenbrockNumpy.Primal = "calc"
ProbRosenbrockNumpy.optimize()


ProbRosenbrockSens = OptimizationSetup(Rosenbrock)
ProbRosenbrockSens.RunFolder = False
nx = 15
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
ProbRosenbrockSens.optimize()
