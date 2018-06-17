#
#   EE 764
#   Wireless & Mobile Communication
#   Course Project
#
#   Variation of Throughput With Distance Between D2D Users
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

brush = cs.draw(0.1)
g = cs.geom(Rc)

cellUsers = [g.getRandomPointInHex() for i in range(Nc)]

dmin = 20
dmax = 110
step = 10
distanceVariation = range(20, 110, 10)

rateVariationCell = []
rateVariationD2d = []
rateVariationBoth = []
print("\n Variation of Throughput With Distance Between D2D Users\n")
for d2dDistance in distanceVariation:
    sys.stdout.write("\r")
    progress = int(100 * ((d2dDistance - dmin) / (dmax - dmin - step)))
    percent = "{:2}".format(progress)
    sys.stdout.write(" " + percent + " % ")
    [sys.stdout.write("##") for x in range(int(d2dDistance / step))]
    sys.stdout.flush()
    throughputCell, throughPutD2d = core.core(Rc, Pc, bw, N0, tSNR, cellUsers,
                                            Nc, Nd, Nrb, d2dDistance,
                                            rbPerD2DPair, RWindowSize, 200, False)
    rateVariationCell.append(throughputCell)
    rateVariationD2d.append(throughPutD2d)
    rateVariationBoth.append(throughputCell + throughPutD2d)
print("")
pl.figure(2)
pl.plot(distanceVariation, np.asarray(rateVariationCell) / 1e6, label="Cell Users")
pl.scatter(distanceVariation, np.asarray(rateVariationCell) / 1e6, marker=">")
pl.plot(distanceVariation, np.asarray(rateVariationD2d) / 1e6, label="D2D Pairs")
pl.scatter(distanceVariation, np.asarray(rateVariationD2d) / 1e6, marker=">")
pl.plot(distanceVariation, np.asarray(rateVariationBoth) / 1e6, label="Both")
pl.scatter(distanceVariation, np.asarray(rateVariationBoth) / 1e6, marker=">")
pl.xlabel("Distance between D2D Users in a Pair (m)")
pl.ylabel("Throughput (Mbits/sec)")
pl.legend(loc="upper left")
pl.grid(True)
pl.show()
