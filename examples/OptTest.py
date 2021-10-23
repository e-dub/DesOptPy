from DesOptPy import OptimizationProblem
from ModelTest1 import Model as Model1
from ModelTest2 import Model as Model2

Prob1 = OptimizationProblem(Model1)
Prob1.x = ['A', 'el']
Prob1.xL = [0.1, 0.1]
Prob1.xU = [1000.0, 1000.0]
Prob1.x0 = [100, 100]
Prob1.xNorm = [True, True]
Prob1.xType = ['continuous', 'continuous']
Prob1.f = ['m']
Prob1.fNorm = [True]
Prob1.g = ['sigma']
Prob1.gType = ['upper']
Prob1.gNorm = [False]
Prob1.gLimit = [100]
Prob1.Alg = 'NLPQLP'
Prob1.fNabla = ['mNabla']
Prob1.gNabla = ['sigmaNabla']
Prob1.Primal = 'calc'
Prob1.Sens = 'calcSens'
Prob1.optimize()
Prob1.plotConvergence()
Prob1.plotBeforeAfter()


Prob2 = OptimizationProblem(Model2)
Prob2.Primal = 'calc'
Prob2.x = ['a', 'ell']
Prob2.x0 = [10, 10]
Prob2.xL = [0.1, 0.1]
Prob2.xU = [1000.0, 1000.0]
Prob2.f = ['m']
Prob2.g = ['sigma']
Prob2.gLimit = [100]
Prob2.Alg = 'NLPQLP'
Prob2.optimize()
Prob2.plotConvergence()
Prob2.plotBeforeAfter()
