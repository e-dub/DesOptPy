
import nlopt

def OptNlOpt(self, x0, xL, xU, SysEq):
    opt = nlopt.opt(nlopt.LD_MMA, self.nx)
    opt.set_lower_bounds(xL)
    opt.set_min_objective(ObjFnSciPy)
    opt.add_inequality_constraint(ConFnSciPy, 0)
    opt.set_xtol_rel(1e-4)
    x = opt.optimize(x0)
