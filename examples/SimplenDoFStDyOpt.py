from SiMuLi.TimeIntegration import Newmark
import numpy as np
from SiMuLi.StDy import Model
from DesOptPy import OptimizationProblem


class DoFn(Model):
    ndof = 50
    m = np.diag(np.ones((ndof,)))
    F = np.zeros((ndof,))
    F[0] = 100
    q = np.zeros((ndof,))
    qd = np.zeros((ndof,))

    def primal(self):
        simulation1 = Newmark()
        simulation1.Model = DoFn()
        simulation1.debug = (
            2  # 0 = no printout, 1 = detailed printout, 2 = short printout
        )
        simulation1.tEnd = 0.1
        simulation1.tDelta = 1e-3
        simulation1.UserStopCrit = False
        simulation1.PrimalNonlinearTol = 1e-6
        simulation1.PrimalNonlinearSolver = "Newton"  # "Broyden"# "Newton"
        simulation1.run()

    def sensitivity(self):
        simulation1 = Newmark()
        simulation1.Model = DoFn()
        simulation1.debug = (
            2  # 0 = no printout, 1 = detailed printout, 2 = short printout
        )
        simulation1.tEnd = 0.1
        simulation1.tDelta = 1e-3
        simulation1.UserStopCrit = False
        simulation1.PrimalNonlinearTol = 1e-6
        simulation1.PrimalNonlinearSolver = "Newton"  # "Broyden"# "Newton"
        simulation1.run()


OptTBT = OptimizationProblem(DoFn)
OptTBT.RunFolder = True
OptTBT.RemoveRunFolder = True
OptTBT.pyOptAlg = True
# OptTBT.SciPyAlg = True


OptTBT.Alg = "ALGENCAN"
# OptTBT.Alg = "CONMIN"
# OptTBT.Alg = "SciPySLSQP"
OptTBT.Alg = "PSQP"
OptTBT.f = ["volume"]
OptTBT.g = ["stress1", "stress2", "stress3", "displacementx", "displacementy"]
OptTBT.gType = ["upper"] * 5
OptTBT.gNorm = [True] * 5
OptTBT.gLimit = [100, 100, 100, 10, 10]
OptTBT.x = ["A1", "A2"]
OptTBT.x0 = [10, 10]
OptTBT.xL = [0.1, 0.1]
OptTBT.xU = [100, 100]
OptTBT.xDelta = 1e-3
OptTBT.xNorm = [True] * 2
OptTBT.xType = ["continuous"] * 2
OptTBT.fNorm = [True]
OptTBT.Primal = "primal"
OptTBT.optimize()
OptTBT.plotConvergence()
OptTBT.plotBeforeAfter()
