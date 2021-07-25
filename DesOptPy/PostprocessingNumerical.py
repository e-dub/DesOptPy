

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
