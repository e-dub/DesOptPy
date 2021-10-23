# -*- coding: utf-8 -*-
"""
Risk minimizing portfolio of assets with a minimum expected return

Values from
http://www.aaii.com/computerizedinvesting/article/mean-variance-optimization-multi-asset-portfolio

only long investments are allowed, no short positions in portfolio !

x* = [0 16.97% 0 0 59.67% 0 0 0 23.35% 0]

fOpt = 14.12%
"""
from DesOptPy import OptimizationProblem
import numpy as np


class Portfolio:
    x = np.zeros(
        [
            2,
        ]
    )

    def SysEq(self):
        mu = np.array(
            (
                41.700,
                20.200,
                19.363,
                45.675,
                17.213,
                33.261,
                10.450,
                19.738,
                9.538,
                60.400,
            )
        )  # average annual return
        # Covariance matrix of assets
        cov = np.matrix(
            (
                (
                    +0.37340700,
                    +0.19057388,
                    +0.14689325,
                    +0.41982713,
                    +0.00867937,
                    +0.46603426,
                    +0.12178250,
                    +0.17739575,
                    +0.09241813,
                    +0.42177650,
                ),
                (
                    +0.19057388,
                    +0.13926950,
                    +0.08995750,
                    +0.27529150,
                    -0.03473650,
                    +0.28961528,
                    +0.08277038,
                    +0.11445100,
                    +0.07290163,
                    +0.33922238,
                ),
                (
                    +0.14689325,
                    +0.08995750,
                    +0.10892573,
                    +0.18899141,
                    +0.00339655,
                    +0.16153702,
                    +0.08957031,
                    +0.14708452,
                    +0.08477552,
                    +0.19014650,
                ),
                (
                    +0.41982713,
                    +0.27529150,
                    +0.18899141,
                    +0.61972394,
                    -0.01809584,
                    +0.58497157,
                    +0.18254475,
                    +0.21086884,
                    +0.09987322,
                    +0.70169938,
                ),
                (
                    +0.00867937,
                    -0.03473650,
                    +0.00339655,
                    -0.01809584,
                    +0.05635436,
                    -0.06528978,
                    +0.00152419,
                    -0.00928305,
                    -0.03337667,
                    -0.10421450,
                ),
                (
                    +0.46603426,
                    +0.28961528,
                    +0.16153702,
                    +0.58497157,
                    -0.06528978,
                    +0.87448850,
                    +0.21600599,
                    +0.21595218,
                    +0.14115362,
                    +0.84694548,
                ),
                (
                    +0.12178250,
                    +0.08277038,
                    +0.08957031,
                    +0.18254475,
                    +0.00152419,
                    +0.21600599,
                    +0.12118450,
                    +0.12938956,
                    +0.06172319,
                    +0.22639375,
                ),
                (
                    +0.17739575,
                    +0.11445100,
                    +0.14708452,
                    +0.21086884,
                    -0.00928305,
                    +0.21595218,
                    +0.12938956,
                    +0.22376523,
                    +0.12879623,
                    +0.21466350,
                ),
                (
                    +0.09241813,
                    +0.07290163,
                    +0.08477552,
                    +0.09987322,
                    -0.03337667,
                    +0.14115362,
                    +0.06172319,
                    +0.12879623,
                    +0.11767298,
                    +0.16805188,
                ),
                (
                    +0.42177650,
                    +0.33922238,
                    +0.19014650,
                    +0.70169938,
                    -0.10421450,
                    +0.84694548,
                    +0.22639375,
                    +0.21466350,
                    +0.16805188,
                    +1.09122450,
                ),
            )
        )
        # portfolio standard deviation == risk
        self.totalVar = np.sqrt(
            np.mat(self.x) * cov * np.transpose(np.mat(self.x))
        )[0, 0]
        # just to know the expected return of the minimum risk portfolio,
        # could be used as objective or as multiple objective
        expected_return = np.dot(self.x, mu)
        # fraction of investments has to sum up to 1,
        # could also be handled as an equality constraint instead of two inequality constraints
        self.g1 = np.sum(self.x) - 1.0
        self.g2 = -np.sum(self.x) + 1.0


OptPortfolio = OptimizationProblem(Portfolio)
OptPortfolio.Primal = 'SysEq'
OptPortfolio.x = 'x'
OptPortfolio.x0 = (
    np.ones(10) * 0.1
)  # start with an equally distributed portfolio
OptPortfolio.xL = np.zeros(
    10
)  # minimum share of asset in portfolio is 0%, all zero
OptPortfolio.xU = np.ones(10)  # max share of asset in portfolio is 100%
OptPortfolio.f = 'totalVar'
OptPortfolio.g = ['g1', 'g2']
OptPortfolio.gLimit = [0, 0]
OptPortfolio.Alg = 'NLPQLP'
OptPortfolio.optimize()
OptPortfolio.plotConvergence()
OptPortfolio.plotBeforeAfter()
