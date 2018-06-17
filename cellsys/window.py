#
#   EE 764
#   Wireless & Mobile Communication
#   Simulation Assignment 1
#
#   Hexagonal geometry functions
#
#   Author: Ritesh
#   RollNo: 163079001
#
# # # # # # # # # # # # # # # # # # # # #

import numpy as np
import math
import random

class meanwindow(object):
    def __init__(self, values, wSize):
        self.values = [[values[i] for x in range(wSize)] for i in range(len(values))]

    # Checks if point p(i, j) is a reuse cell or not
    # for reuse factor 3
    def update(self, newValues):
        [x.pop(0) for x in self.values]
        [x.append(newValue) for x,newValue in zip(self.values, newValues)]
        return [np.mean(x) for x in self.values]
    def get(self):
        return [np.mean(x) for x in self.values]
