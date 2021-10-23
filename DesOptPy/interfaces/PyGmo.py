"""
horrible solution as calling syseq 2x, one obj, one constraint
"""
import numpy as np
from DesOptPy.scaling import normalize, denormalize
import pygmo as pg
import copy


def OptPyGmo(self, x0, xL, xU, SysEq):
    class OptProbPyGMO:
        def fitness(self1, xVal):
            fVal, gVal, fail = SysEq(xVal)
            try:
                gVal = gVal.tolist()
            except:
                pass
            fg = copy.deepcopy(gVal)
            fg.insert(0, fVal)
            self.fAll.append(fVal)
            self.gAll.append(gVal)
            self.xAll.append(xVal)
            return fg

        def get_bounds(self1):
            return (xL, xU)

        def get_nic(self1):
            return self.ng

        def get_nec(self1):
            return 0

        def gradient(self1, xVal):
            return pg.estimate_gradient_h(
                lambda xVal: self1.fitness(xVal), xVal
            )

    """
    PyGMO
    """
    self.gAll = []
    self.fAll = []
    self.xAll = []
    # AlgOptionsChange to AlgOptions
    AlgOptions_nIndiv = 10
    AlgOptions_iter = 10
    AlgOptions_gen = 10
    unconstrained = True
    prob = pg.problem(OptProbPyGMO())
    pop = pg.population(prob=prob, size=AlgOptions_nIndiv)
    prob = pg.problem(OptProbPyGMO())
    # algo = pg.algorithm(uda = pg.nlopt('auglag'))
    # algo.extract(pg.nlopt).local_optimizer = pg.nlopt('var2')
    # pop = pg.population(prob=prob, size=1)

    pop = pg.population(prob=prob, size=AlgOptions_nIndiv)
    if self.Alg[6:] == 'monte_carlo':
        algo = pg.algorithm.monte_carlo(iters=AlgOptions_iter)
    elif self.ng > 0:
        algo = pg.algorithm(
            pg.cstrs_self_adaptive(
                iters=AlgOptions_gen,
                algo=eval(
                    'pg.' + self.Alg[6:] + '(' + str(AlgOptions_nIndiv) + ')'
                ),
            )
        )
        pop.problem.c_tol = [1e-6] * self.ng
    else:
        algo = eval(
            'pg.algorithm(pg.'
            + self.Alg[6:]
            + '('
            + str(AlgOptions_gen)
            + '))'
        )
    pop = algo.evolve(pop)
    xOpt = pop.champion_x
    fOpt = pop.champion_f[0]
    gOpt = pop.champion_f[1:]

    self.xNorm0 = x0
    self.x0 = self.xAll[0]
    self.fNorm0 = self.fAll[0]
    # self.f0 = self.fAll[0]/self.fNormMultiplier
    self.g0 = self.gAll[0]

    self.nIt = None
    self.xIt = None
    self.fIt = None
    self.gIt = None

    if self.g is not None:
        self.gMax = np.max(self.gAll, 1)

    # Denormalization
    self.xOpt = [None] * self.nx
    self.xNormOpt = xOpt
    self.fNormOpt = np.array([fOpt])
    for i in range(self.nx):
        if self.xNorm[i]:
            self.x0[i] = denormalize(x0[i], self.xL[i], self.xU[i])
            self.xOpt[i] = denormalize(xOpt[i], self.xL[i], self.xU[i])
        else:
            self.xOpt[i] = xOpt[i]
    if self.fNorm[0]:
        self.fAll = np.array(self.fAll) * self.f0 / self.fNormMultiplier
        self.fOpt = np.array([fOpt * self.f0 / self.fNormMultiplier])
    else:
        self.fOpt = np.array([fOpt])
    self.gOpt = gOpt
