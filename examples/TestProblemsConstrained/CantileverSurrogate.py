# -*- coding: utf-8 -*-
"""
Cantilever test function for design optimization with surrogate model using
SuPy

Source:  Dakota User's Guide §21.6

xOpt = [ 2.35342485  3.32421007]
fOpt = 7.82327859
"""
from DesOptPy import OptimizationProblem
import numpy as np
from supy.doe import doe
from supy import options as op
from supy import approximation as ap
from supy.preprocessing import outlier_detection as ad


class Cantilever:
    w = 1.8
    t = 1.0

    def SysEq(self):
        e = 2.9e7
        r = 40000.0
        fx = 500.0
        fy = 1000.0
        self.area = self.w * self.t
        D0 = 2.2535
        L = 100.0
        w_sq = self.w * self.w
        t_sq = self.t * self.t
        r_sq = r * r
        x_sq = fx * fx
        y_sq = fy * fy
        self.stress = 600.0 * fy / self.w / t_sq + 600.0 * fx / w_sq / self.t
        D1 = 4.0 * pow(L, 3) / e / self.area
        D2 = pow(fy / t_sq, 2) + pow(fx / w_sq, 2)
        D3 = D1 / np.sqrt(D2) / D0
        self.D4 = D1 * np.sqrt(D2) / D0
        g1 = self.stress / r - 1.0
        g2 = self.D4 - 1.0


xL = np.array([1.0, 1.0])
xU = np.array([4.0, 4.0])
doe_typ = doe.DOE_pyDOE()
nDoE = 200
xDoE = doe_typ.latin_hypercube(
    factors=2,
    n_samples=nDoE,
    criterion="centermaximin",
    iterations=10,
    s_range=[xL, xU],
)

area = [[]] * nDoE
stress = [[]] * nDoE
D4 = [[]] * nDoE
for i in range(nDoE):
    CantileverAnalysis = Cantilever()
    CantileverAnalysis.w = xDoE[0, i]
    CantileverAnalysis.t = xDoE[1, i]
    CantileverAnalysis.SysEq()
    area[i] = CantileverAnalysis.area
    stress[i] = CantileverAnalysis.stress
    D4[i] = CantileverAnalysis.D4

opt = op.Options("RBF_KK")
rf = ap.ApproxFactory()
areaApprox = rf.create(opt)
stressApprox = rf.create(opt)
D4Approx = rf.create(opt)
areaApprox.fit(xDoE, area)
stressApprox.fit(xDoE, stress)
D4Approx.fit(xDoE, D4)


class CantileverApprox:
    def SysEqApprox(self):
        x = np.array([self.w, self.t])
        self.area = areaApprox.predict(x)
        self.stress = stressApprox.predict(x)
        self.D4 = D4Approx.predict(x)


OptCantileverApprox = OptimizationProblem(CantileverApprox)
OptCantileverApprox.Primal = "SysEqApprox"
OptCantileverApprox.x = ["w", "t"]
OptCantileverApprox.x0 = np.array([1.8, 1.0])
OptCantileverApprox.xL = xL
OptCantileverApprox.xU = xU
OptCantileverApprox.f = ["area"]
OptCantileverApprox.g = ["stress", "D4"]
OptCantileverApprox.gLimit = [40000, 1]
OptCantileverApprox.Alg = "NLPQLP"
OptCantileverApprox.optimize()
OptCantileverApprox.plotConvergence()
OptCantileverApprox.plotBeforeAfter()
