"""
Bridge optimization with EasyBeam by V. Gufler

Optimal design:
m = 1.3717276936208906

bC = 103.08191126643098 (50, 300)
h1 = 128.01100364996728 (50, 300)
h2 = 119.65089778984994 (50, 300)
bF = 40.404135169494396 (20, 300)
t = 10.00000000000018 (2, 10)
"""
from EasyBeam import Beam2D
import numpy as np
from scipy.constants import g
from DesOptPy import OptimizationProblem


g *= 1e3  # mm/s^2


class Bridge:
    bC = 60
    h1 = 150
    h2 = 150
    bF = 150
    t = 10

    def calc(self, plot=False):
        E = 210000
        rho = 7.85e-9
        nu = 0.3
        L = 24000  # mm
        el = 23000
        H = 3500
        h = H - 4000
        B = 1500
        n = 13  # Ungerade Zahl!
        mN = 500 * 1e-9  # t/mm^2         # Nutzlast
        mS = 4000 * 1e-9  # t/mm^2         # Schneelast
        Frame = Beam2D()
        Frame.Properties = [
            ['1', rho, E, nu, 'C', self.h1, self.bC, self.t],
            ['2', rho, E, nu, 'C', self.h2, self.bC, self.t],
            ['3', rho, E, nu, 'rect', self.bF, self.t],
            ['4', rho, E, nu, 'rect', self.bF, self.t],
        ]
        F = (mN + mS) * g * B * L / 2
        x = np.linspace(0, L, n)
        y = -4 * H / L ** 2 * x ** 2 + 4 * H / L * x
        z = -4 * h / L ** 2 * x ** 2 + 4 * h / L * x
        Frame.Nodes = [[]] * (2 * n - 2)
        for i in range(n):
            Frame.Nodes[i] = [x[i], z[i]]
        for i in range(n - 2):
            Frame.Nodes[n + i] = [x[i + 1], y[i + 1]]
        Frame.Nodes[0] = [(L - el) / 2, 0]
        Frame.Nodes[n - 1] = [L - (L - el) / 2, 0]
        Frame.El = []
        Frame.PropID = []
        for i in range(n - 1):
            Frame.El.append([i + 1, i + 2])
            Frame.PropID.append('1')
        for i in range(n - 1):
            Frame.El.append([i + n, i + n + 1])
            Frame.PropID.append('2')
        Frame.El[n - 1][0] = 1
        Frame.El[2 * n - 3][1] = n
        for i in range((n - 2)):
            Frame.El.append([i + 2, i + n + 1])
            Frame.PropID.append('3')
        for i in range(int((n - 3) / 2)):
            Frame.El.append([2 * (i + 1) + 1, n + 2 * i + 1])
            Frame.PropID.append('4')
            Frame.El.append([2 * (i + 1) + 1, n + 2 * (i + 1) + 1])
            Frame.PropID.append('4')
        Frame.Disp = [[1, [0, 0, 'f']], [n, ['f', 0, 'f']]]
        Frame.Load = [[]] * (n - 2)
        for i in range(n - 2):
            Frame.Load[i] = [i + 2, [0, -F / (n - 2), 0]]
        Frame.Initialize()
        Frame.StaticAnalysis()
        Frame.ComputeStress()
        self.m = Frame.mass
        # TODO Change to KS!
        self.stressMax = np.max(Frame.sigmaMax)
        self.g2 = self.bC / self.h1
        self.g3 = self.bC / self.h2
        if plot:
            Frame.PlotMesh()
            Frame.PlotStress(stress='all')
            Frame.PlotDisplacement('mag')

    # TODO implement analytical sensitivities


initialDesign = Bridge()
initialDesign.calc(plot=True)

sigmaLim = 235  # MPa
OptBridge = OptimizationProblem(Bridge)
OptBridge.RemoveRunFolder = False
OptBridge.Primal = 'calc'
OptBridge.x = ['bC', 'h1', 'h2', 'bF', 't']
OptBridge.x0 = [60, 150, 150, 100, 10]
OptBridge.xL = [50, 50, 50, 20, 2]
OptBridge.xU = [300, 300, 300, 300, 10]
OptBridge.f = ['m']
OptBridge.g = ['stressMax', 'g2', 'g3']
OptBridge.gLimit = [sigmaLim, 1, 1]
OptBridge.Alg = 'NLPQLP'
OptBridge.optimize()
OptBridge.plotConvergence()
OptBridge.plotBeforeAfter()

optimumDesign = Bridge()
optimumDesign.bC = OptBridge.xOpt[0]
optimumDesign.h1 = OptBridge.xOpt[1]
optimumDesign.h2 = OptBridge.xOpt[2]
optimumDesign.bF = OptBridge.xOpt[3]
optimumDesign.t = OptBridge.xOpt[4]
optimumDesign.calc(plot=True)
