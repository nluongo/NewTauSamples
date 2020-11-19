def bigCluster(myTOB):
    allCells = createBigCellLists(myTOB) #same as createCellList but EM1 and EM2 are now 6 length arrays with the energy of 4+5, 6+7, 8+9, 10+11, 12+13, 14+15

    #for phi=1 I'll add up the energy of the 2 main big cells (8,9,10,11 in fine gran), then also that window shifted to one side (6,7,8,9) and to the other ((10,11,12,13)
    midPhiEM1 = [allCells[1][7]+allCells[1][8],allCells[1][8]+allCells[1][9],allCells[1][9]+allCells[1][10]]
    midPhiEM2 = [allCells[2][7]+allCells[2][8],allCells[2][8]+allCells[2][9],allCells[2][9]+allCells[2][10]]

    #for phi=0 and phi=1 i'll just loop over the two blocks sum energy (6,7 and 8,9 and 10,11 and 12,13)
    upPhiEM1 = [allCells[1][1],allCells[1][2],allCells[1][3],allCells[1][4]]
    lowPhiEM1 = [allCells[1][13],allCells[1][14],allCells[1][15],allCells[1][16]]
    upPhiEM2 = [allCells[2][1],allCells[2][2],allCells[2][3],allCells[2][4]]
    lowPhiEM2 = [allCells[2][13],allCells[2][14],allCells[2][15],allCells[2][16]]

    energyEM1EM2_mid    = [midPhiEM1[0]+midPhiEM2[0],midPhiEM1[1]+midPhiEM2[1],midPhiEM1[2]+midPhiEM2[2]]
    energyEM1EM2_low    = [lowPhiEM1[0]+lowPhiEM2[0],lowPhiEM1[1]+lowPhiEM2[1],lowPhiEM1[2]+lowPhiEM2[2],lowPhiEM1[3]+lowPhiEM2[3]]
    energyEM1EM2_up     = [upPhiEM1[0]+upPhiEM2[0],upPhiEM1[1]+upPhiEM2[1],upPhiEM1[2]+upPhiEM2[2],upPhiEM1[3]+upPhiEM2[3]]

    energyEM1EM2_mid   .sort(reverse = True)
    energyEM1EM2_low   .sort(reverse = True)
    energyEM1EM2_up    .sort(reverse = True)

    energyEM1EM2 = energyEM1EM2_low[0]+energyEM1EM2_mid[0]+energyEM1EM2_up[0]

    #etaMax_PS = findMax(3,myTOB)[0]
    #phiMax_PS = findMax(2,myTOB)[1]
    #E_PS  = shapeTLV_fineGran(myTOB,2,etaMax_PS,phiMax_PS)
    #etaMax_EM3 = findMax(5,myTOB)[0]
    #phiMax_EM3 = findMax(5,myTOB)[1]
    #E_EM3  = shapeTLV_fineGran(myTOB,5,etaMax_EM3,phiMax_EM3)
    #etaMax_HAD = findMax(6,myTOB)[0]
    #phiMax_HAD = findMax(6,myTOB)[1]
    #E_HAD  = shapeTLV_fineGran(myTOB,6,etaMax_HAD,phiMax_HAD)

    #allE = energyEM1EM2+E_PS+E_EM3+E_HAD
    energyPS    = allCells[0]
    energyEM3   = allCells[3]
    energyHAD   = allCells[4]

    energyPS    .sort(reverse = True)
    energyEM3   .sort(reverse = True)
    energyHAD   .sort(reverse = True)

    energyPSEM3HAD = energyPS[0]+energyPS[1]+energyPS[2]+energyEM3[0]+energyEM3[1]+energyHAD[0]+energyHAD[1]+energyHAD[2]

    E_PS=energyPS[0]+energyPS[1]+energyPS[2]
    E_EM3=energyEM3[0]+energyEM3[1]
    E_HAD=energyHAD[0]+energyHAD[1]+energyHAD[2]

    allE = energyEM1EM2+energyPSEM3HAD

    return [allE, energyEM1EM2, E_PS, E_EM3, E_HAD]
    #return allE


def createBigCellLists(myTOB):
    layerOffset = [1, 4, 4, 1, 1]
    layerCells = [i*3 for i in layerOffset]

    allCells = []

    # iterate over layer
    for l in range(5):
        myLayer = []
        # iterate over phi
        for i in range(3):
            # iterate over eta
            if l==1 or l==2:
                for j in range(0,layerCells[l],2):
                    myLayer += [myTOB.getEnergy(l+2, j+layerOffset[l], i+1)+myTOB.getEnergy(l+2, j+1+layerOffset[l], i+1)]
            else:
                for j in range(layerCells[l]):
                    myLayer += [myTOB.getEnergy(l+2, j+layerOffset[l], i+1)]
        allCells += [ myLayer ]
    return allCells
