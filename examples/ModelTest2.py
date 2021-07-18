class Model:
    a = 10
    F = 100
    ell = 10
    sigma = None
    m = None

    def calc(self):
        self.m = self.a*self.ell
        self.sigma = self.F/self.a
        print(self.m*2)
