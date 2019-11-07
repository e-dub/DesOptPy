from DesOptPy import OptimizationSetup
import numpy as np
from copy import deepcopy


class Truss3Bar:
    Fx = 1000
    Fy = 1000
    A1 = 5
    A2 = 5
    el = 100
    E = 210e3

    def primal(self):
        self.volume = 2*2**0.5*self.A1+self.A2
        self.stress1 = 1/2**0.5*(self.Fx/self.A1 +
                                 self.Fy/(self.A1 + 2**0.5*self.A2))
        self.stress2 = 2**0.5*self.Fy/(self.A1 + 2**0.5*self.A2)
        self.stress3 = 1/2**0.5*(-self.Fx/self.A1 +
                                 self.Fy/(self.A1 + 2**0.5*self.A2))
        self.displacementx = 2**0.5*self.el*self.Fx/(self.A1*self.E)
        self.displacementy = (2**0.5*self.el*self.Fy /
                              ((self.A1+2**0.5*self.A2)*self.E))

    def sensitivity(self):
        self.volumeNabla = np.array([2*2**0.5, 1])
        self.stress1Nabla = np.array([-self.Fx/(2**0.5*self.A1**2) - 2**0.5*self.Fy/(2**0.5*self.A1 + 2*self.A2)**2,
                                      -2*self.Fy/(2**0.5*self.A1 + 2*self.A2)**2])
        self.stress2Nabla = np.array([-2**0.5*self.Fy/(self.A1 + 2**0.5*self.A2)**2,
                                      -2*self.Fy/(self.A1 + 2**0.5*self.A2)**2])
        self.stress3Nabla = np.array([+self.Fx/(2**0.5*self.A1**2) - 2**0.5*self.Fy/(2**0.5*self.A1 + 2*self.A2)**2,
                                      -2*self.Fy/(2**0.5*self.A1 + 2*self.A2)**2])
        self.displacementxNabla = np.array([-2**0.5*self.el*self.Fx/(self.A1**2*self.E),
                                            0])
        self.displacementyNabla = np.array([-2**0.5*self.el*self.Fy/((self.A1+2**0.5*self.A2)**2*self.E),
                                            -2*self.el*self.Fy/((self.A1+2**0.5*self.A2)**2*self.E)])


# System evaluation
TBT = Truss3Bar()
TBT.A1 = 10
TBT.A2 = 10
TBT.primal()

# Analytical sensitivity evaluation
TBT.sensitivity()

# Finite difference
xDelta = 0.000001
TBT1 = Truss3Bar()
TBT1.A1 = 10 + xDelta
TBT1.A2 = 10
TBT1.primal()
TBT2 = Truss3Bar()
TBT2.A1 = 10
TBT2.A2 = 10 + xDelta
TBT2.primal()
volumeNabla1FD = (TBT1.volume-TBT.volume)/xDelta
volumeNabla2FD = (TBT2.volume-TBT.volume)/xDelta
sigma1Nabla1FD = (TBT1.stress1-TBT.stress1)/xDelta
sigma1Nabla2FD = (TBT2.stress1-TBT.stress1)/xDelta
sigma2Nabla1FD = (TBT1.stress2-TBT.stress2)/xDelta
sigma2Nabla2FD = (TBT2.stress2-TBT.stress2)/xDelta
sigma3Nabla1FD = (TBT1.stress3-TBT.stress3)/xDelta
sigma3Nabla2FD = (TBT2.stress3-TBT.stress3)/xDelta
displacementxNabla1FD = (TBT1.displacementx-TBT.displacementx)/xDelta
displacementxNabla2FD = (TBT2.displacementx-TBT.displacementx)/xDelta
displacementyNabla1FD = (TBT1.displacementy-TBT.displacementy)/xDelta
displacementyNabla2FD = (TBT2.displacementy-TBT.displacementy)/xDelta

# Optimization with finite differences
OptTBT = OptimizationSetup(Truss3Bar)
OptTBT.RunFolder = False
OptTBT.f = ["volume"]
OptTBT.g = ["stress1", "stress2", "stress3", "displacementx", "displacementy"]
OptTBT.gType = ["upper"]*5
OptTBT.gNorm = [True]*5
OptTBT.gLimit = [100, 100, 100, 10, 10]
OptTBT.x = ["A1", "A2"]
OptTBT.x0 = [10, 10]
OptTBT.xL = [0.1, 0.1]
OptTBT.xU = [100, 100]
OptTBT.xDelta = 1e-3
OptTBT.xNorm = [True]*2
OptTBT.xType = ["continuous"]*2
OptTBT.fNorm = [False]
OptTBT.Alg = "NLPQLP"
OptTBT.Primal = "primal"
OptTBT.optimize()

# Optimization with analytical senstivities
# copied from FD optimization changing sensitivity analysis type and rerunning
OptTBTsens = deepcopy(OptTBT)
OptTBTsens.Sensitivity = "sensitivity"
OptTBTsens.fNabla = ["volumeNabla"]
OptTBTsens.gNabla = ["stress1Nabla", "stress2Nabla", "stress3Nabla",
                     "displacementxNabla", "displacementyNabla"]
OptTBTsens.optimize()


#OptTBTautosens = deepcopy(OptTBTsens)
#OptTBTsens.Sensitivity = "autograd"
#OptTBTsens.optimize()

#TBT.A1 = OptTBT.A1
#TBT.A2 = OptTBT.A2
#TBT.primal()
#
#print(TBT.stress1)
#print(TBT.stress2)
#print(TBT.stress3)
#print(TBT.displacementx)
#print(TBT.displacementy)