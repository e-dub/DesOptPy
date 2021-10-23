import numpy as np
from scipy.linalg import eigh
from DesOptPy import OptimizationProblem


class System2DoF:
    x = [1, 0.5, 1e7, 2e7]
    m1 = 1
    m2 = 0.5
    k1 = 1e7
    k2 = 2e7
    nDoF = 2

    def calc(self):
        self.m = np.array([[self.m1, 0], [0, self.m2]])
        self.k = np.array([[self.k1 + self.k2, -self.k2], [-self.k2, self.k2]])
        self.Lambda, self.phi = eigh(self.k, self.m)
        self.omega = np.sqrt(self.Lambda)
        self.f = self.omega / 2 / np.pi
        self.fLow = self.f[0]
        self.mass = self.m1 + self.m2

    def calcLambdaNabla(self):
        self.LambdaNabla = [[]] * 2
        for i in range(self.nDoF):
            self.LambdaNabla = (
                self.phi[:, 0]
                @ (self.kNabla - self.Lambda[0] * self.mNabla)
                @ self.phi[:, 0]
            )

    def calcEigSens(self):
        # sensitivities for m1, m2, k1, k2 (in that order)
        mNabla1 = np.array([[1, 0], [0, 0]])
        mNabla2 = np.array([[0, 0], [0, 1]])
        mNabla3 = np.zeros((2, 2))
        mNabla4 = np.zeros((2, 2))
        self.mNabla = np.array([mNabla1, mNabla2, mNabla3, mNabla4])

        kNabla1 = np.zeros((2, 2))
        kNabla2 = np.zeros((2, 2))
        kNabla3 = np.array([[1, 0], [0, 0]])
        kNabla4 = np.array([[1, -1], [-1, 1]])
        self.kNabla = np.array([kNabla1, kNabla2, kNabla3, kNabla4])
        self.massNabla = np.array(
            [
                [[1, 0], [0, 0]],
                [[0, 0], [0, 1]],
                [[0, 0], [0, 0]],
                [[0, 0], [0, 0]],
            ]
        )
        self.eigNabla = [[]] * 2
        self.phiNabla = [[]] * 2
        self.LambdaNabla = [[]] * 2
        self.fNabla = [[]] * 2
        for i in range(self.nDoF):
            a1 = self.k - self.Lambda[i] * self.m
            b1 = (-self.m @ self.phi[:, 0]).reshape(2, 1)
            c1 = -self.phi[:, 0] @ self.m
            d1 = np.zeros((1, 1))
            A = np.block([[a1, b1], [c1, d1]])
            a2 = -(self.kNabla - self.Lambda[0] * self.mNabla) @ self.phi[:, 0]
            b2 = 0.5 * self.phi[:, 0].T @ self.mNabla @ self.phi[:, 0]
            B = np.block([[a2.T], [b2]])
            try:
                self.eigNabla[i] = np.linalg.solve(A, B).T
            except:
                self.eigNabla[i] = np.linalg.lstsq(A, B)[0].T
            self.phiNabla[i] = self.eigNabla[i][:, :2]
            self.LambdaNabla[i] = self.eigNabla[i][:, 2]
            self.fNabla[i] = self.LambdaNabla[i] / 2 / self.Lambda[i]
        self.fLowNabla = self.fNabla[0]


# calculate system and sensitivities
Sys = System2DoF()
Sys.calc()
Sys.calcEigSens()


# optimize system
OptProb = OptimizationProblem(System2DoF)
OptProb.Primal = 'calc'
OptProb.x = ['m1', 'm2', 'k1', 'k2']
OptProb.x0 = [1, 0.5, 1e7, 2e7]
OptProb.xL = [0.1, 0.1, 1e5, 1e5]
OptProb.xU = [10, 10, 1e8, 2e8]
OptProb.f = 'fLow'
OptProb.fType = 'max'
OptProb.Alg = 'NLPQLP'
OptProb.Sensitivity = 'calcEigSens'
OptProb.fNabla = ['fLowNabla']
OptProb.optimize()
OptProb.plotConvergence()
OptProb.plotBeforeAfter()
