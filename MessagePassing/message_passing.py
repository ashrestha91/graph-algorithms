"""
Abhinav Shrestha

Message Passing algorithm for binary images (i.e. n x n matrices over F_2)
Uses "loopy" belief propagation.

Inputs:
./message_passing filename theta numberOfPasses

filename: text file consisting of n x n space delimited matrix of 0's and 1's
          up to the user to make sure the file is formatted correctly

theta determines the effect each step of message passing has.

Output:
prints to command line the matrix of the expected output
"""

import sys
from operator import mul
from functools import wraps
from numpy import *
from numpy.linalg import norm
from random import random

def memo(func):
    cache = {}
    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap

#multiplies list together
def prod(lst):
    return reduce(mul, lst, 1)

#reads file, and turns it into an array
#requires file is a space-delimited n x n block of integers
# (0 or 1 for the rest of the code as written)
def parse_file(filename):
    f = open(filename, 'r')
    image = []
    for ln in f.readlines():
        row = ln.split()
        image.append(map(int,row))
    f.close()
    return array(image)

#class representing image
class image(object):
    def __init__(self, arr, theta):
        self.theta = theta
        self.observed = arr
        self.size = len(self.observed[0])

    @classmethod
    def fromFile(cls, filename, theta):
        return cls(parse_file(filename),theta)
    
    #create a copy of img, but with random noise
    #return copy
    @classmethod
    def noisy_copy(cls,img, thresh):
        def make_noise(arr):
            new = copy(arr)
            for i in range(len(arr)):
                for j in range(len(arr)):
                    if(random() < thresh):
                        new[i,j] = 1-new[i,j] #randomly flip bits
            return new
        return cls(make_noise(img.observed),img.theta)

    def get_size(self):
        return self.size

    def get_neighbors(self,i,j):
        n = self.get_size()
        return [ (i + di, j + dj) for (di,dj) in [(0,1), (0,-1), (1,0), (-1,0), (0,0)]
                             if (0 <= i + di < n) and (0 <= j + dj < n)  ]
    def get_observed(self,i,j):
        return self.observed[i][j]
 
    def phi(self,x,y):
        if x == y:
            return 1 + self.theta
        else:
            return 1 - self.theta
#unnormalized probability that (i1,j1) sends message x_ij_prime to (i2,j2) at time 'time'
@memo
def message_unnorm(time,i1,j1,i2,j2,x_ij_prime,img):
    if (i1==i2 and j1==j2):
        return img.phi(img.get_observed(i1,j1),x_ij_prime)
    elif time == 1:
        return float(1)
    #neighbors other than source of this message
    other_ne = img.get_neighbors(i1,j1)
    other_ne.remove((i2,j2))

    #the usual product sum of the messages sent to (i1,j1) at time-1
    val =  sum( [ img.phi(x_ij, x_ij_prime) * 
                          prod([ message_norm(time-1, wx, wy, i1, j1, x_ij, img)
                                         for (wx,wy) in other_ne ]) 
                      for x_ij in [0,1] ] )
    return val

#normalizes message to be a probability
@memo
def message_norm(time,i1,j1,i2,j2,x_ij_prime,img):
    unnormed = (lambda k: message_unnorm(time,i1,j1,i2,j2,k,img))
    return float(unnormed(x_ij_prime)) / (unnormed(0) + unnormed(1))

#probability (i2,j2) has value x_ij_prime after t steps
#not normalized, so doesn't fit usual rules of a probability value
def prob(i2,j2,x_ij_prime,t,img):
    ne = img.get_neighbors(i2,j2)
    return prod([ message_norm(t,i,j,i2,j2,x_ij_prime,img) for (i,j) in ne ])

#run the message passing algorithm on the observed image img, with k passes
#choose the bit with higher probability
#returns just the matrix of bits representing the image
def compute_model(img,k):
    result = zeros((img.get_size(), img.get_size()))
    for i in range(0,img.get_size()):
        for j in range(0,img.get_size()):
            fn = lambda n: prob(i,j,n,k,img)
            _,val = max( (fn(0),0),(fn(1),1))
            result[i,j] = val
    return result

def main():
    img = image.fromFile(sys.argv[1],float(sys.argv[2]))
    print compute_model(img, int(sys.argv[3]) )
    
def test():
    original_img = image.fromFile(sys.argv[1],float(sys.argv[2]))
    threshold = float(sys.argv[4])

    def run():
        disturbed_img = image.noisy_copy(original_img, threshold)  
        model = compute_model(disturbed_img)
        diff = model - original_img.observed
        return count_nonzero(diff)
    
    print average [ run() for i in xrange(5) ]

if __name__ == "__main__":
    main()
