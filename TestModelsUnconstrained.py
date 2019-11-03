import numpy as np
from scipy.optimize import rosen, rosen_der


class Ackley:
    a = 20
    b = 0.2
    c = 2*np.pi

    def calc(self, x):
        n = len(x)
        s1 = sum(x**2)
        s2 = sum(np.cos(self.c * x))
        self.f = (-self.a*np.exp(-self.b*np.sqrt(s1 / n)) -
                  np.exp(s2 / n) + self.a + np.exp(1))


class DixonPrice:
    def calc(self, x):
        n = len(x)
        j = np.arange(2, n+1)
        x2 = 2 * x**2
        self.f = np.sum(j*(x2[1:]-x[:-1])**2)+(x[0]-1)**2


class Eggholder:
    y = 2
    z = 2

    def calc(self):
        self.f = -((self.z+47)*np.sin(np.sqrt(abs(self.z+self.y/2+47))) -
                   self.y*np.sin(np.sqrt(abs(self.y-(self.z+47)))))


class Styblinski:
    z = 2
    y = 2

    def calc(self):
        self.v = 1./2.*(self.z**4-16.*self.z**2+5.*self.z +
                        self.y**4-16.*self.y**2+5.*self.y)


class Griewank:
    def calc(self, x):
        fr = 4000
        n = len(x)
        j = np.arange(1., n+1)
        s = np.sum(x**2)
        p = np.prod(np.cos(x/np.sqrt(j)))
        self.f = s/fr - p + 1


class Himmelblau:
    def calc(self, x):
        self.f = (x[0]**2+x[1]-11)**2+(x[0]+x[1]**2-7)**2


class Levy:
    def calc(self, x):
        n = len(x)
        self.f = 10*n+np.sum(x**2-10*np.cos(2.*np.pi*x))


class Michalewicz:
    def calc(self, x):
        m = 2
        n = len(x)
        j = np.arange(1., n+1)
        self.f = -np.sum(np.sin(x)*np.sin(j*x**2/np.pi)**(2.*m))


class Rastrigin:
    def calc(self, x):
        n = len(x)
        self.f = 10*n+np.sum(x**2-10*np.cos(2.*np.pi*x))


class Rosenbrock:
    def calc(self, x):
        self.obj = rosen(x)

    def calcSens(self, x):
        self.objNabla = rosen_der(x)
