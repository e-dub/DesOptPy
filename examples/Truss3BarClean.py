from DesOptPy import OptimizationProblem
import numpy as np


class Truss3Bar:
    """
    A class must be written for every simulation that will be used in the
    optimization problem. This can also be used in parameter studies,
    uncertainty analysis, going in the direction of a digital twin.

    initialize parametric terms, atleast all those variables used for design
    optimization must be assigned, optimally here.
    """

    Fx = 1000
    Fy = 1000
    A1 = 5
    A2 = 5
    el = 100
    E = 210e3

    def primal(self):
        """
        primal analysis, it is not necessary to specify objective and
        contraints, though all possible optimization and parameters of
        interest, i.e. for a parameter study, must be assigned to self.

        Returns
        -------
        None.

        """
        self.gVal = 1
        self.volume = 2 * 2 ** 0.5 * self.A1 + self.A2
        self.stress1 = (
            1
            / 2 ** 0.5
            * (self.Fx / self.A1 + self.Fy / (self.A1 + 2 ** 0.5 * self.A2))
        )
        self.stress2 = 2 ** 0.5 * self.Fy / (self.A1 + 2 ** 0.5 * self.A2)
        self.stress3 = (
            1
            / 2 ** 0.5
            * (-self.Fx / self.A1 + self.Fy / (self.A1 + 2 ** 0.5 * self.A2))
        )
        self.dispx = 2 ** 0.5 * self.el * self.Fx / (self.A1 * self.E)
        self.dispy = (
            2 ** 0.5
            * self.el
            * self.Fy
            / ((self.A1 + 2 ** 0.5 * self.A2) * self.E)
        )

    def sensitivity(self):
        """
        sensitivtiy analysis, it is not necessary to specify objective and
        contraints senstivities, though all possible senstivities for
        optimization and parameters of interest, i.e. for a parameter study,
        must be assigned to self.

        Returns
        -------
        None.

        """
        self.volumeNabla = np.array([2 * 2 ** 0.5, 1])
        self.stress1Nabla = np.array(
            [
                -self.Fx / (2 ** 0.5 * self.A1 ** 2)
                - 2 ** 0.5 * self.Fy / (2 ** 0.5 * self.A1 + 2 * self.A2) ** 2,
                -2 * self.Fy / (2 ** 0.5 * self.A1 + 2 * self.A2) ** 2,
            ]
        )
        self.stress2Nabla = np.array(
            [
                -(2 ** 0.5) * self.Fy / (self.A1 + 2 ** 0.5 * self.A2) ** 2,
                -2 * self.Fy / (self.A1 + 2 ** 0.5 * self.A2) ** 2,
            ]
        )
        self.stress3Nabla = np.array(
            [
                +self.Fx / (2 ** 0.5 * self.A1 ** 2)
                - 2 ** 0.5 * self.Fy / (2 ** 0.5 * self.A1 + 2 * self.A2) ** 2,
                -2 * self.Fy / (2 ** 0.5 * self.A1 + 2 * self.A2) ** 2,
            ]
        )
        self.dispxNabla = np.array(
            [-(2 ** 0.5) * self.el * self.Fx / (self.A1 ** 2 * self.E), 0]
        )
        self.dispyNabla = np.array(
            [
                -(2 ** 0.5)
                * self.el
                * self.Fy
                / ((self.A1 + 2 ** 0.5 * self.A2) ** 2 * self.E),
                -2
                * self.el
                * self.Fy
                / ((self.A1 + 2 ** 0.5 * self.A2) ** 2 * self.E),
            ]
        )


# optional - run analysis with default parameters
print('primal analysis:')
Analysis = Truss3Bar()
Analysis.primal()
print(Analysis.volume)
print(Analysis.stress1)
print(Analysis.stress2)
print(Analysis.stress3)

# optional - show parametrizatin by change value
print('\nperturbed primal analysis:')
AnalysisPerturbation = Truss3Bar()
AnalysisPerturbation.A1 = 10
AnalysisPerturbation.A2 = 10
AnalysisPerturbation.primal()
print(AnalysisPerturbation.volume)
print(AnalysisPerturbation.stress1)
print(AnalysisPerturbation.stress2)
print(AnalysisPerturbation.stress3)


"""
Optimization problem in which problem is initialized, bounds, nonlinear
constraints, algorithm, design variables, etc.
"""
# Initialize optimization
OptTBT = OptimizationProblem(Truss3Bar)
OptTBT.RunFolder = True
OptTBT.RemoveRunFolder = True
OptTBT.Alg = 'SLSQP'
OptTBT.x = ['A1', 'A2']
OptTBT.x0 = [10, 10]
OptTBT.xL = [0.1, 0.1]
OptTBT.xU = [100, 100]
# OptTBT.xType = ["continuous"]*2
# OptTBT.xNorm = [True]*2
# OptTBT.fNorm = [True]
# OptTBT.gNorm = [True]*5
# OptTBT.gType = ["upper"]*5
OptTBT.gLimit = np.array([100, 100, 100, 10, 10])

# set primal analysis function and parameters
# OptTBT.Model = Truss3Bar
OptTBT.Primal = 'primal'  # Truss3Bar.primal
OptTBT.f = ['volume']
OptTBT.g = ['stress1', 'stress2', 'stress3', 'dispx', 'dispy']

# set sensitivtiy analysis fucntins and parameters
OptTBT.Sensitivity = 'sensitivity'
OptTBT.fNabla = ['volumeNabla']
OptTBT.gNabla = [
    'stress1Nabla',
    'stress2Nabla',
    'stress3Nabla',
    'dispxNabla',
    'dispyNabla',
]


# run optimizations
OptTBT.optimize()
OptTBT.plotConvergence(show=True, savePNG=False, saveTikZ=False, savePDF=False)
OptTBT.plotBeforeAfter(show=True, savePNG=False, saveTikZ=False, savePDF=False)
