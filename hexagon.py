#
#   EE 764
#   Wireless & Mobile Communication
#   Course Project
#
#   Plot of a Hexagonal Cell With Users 
#
#   Authors: Pratik, Ritesh, Shyamal
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# created by us
import cellsys as cs
import core

import numpy as np
import pylab as pl
import sys
import json

with open('config.json', 'r') as f:
    config = json.load(f)

# radius of hexagon
Rc = config["Rc"]
ntiers = config["ntiers"]

# Tx power from CU
Pc = config["Pc"]

# Bandwidth (180 khz without guard band)
bw = config["bw"]

#  Noise PSD in dBm
N_dBm = config["N_dBm"]
N0 = (10**(N_dBm / 10)) * 10**(-3)
N0 = N0 * bw

# Target SNR at BS from CU (dB)
tSNR_dB = config["tSNR_dB"]
tSNR = 10**(tSNR_dB / 10)

# no. of cell users
Nc = config["Nc"]

# no of D2D pairs
Nd = config["Nd"]

# no. of resource blocks
Nrb = config["Nrb"]

# max window
RWindowSize = config["RWindowSize"]

# D2D distance
d2dDistance = config["d2dDistance"]

# Rb per D2D pair
rbPerD2DPair = config["rbPerD2DPair"]

brush = cs.draw(Rc)
g = cs.geom(Rc)

cellUsers = [g.getRandomPointInHex() for i in range(Nc)]

fig1 = pl.figure(1)
pl.scatter(0, 0, color="#777777", zorder=1000, s=24, facecolors='#DDDDDD', label="eNB (Base Station)")
for i in range(len(cellUsers) - 1):
    pl.scatter(cellUsers[i][0], cellUsers[i][1], color="#32DB36", zorder=1000, s=6)
pl.scatter(cellUsers[len(cellUsers) - 1][0], cellUsers[len(cellUsers) - 1][1],
            color="#32DB36", zorder=1000, s=6, label="Cell Users")

d2d_tx = []
d2d_rx = []
plotted = 0
for i in range(0, Nd):
    t,r = g.getD2DInHex(d2dDistance)
    d2d_tx.append(t)
    d2d_rx.append(r)

    if(plotted == 0):
        pl.scatter(t[0], t[1], color="#DB3236", zorder=1000, s=8, label="D2D Transmitter")
        pl.scatter(r[0], r[1], color="#2E58D5", zorder=1000, s=8, label="D2D Receiver")
        line = g.lineFromPoints(t, r, 100)
        xx, yy = zip(*line)
        pl.plot(xx, yy, color="#888888", zorder = 999, linewidth=1)
        plotted = 1
    else:
        pl.scatter(t[0], t[1], color="#DB3236", zorder=1000, s=8)
        pl.scatter(r[0], r[1], color="#2E58D5", zorder=1000, s=8)
        line = g.lineFromPoints(t, r, 100)
        xx, yy = zip(*line)
        pl.plot(xx, yy, color="#888888", zorder = 999, linewidth=1)

brush.drawHex(0, 0, fig1, "#EEEEEE")
#brush.drawTiers(0, (0, 0), fig1, "#EEEEEE")
ax = fig1.gca()
ax.set_xlim(-Rc, Rc)
ax.set_ylim(-Rc, Rc)
ax.set_aspect('equal')

pl.xlabel("distance (m)")
pl.ylabel("distance (m)")
pl.legend(loc="upper right")

pl.show()
