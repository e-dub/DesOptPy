from packaging import version
import os
import numpy as np


def checkAlgorithms():
    print("The following algorithms are available")
    try:
        import pyOpt
        pyOptAlgList = ["ALGENCAN", "ALHSO", "ALPSO", "COBYLA", "CONMIN",
                        "FILTERSD", "FSQP", "GCMMA", "IPOPT", "KSOPT",
                        "MIDACO", "MMA", "MMFD", "NLPQL", "NLPQLP", "NSGA2",
                        "PSQP", "SDPEN", "SLSQP", "SNOT", "SOLVOPT"]
        algAvail = "\npyOpt algorithms available:"
        algNotAvail = "\npyOpt algorithms NOT AVAILABLE:"
        na = 0
        for i in pyOptAlgList:
            try:
                eval("pyOpt." + i + "()")
                algAvail += "\n" + i + " available"
            except:
                algNotAvail += "\n" + i + " NOT AVAILABLE"
                na = 1
        print('\033[32m' +  algAvail + '\033[0m')
        if na:
            print('\033[31m' + algNotAvail + '\033[0m')

    except:
        print('\033[41m' + "pyOpt NOT INSTALLED" + '\033[0m')

    try:
        import scipy
        import scipy.optimize as spopt
        SciPyAlgList = ['slsqp', 'trust-constr', 'differential_evolution']
        algAvail = '\nSciPy ' + scipy.__version__ + ' algorithms available:'
        algNotAvail = "\nSciPy algorithms NOT AVAILABLE:"
        algAvail += "\n" + "SLSQP" + " available"
        algAvail += "\n" + "trust-constr" + " available"
        na = 0
        if version.parse(scipy.__version__) >= version.parse("1.7.0"):
            for i in SciPyAlgList[2:]:
                try:
                    eval("spopt." + i)
                    algAvail += "\n" + i + " available"
                except:
                    algNotAvail += "\n" + i + " NOT AVAILABLE"
                    na = 1
            print('\033[32m' +  algAvail + '\033[0m')
            if na:
                print('\033[31m' + algNotAvail + '\033[0m')
        else:
            print("\nDesOptPy tested with version SciPy version 1.7.0")
            print("update to this version, e.g.")
            print("    pip install scipy -U")


    except:
        print('\033[31m' + "SciPy NOT INSTALLED" + '\033[0m')

def printResults(self):
    lines = "-" * 75
    print()
    #print(lines)
    print("Optimization results - DesOptPy 2.0")
    #print(lines)
    print("Optimization algorithm = " + self.Alg)
    print()
    print("Optimization model values")
    print()
    print("f* = ", end="")
    print(*self.fNormOpt, sep="\n     ", flush=True)
    print()
    if self.gOpt is not None:
        print("g* = ", end="")
        print(*np.array(self.gOpt), sep="\n     ", flush=True)
    print()
    print("x* = ", end="")
    print(*self.xNormOpt, sep="\n     ", flush=False)
    print()

    # add function to normalize and denormlaize constraints, change here.
    print("Evaluation system values")
    print()
    print("optimal objective response:")
    for i in range(self.nf):
        print(self.f[i] +" = " + str((self.fOpt[i])))
    print()
    print("optimal constrained response (limit):")
    for i in range(self.ng):
        print(self.g[i] +" = " +
              str((self.gOpt[i]+1)*self.gLimit[i]) + " (" +
              str(self.gLimit[i]) + ")")
    print()
    print("optimal design (lower bound, upper bound):")
    for i in range(self.nx):
        print(self.x[i] +" = " + str((self.xOpt[i])) + " (" +
              str(self.xL[i]) + ", " + str(self.xU[i]) + ")")
    print()
    print("t = " + str(self.tOpt) +
          " [h:mm:ss]")
    print()
    if self.nGen:
        print("nGen = " + str(self.nGen))
    else:
        print("nIt = " + str(self.nIt))
    print("nEval = " + str(self.nEval))
    if self.nSensEval is not None:
        print("nSensEval = " + str(self.nSensEval))
    print()
    if self.RunFolder and self.RemoveRunFolder is False:
        print("See run directory: " + self.RunDir)
    elif self.RunFolder and self.RemoveRunFolder:
        print("Run cleaned, run directory deleted")
    else:
        print("Local run, all results saved in current directory")
    #print(lines)
    if self.OS == "Linux" and self.Alarm:
        os.system("play --no-show-progress --null --channels 1 " +
                  "-t alsa synth 2 sine 329.63 fade q 0.05 0.9 0.05")
    print()
