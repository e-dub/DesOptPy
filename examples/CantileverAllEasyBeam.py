from DesOptPy import OptimizationProblem
from DesOptPy.FunctionAggregation import KS2, KS2Sens
from EasyBeam import Beam2D
import numpy as np

# Initialisiern des Problems
class OptModel:
    h_x = [20] * 10
    b_x = [10] * 10
    xGeo = [20]*20
    class AnalysisModel(Beam2D):

        xGeo = [20]*20
        F_x = -1000        # N
        l_x = 1000        # mm
        E_x = 70000      # MPa
        rho_x = 2.8e-9   # t/mm^3
        nu_x = 0.3
        DesVar = [[]]*20
        for i in range(10):
            exec('h_x'+str(i+1)+"=1")
            exec('b_x'+str(i+1)+"=1")
            DesVar[i] ='h_x'+str(i+1)
            DesVar[i+10] ='b_x'+str(i+1)
        def __init__(self):
            self.nEl = 10
            self.nSeg = 2
            self.stiffMatType = 'Euler-Bernoulli'
            self.massMatType = 'consistent'
            self.PropID = []
            self.Properties = []
            for i in range(10):
                self.Properties.append([
                        'Prop' + str(i + 1),
                        self.rho_x,
                        self.E_x,
                        self.nu_x,
                        'rect',
                        eval("self.h_x"+str(i+1)),
                        eval("self.b_x"+str(i+1)),
                ])
                self.PropID.append('Prop'+str(i+1))
            self.Nodes = [[]] * (self.nEl + 1)
            for i in range(self.nEl + 1):
                self.Nodes[i] = [self.l_x * i / self.nEl, 0.0]
            self.El = [[]] * (self.nEl)
            for i in range(self.nEl):
                self.El[i] = [i + 1, i + 2]
            self.Disp = [[1, [0, 0, 0]]]
            self.Load = [[self.nEl + 1, [self.F_x, self.F_x, 0]]]

    def calc(self):
        self.Cantilever = self.AnalysisModel()
        for i in range(10):
                exec("self.Cantilever.h_x"+str(i+1)+" = self.xGeo["+str(i)+"]")
                exec("self.Cantilever.b_x"+str(i+1)+" = self.xGeo["+str(i+10)+"]")
        self.Cantilever.xGeo = self.xGeo
        self.Cantilever.StaticAnalysis()
        self.Cantilever.ComputeStress()
        self.u = self.Cantilever.u
        self.epsilon = self.Cantilever.epsilon
        self.sigma = self.Cantilever.sigma
        self.mass = self.Cantilever.mass
        self.uMax = -self.u[-2]
        self.sigmaMax = KS2(
            np.reshape(
                self.Cantilever.sigmaEqvMax,
                self.Cantilever.nEl * (self.Cantilever.nSeg + 1),
            )
        )

    def sens(self):
        self.Cantilever.SensitivityAnalysis(xDelta=1e-9)
        self.Cantilever.ComputeStressSensitivity()
        self.uNabla = self.Cantilever.uNabla
        self.epsislonNabla = self.Cantilever.epsilonNabla
        self.sigmaNabla = self.Cantilever.sigmaNabla
        self.massNabla = self.Cantilever.massNabla
        self.uMaxNabla = -self.Cantilever.uNabla[-1, :]
        self.sigmaMaxNabla = KS2Sens(
            np.reshape(
                self.Cantilever.sigmaEqvMax,
                self.Cantilever.nEl * (self.Cantilever.nSeg + 1),
            ),
            np.reshape(
                self.Cantilever.sigmaEqvMaxNabla,
                (self.Cantilever.nEl * (self.Cantilever.nSeg + 1), 20),
            )
        )

CantileverOpt = OptimizationProblem(OptModel)
CantileverOpt.Primal = 'calc'
CantileverOpt.x = ['xGeo']
CantileverOpt.nx = [20]
CantileverOpt.x0 = [10]*20
CantileverOpt.xL = [1]*20
CantileverOpt.xU = [300]*20
CantileverOpt.f = ['mass']
CantileverOpt.g = ['uMax', 'sigmaMax']
CantileverOpt.gLimit = [10.0, 100.0]
CantileverOpt.Sensitivity = 'sens'
CantileverOpt.fNabla = ['massNabla']
CantileverOpt.gNabla = ['uMaxNabla', 'sigmaMaxNabla']
CantileverOpt.Alg = 'NLPQLP'
CantileverOpt.optimize()
CantileverOpt.plotConvergence()
CantileverOpt.plotBeforeAfter()
