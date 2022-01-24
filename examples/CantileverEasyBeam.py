from DesOptPy import OptimizationProblem
from DesOptPy.FunctionAggregation import KS2, KS2Sens
from EasyBeam import Beam2D
import numpy as np

# Initialisiern des Problems
class OptModel:
    h_x = 20
    b_x = 10

    class AnalysisModel(Beam2D):
        b_x = 10          # mm
        h_x = 20          # mm
        F_x = -1000        # N
        l_x = 1000        # mm
        E_x = 70000      # MPa
        rho_x = 2.8e-9   # t/mm^3
        nu_x = 0.3
        DesVar = ['h_x', 'b_x']

        def __init__(self):
            self.nEl = 10
            self.nSeg = 2
            self.stiffMatType = 'Euler-Bernoulli'
            self.massMatType = 'consistent'
            self.Properties = [
                [
                    'Prop1',
                    self.rho_x,
                    self.E_x,
                    self.nu_x,
                    'rect',
                    self.h_x,
                    self.b_x,
                ]
            ]
            self.Nodes = [[]] * (self.nEl + 1)
            for i in range(self.nEl + 1):
                self.Nodes[i] = [self.l_x * i / self.nEl, 0.0]
            self.El = [[]] * (self.nEl)
            for i in range(self.nEl):
                self.El[i] = [i + 1, i + 2]
            self.PropID = ['Prop1'] * self.nEl
            self.Disp = [[1, [0, 0, 0]]]
            self.Load = [[self.nEl + 1, [self.F_x, self.F_x, 0]]]

    def calc(self):
        self.Cantilever = self.AnalysisModel()
        self.Cantilever.h_x = self.h_x
        self.Cantilever.b_x = self.b_x
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
        self.Cantilever.SensitivityAnalysis()
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
                (self.Cantilever.nEl * (self.Cantilever.nSeg + 1), 2),
            ),
        )
        print(self.sigmaMaxNabla)


# Cantilever = OptModel()
# Cantilever.h_x = 20
# Cantilever.calc()
# Cantilever.sens()
# Cantilever.Cantilever.PlotDisplacement(scale=1)


CantileverOpt = OptimizationProblem(OptModel)
CantileverOpt.Primal = 'calc'
CantileverOpt.x = ['h_x', 'b_x']
CantileverOpt.x0 = [1, 1]
CantileverOpt.xL = [1, 1]
CantileverOpt.xU = [300, 300]
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
