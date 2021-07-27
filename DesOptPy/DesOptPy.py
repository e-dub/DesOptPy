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
from DesOptPy.tools import printResults, checkProblem
from DesOptPy import plotting
#from DesOptPy import plotting



def OptimizationProblem(Model):
    class Opt(Model):
        ModelName = str(Model.__name__)
        fType = "min"
        x = None
        f = None
        g = None
        xL = None
        xU = None

        Primal = None
        Sensitivity = None

        ng = None
        nf = None
        nx = None

        xOpt = None
        fOpt = None
        gOpt = None

        fNabla = None
        gNabla = None

        fNorm = True
        xNorm = True
        gNorm = True

        gType = None

        f0 = None
        g0 = None

        xLast = None

        gLimit = [None]

        nGen = None
        nSensEval = None

        fNormMultiplier = 1e3
        xDelta = 1e-4
        Alg = "SLSQP"

        pyOptAlg = None
        SciPyAlg = None
        pyGmoAlg = None
        nloptAlg = None


        PrintOutput = True
        Alarm = False
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
            cpu = None

        #class KaruschKuhnTucker:
        from DesOptPy.plotting import plotConvergence
        from DesOptPy.postprocessingNumerical import (
            checkKKT,
            calcShadowPrices,
            checkActiveConstraints,
            LagrangianFunction
            )

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
            self.xNormIt = [None]*self.nIt
            self.gIt = [None]*self.nIt
            self.gMaxIt = [None]*self.nIt
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
                self.xIt[ii] = xAll[iii][0:self.nx]
                self.xNormIt[ii] = xNormAll[iii][0:self.nx]
                if self.g is not None:
                    self.gIt[ii] = gAll[iii]
                    self.gMaxIt[ii] = np.max(gAll[iii])

            self.xAll = xAll
            self.xNormAll = xNormAll
            self.fAll = fAll
            self.gAll = gAll
            self.gNablaIt = gNablaIt
            self.fNablaIt = fNablaIt
            if self.g is not None:
                self.gOpt = np.array(self.gIt[-1])
                self.gMax = np.max(self.gAll, 1)
                self.g0 = self.gIt[0]

        def optimize(self):

            self.Model = Model
            #self.ModelName = str(self.Model.__name__)
            self.t0 = datetime.datetime.now()
            self.t0str = self.t0.strftime("%Y%m%d%H%M%S")
            self.Name = self.ModelName+self.Alg+self.t0str
            self.nEval = 0

            checkProblem(self)
            if type(self.f) == str:
                self.f = [self.f]

            # set general sizes of optimization problem
            self.nx = max(np.size(self.x), np.size(self.x0), np.size(self.xL))
            self.nf = np.size(self.f)
            if self.g == None or self.g == []:
                self.ng = 0
            else:
                self.ng = max(np.size(self.g), np.size(self.gLimit))

            # check if one parameter for all design variables, i.e. vector
            if np.size(self.x) == 1 and  self.nx>1:
                self.xVector = True
            else:
                self.xVector = False

            # # check if one parameter for all constraints, i.e. vector
            if np.size(self.g) == 1 and self.ng>1:
                 self.gVector = True
            else:
                 self.gVector = False

            # Reformat x0, xL and xU to be np.arrays and of proper size
            if type(self.x0) == list:
                self.x0 = np.array(self.x0)
            if type(self.xL) == list:
                self.xL = np.array(self.xL)
            if type(self.xU) == list:
                self.xU = np.array(self.xU)
            if np.size(self.xL) == 1 and  self.nx>1:
                self.xL = np.array([self.xL]*self.nx)
                self.xU = np.array([self.xU]*self.nx)

            # Reformat and set normalization (scaling)
            if(self.xNorm == None or self.xNorm == True or
               self.xNorm == [True]):
                self.xNorm = [True]*self.nx
            elif self.xNorm == False or self.xNorm == [False]:
                self.xNorm = [False]*self.nx

            if(self.fNorm == None or self.fNorm == True or
               self.fNorm == [True]):
                self.fNorm = [True]*self.nf
                #self.fNorm =
            elif self.fNorm == False or self.fNorm == [False]:
                self.fNorm = [False]*self.nf
                #self.fNorm = False

            if(self.gNorm == None or self.gNorm == True or
               self.gNorm == [True] or self.gNorm == []):
                self.gNorm = [True]*self.ng
            elif self.gNorm == False or self.gNorm == [False]:
                self.gNorm = [False]*self.ng
            for i, gLimiti in enumerate(self.gLimit):
                if gLimiti == 0:
                    self.gNorm[i] = False

            if(self.gType == None  or self.gType == "upper" or
               self.gType == ["upper"]):
                self.gType = ["upper"]*self.ng
            elif self.gType == "lower" or self.gType == ["lower"]:
                self.xNorm = ["lower"]*self.nx
            # TODO equality constraints?


            # TODO
            #if self.fType.upper()[0:3] == "MIN":
            #
            #

            # Optimization Algorithm
            self.SciPyAlg = False
            self.pyOptAlg = False
            self.pyGmoAlg = False
            self.nloptAlg = False
            if (self.Alg).upper() in {"ALGENCAN", "ALHSO", "ALPSO", "COBYLA",
                                      "CONMIN", "FILTERSD", "FSQP", "GCMMA",
                                      "IPOPT", "KSOPT", "MIDACO", "MMA",
                                      "MMFD", "NLPQLP", "NSGA2", "PSQP",
                                      "SDPEN", "SLSQP", "SOLVOPT"}:
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
            else:
                raise Exception("Not a valid optimization algorithm")
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
                xVal = xVal[0:self.nx]

                # Denorm and assign of design variables
                if self.xVector:
                    if self.xNorm[0]:
                        xVal = denormalize(xVal, self.xL, self.xU)
                    setattr(self.Model, self.x, xVal)
                else:
                    for i, xi in enumerate(xVal):
                        if self.xNorm[i]:
                            xVal[i] = denormalize(xi, self.xL[i], self.xU[i])
                        if self.x is not None:
                            setattr(self.Model, self.x[i], xVal[i])

                # Call
                if self.x is None:
                    eval("self."+self.Primal+"(xVal)")
                else:
                    eval("self.Model."+self.Primal+"(self.Model)")

                # Objective and scaling (norm)
                fVal = getattr(self.Model, self.f[0])
                if self.fNorm[0]:
                    if self.f0 is None:
                        self.f0 = fVal
                    if self.f0 == 0:
                        fVal = fVal*self.fNormMultiplier
                    else:
                        fVal = fVal/abs(self.f0)*self.fNormMultiplier
                #change the amass = 0.005056928723802732bove to allow for multiobjective
                #fVal = []
                #for fi in self.f:
                #    print(getattr(self, fi))

                # Formulate constraint function (upper/lower, normalized)
                rconval = []
                if self.g:
                    gVal = [None]*self.ng
                    for i, gi in enumerate(self.g):
                        rconvalAll = np.array(getattr(self.Model, gi))
                        if np.size(rconvalAll) == 1:
                            rconvalAll = rconvalAll.reshape((1,))
                        #nr = np.size(rconval)
                        #for j in range(nr):
                        for j, rconval in enumerate(rconvalAll):
                            if self.gNorm[i+j]:
                                if self.gType[i+j] == "upper":
                                    gVal[i+j] = rconval/self.gLimit[i+j]-1
                                elif self.gType[i+j] == "lower":
                                    gVal[i+j] = 1-rconval/self.gLimit[i+j]
                            else:
                                if self.gType[i+j] == "upper":
                                    gVal[i+j] = rconval-self.gLimit[i+j]
                                elif self.gType[i+j] == "lower":
                                    gVal[i+j] = self.gLimit[i+j]-rconval
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

                xVal = xVal[0:self.nx]

                # Denorm and assign of design variables
                if self.xVector:
                    if self.xNorm[0]:
                        xVal = denormalize(xVal, self.xL, self.xU)
                    setattr(self.Model, self.x, xVal)
                else:
                    for i, xi in enumerate(xVal):
                        if self.xNorm[i]:
                            xVal[i] = denormalize(xi, self.xL[i], self.xU[i])
                        if self.x is not None:
                            setattr(self, self.x[i], xVal[i])

                # Call
                if self.x is None:
                    eval("self."+self.Sensitivity+"(xVal)")
                else:
                    eval("self.Model."+self.Sensitivity+"(self.Model)")

                # Senstivity of objective
                fNablaVal = getattr(self.Model, self.fNabla[0])
                if self.fNorm[0]:
                    if self.f0 == 0:
                        fNablaVal = fNablaVal *self.fNormMultiplier
                    else:
                        fNablaVal = fNablaVal /abs(self.f0)*self.fNormMultiplier
                for i in range(len(xVal)):
                    if self.xNorm[i]:
                        fNablaVal[i] *= (self.xU[i]-self.xL[i])

                # Senstivity of constraints
                # Not working for gVector type of constraint definition
                # TODO redesign for gVector = True
                if self.g:
                    gNablaVal = [None]*self.ng
                    if self.gVector:
                        rNablaValAll = getattr(self.Model, self.gNabla[0])
                    for i, gNablai in enumerate(self.gNabla):
                        # if self.gVector:
                        #     rNablaVal = rNablaValAll[i]
                        # else:
                        #     rNablaVal = getattr(self.Model, gNablai)
                        rNablaVal = getattr(self.Model, gNablai)
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
                    if self.f0 == 0:
                        fNablaVal = fVal*self.fNormMultiplier
                    else:
                        fNablaVal = fVal/abs(self.f0)*self.fNormMultiplier
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
                    if self.f0 == 0:
                        self.fOpt = fOpt/self.fNormMultiplier
                    else:
                        self.fOpt = fOpt*abs(self.f0)/self.fNormMultiplier
                else:
                    self.fOpt = fOpt
                # if self.PrintOutput:
                #     pass

                try:
                    self.inform = Alg.getInform(0)
                except:
                    self.inform = inform

                self.readHistory()
                self.fNablaIt = np.array(self.fNablaIt)
                self.fNormNablaIt = copy.deepcopy(self.fNablaIt)
                self.fNablaOpt =  copy.deepcopy(self.fNablaIt[-1])
                self.fNormNablaOpt =  copy.deepcopy(self.fNablaIt[-1])
                if self.fNorm[0]:
                    if self.f0 == 0:
                         self.fNablaIt  = self.fNablaIt/self.fNormMultiplier
                         self.fNablaOpt = self.fNablaOpt/self.fNormMultiplier
                    else:
                         self.fNablaIt  = self.fNablaIt/self.fNormMultiplier*abs(self.f0)
                         self.fNablaOpt = self.fNablaOpt/self.fNormMultiplier*abs(self.f0)
                self.gNablaOpt = np.array(self.gNablaIt[-1]).reshape(self.ng, self.nx)

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
