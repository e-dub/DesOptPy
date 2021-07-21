"""
horrible solution as calling syseq 2x, one obj, one constraint
"""
import numpy as np
from DesOptPy.scaling import normalize, denormalize
import pygmo as pg

def OptPyGmo(self, x0, xL, xU, SysEq):
    class OptProbPyGMO(Model):
        def fitness(self1, xVal):
            f, g, fail = SysEq(xVal)
            try:
                g = g.tolist()
            except:
                pass
            fg = g
            fg.insert(0, f)
            return(fg)

        def get_bounds(self1):
            return (xL, xU)

        def get_nic(self1):
            return(len(self.g))

        def get_nec(self1):
            return 0

        def gradient(self1, xVal):
            return pg.estimate_gradient_h(lambda xVal:
                                          self1.fitness(xVal), xVal)

    """
    PyGMO
    """
    #AlgOptionsChange to AlgOptions
    AlgOptions_nIndiv = 10
    AlgOptions_iter = 10
    AlgOptions_gen = 10
    unconstrained = True
    Alg = "123456de"
    prob = pg.problem(OptProbPyGMO())
    pop = pg.population(prob=prob, size=AlgOptions_nIndiv)
