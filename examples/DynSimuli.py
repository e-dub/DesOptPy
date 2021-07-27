from DesOptPy import OptimizationProblem
from SiMuLi.TimeIntegration import GeneralizedAlpha, Newmark
from SiMuLi.StDy import Model
import numpy as np
import matplotlib.pyplot as plt

class Dyn(Model):
    m = 1
    k = 5
    d = 1
    F = 100
    q = 0
    qd = 1
    DesVar = ["m", "k", "d"]

class DynModelOpt:
    m = 1
    k = 5
    d = 1

    def calc(self, plot=False):
        Model = Dyn()
        Model.m = self.m
        Model.d = self.d
        Model.k = self.k
        simulation1 = GeneralizedAlpha()
        simulation1.Model = Model
        simulation1.tEnd = 10
        simulation1.tDelta = 0.1
        simulation1.SensCalc = False
        simulation1.run()
        self.qMax = np.max(np.abs(simulation1.q))
        self.qdMax = np.max(np.abs(simulation1.qd))
        self.qddMax = np.max(np.abs(simulation1.qdd))
        if plot:
            plt.plot(simulation1.tAll, simulation1.q, label="$q$")
            plt.plot(simulation1.tAll, simulation1.qd, label="$\\dot{q}$")
            plt.plot(simulation1.tAll, simulation1.qdd, label="$\\ddot{q}$")
            plt.xlabel("time $t$")
            plt.legend(frameon=False)
            plt.show()

    # def sens(self, plot=False):
    #     Model = Dyn()
    #     Model.m = self.m
    #     Model.d = self.d
    #     Model.k = self.k
    #     simulation1 = GeneralizedAlpha()
    #     simulation1.Model = Model
    #     simulation1.tEnd = 10
    #     simulation1.tDelta = 0.1
    #     simulation1.SensCalc = True
    #     simulation1.run()
    #     print(simulation1.qdd)
    #     if plot:
    #         plt.plot(simulation1.tAll, simulation1.qNabla[:,0, :], label="$\\nabla q$")
    #         plt.xlabel("time $t$")
    #         plt.legend(frameon=False)
    #         plt.show()

    #         plt.plot(simulation1.tAll, simulation1.qdNabla[:,0, :], label="$\\nabla \\dot{q}$")
    #         plt.xlabel("time $t$")
    #         plt.legend(frameon=False)
    #         plt.show()

    #         plt.plot(simulation1.tAll, simulation1.qddNabla[:,0, :], label="$\\nabla \\ddot{q}$")
    #         plt.xlabel("time $t$")
    #         plt.legend(frameon=False)
    #         plt.show()

initialDesign = DynModelOpt()
initialDesign.calc(plot=True)

OptDyn = OptimizationProblem(DynModelOpt)
OptDyn.Primal = "calc"
OptDyn.x = ["m", "k", "d"]
OptDyn.x0 = [ 1,  1, 1]
OptDyn.xL = [ 1,  1, 1]
OptDyn.xU = [30, 30, 10]
OptDyn.f = ["qddMax"]
#OptDyn.g = [""]
#OptDyn.gLimit = [75]
OptDyn.Alg = "NLPQLP"
OptDyn.optimize()
OptDyn.plotConvergence()

optimumDesign = DynModelOpt()
optimumDesign.m = OptDyn.xOpt[0]
optimumDesign.k = OptDyn.xOpt[1]
optimumDesign.d = OptDyn.xOpt[2]
optimumDesign.calc(plot=True)
