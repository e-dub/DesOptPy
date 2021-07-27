import numpy as np
import numpy.linalg as npla


def checkActiveConstraints(self, activeTol=1e-3):
    self.igActive = np.where(self.gOpt > -activeTol)[0].tolist()
    self.ixLActive = np.where((self.xL-self.xOpt) > -activeTol)[0].tolist()
    self.ixUActive = np.where((self.xOpt-self.xU) > -activeTol)[0].tolist()
    # if len(self.igActive) == 0:
    #     self.igActive = None
    # if len(self.ixLActive) == 0:
    #     self.ixLActive = None
    # if len(self.ixUActive) == 0:
    #     self.ixUActive = None
    #self.iActive = np.block([self.igActive, self.ixLActive, self.ixUActive])
    self.iActive = self.igActive + self.ixLActive + self.ixUActive

def LagrangianFunction(self):

    self.ConNabla = np.block([
        self.gNablaOpt,
        np.diag([-1]*self.nx),
        np.diag([1]*self.nx)
    ])
    self.ConActiveNabla = np.block([
        self.gNablaOpt[:, self.igActive],
        np.diag([-1]*self.nx)[:, self.ixLActive],
        np.diag([1]*self.nx)[:, self.ixUActive]
    ])
    #self.LambdaAll = npla.pinv(self.ConNabla)@-self.fNablaOpt
    #self.LambdaActiveCheck = self.Lambda[self.iActive]
    self.Lambda = np.zeros((self.ng+2*self.nx,))
    self.LambdaActive = npla.pinv(self.ConActiveNabla)@-self.fNablaOpt
    self.Lambda[self.iActive] = self.LambdaActive
    self.OptResidual = self.fNablaOpt + self.ConNabla@self.Lambda

def checkKKT(self, kkteps=1e-3):
    checkActiveConstraints(self)
    LagrangianFunction(self)
    # from numpy.linalg import norm, lstsq, pinv
    # self.kkteps = 1e-3
    # iActive = list(np.array(self.gOpt) > -self.kkteps).index(True)
    # if len(iActive) == 1:
    #    lam= np.divide(np.array(self.fNablaIt[-1]),
    #                   np.array(self.gNablaIt[-1]).reshape(5,2)[iActive,:])
    #    Lambda = np.average(lam)
    self.PrimalFeas = (max(self.gOpt) < kkteps)
    self.ComplSlack = (max(self.gOpt*self.Lambda[0:self.ng]) < kkteps)
    self.DualFeas = (min(self.Lambda) > -kkteps)
    self.kktOpt = bool(self.PrimalFeas*self.DualFeas*self.ComplSlack)
    self.Opt1Order = np.linalg.norm(self.OptResidual)
    self.kktMax = max(abs(self.OptResidual))
    if self.kktOpt:
        print("Karush-Kuhn-Tucker optimality criteria fulfilled")
    elif self.kktOpt==0:
        print("Karush-Kuhn-Tucker optimality criteria NOT fulfilled")
    if self.Opt1Order:
        print("First-order residual of Lagrangian function = " + str(self.Opt1Order))


def calcShadowPrices(self):
    self.ShadowPrices = []


if __name__ == "__main__":
    print("testing")

    class test:
        pass
    self = test()
    self.gOpt = np.array([0, 1, -1])
    self.fOpt =  np.array([10])
    self.xOpt =  np.array([3, 2, 3])
    self.xL =  np.array([1, 1, 1])
    self.xU =  np.array([3, 3, 3])
    checkActiveConstraints(self)
