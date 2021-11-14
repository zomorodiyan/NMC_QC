import numpy as np
from math import ceil
import matplotlib.pyplot as plt

class Bloch:
    def __init__(self,feature=None,pauli=None,density=None,clas=None):
        self.feature = feature
        self.pauli = pauli          #pauli components
        self.density = None         #density matrix
        self.clas = clas

        if self.feature is None: self.featureready = False
        else:
            self.featureready = True
            for f in self.feature:
                if type(f) not in [int, float, np.int64, np.float64]:
                    raise TypeError("features must be real numbers")


        if pauli is None: self.pauliready = False
        else:
            self.pauliready = True
            if self.pauli[-1] == 1:
                raise ValueError('last pauli components cannot be 1')
            radius = sum(p**2 for p in self.pauli)
            if radius >= 1:
                raise ValueError('pauli components must be normalized while'
                    +'radius='+str(radius))

        #evalue self.dim (which stands for features dimension)
        if self.featureready: self.dim = len(self.feature)
        elif self.pauliready: self.dim = ceil(len(self.pauli)**0.5)
        else: self.dim = None

    def pauli_matrix(self,n):
        raise NotImplementedError('nope')

    def evalpauli(self):
        if not self.featureready:
            raise ValueError('feature is required but is None')

        denom = sum(f**2 for f in self.feature) + 1
        pauli = []
        for f in self.feature:
            pauli.append(2*f/denom)
        pauli.append((denom-2)/denom)
        self.pauli = pauli
        '''
        x = self.feature[0]
        y = self.feature[1]
        self.pauli =[2*x/(x**2+y**2+1), 2*y/(x**2+y**2+1),\
                (x**2+y**2-1)/(x**2+y**2+1)]
        '''

    def evaldensity(self):
        if not self.pauliready:
            evalpauli(self)
        raise NotImplementedError('nope')

    def distance(self,bloch2): #done?
        if not self.featureready or not bloch2.featureready:
            raise ValueError('both features must be ready. self.featureready:'\
                +str(self.featureready)+' bloch2.featureready:'\
                +str(bloch2.featureready))
        if self.dim is not bloch2.dim:
            raise ValueError('bloch1.dim: ('+str(self.dim)+')'
                +' is not equal to bloch2.dim: ('+str(bloch2.dim)+')')
        sum = 0
        for i in range(self.dim):
            sum+=(self.feature[i]-bloch2.feature[i])**2
        return sum**0.5
