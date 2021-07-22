import datetime
import os
import copy
import shutil
import numpy as np
try:
    import cpuinfo
except:
    pass
from DesOptPy.scaling import normalize, denormalize
from DesOptPy.tools import printResults
from DesOptPy import plotting
def OptimizationProblem(Model):
    class Opt(Model):
        fType = "min"
        x = None
        f = None
        g = None
        xOpt = None
        fOpt = None
        gOpt = None
        fNabla = None
        gNabla = None
        xNorm = True
        fNorm = True
        fNormMultiplier = 1000
        xLast = None
        Primal = "calc"
        Sensitivity = None
        xDelta = 1e-3
        Alg = "NLPQLP"
        nGen = None
        pyOptAlg = None
        SciPyAlg = None
        pyGmoAlg = None
        nloptAlg = None
        PrintOutput = True
        ModelName = str(Model.__name__)
        Alarm = True
        RunFolder = True
        RemoveRunFolder = True
        SaveEvaluations = False
        OS = os.uname()[0]
        Computer = os.uname()[1]
        architecture = os.uname()[4]
        nProcessors = os.cpu_count()
        userName = os.getlogin()
        Monitoring = True
        RunDir = None
        MainDir = None
        try:
            cpu = cpuinfo.get_cpu_info()['brand']
        except:
            pass

        #class KaruschKuhnTucker:

        def checkKKT(self):
            from numpy.linalg import norm, lstsq, pinv
            self.kkteps = 1e-3
            iActive = list(np.array(self.gOpt) > -self.kkteps).index(True)
            if len(iActive) == 1:
               lam= np.divide(np.array(self.fNablaIt[-1]),
                              np.array(self.gNablaIt[-1]).reshape(5,2)[iActive,:])
               Lambda = np.average(lam)
            self.PrimalFeas = (max(self.gOpt) < self.kkteps)
            self.ComplSlack = (max(self.gOpt@self.Lambda) < self.kkteps)
            self.DualFeas = (min(self.Lambda) > -self.kkteps)
            self.kktOpt = bool(self.PrimalFeas*self.DualFeas*self.ComplSlack)
            self.Opt1Order = np.linalg.norm(self.OptResidual)
            self.kktMax = max(abs(self.OptResidual))
            if np.size(lambda_c) > 0:
                print("Lagrangian multipliers = " +
                str(lambda_c.reshape(np.size(lambda_c,))))
                print("Type of active constraints = " + str(gAllActiveType))
                print("Shadow prices = " + str(SPg))
            if kktOpt:
                print("Karush-Kuhn-Tucker optimality criteria fulfilled")
            elif kktOpt==0:
                print("Karush-Kuhn-Tucker optimality criteria NOT fulfilled")
            if Opt1Order:
                print("First-order residual of Lagrangian function = " + str(Opt1Order))

        def calcPosprocessing(self):
            self.ShadowPrices = []

        def readHistory(self):
            # make function of new file
            import pyOpt
            OptHist = pyOpt.History(self.Name, "r")
            xAll = OptHist.read([0, -1], ["x"])[0]["x"]
            xNormAll = copy.deepcopy(xAll)
            #xNormAll = xAll.copy()
            for ei in range(len(xAll)):
                for xi, xNormi in enumerate(self.xNorm):
                    if xNormi:
                        xAll[ei][xi] = denormalize(xAll[ei][xi], self.xL[xi],
                                                   self.xU[xi])
            fAll = OptHist.read([0, -1], ["obj"])[0]["obj"]
            gAll = OptHist.read([0, -1], ["con"])[0]["con"]
            gNablaIt = OptHist.read([0, -1], ["grad_con"])[0]["grad_con"]
            if self.Alg == "NLPQLP":
                gAll = [g*-1 for g in gAll]
            fNablaIt = OptHist.read([0, -1], ["grad_obj"])[0]["grad_obj"]
            failIt = OptHist.read([0, -1], ["fail"])[0]["fail"]
            OptHist.close()
            xAll = [i.tolist() for i in xAll]
            xNormAll = [i.tolist() for i in xNormAll]
            fAll = [i.tolist() for i in fAll]
            gAll = [i.tolist() for i in gAll]
            fNablaIt = [i.tolist() for i in fNablaIt]
            gNablaIt = [i.tolist() for i in gNablaIt]
            failIt = [i.tolist() for i in failIt]

            self.nIt = len(fNablaIt)
            self.fIt = [None]*self.nIt
            self.xIt = [None]*self.nIt
            self.gIt = [None]*self.nIt
            for ii in range(self.nIt):
                Posdg = OptHist.cues["grad_con"][ii][0]
                Posf = OptHist.cues["obj"][ii][0]
                iii = 0
                while Posdg > Posf:
                    iii = iii + 1
                    try:
                        Posf = OptHist.cues["obj"][iii][0]
                    except:
                        Posf = Posdg + 1
                iii = iii - 1
                self.fIt[ii] = fAll[iii]
                self.xIt[ii] = xAll[iii]
                self.gIt[ii] = gAll[iii]

            self.xAll = xAll
            self.xNormAll = xNormAll
            self.fAll = fAll
            self.gAll = gAll
            self.gNablaIt = gNablaIt
            self.fNablaIt = fNablaIt
            self.gOpt = self.gIt[-1]
            self.gMax = np.max(self.gAll, 1)
            self.g0 = self.gIt[0]

        def optimize(self):
            self.t0 = datetime.datetime.now()
            self.t0str = self.t0.strftime("%Y%m%d%H%M%S")
            self.Name = self.ModelName+self.Alg+self.t0str
            self.nEval = 0
            self.nSensEval = None
            self.f0 = None
            self.g0 = None
            self.nx = len(self.x)
            self.ng = len(self.g)
            self.nf = len(self.f)
            # TODO
            #if self.fType.upper()[0:3] == "MIN":
            #
            #

            # Optimization Algorithm
            self.SciPyAlg = False
            self.pyOptAlg = False
            self.pyGmoAlg = False
            self.nloptAlg = False
            if (self.Alg).upper() in {"ALGENCAN", "ALHSO", "COBYLA", "CONMIN",
                                      "FILTERSD", "FSQP", "GCMMA", "IPOPT",
                                      "KSOPT", "MIDACO", "MMA", "MMFD",
                                      "NLPQLP", "PSQP", "SDPEN", "SLSQP",
                                      "SOLVOPT"}:
                self.pyOptAlg = True
            elif ((self.Alg[:5]).upper() == "SCIPY" or
                  (self.Alg[-5:]).upper == "SCIPY"):
                self.SciPyAlg = True
            elif ((self.Alg[:5]).upper() == "PYGMO" or
                  (self.Alg[-5:]).upper == "PYGMO"):
                self.pyGmoAlg = True
            elif ((self.Alg[:5]).upper() == "NLOPT" or
                  (self.Alg[-5:]).upper == "NLOPT"):
                self.nloptAlg = True

            # File handling
            if self.RunFolder:
                self.MainDir = os.getcwd()
                self.RunDir = self.MainDir+os.sep+"DesOpt"+self.Name
                if os.path.isdir(self.RunDir):
                    datetime.time.wait(1)
                    self.t0 = datetime.datetime.now()
                    self.t0str = self.t0.strftime("%Y%m%d%H%M%S")
                    self.Name = self.ModelName+self.Alg+self.t0str
                    self.RunDir = self.MainDir+os.sep+"DesOpt"+self.Name
                shutil.copytree(self.MainDir, self.RunDir,
                                ignore=shutil.ignore_patterns("DesOpt*", ".*",
                                                              ".git*",
                                                              "*.pyc", "tmp*",
                                                              "__*"))
                os.chdir(self.RunDir)

            if self.Monitoring and self.RunFolder:
                print("\nTo start monitoring visualization," +
                      " enter the following command in terminal:" +
                      "\n\n    bokeh serve --show DesOptMonitor.py \n\n" +
                      "from the following folder:"
                      "\n\n    " + self.RunDir + "\n\n")

            def SysEq(xVal):
                # create folder and change into it
                if self.SaveEvaluations:
                    EvalDir = self.RunDir+os.sep+str(self.nEval+1).zfill(5)
                    shutil.copytree(self.MainDir, EvalDir,
                                    ignore=shutil.ignore_patterns("DesOpt*",
                                                                  ".git*",
                                                                  ".*",
                                                                  "*.pyc",
                                                                  "tmp*",
                                                                  "__*"))
                    os.chdir(EvalDir)

                # Use only physical design variables (some algorithms
                # supplement design vector with other values, e.g. CONMIN)
                xVal = xVal[0:len(self.xL)]

                # Denorm and assign of design variables
                for i, xi in enumerate(xVal):
                    if self.xNorm[i]:
                        xVal[i] = denormalize(xi, self.xL[i], self.xU[i])
                    if self.x is not None:
                        setattr(self, self.x[i], xVal[i])

                # Call
                if self.x is None:
                    eval("self."+self.Primal+"(xVal)")
                else:
                    eval("self."+self.Primal+"()")

                # Objective and scaling (norm)
                fVal = getattr(self, self.f[0])
                if self.fNorm[0]:
                    if self.f0 is None:
                        self.f0 = fVal
                    fVal = fVal/self.f0*self.fNormMultiplier
                #change the above to allow for multiobjective
                #fVal = []
                #for fi in self.f:
                #    print(getattr(self, fi))

                # Formulate constraint function (upper/lower, normalized)
                rconval = []
                if self.g:
                    gVal = [None]*len(self.g)
                    for i, gi in enumerate(self.g):
                        rconval = getattr(self, gi)
                        if self.gNorm[i]:
                            if self.gType[i] == "upper":
                                gVal[i] = rconval/self.gLimit[i]-1
                            elif self.gType[i] == "lower":
                                gVal[i] = 1-rconval/self.gLimit[i]
                        else:
                            if self.gType[i] == "upper":
                                gVal[i] = rconval-self.gLimit[i]
                            elif self.gType[i] == "lower":
                                gVal[i] = self.gLimit[i]-rconval
                else:
                    gVal = []

                # Revert to normalized design variables (why necessary?)
                for i in range(len(self.x0)):
                    if self.xNorm[i]:
                        xVal[i] = normalize(xVal[i], self.xL[i], self.xU[i])

                # Move back into run folder
                if self.SaveEvaluations:
                    os.chdir("..")

                self.nEval += 1

                return(fVal, gVal, 0)

            def SensEq(xVal, fVal, gVal):
                # create folder and change into it
                if self.SaveEvaluations:
                    EvalDir = (self.RunDir + os.sep +
                               str(self.nSensEval+1).zfill(5)+"Sens")
                    shutil.copytree(self.MainDir, EvalDir,
                                    ignore=shutil.ignore_patterns("DesOpt*",
                                                                  ".git*",
                                                                  ".*",
                                                                  "*.pyc",
                                                                  "tmp*",
                                                                  "__*"))
                    os.chdir(EvalDir)

                # Denorm and assign of design variables
                for i, xi in enumerate(xVal):
                    if self.xNorm[i]:
                        xVal[i] = denormalize(xi, self.xL[i], self.xU[i])
                    if self.x is not None:
                        setattr(self, self.x[i], xVal[i])

                # Call
                if self.x is None:
                    eval("self."+self.Sensitivity+"(xVal)")
                else:
                    eval("self."+self.Sensitivity+"()")

                # Senstivity of objective
                fNablaVal = getattr(self, self.fNabla[0])
                if self.fNorm[0]:
                    fNablaVal = fNablaVal/self.f0*self.fNormMultiplier
                for i in range(len(xVal)):
                    if self.xNorm[i]:
                        fNablaVal[i] *= (self.xU[i]-self.xL[i])

                # Senstivity of constraints
                if self.g:
                    gNablaVal = [None]*len(self.gNabla)
                    for i, gNablai in enumerate(self.gNabla):
                        rNablaVal = getattr(self, gNablai)
                        if self.gNorm[i]:
                            if self.gType[i] == "upper":
                                gNablaVal[i] = rNablaVal/self.gLimit[i]
                            elif self.gType[i] == "lower":
                                gNablaVal[i] = -rNablaVal/self.gLimit[i]
                        else:
                            if self.gType[i] == "upper":
                                gNablaVal[i] = rNablaVal
                            elif self.gType[i] == "lower":
                                gNablaVal[i] = -rNablaVal
                    for i in range(len(self.x0)):
                        if self.xNorm[i]:
                            for j in range(len(self.gNabla)):
                                gNablaVal[j][i] *= (self.xU[i]-self.xL[i])
                else:
                    gNablaVal = []

                # Revert to normalized design variables (why necessary?)
                for i in range(len(self.x0)):
                    if self.xNorm[i]:
                        xVal[i] = normalize(xVal[i], self.xL[i], self.xU[i])

                # Move back into run folder
                if self.SaveEvaluations:
                    os.chdir("..")

                self.nSensEval += 1
                return(np.array([fNablaVal]), gNablaVal, 0)

            # Maybe all too much, can i just put this as a function in opt call?
            # TODO move the next 40 lines to new file
            def ObjCon(xVal):
                f, g, fail = SysEq(xVal)
                np.array([f])
                np.array(g)
                if self.g is not None:
                    f = np.concatenate((f, g))
                return(f)

            def AutoSensEq(xVal, fVal, gVal):
                import autograd
                for i, xi in enumerate(xVal):
                    if self.xNorm[i]:
                        xVal[i] = denormalize(xi, self.xL[i], self.xU[i])
                ObjConNabla = autograd.jacobian(ObjCon)
                fNablaVal = ObjConNabla(xVal)
                if self.g is not None:
                    fNablaVal, rNablaVal = fNablaVal[0], fNablaVal[1:]
                if self.fNorm[0]:
                    fNablaVal = fVal/self.f0*self.fNormMultiplier
                for i in range(len(xVal)):
                    if self.xNorm[i]:
                        fNablaVal[i] *= (self.xU[i]-self.xL[i])
                if self.g:
                    gNablaVal = [None]*len(self.gNabla)
                    for i, gNablai in enumerate(self.gNabla):
                        if self.gNorm[i]:
                            if self.gType[i] == "upper":
                                gNablaVal[i] = rNablaVal[i]/self.gLimit[i]
                            elif self.gType[i] == "lower":
                                gNablaVal[i] = -rNablaVal[i]/self.gLimit[i]
                        else:
                            if self.gType[i] == "upper":
                                gNablaVal[i] = rNablaVal[i]
                            elif self.gType[i] == "lower":
                                gNablaVal[i] = -rNablaVal[i]
                    for i in range(len(self.x0)):
                        if self.xNorm[i]:
                            for j in range(len(self.gNabla)):
                                gNablaVal[j][i] *= (self.xU[i]-self.xL[i])
                else:
                    gNablaVal = []
                for i in range(len(self.x0)):
                    if self.xNorm[i]:
                        xVal[i] = normalize(xVal[i], self.xL[i], self.xU[i])
                self.nSensEval += 1


            # Normalization
            x0 = [None]*self.nx
            xL = [None]*self.nx
            xU = [None]*self.nx
            for i in range(self.nx):
                if self.xNorm[i]:
                    x0[i] = normalize(self.x0[i], self.xL[i], self.xU[i])
                    xL[i] = 0
                    xU[i] = 1
                else:
                    x0[i] = self.x0[i]
                    xL[i] = self.xL[i]
                    xU[i] = self.xU[i]

#----------------------------------------------
            # Seperate file an dchild class??...
            if self.pyOptAlg:
                """
                PyOpt
                """
                import pyOpt
                Alg = eval("pyOpt." + self.Alg + '()')
                Problem = pyOpt.Optimization(self.ModelName, SysEq)
                for i in range(self.nx):
                    Problem.addVar('x'+str(i+1), 'c', value=x0[i], lower=xL[i],
                                   upper=xU[i])
                for i in range(self.nf):
                    Problem.addObj('f'+str(i+1))
                if self.g:
                    for i in range(self.ng):
                        Problem.addCon('g'+str(i+1), 'i')
                if self.PrintOutput:
                    print(Problem)

                # Call
                if self.Sensitivity is None:
                    if self.Alg in ["NLPQLP", "MMA", "GCMMA", "IPOPT", "FSQP",
                                    "PSQP", "CONMIN", "MMFD", "SLSQP",
                                    "SOLVEOPT"]:
                        fOpt, xOpt, inform = Alg(Problem,
                                                 sens_step=self.xDelta,
                                                 store_hst=self.Name)
                    else:
                        fOpt, xOpt, inform = Alg(Problem, store_hst=self.Name)

                elif self.Sensitivity == "autograd":
                    fOpt, xOpt, inform = Alg(Problem, sens_type=AutoSensEq,
                                             store_hst=self.Name)
                else:
                    self.nSensEval = 0
                    fOpt, xOpt, inform = Alg(Problem, sens_type=SensEq,
                                             store_hst=self.Name)

                # proper size xOpt
                xOpt = np.array(xOpt).reshape(len(xOpt),)

                # proper size fOpt
                fOpt = np.array(fOpt).reshape(1,)

                # Todo: same for all algorithms?
                # Todo change to array?
                # Denormalization
                self.xOpt = [None]*self.nx
                self.xNormOpt = xOpt
                self.fNormOpt = fOpt
                for i in range(len(self.x0)):
                    if self.xNorm[i]:
                        self.xOpt[i] = denormalize(xOpt[i], self.xL[i],
                                                   self.xU[i])
                    else:
                        self.xOpt[i] = xOpt[i]
                if self.fNorm[0]:
                    self.fOpt = fOpt*self.f0/self.fNormMultiplier
                else:
                    self.fOpt = fOpt


                # if self.PrintOutput:
                #     pass

                try:
                    self.inform = Alg.getInform(0)
                except:
                    self.inform = inform

                self.readHistory()

#----------------------------------------------
            elif self.pyGmoAlg:
                from DesOptPy.interfaces import PyGmo
                PyGmo.OptPyGmo(self, x0, xL, xU, SysEq)

#----------------------------------------------
            # Seperate file and child class??
            elif self.SciPyAlg:
                from DesOptPy.interfaces import SciPy
                SciPy.OptSciPy(self, x0, xL, xU, SysEq)

#----------------------------------------------
            # Seperate file and child class??
            elif self.nloptAlg:
                from DesOptPy.interfaces import NlOpt
                NlOpt.OptNlOpt(self, x0, xL, xU, SysEq)



            def optimizeMutiobjective(self):


#----------------------------------------------
                pass
# Optimization over...now postprocessing and such
            self.t1 = datetime.datetime.now()
            self.tOpt = (self.t1-self.t0)

            if self.PrintOutput:
                printResults(self)

            if self.RunFolder:
                os.chdir(self.MainDir)
                if self.RemoveRunFolder:
                    shutil.rmtree(self.RunDir)
    return Opt()
