# units: SI - kg, m, N-m, rad/s (shown also in Hz)
import numpy as np
from scipy.linalg import eigh
from DesOptPy import OptimizationProblem
from DesOptFn.RangeConstraint import BandConParabolicFn
from DesOptFn.RangeConstraint import BandConBallisticFn
from DesOptFn.RangeConstraint import BandConBallisticSensFn


class Oscillator2Mass:
    m1 = 0.2
    m2 = 0.2
    k1 = 1e7
    k2 = 2e7
    mAdded1 = 0
    mAdded2 = 0
    omegaBands = np.array([[   0,  500],
                           [ 650,  800],
                           [1000, 1350],
                           [2000, 2500]])

    def primal(self):
        self.m = np.diag([self.m1+self.mAdded1, self.m2+self.mAdded1])
        self.k = np.array([[self.k1+self.k2, -self.k2],
                           [       -self.k2,  self.k2]])
        self.Lambda, self.Phi = eigh(self.k, self.m, eigvals=(0, 1))
        self.omegan = np.sqrt(self.Lambda)
        self.fn = self.omegan/(2*np.pi)
        self.gFreqParabala = BandConParabolicFn(self.fn, self.omegaBands,
                                                norm=False)
        self.gFreqBallistic = BandConBallisticFn(self.fn, self.omegaBands,
                                                 a=100, b=0, norm=True,
                                                 infFilter=1e6)
        self.mTot = self.m1+self.mAdded1 + self.m2+self.mAdded2
        self.mAddedTot = self.mAdded1+self.mAdded2
        self.g1 = self.gFreqBallistic[0]
        self.g2 = self.gFreqBallistic[1]
        self.g3 = self.gFreqBallistic[2]
        self.g4 = self.gFreqBallistic[3]
        self.g5 = self.gFreqBallistic[4]
        self.g6 = self.gFreqBallistic[5]
        self.g7 = self.gFreqBallistic[6]
        self.g8 = self.gFreqBallistic[7]
        print(self.gFreqBallistic)

    # def sensitivity(self):
    #     omeganNabla = np.zeros((2, len(self.omegan)))
    #     for j in range(2):
    #         for i in range(len(self.omegan)):
    #             omeganNabla[i, j] = -self.omegan[i]/2*self.Phi[j, i]**2
    #     self.fnNabla = omeganNabla/2/np.pi
    #     self.gFreqBallisticNabla = BandConBallisticSensFn(self.fn,
    #                                                       self.fnNabla,
    #                                                       self.omegaBands,
    #                                                       a=100, b=0,
    #                                                       norm=True,
    #                                                       infFilter=1e6)
    #     self.mTotNabla = np.array([1.0, 1.0])





Prob1 = OptimizationProblem(Oscillator2Mass)
#Prob1.primal()
#Prob1.sensitivity()
Prob1.x = ["mAdded1", "mAdded2"]
Prob1.x0 = [1, 0]
Prob1.xL = [0.0, 0.0]
Prob1.xU = [2.0, 2.0]
Prob1.xNorm = [False]*2
Prob1.xType = ["continuous"]*2
Prob1.f = ["mAddedTot"]
Prob1.fNorm = [True]
Prob1.g = ["g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8"]
#Prob1.g = ["gFreqBallistic"]
Prob1.gType = ["upper"]*8
Prob1.gNorm = [False]*8
Prob1.gLimit = [0]*8
Prob1.Alg = "NLPQLP"

#Prob1.fNabla = ["mTotNabla"]
#Prob1.gNabla = ["gFreqBallisticNabla"]
Prob1.Primal = "primal"
#Prob1.Sensitivity = "sensitivity"
Prob1.TablesPlots = False
Prob1.optimize()
