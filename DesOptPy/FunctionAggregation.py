"""
Function aggregation with
    Kreisselmeier-Steinhauser (KS)
    p-Norm (pNorm)
    Kreisselmeier-Steinhauser with offset to avoid data overflow (KS2)
    p-Norm with offset to avoid data overflow (pNorm2)
    Induced exponential (IE)
    Induced power (IP)

Recommendation for use: KS2 with p>100


Literature:
    G. Kreisselmeier and R. Steinhauser (1979) Systematic control design by
    optimizing a vector performance index. In International Federation of
    Active Controls Syposium on Computer-Aided Design of Control Systems,
    Zurich, Switzerland.

Second version of the functions as described in
    A. B. Lambe, J. R. R. A. Martins, and G. J. Kennedy. An evaluation of
    constraint aggregation strategies for wing boxmass minimization. Structural
    and Multidisciplinary Optimization, 55(1):257–277, January 2017
Was the KS version of this first published in???
    Martins and Poon (2005) On structural optimization using constraint
    aggregation 6th World Congress on Structural and Multidisciplinary
    Optimization, Rio de Janeiro, Brazil.

Induced exponential aggregation introduced by
    Kennedy (2015) Strategies for adaptive optimization with aggregation
    constraints using interior-point methods, Computers & Structures, 153:
    217-229.
and
    Kennedy and Hicken (2015) Improved constraint-aggregation methods. Computer
    Methods in Applied Mechanics and Engineering 289:332-354.

Papers can be found here:
    http://gkennedy.gatech.edu/publications/
    http://mdolab.engin.umich.edu/biblio


Note:
p-norm and induced power aggregation do not work with negative numbers or mix
of positive and negative numbers(minimum problem, i.e. frequencies)


TODO implement sensitivities for IP and IE
"""
import numpy as np


def KS(f, p=200):
    """
    Return returns scalar KS function from vector f.
    """
    p = float(p)
    return 1 / p * (np.log(np.sum(np.exp(p * f))))


def KSSens(f, dfdx, p=200):
    """
    Return vector sensitvities of KS function from vector f and matrix dfdx.
    """
    p = float(p)
    return 1 / np.sum(np.exp(p * f)) * np.exp(p * f) @ dfdx


def KS2(f, p=200):
    """
    Return returns scalar KS function from vector f.
    """
    p = float(p)
    return np.max(f) + 1 / p * np.log(np.sum(np.exp(p * (f - np.max(f)))))


def KS2Sens(f, dfdx, p=200):
    """
    Return vector sensitvities of KS function from vector f and matrix dfdx.
    """
    p = float(p)
    return (
        1
        / np.sum(np.exp(p * (f - np.max(f))))
        * np.exp(p * (f - np.max(f)))
        @ dfdx
    )


def pNorm(f, p=200):
    """Return returns scalar p-norm from vector f."""
    p = float(p)
    return np.sum(f ** p) ** (1 / p)


def pNormSens(f, dfdx, p=200):
    """Return vector sensitvities of p-norm from vector f and matrix dfdx."""
    p = float(p)
    return np.sum(f ** p) ** (1 / p - 1) * (f ** (p - 1)) @ dfdx


def pNorm2(f, p=200):
    """Return scalar p-norm from vector f."""
    p = float(p)
    return np.max(f) * np.sum((f / np.max(f)) ** p) ** (1 / p)


def pNorm2Sens(f, dfdx, p=200):
    """Return vector sensitvities of p-norm from vector f and matrix dfdx."""
    p = float(p)
    return (
        np.sum((f / np.max(f)) ** p) ** (1 / p - 1)
        * ((f / np.max(f)) ** (p - 1))
        @ dfdx
    )

def IE(f, p=200):
    """Return scalar induced exponential aggregation from vector f."""
    p = float(p)
    return np.sum(f * np.exp(p * f)) / np.sum(np.exp(p * f))

def IESens(f, dfdx, p=200):
    """Return vector sensitvities of induced exponential from vector f and matrix dfdx."""
    p = float(p)
    return KSSens(f, dfdx, p)


def IP(f, p=200):
    """Return scalar induced power aggregation from vector f."""
    p = float(p)
    return np.sum(f ** (p + 1)) / np.sum(f ** p)

def IPSens(f, dfdx, p=200):
    """Return vector sensitvities of induced power from vector f and matrix dfdx."""
    p = float(p)
    #return ((1/f*np.sum(f ** (p + 1))) / np.sum(f ** p))@dfdx
    return ((f ** p) / np.sum(f ** p))@dfdx


if __name__ == '__main__':
    print('')
    print('Testing of functions:')
    print('')
    p = 200
    print('-' * 50)
    print('Example 1 - simple example, small values, small number of values')
    print('-' * 50)
    f = np.array([1, 2, 3])
    dfdx = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]).T
    dfdx[-1, -1] = 0
    print('fKS:', KS(f, p))
    print('nabla_fKS:', KSSens(f, dfdx, p))
    print('fp:', pNorm(f, p))
    print('nabla_fp:', pNormSens(f, dfdx, p))
    print('fKS2:', KS2(f, p))
    print('nabla_fKS2:', KS2Sens(f, dfdx, p))
    print('fp2:', pNorm2(f, p))
    print('nabla_fp2:', pNorm2Sens(f, dfdx, p))
    print('fIE:', IE(f, p))
    print('nabla_fIE:', IESens(f, dfdx, p))
    print('fIP:', IP(f, p))
    print('nabla_fIP:', IPSens(f, dfdx, p))
    print('')
    print('True values:')
    print('fMax :', np.max(f))
    print('fMaxNabla :', dfdx[:, -1])
    print('-' * 50)
    print('')
    print('-' * 50)
    print('Example 2 - large values, large number of values')
    print('-' * 50)
    nr2 = 100000
    nx2 = 3
    fVal = 10000
    dfdxVal = 10000
    f = np.linspace(1, fVal, nr2)
    dfdx = np.linspace(1, dfdxVal, nr2 * nx2).reshape(nr2, nx2)
    dfdx[0:-1, -1] = 0.0
    print('fKS:', KS(f, p))
    print('nabla_fKS:', KSSens(f, dfdx, p))
    print('fp:', pNorm(f, p))
    print('nabla_fp:', pNormSens(f, dfdx, p))
    print('fKS2:', KS2(f, p))
    print('nabla_fKS2:', KS2Sens(f, dfdx, p))
    print('fp2:', pNorm2(f, p))
    print('nabla_fp2:', pNorm2Sens(f, dfdx, p))
    print('fIE:', IE(f, p))
    print('fIP:', IP(f, p))
    print('')
    print('True values:')
    print('fMax :', np.max(f))
    print('fMaxNabla :', dfdx[:, -1])
    print('-' * 50)
    print('')
    print('-' * 50)
    print('Example 3 - negative values')
    print('-' * 50)
    f = np.array([1, 2, 3])
    dfdx = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]).T
    dfdx[-1, -1] = 0
    print('fKS:', -KS(-f, p))
    print('nabla_fKS:', -KSSens(-f, -dfdx, p))
    print('fp:', -pNorm(-f, p))
    print('nabla_fp:', -pNormSens(-f, -dfdx, p))
    print('fKS2:', -KS2(-f, p))
    print('nabla_fKS2:', -KS2Sens(-f, -dfdx, p))
    print('fp2:', -pNorm2(-f, p))
    print('nabla_fp2:', -pNorm2Sens(-f, -dfdx, p))
    print('fIE:', -IE(-f, p))
    print('fIP:', -IP(-f, p))
    print('')
    print('True values:')
    print('fMin:', np.min(f))
    print('fMinNabla :', dfdx[:, 0])
    print('-' * 50)
    print('')
    print('-' * 50)
    print('Example 4 - pseudo topology optimization, very large sparse matrix')
    from scipy import sparse as sp

    print('-' * 50)
    nr = 1000000
    nx = 1000000
    fVal = 1000
    dfdxVal = 10000
    fTop = np.linspace(1, fVal, nr)
    dfdxTop = sp.diags(fTop)
    # dfdxTop = np.diag(fTop)
    print('fKS2:', KS2(fTop, p))
    dfdxTopKS2 = KS2Sens(fTop, dfdxTop, p)
    # print("max nabla_fKS2:", np.max(dfdxTopKS2))
    print('where nabla_fKS2>1:', np.argwhere(dfdxTopKS2 > 1e0))
    print('nabla_fKS2:', dfdxTopKS2[np.argwhere(dfdxTopKS2 > 1e0)])
    print('max nabla_fKS2:', np.max(dfdxTopKS2))
    print('fp2:', pNorm2(fTop, p))
    dfdxToppNorm2 = KS2Sens(fTop, dfdxTop, p)
    print('n(nabla_fp2)>1.0:', np.size(np.argwhere(dfdxToppNorm2 > 1e0)))
    print('max nabla_fpNorm2:', np.max(dfdxToppNorm2))
    print('')
    print('True values:')
    print('fMax :', np.max(fTop))
    print('fNabla > 1e0: [' + str(nx - 1) + ']')
    print('fNabla:', dfdxTop.tocsr()[nr - 1, nx - 1])
    print('-' * 50)
    print('')
    print('-' * 50)
    print('Example 5 - large values, large numbers, range of exponent')
    print('-' * 50)
    from matplotlib import pylab as plt

    nr2 = 100000
    nx2 = 3
    fVal = 10000
    dfdxVal = 10000
    f = np.linspace(1, fVal, nr2)
    dfdx = np.linspace(1, dfdxVal, nr2 * nx2).reshape(nx2, nr2)
    dfdx[0:-1, -1] = 0.0
    pList = np.logspace(-3, 5, 1001)

    fKS = []
    fpNorm = []
    fKS2 = []
    fpNorm2 = []
    fIE = []
    fIP = []
    for pi in pList:
        fKS.append(KS(f, pi))
        fKS2.append(KS2(f, pi))
        fpNorm.append(pNorm(f, pi))
        fpNorm2.append(pNorm2(f, pi))
        fIE.append(IE(f, pi))
        fIP.append(IP(f, pi))
    plt.semilogx(
        [10 ** -3, 10 ** 5], [fVal, fVal], 'k', linewidth=0.5, label='true'
    )
    plt.semilogx(pList, fKS, 'r', linestyle='dotted', label='KS')
    plt.semilogx(pList, fKS2, 'r', linestyle=(0, (5, 10)), label='modified KS')
    plt.semilogx(pList, fpNorm, 'b', linestyle='dotted', label='$p$-norm')
    plt.semilogx(
        pList, fpNorm2, 'b', linestyle=(0, (5, 10)), label='modified $p$-norm'
    )
    plt.semilogx(pList, fIE, 'g-', label='IE')
    plt.semilogx(pList, fIP, 'y-', label='IP')
    plt.xlim((10 ** -3, 10 ** 5))
    plt.ylim((8000, 12000))
    plt.xlabel('aggregation parameter $p$')
    plt.ylabel('approximated maximum value $\\max(f)$')
    plt.legend(frameon=False, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('Example 5: large values, large number of values')
    plt.show()

    print(
        """
Explanation of above:
    Original functions do not work with large numbers of values or large values
    p-Norm has problems with sensitvitivies with large difference in values
    p-Norm does not work with negative numbers
    Generally KS2 works well in all cases
          """
    )
