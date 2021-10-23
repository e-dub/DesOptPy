import copy
import numpy as np
from DesOptPy.scaling import normalize, denormalize


def readHistory(self):
    # make function of new file
    import pyOpt

    # read values from history
    OptHist = pyOpt.History(self.Name, 'r')
    xAll = OptHist.read([0, -1], ['x'])[0]['x']
    fAll = OptHist.read([0, -1], ['obj'])[0]['obj']
    gAll = OptHist.read([0, -1], ['con'])[0]['con']
    gNablaIt = OptHist.read([0, -1], ['grad_con'])[0]['grad_con']
    fNablaIt = OptHist.read([0, -1], ['grad_obj'])[0]['grad_obj']
    failIt = OptHist.read([0, -1], ['fail'])[0]['fail']
    OptHist.close()

    # denormalize design variable values
    xNormAll = copy.deepcopy(xAll)
    for ei in range(len(xAll)):
        for xi, xNormi in enumerate(self.xNorm):
            if xNormi:
                xAll[ei][xi] = denormalize(
                    xAll[ei][xi], self.xL[xi], self.xU[xi]
                )
    # NLPQLP g>0
    if self.Alg == 'NLPQLP':
        gAll = [g * -1 for g in gAll]

    # convert to list
    # TODO should be np.arrays??!!
    xAll = [i.tolist() for i in xAll]
    xNormAll = [i.tolist() for i in xNormAll]
    fAll = [i.tolist() for i in fAll]
    gAll = [i.tolist() for i in gAll]
    fNablaIt = [i.tolist() for i in fNablaIt]
    gNablaIt = [i.tolist() for i in gNablaIt]
    failIt = [i.tolist() for i in failIt]

    # initialize assignment to object
    self.nIt = len(fNablaIt)
    self.fIt = [None] * self.nIt
    self.fNormIt = [None] * self.nIt
    self.xIt = [None] * self.nIt
    self.xNormIt = [None] * self.nIt
    self.gIt = [None] * self.nIt
    self.gMaxIt = [None] * self.nIt

    self.gNablaIt = gNablaIt
    self.fNablaIt = fNablaIt

    # #TODO remove this
    # len(fAll) not = nEval for gradientbased!!!
    # if self.nEval == len(fAll):
    #     pass
    # else:
    #     raise Exception("something evil")

    # check if non-iteration-based algorithm
    if self.nIt == 0 and self.nEval > 0:
        self.nIt = None
        self.xNorm0 = xNormAll[0]
        if self.g is not None:
            self.g0 = np.array(gAll[0])
            self.gOpt = np.array(gAll[-1])
    else:

        for ii in range(self.nIt):
            Posdg = OptHist.cues['grad_con'][ii][0]
            Posf = OptHist.cues['obj'][ii][0]
            iii = 0
            while Posdg > Posf:
                iii = iii + 1
                try:
                    Posf = OptHist.cues['obj'][iii][0]
                except:
                    Posf = Posdg + 1
            iii = iii - 1
            if self.fNorm[0]:
                if self.f0 == 0:
                    self.fIt[ii] = (
                        np.array(fAll[iii])
                        / self.fNormMultiplier
                        * self.fMinMax
                    )
                else:
                    self.fIt[ii] = (
                        np.array(fAll[iii])
                        * abs(self.f0)
                        / self.fNormMultiplier
                        * self.fMinMax
                    )
            else:
                self.fIt[ii] = fAll[iii]
            self.fNormIt[ii] = fAll[iii]

            self.xIt[ii] = xAll[iii][0 : self.nx]
            self.xNormIt[ii] = xNormAll[iii][0 : self.nx]
            if self.g is not None:
                self.gIt[ii] = gAll[iii]
                self.gMaxIt[ii] = np.max(gAll[iii])
        self.xNorm0 = xNormAll[0][0 : self.nx]
        if self.g is not None:
            self.gOpt = np.array(self.gIt[-1])
            self.g0 = np.array(self.gIt[0])

        self.fNablaIt = np.array(self.fNablaIt) * self.fMinMax
        self.fNormNablaIt = copy.deepcopy(self.fNablaIt)
        self.fNablaOpt = copy.deepcopy(self.fNablaIt[-1])
        self.fNormNablaOpt = copy.deepcopy(self.fNablaIt[-1])

        if self.fNorm[0]:
            if self.f0 == 0:
                self.fNablaIt = self.fNablaIt / self.fNormMultiplier
                self.fNablaOpt = self.fNablaOpt / self.fNormMultiplier
            else:
                self.fNablaIt = (
                    self.fNablaIt / self.fNormMultiplier * abs(self.f0)
                )
                self.fNablaOpt = (
                    self.fNablaOpt / self.fNormMultiplier * abs(self.f0)
                )
        self.gNablaOpt = np.array(self.gNablaIt[-1]).reshape(self.ng, self.nx)
    self.xAll = xAll
    self.xNormAll = xNormAll * self.fMinMax
    self.fAll = fAll * self.fMinMax
    self.gAll = gAll
    if self.g is not None:
        self.gMax = np.max(self.gAll, 1)
