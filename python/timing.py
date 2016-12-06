import numpy as np
import os
import sys
from matplotlib import rc
rc('font',**{'family':'serif'})

n = 10**np.array(range(2,7))
N = len(n)

verlet_data = np.array([[0.003407,0.004464,0.004802],
                        [0.027886,0.03126,0.033924],
                        [0.235116,0.233484,0.223675],
                        [2.21688,2.21937,2.22638],
                        [22.26543,22.1216,22.0843]])
euler_data = np.array([[0.002043,0.004011,0.001375],
                       [0.01955,0.018482,0.018824],
                       [0.10053,0.104212,0.103983],
                       [0.952888,0.965634,0.94352],
                       [9.41174,9.43143,9.45151]])

verlet_mean = verlet_data.mean(axis=1)
verlet_mean = np.reshape(verlet_mean,newshape=(5,1))
verlet_variance = np.sum((verlet_data - verlet_mean)**2,axis=1)/3.0
verlet_stddev = np.sqrt(verlet_variance)

euler_mean = euler_data.mean(axis=1)
euler_mean = np.reshape(euler_mean,newshape=(5,1))
euler_variance = np.sum((euler_data - euler_mean)**2,axis=1)/3.0
euler_stddev = np.sqrt(euler_variance)

#print in a latex-friendly fashion
print "\\hline n & Euler [s] & Verlet [s] \\\\ \\hline"
for i in range(N):
    print "%1.0e & %.8f $\\pm$ %.8f & %.8f $\\pm$ %.8f \\\\ \\hline" %(n[i], euler_mean[i], euler_stddev[i], verlet_mean[i], verlet_stddev[i])

    
