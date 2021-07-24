"""
Bridge optimization with EasyBeam by V. Gufler
"""
from EasyBeam import Beam2D
import numpy as np
from scipy.constants import g
from DesOptPy import OptimizationProblem


g *= 1e3    # mm/s^2
class Bridge:
    def calc(self):
        # Initialisiern des Problems
        Frame = Beam2D()
        Frame.Properties = [['Prop1', 7.85e-9, 210000, 0.3, 'C', self.h1, self.bC, self.t],
                            ['Prop2', 7.85e-9, 210000, 0.3, 'C', self.h2,self. bC, self.t],
                            ['Prop3', 7.85e-9, 210000, 0.3, 'rect', self.bF, self.t],
                            ['Prop4', 7.85e-9, 210000, 0.3, 'rect', self.bF, self.t]]

        L = 24000    # mm
        l = 23000
        H = 3500
        h = H-4000
        B = 1500
        n = 13       # Ungerade Zahl!

        # Nutzlast
        mN = 500*1e-9   # t/mm^2
        # Schneelast
        mS = 4000*1e-9  # t/mm^2

        F = (mN+mS)*g*B*L/2

        x = np.linspace(0, L, n)
        y = -4*H/L**2*x**2+4*H/L*x
        z = -4*h/L**2*x**2+4*h/L*x

        # Knoten [mm]
        Frame.Nodes = [[]]*(2*n-2)
        for i in range(n):
            Frame.Nodes[i] = [x[i], z[i]]
        for i in range(n-2):
            Frame.Nodes[n+i] = [x[i+1], y[i+1]]

        Frame.Nodes[0] = [(L-l)/2, 0]
        Frame.Nodes[n-1] = [L-(L-l)/2, 0]

        # Elemente: verbindet die Knoten
        Frame.El = []
        Frame.PropID = []
        for i in range(n-1):
            Frame.El.append([i+1, i+2])
            Frame.PropID.append('Prop1')
        for i in range(n-1):
            Frame.El.append([i+n, i+n+1])
            Frame.PropID.append('Prop2')
        Frame.El[n-1][0] = 1
        Frame.El[2*n-3][1] = n

        # VertikalstÃ¤be
        for i in range((n-2)):
            Frame.El.append([i+2, i+n+1])
            Frame.PropID.append('Prop3')

        # WindverbÃ¤nde
        for i in range(int((n-3)/2)):
            Frame.El.append([2*(i+1)+1, n+2*i+1])
            Frame.PropID.append('Prop4')
            Frame.El.append([2*(i+1)+1, n+2*(i+1)+1])
            Frame.PropID.append('Prop4')

        # Randbedingungen und Belastung [N] bzw. [Nmm]
        Frame.Disp = [[1, [  0, 0, 'f']],
                      [n, ['f', 0, 'f']]]

        Frame.Load = [[]]*(n-2)
        for i in range(n-2):
            Frame.Load[i] = [i+2, [0, -F/(n-2), 0]]

        # Initialisieren des Modells
        Frame.Initialize()

        # Grafische Darstellung
        # Frame.PlotMesh()

        # LÃ¶sen
        Frame.StaticAnalysis()
        # Frame.Scale = 10
        Frame.ComputeStress()
        # Frame.EigenvalueAnalysis(nEig=1)

        # Frame.PlotStress(stress="all")
        # Frame.PlotDisplacement('mag')

        # Frame.ScalePhi = 1000
        # Frame.PlotMode()

        print('Gewicht', Frame.mass, 't')
        print('sigmaMax', np.max(Frame.sigmaMax), 'MPa')
        # print('fn1', Frame.f0[0], 'Hz')

        self.m = Frame.mass
        self.stressMax = np.max(Frame.sigmaMax)
        #g1 = np.max(Frame.sigmaMax)/sigmaLim-1
        self.g2 = self.bC/self.h1
        self.g3 = self.bC/self.h2


sigmaLim = 235 # MPa
OptBridge = OptimizationProblem(Bridge)
OptBridge.Primal = "calc"
OptBridge.x = ["bC", "h1", "h2", "bF", "t"]
OptBridge.x0 = [ 60, 150, 150, 100,  10]
OptBridge.xL = [ 50,  50,  50,  20,  2]
OptBridge.xU = [300, 300, 300, 300, 10]
OptBridge.f = ["m"]
OptBridge.g = ["stressMax", "g2", "g3"]
OptBridge.gLimit = [sigmaLim, 1, 1]
OptBridge.Alg = "SLSQP"
OptBridge.optimize()
OptBridge.plotConvergence()
