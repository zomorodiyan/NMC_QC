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
            if radius > 1:
                raise ValueError('pauli components must be normalized while'
                    +'radius='+str(radius))
        #evalue self.dim (which stands for features dimension)
        if self.featureready: self.dim = len(self.feature)
        elif self.pauliready: self.dim = ceil(len(self.pauli)**0.5)
        else: self.dim = None

    def evalpauli(self):
        if not self.featureready:
            raise ValueError('feature is required but is None')
        denom = sum(f**2 for f in self.feature) + 1
        pauli = []
        for f in self.feature:
            pauli.append(2*f/denom)
        pauli.append((denom-2)/denom)
        self.pauli = pauli

    def evalfeature(self):
        if not self.pauliready:
            raise ValueError('pauli is required but is None')
        denom = 1-self.pauli[-1]
        feature = []
        for f in self.pauli[:-1]:
            feature.append(f/denom)
        self.feature = feature

    def pauli_matrix(self,n):
        if self.dim is None:
            raise ValueError('dim must be defined')
        counter = 0
        for i in range(self.dim-1):
            for j in range(i+1,self.dim):
                matrix = np.zeros((self.dim,self.dim))
                matrix[i,j]=1
                matrix[j,i]=1
                if n==counter:
                    return matrix
                counter+=1
        for i in range(self.dim-1):
            for j in range(i+1,self.dim):
                matrix = np.zeros((self.dim,self.dim),dtype=np.complex_)
                matrix[i,j]=-1j
                matrix[j,i]=1j
                if n==counter:
                    return matrix
                counter+=1
        matrix = np.zeros((self.dim,self.dim),dtype=np.complex_)
        for i in range(0,self.dim-1):
            for j in range(i+1):
                matrix[j,j]=1*(2/(i+1)/(i+2))**0.5
            matrix[i+1,i+1]=-1*(i+1)*(2/(i+1)/(i+2))**0.5
            if n==counter:
                return matrix
            counter+=1
        raise ValueError('n should be a non-negative int smaller than dim^2-1')




    def evaldensity(self):
        if not self.pauliready:
            evalpauli(self)
        raise NotImplementedError('nope')

    def distance(self,bloch2):
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
