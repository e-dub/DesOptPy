import numpy as np

def checkActiveConstraints(self, activeTol=1e-3):
    self.igActive = np.where(self.gOpt > -activeTol)[0]
    self.ixLActive = np.where((self.xL-self.xOpt) > -activeTol)[0]
    self.ixUActive = np.where((self.xOpt-self.xU) > -activeTol)[0]
    if len(self.igActive) == 0:
        igActive = None
    if len(self.ixLActive) == 0:
        ixLActive = None
    if len(self.ixUActive) == 0:
        ixUActive = None


def checkKKT(self):
    from numpy.linalg import norm, lstsq, pinv
    self.kkteps = 1e-3
    iActive = list(np.array(self.gOpt) > -self.kkteps).index(True)
    if len(iActive) == 1:
       lam= np.divide(np.array(self.fNablaIt[-1]),
                      np.array(self.gNablaIt[-1]).reshape(5,2)[iActive,:])
       Lambda = np.average(lam)
    self.PrimalFeas = (max(self.gOpt) < self.kkteps)
    self.ComplSlack = (max(self.gOpt@self.Lambda) < self.kkteps)
    self.DualFeas = (min(self.Lambda) > -self.kkteps)
    self.kktOpt = bool(self.PrimalFeas*self.DualFeas*self.ComplSlack)
    self.Opt1Order = np.linalg.norm(self.OptResidual)
    self.kktMax = max(abs(self.OptResidual))
    if np.size(lambda_c) > 0:
        print("Lagrangian multipliers = " +
        str(lambda_c.reshape(np.size(lambda_c,))))
        print("Type of active constraints = " + str(gAllActiveType))
        print("Shadow prices = " + str(SPg))
    if kktOpt:
        print("Karush-Kuhn-Tucker optimality criteria fulfilled")
    elif kktOpt==0:
        print("Karush-Kuhn-Tucker optimality criteria NOT fulfilled")
    if Opt1Order:
        print("First-order residual of Lagrangian function = " + str(Opt1Order))


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
