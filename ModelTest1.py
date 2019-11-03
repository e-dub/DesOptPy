class Model:
    A = 10
    F = 100
    el = 10
    sigma = None
    m = None

    def calc(self):
        self.m = self.A*self.el
        self.sigma = self.F/self.A

    def calcSens(self):
        mNablaA = self.el
        mNablael = self.A
        self.mNabla = [mNablaA, mNablael]
        sigmaNablaA = -2*self.F*self.A**-2
        sigmaNablael = 0
        self.sigmaNabla = [sigmaNablaA, sigmaNablael]
