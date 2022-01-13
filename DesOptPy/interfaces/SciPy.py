"""
horrible solution as calling syseq 2x, one obj, one constraint
"""
import numpy as np
from DesOptPy.scaling import normalize, denormalize


def OptSciPy(self, x0, xL, xU, SysEq):
    def ObjFnSciPy(xVal):
        if np.array_equal(self.xLast, xVal) != True:
            self.fVal, self.gVal, flag = SysEq(xVal)
            self.xLast = xVal.copy()
            self.fAll.append(self.fVal)
            self.gAll.append(self.gVal)
            self.xAll.append(xVal)
        return self.fVal

    def ConFnSciPy(xVal):
        if np.array_equal(self.xLast, xVal) != True:
            self.fVal, self.gVal, flag = SysEq(xVal)
            self.xLast = xVal.copy()
            self.fAll.append(self.fVal)
            self.gAll.append(self.gVal)
            self.xAll.append(xVal)
        return self.gVal

    """
    SciPy

    TODO: options need to be mapped to main options
    TODO: constraint formulation with upper or lower

    The minimize function supports the following methods:

        minimize(method=’Nelder-Mead’)
        minimize(method=’Powell’)
        minimize(method=’CG’)
        minimize(method=’BFGS’)
        minimize(method=’Newton-CG’)
        minimize(method=’L-BFGS-B’)
        minimize(method=’TNC’)
        minimize(method=’COBYLA’)
        minimize(method=’SLSQP’)
        minimize(method=’trust-constr’)
        minimize(method=’dogleg’)
        minimize(method=’trust-ncg’)
        minimize(method=’trust-krylov’)
        minimize(method=’trust-exact’)

    """
    from scipy import optimize as spopt

    self.gAll = []
    self.fAll = []
    self.xAll = []
    if 'SLSQP' in (self.Alg).upper():
        Results = spopt.minimize(
            ObjFnSciPy,
            x0,
            args=(),
            method='SLSQP',
            jac=None,
            bounds=spopt.Bounds(xL, xU),
            constraints=spopt.NonlinearConstraint(ConFnSciPy, -np.inf, 0),
            tol=None,
            callback=None,
            options={
                'maxiter': 100,
                'ftol': 1e-06,
                'iprint': 1,
                'disp': False,
                'eps': self.xDelta,
                'finite_diff_rel_step': None,
            },
        )
    elif 'trust-constr' in (self.Alg).lower():
        Results = spopt.minimize(
            ObjFnSciPy,
            x0,
            method='trust-constr',
            bounds=spopt.Bounds(xL, xU),
            constraints=spopt.NonlinearConstraint(ConFnSciPy, -np.inf, 0),
            options={
                'xtol': 1e-08,
                'gtol': 1e-08,
                'barrier_tol': 1e-08,
                'sparse_jacobian': None,
                'maxiter': 1000,
                'verbose': 0,
                'finite_diff_rel_step': None,
                'initial_constr_penalty': 1.0,
                'initial_tr_radius': 1.0,
                'initial_barrier_parameter': 0.1,
                'initial_barrier_tolerance': 0.1,
                'factorization_method': None,
                'disp': False,
            },
        )
        #'grad': None,
    elif 'differential_evolution' in (self.Alg).lower():
        """
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html#scipy.optimize.differential_evolutionhttps://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html#scipy.optimize.differential_evolution
        """
        Results = spopt.differential_evolution(
            ObjFnSciPy,
            x0=x0,
            bounds=spopt.Bounds(xL, xU),
            args=(),
            strategy='best1bin',
            maxiter=1000,
            popsize=15,
            tol=0.01,
            mutation=(0.5, 1),
            recombination=0.7,
            seed=None,
            disp=False,
            polish=True,
            init='latinhypercube',
            atol=0,
            updating='immediate',
            workers=1,
            constraints=spopt.NonlinearConstraint(ConFnSciPy, -np.inf, 0),
        )

    # elif 'COBYLA' in (self.Alg).upper():
    #     """
    #     Not working, no bounds
    #     https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyla.html
    #     """
    #     Results = spopt.minimize(ObjFnSciPy, x0,
    #                              args=(),
    #                              bounds=spopt.Bounds(xL, xU),
    #                              method='COBYLA',
    #                              constraints=spopt.NonlinearConstraint(ConFnSciPy, -np.inf, 0),
    #                              tol=None,
    #                              callback=None,
    #                              options={'rhobeg': 1.0,
    #                                       'maxiter': 1000,
    #                                       'disp': False,
    #                                       'catol': 0.0002})
    #     Results.nit = None
    #     Results.njev = None
    #     Results.jac = None
    # elif 'dual_annealing' in (self.Alg).lower():
    #     """
    #     No constraint
    #     https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html
    #     """
    #     Results = spopt.dual_annealing(ObjFnSciPy,
    #                                    args=(),
    #                                    bounds=tuple((np.block([xL, xU]).T).tolist()),
    #                                    #bounds=([0, 1], [0, 1]), #(xL, xU),
    #                                    maxiter=1000,
    #                                    local_search_options={},
    #                                    initial_temp=5230.0,
    #                                    restart_temp_ratio=2e-05,
    #                                    visit=2.62,
    #                                    accept=- 5.0,
    #                                    maxfun=10000000.0,
    #                                    seed=None,
    #                                    no_local_search=False,
    #                                    callback=None,
    #                                    x0=x0)
    #     Results.jac = None
    elif 'shgo' in (self.Alg).lower():
        """
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.shgo.html
        """
        Results = spopt.shgo(
            ObjFnSciPy,
            x0,
            args=(),
            bounds=spopt.Bounds(xL, xU),
            constraints=spopt.NonlinearConstraint(ConFnSciPy, -np.inf, 0),
            n=None,
            iters=1,
            callback=None,
            minimizer_kwargs=None,
            options=None,
            sampling_method='simplicial',
        )
    else:
        raise Exception(
            'Not a valid SciPy algorithm for constrained nonlinear optimization'
        )
    xOpt = np.array(Results.x)
    fOpt = np.array([Results.fun])

    self.xNorm0 = x0
    self.x0 = self.xAll[0]
    self.f0 = self.fAll[0]
    self.g0 = self.gAll[0]
    if (self.Alg).upper() in ['slsqp', 'trust-constr']:
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

    if (self.Alg).upper() in ['slsqp', 'trust-constr']:
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
