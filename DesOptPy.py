"""
TODOS:

TODO return arrays!!! not lists, for gradients important!
TODO test gradients that they work well!!!
xTODO new github repository
TODO add pygmo
TODO add scipy optimization
scipy.optimize https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html
TODO add or-tools?
TODO add Hybrid Cellular Automata
https://developers.google.com/optimization/introduction/python
TODO add algorithm list?
xTODO variable function for primal and sens
xTODO different way to define design variables with x vector
xTODO read in history at end
TODO renorm etc with history!!! Iteration values, Optimal values
xTODO File handling and run results folder (no run only modelname with time stamp)
xTODO File handling save all evaluation data
TODO filehandling for saving all evaluation to find if it is a new iteration or a finite differencing iteration (or also step length)
TODO Postprocessing for shadow prices
TODO surrogating?
TODO ResultReport
TODO Optimization live monitoring!
TODO Algorithm options
TODO Variable linking?

sources
 mdao py for pyopt???
"""

import datetime
import os
from copy import deepcopy
import shutil
import numpy as np
try:
    import cpuinfo
except: pass

__title__ = "DESign OPTimization in PYthon"
__shorttitle__ = "DesOptPy"
__version__ = "2.0 prerelease"
__all__ = ["DesOpt"]
__author__ = "E. J. Wehrle"
__copyright__ = "Copyright 2019 E. J. Wehrle"
__email__ = "Erich.Wehrle(a)unibz.it"
__url__ = 'github.com/edub/DesOptPy2'
#TODO decide on license for new version
__license__ = "TBD"  #"GNU Lesser General Public License"


def PrintDesOptPy():
    print()
    print("-"*75)
    print(__title__+" - "+__shorttitle__)
    print("-"*75)
    print("Version:    "+__version__)
    print("License:    "+__license__)
    print("Internet:   "+__url__)
    print("\n")


def normalize(x, xL, xU):
    return(x-xL)/(xU-xL)


def denormalize(xNorm, xL, xU):
    return(xNorm*(xU-xL)+xL)


PrintDesOptPy()


def OptimizationSetup(Model):
    class Opt(Model):
        x = None
        f = None
        g = None
        xLast = None
        xOpt = None
        fOpt = None
        gOpt = None
        fNabla = None
        gNabla = None
        xNorm = True
        fNorm = True
        Primal = "calc"
        Sensitivity  = None
        xDelta = 1e-3
        Alg = "NLPQLP"
        pyOptAlg = None
        SciPyAlg = None
        pyGmoAlg = None
        PrintOutput = True
        ModelName = str(Model.__name__)
        fNormMultiplier = 1000
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
        except: pass

        class KaruschKuhnTucker(object):
            from numpy.linalg import norm, lstsq
            kkteps = 1e-3
            def checkKKT(self):
                self.PrimalFeas = (max(self.gOpt) < self.kkteps)
                self.ComplSlack = (max(self.gOpt@self.Lambda) < self.kkteps)
                self.DualFeas = (min(self.Lambda) > -self.kkteps)
                self.kktOpt = bool(self.PrimalFeas*self.DualFeas*self.ComplSlack)
                self.Opt1Order = norm(self.OptResidual)
                self.kktMax = max(abs(self.OptResidual))

        def calcPosprocessing(self):
            ShadowPrices = []

        def readHistory(self):
            # make function of new file
            import pyOpt
            OptHist = pyOpt.History(self.Name, "r")
            xAll = OptHist.read([0, -1], ["x"])[0]["x"]
            xNormAll = deepcopy(xAll)
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
            xAll = [l.tolist() for l in xAll]
            xNormAll = [l.tolist() for l in xNormAll]
            fAll = [l.tolist() for l in fAll]
            gAll = [l.tolist() for l in gAll]
            fNablaIt = [l.tolist() for l in fNablaIt]
            gNablaIt = [l.tolist() for l in gNablaIt]
            failIt = [l.tolist() for l in failIt]

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



        def optimize(self):
            self.t0 = datetime.datetime.now()
            self.t0str = self.t0.strftime("%Y%m%d%H%M%S")
            self.Name = self.ModelName+self.Alg+self.t0str
            self.nEval = 0
            self.nSensEval = None
            self.f0 = None

            # Optimization Algorithm
            if (self.Alg).upper() in {"SLSQP", "NLPQLP", "COBYLA"}:
                self.pyOptAlg = True
                self.SciPyAlg = False
                self.pyGmoAlg  = False
            elif (self.Alg[:5]).upper() == "SCIPY" or (self.Alg[-5:]).upper == "SCIPY":
                self.SciPyAlg = True
                self.pyOptAlg = False
                self.pyGmoAlg  = False


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
                print("\nTo start monitoring visualization enter, run folder" +
                      "\n\n    " + self.RunDir + "\n\n"
                      "and enter the following command in terminal:" +
                      "\n\n    bokeh serve --show DesOptMonitor.py \n\n")

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

                # Constraints
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
                
            def ObjFnSciPy(xVal):
                if np.array_equal(self.xLast, xVal) != True:
                    self.fVal, self.gVal, flag = SysEq(xVal)
                    self.xLast = xVal.copy()
                return(self.fVal)
            
            def ConFnSciPy(xVal):
                if np.array_equal(self.xLast, xVal) != True:
                    self.fVal, self.gVal, flag = SysEq(xVal)
                    self.xLast = xVal.copy()
                return(self.gVal)

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
                    fNablaVal = fVal/self.f0*self.fNormMultiplier
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
            x0 = [None]*len(self.x0)
            xL = [None]*len(self.x0)
            xU = [None]*len(self.x0)
            for i in range(len(self.x0)):
                if self.xNorm[i]:
                    x0[i] = normalize(self.x0[i], self.xL[i], self.xU[i])
                    xL[i] = 0
                    xU[i] = 1
                else:
                    x0[i] = self.x0[i]
                    xL[i] = self.xL[i]
                    xU[i] = self.xU[i]
                
            # Seperate file an dchild class??
            if self.pyOptAlg:
                import pyOpt
                Alg = eval("pyOpt." + self.Alg + '()')
                Problem = pyOpt.Optimization(self.ModelName, SysEq)
                for i in range(len(self.x0)):   
                    Problem.addVar('x'+str(i+1), 'c', value=x0[i], lower=xL[i],
                                   upper=xU[i])
                for i in range(len(self.f)):
                    Problem.addObj('f'+str(i+1))
                if self.g:
                    for i in range(len(self.g)):
                        Problem.addCon('g'+str(i+1), 'i')
                if self.PrintOutput:
                    print(Problem)

                # Call
                if self.Sensitivity is None:
                    fOpt, xOpt, inform = Alg(Problem, sens_step=self.xDelta,
                                             store_hst=self.Name)
                elif self.Sensitivity == "autograd":
                    fOpt, xOpt, inform = Alg(Problem, sens_type=AutoSensEq,
                                             store_hst=self.Name)
                else:
                    self.nSensEval = 0
                    fOpt, xOpt, inform = Alg(Problem, sens_type=SensEq,
                                             store_hst=self.Name)

                if self.PrintOutput:
                    pass

                self.inform = Alg.getInform(0)
                self.readHistory()
                
                # Denormalization
                self.xOpt = [None]*len(self.x0)
                for i in range(len(self.x0)):
                    if self.xNorm[i]:
                        self.xOpt[i] = denormalize(xOpt[i][0], self.xL[i],
                                                   self.xU[i])
                    else:
                        self.xOpt[i] = xOpt[i]
                if self.fNorm[0]:
                    self.fOpt = fOpt*self.f0/self.fNormMultiplier
                else:
                    self.fOpt = fOpt

            # Seperate file and child class??
            elif self.pyGmoAlg:
                import pygmo


            # Seperate file and child class??
            elif self.SciPyAlg:
                from scipy import optimize as spopt
                Alg = "SLSQP"
                #Alg = "trust-constr"
                Results = spopt.minimize(ObjFnSciPy, x0, method=Alg, 
                                         bounds=spopt.Bounds(xL, xU),
                                         constraints=spopt.NonlinearConstraint(ConFnSciPy, -np.inf, 0),
                                         options={"eps": self.xDelta, 
                                                  "ftol": 1e-6,
                                                  "disp": False,
                                                  "iprint": 1,
                                                  "maxiter": 100})
                xOpt = Results.x
                fOpt = Results.fun
                self.fNablaOpt = Results.jac
                self.nIt = Results.nit
                self.nEval = Results.nfev
                self.nSensEval = Results.njev
                self.inform = Results.success
                
                # Denormalization
                self.xOpt = [None]*len(self.x0)
                for i in range(len(self.x0)):
                    if self.xNorm[i]:
                        self.xOpt[i] = denormalize(xOpt[i], self.xL[i],
                                                   self.xU[i])
                    else:
                        self.xOpt[i] = xOpt[i]
                if self.fNorm[0]:
                    self.fOpt = [fOpt*self.f0/self.fNormMultiplier]
                else:
                    self.fOpt = [fOpt]
                
            # Seperate file and child class??
            elif self.ortoolsAlg:
                pass

            def optimizeMutiobjective(self):
                pass
            

                
                
            self.t1 = datetime.datetime.now()
            self.tOpt = (self.t1-self.t0)
            if self.PrintOutput:
                lines = "-"*75
                print()
                print(lines)
                print("Optimization results - DesOptPy 2.0")
                print(lines)
                print("Optimization algorithm = " + self.Alg)
                print("f* = " + str(self.fOpt[0]))
                if self.gOpt is not None:
                    if len(self.gOpt) > 3:
                        print("g* = ")
                        print(*self.gOpt, sep="\n", flush=True)
                    else:
                        print("g* = " + str(self.gOpt))
                if len(self.xOpt) > 3:
                    print("x* = ")
                    print(*self.xOpt, sep="\n", flush=True)
                else:
                    print("x* = " + str(self.xOpt))
#                if np.size(lambda_c) > 0:
#                    print("Lagrangian multipliers = " +
#                          str(lambda_c.reshape(np.size(lambda_c,))))
#                    print("Type of active constraints = " + str(gAllActiveType))
#                    print("Shadow prices = " + str(SPg))
#                if kktOpt:
#                    print("Karush-Kuhn-Tucker optimality criteria fulfilled")
#                elif kktOpt==0:
#                    print("Karush-Kuhn-Tucker optimality criteria NOT fulfilled")
#                if Opt1Order:
#                    print("First-order residual of Lagrangian function = " + str(Opt1Order))
                print("Time of optimization [h:mm:ss:ms] = " + str(self.tOpt))
                try:
                    print("nGen = " + str(self.nGen))
                except:
                    print("nIt = " + str(self.nIt))
                print("nEval = " + str(self.nEval))
                if self.nSensEval is not None:
                    print("nSensEval = " + str(self.nSensEval))
                if self.RunFolder and self.RemoveRunFolder is False:
                    print("See run directory: " + self.RunDir)
                elif self.RunFolder and self.RemoveRunFolder:
                    print("Run cleaned, run directory deleted")
                else:
                    print("Local run, all results saved in current directory")
                print(lines)
                if self.OS == "Linux" and self.Alarm:
                    os.system("play --no-show-progress --null --channels 1 " +
                              "synth 2 sine 329.63 fade q 0.05 0.9 0.05")

            if self.RunFolder:
                os.chdir(self.MainDir)
                if self.RemoveRunFolder:
                    shutil.rmtree(self.RunDir)
    return Opt()
