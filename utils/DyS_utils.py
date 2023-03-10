import pandas as pd
import numpy as np
from math import sqrt,log
import math

class Distances(object):
    
    def __init__(self,P,Q):
        if sum(P)<1e-20 or sum(Q)<1e-20:
            raise "One or both vector are zero (empty)..."
        if len(P)!=len(Q):
            raise "Arrays need to be of equal sizes..."
        #use numpy arrays for efficient coding
        P=np.array(P,dtype=float);Q=np.array(Q,dtype=float)
        #Correct for zero values
        P[np.where(P<1e-20)]=1e-20
        Q[np.where(Q<1e-20)]=1e-20
        self.P=P
        self.Q=Q
        
    def sqEuclidean(self):
        P=self.P; Q=self.Q; d=len(P)
        return sum((P-Q)**2)
    
    def probsymm(self):
        P=self.P; Q=self.Q; d=len(P)
        return 2*sum((P-Q)**2/(P+Q))
    
    def topsoe(self):
        P=self.P; Q=self.Q
        return sum(P*np.log(2*P/(P+Q))+Q*np.log(2*Q/(P+Q)))
    def hellinger(self):
        P=self.P; Q=self.Q
        return 2 * np.sqrt(1 - sum(np.sqrt(P * Q)))


def DyS_distance(sc_1, sc_2, measure):
    """This function applies a selected distance metric"""
    
    dist = Distances(sc_1, sc_2)
    
    if measure == 'topsoe':
        return dist.topsoe()
    if measure == 'probsymm':
        return dist.probsymm()
    if measure == 'hellinger':
        return dist.hellinger()
    return 100


def TernarySearch(left, right, f, eps=1e-4):
    """This function applies Ternary search"""

    while True:
        if abs(left - right) < eps:
            return(left + right) / 2
    
        leftThird  = left + (right - left) / 3
        rightThird = right - (right - left) / 3
    
        if f(leftThird) > f(rightThird):
            left = leftThird
        else:
            right = rightThird 


def getHist(scores, nbins):
    """This function recieves the scores and number of bins to make the histogram distribution
    
    Parameters
    ----------
    scores: array
        A numeric vector of scores estimated from the validation set using 10-fold cross-validation.
    nbins : integer
        The number of bins for histogram distribution   
    
    Returns
    -------
    array
        number of instances in each bin. 
    """

    breaks = np.linspace(0, 1, int(nbins)+1)
    breaks = np.delete(breaks, -1)
    breaks = np.append(breaks,1.1)
    
    re = np.repeat(1/(len(breaks)-1), (len(breaks)-1))  
    for i in range(1,len(breaks)):
        re[i-1] = (re[i-1] + len(np.where((scores >= breaks[i-1]) & (scores < breaks[i]))[0]) ) / (len(scores)+ 1)

    return re
