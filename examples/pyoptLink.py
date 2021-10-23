#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 01:12:55 2019

@author: wehrle
"""


class pyOptOptimization:

    opt_prob = Optimization('Rosenbrock Unconstraint Problem', objfunc)
    opt_prob.addVar('x1', 'c', lower=-10.0, upper=10.0, value=-3.0)
    opt_prob.addVar('x2', 'c', lower=-10.0, upper=10.0, value=-4.0)
