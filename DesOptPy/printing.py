import numpy as np


def printResults(self):
    """


    Returns
    -------
    None.

    """
    lines = '-' * 75
    print()
    # print(lines)
    print('Optimization results - DesOptPy 2.0')
    print()
    # print(lines)
    print(self.ModelName)
    print('Optimization algorithm = ' + self.Alg)
    print()
    print('Optimization model values:')
    # print()
    print('f* = ', end='')
    print(*self.fNormOpt, sep='\n     ', flush=True)
    print()
    if self.gOpt is not None:
        print('g* = ', end='')
        print(*np.array(self.gOpt), sep='\n     ', flush=True)
        print()
    print('x* = ', end='')
    print(*self.xNormOpt[0 : self.nx], sep='\n     ', flush=False)
    print()

    # add function to normalize and denormlaize constraints, change here.
    # print("Evaluation system values")
    # print()
    print('objective response at optimum:')
    for i in range(self.nf):
        print(self.f[i] + ' = ' + str((self.fOpt[i])))
    print()
    if self.g is not None:
        print('constrained response at optimum (limit):')
        # for i in range(self.ng):
        for i, gi in enumerate(self.gOpt):
            if self.gNorm[i]:
                if self.gType[i] == 'upper':
                    r = (gi + 1) * self.gLimit[i]
                elif self.gType[i] == 'lower':
                    r = -(gi - 1) * self.gLimit[i]
            else:
                if self.gType[i] == 'upper':
                    r = gi + self.gLimit[i]
                elif self.gType[i] == 'lower':
                    r = self.gLimit[i] - gi
            if np.size(self.g) == 1 and np.size(r) == 1:
                print(
                    self.g[0]
                    + ' = '
                    + str(r)
                    + ' ('
                    + str(self.gLimit[i])
                    + ', '
                    + self.gType[i]
                    + ')'
                )
            elif np.size(self.g) == 1 and self.ng > 1:
                print(
                    self.g[i]
                    + ' = '
                    + str(r[0])
                    + ' ('
                    + str(self.gLimit[i])
                    + ', '
                    + self.gType[i]
                    + ')'
                )
                for j in range(1, np.size(self.gi)):
                    print(*np.array(self.r[j]), sep='\n     ', flush=True)
            else:
                print(
                    self.g[i]
                    + ' = '
                    + str(r)
                    + ' ('
                    + str(self.gLimit[i])
                    + ', '
                    + self.gType[i]
                    + ')'
                )
        print()
    print('design at optimum (lower bound, upper bound):')
    if self.xVector:
        print(
            self.x
            + ' = '
            + str(self.xOpt[0])
            + ' ('
            + str(self.xL[0])
            + ', '
            + str(self.xU[0])
            + ')'
        )
        for j in range(1, np.size(self.xOpt)):
            print(
                '    '
                + str(self.xOpt[j])
                + ' ('
                + str(self.xL[j])
                + ', '
                + str(self.xU[j])
                + ')'
            )
    else:
        for i in range(self.nx):
            print(
                self.x[i]
                + ' = '
                + str((self.xOpt[i]))
                + ' ('
                + str(self.xL[i])
                + ', '
                + str(self.xU[i])
                + ')'
            )
    print()
    print('t = ' + str(self.tOpt) + ' [h:mm:ss]')
    print()
    if self.nGen:
        print('nGen = ' + str(self.nGen))
    else:
        print('nIt = ' + str(self.nIt))
    print('nEval = ' + str(self.nEval))
    if self.nSensEval is not None:
        print('nSensEval = ' + str(self.nSensEval))
    print()
    if self.RunFolder and self.RemoveRunFolder is False:
        print('See run directory: ' + self.RunDir)
    elif self.RunFolder and self.RemoveRunFolder:
        print('Run cleaned, run directory deleted')
    else:
        print('Local run, all results saved in current directory')
    # print(lines)
    print()
