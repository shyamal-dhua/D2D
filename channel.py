import numpy as np
import random

# contact Shyamal
def getGcbMatrix(Nc, ms, number_of_channels):
    g1 = np.random.rayleigh(1, [Nc, number_of_channels])
    g_CB = np.zeros([Nc, number_of_channels])
    d_CB = []      # Distance of CU from Base station
    for i in range(0, Nc):
        a = ms[i]
        d_CB.append(np.sqrt(a[0]**2 + a[1]**2) / 1000)
    pL_1 = 128.1 + 37.6 * np.log10(d_CB)   # Path loss in dB
    pl_1 = 10**(pL_1 / 10)   # Path loss in linear scale
    for i in range(Nc):
        g_CB[i] = (g1[i]**2) / pl_1[i]
    return g_CB

# contact Ritesh
def chGainsToRates(gains, Pc, bw, sigmaNsq):
    rates = []
    for gain in gains:
        snr = (Pc * gain) / sigmaNsq
        rate = bw * np.log2(1 + snr)
        rates.append(rate)
    return rates

# contact Shyamal
def chGains(Nd, number_of_channels, cellUsers, allocated_cell_users, d2d_tx, d2d_rx, Pc, d_dTdR):
    P=Pc         # tx power from CU
    d_dTB=[]     # distance of D2D Transmitter from Base station (1xNd)
    #d_dTdR=0.01  # distance between D2D Tx and D2D Rx
    d_CdR=[]     # distance between cell user and d2d receiver

    g_d2b = np.random.rayleigh(1,[Nd,number_of_channels])   # D2D Tx to BS rayleigh fading
    g_dTB = np.zeros([Nd,number_of_channels])

    g_d2dR = np.random.rayleigh(1,[1,number_of_channels])   # D2D Tx and D2D Rx rayleigh fading
    g_dTdR = np.zeros([1,number_of_channels])

    g_cdR = np.random.rayleigh(1,[Nd,number_of_channels])   # cell user to d2d receiver rayleigh fading
    g_CdR = np.zeros([Nd,number_of_channels])

    for i in range(0,len(d2d_tx)):
        distance = np.sqrt((d2d_tx[i][0]**2) + (d2d_tx[i][1]**2))
        distance = distance / 1000
        d_dTB.append(distance)

    for i in range(0,len(d2d_rx)):
        dist = []
        for j in range(0,len(allocated_cell_users)):
            cell_x = cellUsers[allocated_cell_users[j]][0]
            cell_y = cellUsers[allocated_cell_users[j]][1]
            d2d_x = d2d_rx[i][0]
            d2d_y = d2d_rx[i][1]
            distance =np.sqrt(((cell_x-d2d_x)**2) + ((cell_y-d2d_y)**2))
            distance=distance/1000
            dist.append(distance)
        d_CdR.append(dist)

    pL_dTB = 128.1 + 37.6*np.log10(d_dTB)  # d_dTB=distance in kms
    pL_dTdR = 128.1 + 37.6*np.log10(d_dTdR / 1000)

    pL_CdR = np.zeros([Nd,number_of_channels])
    pl_CdR = np.zeros([Nd,number_of_channels])
    for i in range(0,Nd):
        pL_CdR[i] = 128.1 + 37.6*np.log10(d_CdR[i])
    for i in range(0,Nd):
        pl_CdR[i] = 10**(pL_CdR[i]/10)


    pl_dTB = 10**(pL_dTB/10)   # Path loss in linear scale (1xNd)
    pl_dTdR = 10**(pL_dTdR/10) #(1x1 -> scalar)

    for i in range(0,Nd):
        g_dTB[i] = (g_d2b[i]**2)/(pl_dTB[i])    # Channel Gains : from D2D Tx to BS (Ndxnumber_of_channels)

    g_dTdR = ((g_d2dR**2)/pl_dTdR)    # Channel Gains : from D2D Tx to D2D Rx (1xnumber_of_channels)

    for i in range(0,Nd):
        g_CdR[i] = (g_cdR[i]**2)/(pl_CdR[i])    # Channel Gains : from CU to D2D Rx (Ndxnumber_of_channels)

    g_dTB_list = []
    g_dTdR_list = g_dTdR.tolist()
    g_CdR_list = []

    for i in range(0,Nd):
        g_dTB_list.append(list(g_dTB[i]))
        g_CdR_list.append(list(g_CdR[i]))

    return np.asarray(g_dTB_list),np.asarray(g_dTdR_list[0]),np.asarray(g_CdR_list)
