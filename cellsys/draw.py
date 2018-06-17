#
#   EE 764
#   Wireless & Mobile Communication
#   Simulation Assignment 1
#
#   Drawing class to draw hexagons and clusters of hexagons
#
#   Author: Ritesh
#   RollNo: 163079001
#
# # # # # # # # # # # # # # # # # # # # #

import numpy as np
import pylab as pl
import math
import random
import matplotlib.patches as patches

from mpl_toolkits.mplot3d import Axes3D

from .geom import *

def ss(theta):
        return np.sin(theta)
def cc(theta):
        return np.cos(theta)

# for color adjustment
# in hex colors, this function keeps a digit from being less than 0
def keepzero(some):
    if(some < 97):
        return 97
    elif(some < 47):
        return 48
    else:
        return some

class draw(object):
    def __init__(self, radius):
        ta = np.pi / 3
        verts = [ (      1,       0),
                  ( cc(ta),  ss(ta)),
                  (-cc(ta),  ss(ta)),
                  (     -1,       0),
                  (-cc(ta), -ss(ta)),
                  ( cc(ta), -ss(ta)) ]
        self.radius = radius
        self.redge = radius * cc(np.pi / 6)
        self.basis = np.asarray([np.asarray(item) for item in verts])
        self.basisdef = self.basis
        self.basis *= radius

    def drawHex(self, ci, cj, fig, fclr):
        x = ci * np.cos(np.pi / 6)
        y = cj + (ci * np.sin(np.pi / 6))
        center = np.asarray([2 * self.redge * x, 2 * self.redge * y])
        vertices = [(center + z) for z in self.basis]
        eclr = [chr(keepzero(ord(vl) - 1)) for vl in fclr]
        eclr[0] = '#'
        axis = fig.gca()
        axis.add_patch(patches.RegularPolygon((center[0], center[1]), 6, self.radius, orientation=(np.pi/2), fc=fclr, ec=''.join(eclr)))

    def drawSquare(self, x, y, fig, fclr):
        axis = fig.gca()
        axis.add_patch(patches.RegularPolygon((x, y), 4, self.radius, orientation=(np.pi/4), fc=fclr))

    def drawHexSectored(self, ci, cj, fig, fclr):
        x = ci * np.cos(np.pi / 6)
        y = cj + (ci * np.sin(np.pi / 6))
        center = np.asarray([2 * self.redge * x, 2 * self.redge * y])
        vertices = [(center + z) for z in self.basis]
        sverts = [
            [vertices[0], vertices[1], center, vertices[5]],
            [vertices[1], vertices[2], vertices[3], center],
            [vertices[3], vertices[4], vertices[5], center]
        ]
        axis = fig.gca()
        axis.add_patch(patches.Polygon(np.asarray(vertices), fill=False, ec="#DB3236", zorder=50))
        for i in range(0, 3):
            axis.add_patch(patches.Polygon(np.asarray(sverts[i]), fc=fclr[i], ec=fclr[i]))

    def drawTiers(self, ntiers, off, fig, clr):
        hexlist = []
        #######
        x = off[0] * cc(np.pi / 6)
        y = off[1] + (off[0] * ss(np.pi / 6))
        if(off == (0, 0)):
            pl.scatter(2 * self.redge * x, 2 * self.redge * y, s=10,
                        facecolors='none', color='#FFFFFF', zorder=100)
        else:
            pl.scatter(2 * self.redge * x, 2 * self.redge * y, s=10,
                        facecolors='none', color='#00FF00', zorder=100)
        #######
        p = -1 * ntiers
        q = 0
        r = ntiers
        while(q < ntiers):
            for i in range(p, q + 1):
                if((i, r) == (0, 0)):
                    self.drawHex(i + off[0], r + off[1], fig, '#009999')
                else:
                    hexlist.append((i, r))
                    self.drawHex(i + off[0], r + off[1], fig, clr)
            r -= 1
            q += 1
        while(p <= 0):
            for i in range(p, q + 1):
                if((i, r) == (0, 0)):
                    self.drawHex(i + off[0], r + off[1], fig, '#009999')
                else:
                    hexlist.append((i, r))
                    self.drawHex(i + off[0], r + off[1], fig, clr)
            r -= 1
            p += 1
        return hexlist

    def drawTiersSectored(self, ntiers, off, fig, clr):
        ax = fig.gca()
        figsz = math.ceil((2 * (ntiers + 1)) * self.redge)
        ax.set_xlim(-figsz, figsz)
        ax.set_ylim(-figsz, figsz)
        ax.set_aspect('equal')
        geome = geom(1.0)
        # darker colors
        dclr = clr[1]
        lclr = clr[0]
        #######
        x = off[0] * cc(np.pi / 6)
        y = off[1] + (off[0] * ss(np.pi / 6))
        pl.scatter(2 * self.redge * x, 2 * self.redge * y, s=2, facecolors='none', color='#00FF00', zorder=100)
        #######
        p = -1 * ntiers
        q = 0
        r = ntiers
        while(q < ntiers):
            for i in range(p, q + 1):
                if(geome.checkReuseSectored((i, r))):
                    self.drawHexSectored(i + off[0], r + off[1], fig, dclr)
                else:
                    self.drawHexSectored(i + off[0], r + off[1], fig, lclr)
            r -= 1
            q += 1
        while(p <= 0):
            for i in range(p, q + 1):
                if(geome.checkReuseSectored((i, r))):
                    self.drawHexSectored(i + off[0], r + off[1], fig, dclr)
                else:
                    self.drawHexSectored(i + off[0], r + off[1], fig, lclr)
            r -= 1
            p += 1

    def drawTiersSectoredHet(self, ntiers, incells, off, fig, clr):
        ax = fig.gca()
        figsz = math.ceil((2 * (ntiers + 1)) * self.redge)
        ax.set_xlim(-figsz, figsz)
        ax.set_ylim(-figsz, figsz)
        ax.set_aspect('equal')
        geome = geom(1.0)
        # darker colors
        dclr = clr[1]
        lclr = clr[0]
        #######
        x = off[0] * cc(np.pi / 6)
        y = off[1] + (off[0] * ss(np.pi / 6))
        pl.scatter(2 * self.redge * x, 2 * self.redge * y, s=2, facecolors='none', color='#00FF00', zorder=100)
        #######
        p = -1 * ntiers
        q = 0
        r = ntiers
        while(q < ntiers):
            for i in range(p, q + 1):
                if((i, r) in incells):
                    if(geome.checkReuseSectored((i, r))):
                        self.drawHexSectored(i + off[0], r + off[1], fig, dclr)
                    else:
                        self.drawHexSectored(i + off[0], r + off[1], fig, lclr)
                else:
                    self.drawHex(i + off[0], r + off[1], fig, "#EEEEEE")
            r -= 1
            q += 1
        while(p <= 0):
            for i in range(p, q + 1):
                if((i, r) in incells):
                    if(geome.checkReuseSectored((i, r))):
                        self.drawHexSectored(i + off[0], r + off[1], fig, dclr)
                    else:
                        self.drawHexSectored(i + off[0], r + off[1], fig, lclr)
                else:
                    self.drawHex(i + off[0], r + off[1], fig, "#EEEEEE")
            r -= 1
            p += 1

    def drawLayout(self, ntiers, freuse, cells, fig):
        ax = fig.gca()
        figsz = math.ceil((2 * (ntiers + 1) + 1) * self.redge)
        ax.set_xlim(-figsz, figsz)
        ax.set_ylim(-figsz, figsz)
        ax.set_aspect('equal')
        ntiersToPlot = int(np.floor(np.sqrt((freuse - 1) / 3)))
        if(freuse == 3):
            ntiersToPlot = 1
        for cell in cells:
            #clr = "#%06x" % random.randint(0, 0xFFFFFF)
            clr = "#EEEEEE"
            self.drawTiers(ntiersToPlot, cell, fig, clr)
        pl.scatter(0, 0, s=10,
                    facecolors='none', color='#00FF00', zorder=0,
                    label="Interfering Base Stations")

    def drawPointsInHexagon(self, pointsList, hexCenter, hexRadius, fig):
        # Plot of random user points in the hexagon
        # need fix for hexCenter not (0, 0)
        #ax = fig.gca()
        #ax.set_xlim(-hexRadius, hexRadius)
        #ax.set_ylim(-hexRadius, hexRadius)
        #ax.set_aspect('equal')

        x = hexCenter[0] * np.cos(np.pi / 6)
        y = hexCenter[1] + (hexCenter[0] * np.sin(np.pi / 6))
        center = np.asarray([2 * self.redge * x, 2 * self.redge * y])
        pointsList = [(center + np.asarray(z)) for z in pointsList]

        xsc, ysc = zip(*pointsList)
        #self.updateRadius(hexRadius)
        #self.drawHex(0, 0, fig, "#EEEEEE")
        ax = fig.gca()
        ax.scatter(xsc, ysc, s=1.0, color='#DB3236', zorder=200, label='Users')
        ax.legend(scatterpoints=5)

    def updateRadius(self, radius):
        self.radius = radius
        self.redge = radius * cc(np.pi / 6)
        self.basis = radius * self.basisdef
