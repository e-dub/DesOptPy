# -*- coding: utf-8 -*-
"""
Title:              RangeConstraint.py
Units:              -
Author:             E.J. Wehrle, V. Gufler
Date:               September 21, 2018
-------------------------------------------------------------------------------
Description:
A function for band constraints, as in the constraining of
resonance frequency bands.
-------------------------------------------------------------------------------
Future work:
TODO Add sensitivities of ballistic constraint function
TODO Add plotting capability of constraint functions

Warnings:
RangeConstraint.py:94: RuntimeWarning: overflow encountered in exp
  np.exp(c*(omega[jj]+d-omegaBands[ii][0])))

RangeConstraint.py:116: RuntimeWarning: overflow encountered in exp
  dgdx[ig, :] = c/a*domegadx[jj]*(1-np.exp(c*(omega[jj]+d -
-------------------------------------------------------------------------------
"""
import numpy as np
from scipy.special import lambertw


def BandConParabolicFn(omega, omegaBands, c=2e-5, norm=False):
    g = np.zeros((np.shape(omegaBands)[0] * np.size(omega)))
    ig = 0
    if np.size(omega) == 1:
        omega = [omega]
    for jj in range(np.size(omega)):
        for ii in range(np.shape(omegaBands)[0]):
            if norm:
                g[ig] = (
                    c
                    * (omega[jj] / omegaBands[ii][0] - 1)
                    * (1 - omega[jj] / omegaBands[ii][1])
                )
            else:
                g[ig] = (
                    c
                    * (omegaBands[ii][0] - omega[jj])
                    * (omega[jj] - omegaBands[ii][1])
                )
            ig += 1
    return g


def ConSens(omega, domegadx, omegaL, omegaU, c):
    return (
        -c * omegaU * (-1 + omega / omegaL) * domegadx / omega ** 2
        + c * (omegaU / omega - 1) * domegadx / omegaL
    )


def BandConParabolicSensFn(omega, domegadx, omegaBands, c=2e-5, norm=False):
    dgdx = np.zeros(np.size(omega) * np.shape(omegaBands)[0])
    ig = 0
    for jj in range(np.size(omega)):
        for ii in range(np.shape(omegaBands)[0]):
            if norm:
                dgdx[ig] = ConSens(
                    omega[jj],
                    domegadx[jj],
                    omegaBands[ii, 0],
                    omegaBands[ii, 0],
                    (omegaBands[ii, 1] + omegaBands[ii, 0]) / 2.0,
                )
            else:
                dgdx[ig] = (
                    c * omegaBands[ii][0] * domegadx[ii]
                    + c * omegaBands[ii][1] * domegadx[ii]
                    + c * 2 * omega[ii] * domegadx[ii]
                )
            ig += 1
    return dgdx


def BandConSawToothFn(omega, omegaBands, norm=True, c=[]):
    g = np.zeros((np.shape(omegaBands)[0] * np.size(omega)))
    ig = 0
    if np.size(omega) == 1:
        omega = [omega]
    for jj in range(np.size(omega)):
        for ii in range(np.shape(omegaBands)[0]):
            if norm:
                if omega[jj] < omegaBands[ii][1]:
                    g[ig] = (
                        (omega[jj] / omegaBands[ii][0] - 1)
                        * omegaBands[ii][0]
                        / (omegaBands[ii][1] - omegaBands[ii][0])
                    )
                else:
                    g[ig] = (
                        (1 - omega[jj] / omegaBands[ii][1])
                        * omegaBands[ii][0]
                        / (omegaBands[ii][1] - omegaBands[ii][0])
                    )
            else:
                if omega[jj] < omegaBands[ii][1]:
                    g[ig] = omega[jj] - omegaBands[ii][0]
                else:
                    g[ig] = omegaBands[ii][1] - omega[jj]
            ig += 1
    return g


def BandConBallisticFn(
    omega, omegaBands, a=1e-8, b=0, norm=True, infFilter=False
):
    g = np.zeros((np.shape(omegaBands)[0] * np.size(omega)))
    ig = 0
    if np.size(omega) == 1:
        omega = [omega]
    for jj in range(np.size(omega)):
        for ii in range(np.shape(omegaBands)[0]):
            c = (
                (-1 - 2 * b)
                / (omegaBands[ii][1] - omegaBands[ii][0])
                * (
                    lambertw(-1 / np.exp(1 + a), -1)
                    - lambertw(-1 / np.exp(1 + a), 0)
                ).real
            )
            d = 1 / c * (-lambertw(-1 / np.exp(1 + a), b) - (1 + a)).real
            if norm:
                g[ig] = (
                    1
                    / a
                    * (
                        (1 + a)
                        + c * (omega[jj] + d - omegaBands[ii][0])
                        - np.exp(c * (omega[jj] + d - omegaBands[ii][0]))
                    )
                )
            else:
                g[ig] = (
                    (1 + a)
                    + c * (omega[jj] + d - omegaBands[ii][0])
                    - np.exp(c * (omega[jj] + d - omegaBands[ii][0]))
                )
            ig += 1
            if infFilter:
                g[g < -infFilter] = -infFilter
    return g


def BandConBallisticSensFn(
    omega, domegadx, omegaBands, a=1e-8, b=0, norm=True, infFilter=False
):

    dgdx = np.zeros(
        [np.size(omega) * np.shape(omegaBands)[0], np.shape(domegadx)[1]]
    )

    ig = 0
    for jj in range(np.size(omega)):
        for ii in range(np.shape(omegaBands)[0]):
            c = (
                (-1 - 2 * b)
                / (omegaBands[ii][1] - omegaBands[ii][0])
                * (
                    lambertw(-1 / np.exp(1 + a), -1)
                    - lambertw(-1 / np.exp(1 + a), 0)
                ).real
            )
            d = 1 / c * (-lambertw(-1 / np.exp(1 + a), b) - (1 + a)).real
            if norm:
                dgdx[ig, :] = (
                    c
                    / a
                    * domegadx[jj]
                    * (1 - np.exp(c * (omega[jj] + d - omegaBands[ii][0])))
                )
            else:
                dgdx[ig, :] = (
                    c
                    * domegadx[jj]
                    * (1 - np.exp(c * (omega[jj] + d - omegaBands[ii][0])))
                )
            ig += 1
    if infFilter:
        dgdx = np.clip(dgdx, -infFilter, infFilter)
    return dgdx
