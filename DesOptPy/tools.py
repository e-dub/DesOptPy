from packaging import version
import os
import numpy as np


def checkProblem(self):
    # idiot check
    if self.x == None:
        raise Exception('Design variables x not set. ')
    # if self.xL == None:
    #    raise Exception("Lower bound of design variables xL not set. ")
    # if self.xU == None:
    #    raise Exception("Lower bound of design variables xU not set. ")
    if self.f == None:
        raise Exception('Objective f not set. ')
    if self.Primal == None:
        raise Exception('Primal not set. ')


def checkAlgorithms():
    """


    Returns
    -------
    None.

    """
    print('The following algorithms are available')
    try:
        import pyOpt

        pyOptAlgList = [
            'ALGENCAN',
            'ALHSO',
            'ALPSO',
            'COBYLA',
            'CONMIN',
            'FILTERSD',
            'FSQP',
            'GCMMA',
            'IPOPT',
            'KSOPT',
            'MIDACO',
            'MMA',
            'MMFD',
            'NLPQL',
            'NLPQLP',
            'NSGA2',
            'PSQP',
            'SDPEN',
            'SLSQP',
            'SNOT',
            'SOLVOPT',
        ]
        algAvail = '\npyOpt algorithms available:'
        algNotAvail = '\npyOpt algorithms NOT AVAILABLE:'
        na = 0
        for i in pyOptAlgList:
            try:
                eval('pyOpt.' + i + '()')
                algAvail += '\n' + i + ' available'
            except:
                algNotAvail += '\n' + i + ' NOT AVAILABLE'
                na = 1
        print('\033[32m' + algAvail + '\033[0m')
        if na:
            print('\033[31m' + algNotAvail + '\033[0m')
    except:
        print('\033[41m' + 'pyOpt NOT INSTALLED' + '\033[0m')

    try:
        import scipy
        import scipy.optimize as spopt

        SciPyAlgList = ['slsqp', 'trust-constr', 'differential_evolution']
        algAvail = '\nSciPy ' + scipy.__version__ + ' algorithms available:'
        algNotAvail = '\nSciPy algorithms NOT AVAILABLE:'
        algAvail += '\n' + 'SLSQP' + ' available'
        algAvail += '\n' + 'trust-constr' + ' available'
        na = 0
        if version.parse(scipy.__version__) >= version.parse('1.7.0'):
            for i in SciPyAlgList[2:]:
                try:
                    eval('spopt.' + i)
                    algAvail += '\n' + i + ' available'
                except:
                    algNotAvail += '\n' + i + ' NOT AVAILABLE'
                    na = 1
            print('\033[32m' + algAvail + '\033[0m')
            if na:
                print('\033[31m' + algNotAvail + '\033[0m')
        else:
            print('\nDesOptPy tested with version SciPy version 1.7.0')
            print('update to this version, e.g.')
            print('    pip install scipy -U')
    except:
        print('\033[31m' + 'SciPy NOT INSTALLED' + '\033[0m')

    try:
        import pygmo

        algAvail = 'pyGMO algorithms available'
        print('\033[32m' + algAvail + '\033[0m')
    except:
        print('\033[31m' + 'pyGMO NOT INSTALLED' + '\033[0m')
