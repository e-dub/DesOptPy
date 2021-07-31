from SiMuLi.TimeIntegration import Newmark
from SiMuLi.StDy import Model as DynModel
import matplotlib.pyplot as plt
from SiMuLi.Crash import CrushSquare
import numpy as np
import seaborn as sns


class CT(DynModel):
    ndof = 1
    vel = 60
    qd = vel * 1000 * 1000 / 60 / 60
    q = 0
    El1 = CrushSquare()
    b1 = 80
    El1.d = 2
    El1.ell = 150
    El1.b = b1
    #    El1.initialize()
    El2 = CrushSquare()
    b2 = 120
    El2.d = 3
    El2.ell = 300
    El2.b = b2
    #    El2.initialize()
    El3 = CrushSquare()
    b3 = 160
    El3.d = 6
    El3.b = b3
    El3.ell = 500
    #    El3.initialize()
    FHigh = 350e3

    def initialize(self):
        self.model()
        pass

    def model(self):
        self.m = 0.5000
        self.d = 0.0
        self.k = 0
        # self.stiff()
        # El1 = CrushSquare()
        self.El1.b = self.b1
        # El2 = CrushSquare()
        self.El2.b = self.b2
        # El3 = CrushSquare()
        self.El3.b = self.b3
        q = np.abs(self.q)
        if q < self.El1.ell:
            self.El1.q = self.q
            self.El1.calc()
            self.F = -self.El1.FInt
            # self.El1.b = self.b1
            # self.El1.q = self.q
            # self.El1.calc()
            # self.F = -self.El1.FInt
        elif q < self.El1.ell + self.El2.ell:
            self.El2.q = self.q - self.El1.ell
            self.El2.calc()
            self.F = -self.El2.FInt
            # self.El2.b = self.b2
            # self.El2.q = self.q-self.El1.q
            # self.El2.calc()
            # self.F = -self.El2.FInt
        elif q < self.El1.ell + self.El2.ell + self.El3.ell:
            self.El3.q = self.q - self.El1.ell - self.El2.ell
            self.El3.calc()
            self.F = -self.El3.FInt
            # self.El3.b = self.b3
            # self.El3.q = self.q - self.El1.q - self.El2.q
            # self.El3.calc()
            # self.F = -self.El3.FInt
        else:
            self.F = -self.FHigh
        # self.F = 0.0

        # print(El1.b)
        # print(self.b1)
        # print(El2.b)
        # print(self.b2)
        # print(El3.b)
        # print(self.b3)

    def velocityMag(self):
        MFMax = 1.5  # /1000 / 1000 * 60 * 60
        MFSlp = 0.15  # /1000 / 1000 * 60 * 60
        q = np.abs(self.q)
        self.MF = 1 + (2 / np.pi) * (MFMax - 1) * np.arctan(
            (np.pi / 2) * (MFSlp / (MFMax - 1) * np.abs(self.qd))
        )

    def solve(self):
        self.velocityMag()
        # self.qdd = 1/self.m * (self.F*self.MF - self.d*self.qd - self.k*self.q)
        self.qdd = 1 / self.m * (self.F - self.d * self.qd - self.k * self.q)

    def residual(self):
        self.velocityMag()
        self.R = (
            self.m * self.qdd + self.d * self.qd + self.MF * self.k * self.q - self.F
        )

    def calcUserStop(self):
        if self.qd <= 0:
            self.Stop = True


Model = CT()
Model.initialize()
Model.DesVar = ["b1", "b2", "b3"]
Model.DesVarLabels = Model.DesVar
Model.nx = len(Model.DesVar)
simulation1 = Newmark()
simulation1.Model = Model
simulation1.debug = 0
simulation1.t0 = 0
simulation1.tEnd = 10
simulation1.tDelta = 1e-4
simulation1.debug = True
simulation1.PrimalNonlinearDebug = True
simulation1.PrimalNonlinearJacobian = True
simulation1.PrimalNonlinearSolver = "Newton"
simulation1.SensCalc = True
simulation1.SensNonlinearDebug = True
simulation1.SensNonlinearJacobian = True
simulation1.SensNonlinearSolver = "Newton"
simulation1.run()
plt.figure()
plt.plot(simulation1.tAll, simulation1.q, label=simulation1.PrimalNonlinearSolver)
# plt.title("Position")
plt.ylabel("position $q$ [mm]")
plt.xlabel("time $t$ [s]")
sns.despine()
plt.show()
plt.figure()
plt.plot(
    simulation1.tAll,
    simulation1.qd / 1000 / 1000 * 60 * 60,
    label=simulation1.PrimalNonlinearSolver,
)
# plt.title('Velocity')
plt.ylabel("velocity $\\dot{q}$ [km/h]")
plt.xlabel("time $t$ [s]")
sns.despine()
plt.show()
plt.figure()
plt.plot(
    simulation1.tAll, simulation1.qdd / 1000, label=simulation1.PrimalNonlinearSolver
)
# plt.title('Acceleration')
plt.xlabel("time $t$ [s]")
plt.ylabel("acceleration $\\ddot{q}$ [m/s²]")
sns.despine()
plt.show()
plt.figure()
plt.plot(simulation1.q, -1 * simulation1.F, label=simulation1.PrimalNonlinearSolver)
# plt.title('Acceleration')
plt.xlabel("position $q$ [mm]")
plt.ylabel("Force $F$ [N]")
sns.despine()
plt.show()
plt.figure()
plt.plot(
    simulation1.tAll, simulation1.qNabla[:, 0], label=simulation1.PrimalNonlinearSolver
)
# plt.title('Position sensitivity')
# plt.title('position sensitivity $\\nabla q$ [$\partial$ mm / $\partial x$]')
plt.xlabel("time $t$ [s]")
plt.legend(
    Model.DesVarLabels, frameon=False, loc="center left", bbox_to_anchor=(1, 0.5)
)
sns.despine()
plt.show()
plt.figure()
plt.plot(
    simulation1.tAll,
    simulation1.qdNabla[:, 0] / 1000 / 1000 * 60 * 60,
    label=simulation1.PrimalNonlinearSolver,
)
# plt.title("Velocity senstivity")
plt.ylabel("velocity senstivity $\\nabla\\dot{q}$ [$\\partial$ km/h / $\\partial x$]")
plt.xlabel("time $t$ [s]")
plt.legend(
    Model.DesVarLabels, frameon=False, loc="center left", bbox_to_anchor=(1, 0.5)
)
sns.despine()
plt.show()
plt.figure()
plt.plot(
    simulation1.tAll,
    simulation1.qddNabla[:, 0] / 1000,
    label=simulation1.PrimalNonlinearSolver,
)
# plt.title('Acceleration sensitivity')
plt.ylabel(
    "acceleration sensitivity $\\nabla\\ddot{q}$  [$\\partial$ m/s² / $\\partial x$]"
)
plt.xlabel("time $t$ [s]")
plt.legend(
    Model.DesVarLabels, frameon=False, loc="center left", bbox_to_anchor=(1, 0.5)
)
sns.despine()
plt.show()

# r = np.linspace(0, 500, 5000)
# F = []
# k = []
# for ri in r:
#     Model.q = ri
#     Model.stiff()
#     F.append(Model.k*Model.q)
#     k.append(Model.k)
# plt.figure()
# plt.plot(r, F)
# #plt.plot([0, 30, 50, 100, 400],
# #         [0, Model.FLevel1, Model.FLevel2, Model.FLevel3, Model.FLevel4],
# #         "o")
# plt.ylabel("force $F$ [N]")
# plt.xlabel("position $q$ [mm]")
# sns.despine()
# plt.show()
