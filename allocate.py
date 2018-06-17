import numpy as np
import sys
from munkres import Munkres, make_cost_matrix, print_matrix
import channel

def cellAllocate(Nc, Nrb, Pc, bw, N0, msCh, preAv):
    assignment = [[] for x in range(Nc)]
    assignmentRB = [-1 for x in range(Nrb)]
    assigned = []
    currentRates = np.asarray([0 for x in range(Nc)])
    currentRatesRB = []

    lambdas = []
    rates = []
    for ms,R in zip(msCh, preAv):
        rates.append(channel.chGainsToRates(ms, Pc, bw, N0))
        lambdas.append(channel.chGainsToRates(ms, Pc, bw, N0) / R)
    lambdast = lambdas
    lambdas = np.transpose(lambdas)

    # for each RB that is
    for i in range(len(lambdas)):
        sortedLambdas = np.argsort(lambdas[i])
        toAssign = len(sortedLambdas) - 1
        while(sortedLambdas[toAssign] in assigned):
            toAssign -= 1
        if(len(assignment[sortedLambdas[toAssign]]) == 0):
            if(i > 0):
                assigned.append(assignmentRB[i - 1])
        assignment[sortedLambdas[toAssign]].append(i)
        assignmentRB[i] = sortedLambdas[toAssign]
        currentRatesRB.append(rates[sortedLambdas[toAssign]][i])
    for i in range(Nc):
        for y in assignment[i]:
            currentRates[i] += rates[i][y]
        if(len(assignment[i]) == 0):
            currentRates[i] = 1
    gcBs = [msCh[assignmentRB[i]][i] for i in range(len(assignmentRB))]
    return assignment, assignmentRB, gcBs, currentRates, currentRatesRB

def d2dAllocate(lambda_matrix,maximum_rb_allowed):
    #if multiple resource blocks are allowed for d2d users then repeat the rows
    if(not(maximum_rb_allowed==1)):
        lambda_matrix_new = []
        for i in range(0,len(lambda_matrix)):
            for j in range(0,maximum_rb_allowed):
                lambda_matrix_new.append(lambda_matrix[i])
        lambda_matrix = lambda_matrix_new

    #convert profit matrix to cost matrix
    cost_matrix = make_cost_matrix(lambda_matrix, lambda cost: sys.maxsize - cost)

    m = Munkres()
    indexes = m.compute(cost_matrix) #indexes contains the 2d indexes of the maximum weight allocations

    allocated_d2d_in_channels = np.zeros(len(lambda_matrix[0]))-1

    d2d_and_indexes = [] #indexes to return

    for row, column in indexes:
        allocated_d2d_in_channels[column] = int(row/maximum_rb_allowed)

    allocated_d2d_in_channels = allocated_d2d_in_channels.astype(int)

    for i in range(0,len(allocated_d2d_in_channels)):
        if(not(allocated_d2d_in_channels[i]==-1)):
            d2d_and_indexes.append([allocated_d2d_in_channels[i],[allocated_d2d_in_channels[i],i]])

    return d2d_and_indexes
