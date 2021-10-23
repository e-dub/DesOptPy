import numpy as np
import numpy.linalg as npla


def checkActiveConstraints(self, activeTol=1e-3):
    self.igActive = np.where(self.gOpt > -activeTol)[0].tolist()
    self.ixLActive = np.where((self.xL - self.xOpt) > -activeTol)[0].tolist()
    self.ixUActive = np.where((self.xOpt - self.xU) > -activeTol)[0].tolist()
    # if len(self.igActive) == 0:
    #     self.igActive = None
    # if len(self.ixLActive) == 0:
    #     self.ixLActive = None
    # if len(self.ixUActive) == 0:
    #     self.ixUActive = None
    # self.iActive = np.block([self.igActive, self.ixLActive, self.ixUActive])
    self.iActive = self.igActive + self.ixLActive + self.ixUActive


def LagrangianFunction(self):
    if not hasattr(self, 'iActive'):
        checkActiveConstraints(self)
    self.ConNabla = np.block(
        [self.gNablaOpt.T, np.diag([-1] * self.nx).T, np.diag([1] * self.nx).T]
    )
    self.ConActiveNabla = np.block(
        [
            self.gNablaOpt[self.igActive, :].T,
            np.diag([-1] * self.nx)[self.ixLActive, :].T,
            np.diag([1] * self.nx)[self.ixUActive, :].T,
        ]
    )
    # self.LambdaAll = npla.pinv(self.ConNabla)@-self.fNablaOpt
    # self.LambdaActiveCheck = self.LambdaAll[self.iActive]
    self.Lambda = np.zeros((self.ng + 2 * self.nx,))
    self.LambdaActive = npla.pinv(self.ConActiveNabla) @ -self.fNablaOpt
    self.Lambda[self.iActive] = self.LambdaActive
    self.OptResidual = self.fNablaOpt + self.ConNabla @ self.Lambda


def checkKKT(self, KKTTol=1e-3):
    if not hasattr(self, 'iActive'):
        checkActiveConstraints(self)
    if not hasattr(self, 'Lambda'):
        LagrangianFunction(self)
    # from numpy.linalg import norm, lstsq, pinv
    # self.kkteps = 1e-3
    # iActive = list(np.array(self.gOpt) > -self.kkteps).index(True)
    # if len(iActive) == 1:
    #    lam= np.divide(np.array(self.fNablaIt[-1]),
    #                   np.array(self.gNablaIt[-1]).reshape(5,2)[iActive,:])
    #    Lambda = np.average(lam)
    self.PrimalFeas = max(self.gOpt) < KKTTol
    self.ComplSlack = max(self.gOpt * self.Lambda[0 : self.ng]) < KKTTol
    self.DualFeas = min(self.Lambda) > -KKTTol
    self.KKTOpt = bool(self.PrimalFeas * self.DualFeas * self.ComplSlack)
    self.Opt1Order = np.linalg.norm(self.OptResidual)
    self.KKTMax = max(abs(self.OptResidual))
    if self.KKTOpt:
        print('Karush-Kuhn-Tucker optimality criteria fulfilled')
    elif self.KKTOpt == 0:
        print('Karush-Kuhn-Tucker optimality criteria NOT fulfilled')
    # if self.Opt1Order:
    print(
        'First-order residual of Lagrangian function = ' + str(self.Opt1Order)
    )


def calcShadowPrices(self):
    if not hasattr(self, 'iActive'):
        checkActiveConstraints(self)
    if not hasattr(self, 'Lambda'):
        LagrangianFunction(self)
    self.ShadowPrice = np.zeros_like(self.Lambda)
    for i in range(self.ng):
        if self.gType[i] == 'upper':
            if self.gNorm[i]:
                self.ShadowPrice[i] = -self.Lambda[i] / self.gLimit[i]
            else:
                self.ShadowPrice[i] = -self.Lambda[i]
        else:
            if self.gNorm[i]:
                self.ShadowPrice[i] = self.Lambda[i] / self.gLimit[i]
            else:
                self.ShadowPrice[i] = self.Lambda[i]
    for i in range(self.ng, self.ng + self.nx):
        self.ShadowPrice[i] = self.Lambda[i]
    for i in range(self.ng + self.nx, self.ng + self.nx + self.nx):
        self.ShadowPrice[i] = -self.Lambda[i]
    self.gShadowPrice = self.ShadowPrice[0 : self.ng]
    self.xLShadowPrice = self.ShadowPrice[self.ng : self.ng + self.nx]
    self.xUShadowPrice = self.ShadowPrice[
        self.ng + self.nx : self.ng + self.nx + self.nx
    ]


if __name__ == '__main__':
    print('testing')

    class test:
        pass

    self = test()
    self.gOpt = np.array([0, 1, -1])
    self.fOpt = np.array([10])
    self.xOpt = np.array([3, 2, 3])
    self.xL = np.array([1, 1, 1])
    self.xU = np.array([3, 3, 3])
    checkActiveConstraints(self)
