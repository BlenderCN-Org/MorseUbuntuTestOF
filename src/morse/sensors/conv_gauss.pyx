cpdef float[:] convGauss(unsigned char[:, :] imgmat, float[:, :] gaussMat, int size):
    cdef float[2] scal=[0,0]
    #cdef int[2] tt=[0,0]
    cdef int p, x, y, pas 
    for p in range (2):
        pas = p * size / 2
        for x in range (pas,size+pas):
            for y in range (size):
                #scal[p]=p
                #print 'X:',x,' Y:',y,' P:', p
                #print 'imgmat: ', imgmat[y, x]
                #print 'gaussmat: ',x-pas, y,'  ', gaussMat[x-pas, y]
                scal[p] += imgmat[y, x] * gaussMat[x-pas, y]
    #print scal
                
        #scal[p] = tt[p]/693895
    return scal
