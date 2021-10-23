"""
horrible solution as calling syseq 2x, one obj, one constraint

def BOBYQA(func, x0, args, tol=1e-6):
    # Set optimizer
    opt = nlopt.opt(nlopt.LN_BOBYQA, len(x0))
    res = results()
    prob = opt_problem(func, res, args)
    opt.set_ftol_abs(tol)
    opt.set_min_objective(prob.objfun)
    opt.add_inequality_constraint(prob.constrfun)
    res.x = opt.optimize(x0)
    res.fun = opt.last_optimum_value()
    return res


class results:
    def __init__(self):
        self.x = None
        self.fun = None
        self.nit = 0
        self.nfev = 0


class opt_problem:
    def __init__(self, func, res, args):
        self.func = func
        self.curr_x = None
        self.fobj = 0.0
        self.grad = None
        self.res = res
        self.args = args

    def objfun(self, x, *_):
        if self.curr_x != x:
            self.res.nit += 1
            self.res.nfev += 1
            self.curr_x = x
            self.res.x = x
            self.fobj, self.grad = self.func(x, *self.args)
        return self.fobj

    def constrfun(self, x, *_):
        if self.curr_x != x:
            self.res.nit += 1
            self.res.nfev += 1
            self.curr_x = x
            self.res.x = x
            self.fobj, self.grad = self.func(x, *self.args)
        return self.grad
"""
import numpy as np
from DesOptPy.scaling import normalize, denormalize
import nlopt


def OptNlOpt(self, x0, xL, xU, SysEq):
    def ObjFn(self, xVal, grad):
        if np.array_equal(self.xLast, xVal) != True:
            self.fVal, self.gVal, flag = SysEq(xVal)
            self.xLast = xVal.copy()
            self.fAll.append(self.fVal)
            self.gAll.append(self.gVal)
            self.xAll.append(xVal)
            print(self.fVal)
        return float(self.fVal)

    def ConFn(self, xVal, grad):
        if np.array_equal(self.xLast, xVal) != True:
            self.fVal, self.gVal, flag = SysEq(xVal)
            self.xLast = xVal.copy()
            self.fAll.append(self.fVal)
            self.gAll.append(self.gVal)
            self.xAll.append(xVal)
        return self.gVal

    self.gAll = []
    self.fAll = []
    self.xAll = []

    algorithm = nlopt.LD_MMA
    algorithm = nlopt.LN_COBYLA
    # algorithm = nlopt.LN_COBYLA
    # algorithm = nlopt.LN_BOBYQA

    opt = nlopt.opt(algorithm, self.nx)
    # opt = nlopt.opt(algorithm, self.nx)
    opt.set_min_objective(ObjFn)
    # opt.set_max_objective(f)
    opt.set_lower_bounds(self.xL)
    opt.set_upper_bounds(self.xU)
    opt.add_inequality_constraint(ConFn)
    # opt.add_inequality_constraint(lambda x, grad: ConFn(x, grad))

    # opt.set_stopval(stopval)
    # opt.set_ftol_rel(tol)
    # opt.set_ftol_rel(tol)
    # opt.set_xtol_abs(tol)
    # opt.set_xtol_rel(tol)
    # opt.set_maxeval(maxeval)
    # opt.set_maxtime(maxtime)
    xopt = opt.optimize(self.x0)

    xOpt = np.array(Results.x)
    fOpt = np.array([Results.fun])

    self.xNorm0 = x0
    self.x0 = self.xAll[0]
    self.f0 = self.fAll[0]
    self.g0 = self.gAll[0]
    self.fNablaOpt = Results.jac
    self.nIt = Results.nit
    self.xIt = None
    self.fIt = None
    self.gIt = None

    # Todo this is ugly
    self.nIt = Results.nfev
    try:
        self.nSensEval = Results.njev
    except:
        self.nSensEval = None
    self.inform = Results.success

    if 'SLSQP' in (self.Alg).upper():
        self.fNablaOpt = Results.jac
    elif 'trust-constr' in (self.Alg).lower():
        self.fNablaOpt = Results.grad
        self.gNablaOpt = Results.jac[0]

    if self.g is not None:
        self.gMax = np.max(self.gAll, 1)

    # Denormalization
    self.xOpt = [None] * self.nx
    self.xNormOpt = xOpt
    self.fNormOpt = fOpt
    for i in range(self.nx):
        if self.xNorm[i]:
            self.xOpt[i] = denormalize(xOpt[i], self.xL[i], self.xU[i])
        else:
            self.xOpt[i] = xOpt[i]
    if self.fNorm[0]:
        self.fOpt = fOpt * self.f0 / self.fNormMultiplier
    else:
        self.fOpt = fOpt
    self.gOpt = self.gVal
