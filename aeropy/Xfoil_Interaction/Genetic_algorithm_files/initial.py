'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script requires from the main program a serie of  profile genomes.
The number of profiles is "num_pop"
This subprogram, first, uses the script "transcript.py" in order to translate
the genomes into a series of points that Xfoil can understand.

Then, sends them to Xfoil, and ask it to analize them.

At last, it sends back to the main program the results obtained. 

'''



import subprocess
import sys
import os
import interfaz as interfaz
import numpy as np
import testing as test


def start_pop(pop_num):
    
    genes = np.array([150*np.pi/180, #ang s1
                  0.2,           #dist s1
                  0.5,           #x 1
                  0.12,          #y 1
                  0,             #ang 1
                  0.2,           #dist b1
                  0.2,           #dist c1
                  0.1,           #dist a1
                  0.05,          #dist a2
                  0.4,           #x 2
                  -0.07,          #y 2
                  5*np.pi/180,   #ang 2
                  0.2,           #dist b2 
                  0.2,           #dist c2
                  270*np.pi/180, #ang s2
                  0.2])          #dist s2

#    generation = 0
#profile_number = 1
    genome = np.zeros([pop_num,16])
    
    gen_deviation = np.array([10*np.pi/180, #ang s1
                  0.15,           #dist s1
                  0.2,           #x 1
                  0.1,           #y 1
                  10*np.pi/180,  #ang 1
                  0.2,           #dist b1
                  0.2,           #dist c1
                  0.1,           #dist a1
                  0.1,          #dist a2
                  0.4,           #x 2
                  0.05,          #y 2
                  10*np.pi/180,   #ang 2
                  0.2,           #dist b2 
                  0.2,           #dist c2
                  30*np.pi/180, #ang s2
                  0.15])          #dist s2
                  
                  
    for profile in np.arange(0, pop_num, 1):
        deviation = 0.7 * np.random.randn(16) * gen_deviation
        genome[profile,:] = genes + deviation
        genome[profile, 14] = genome[profile, 0] + abs(deviation[14])
        while not(test.test_perfil(genome[profile,:])):
            deviation = 0.7 * np.random.randn(16) * gen_deviation
            genome[profile,:] = genes + deviation
            genome[profile, 14] = genome[profile, 0] + abs(deviation[14])
        
#        for gen in np.arange(0,16,1):
#            genome[profile, gen] = genome[profile, gen] * (1 + 0.1 * np.random.randn())
#    
#    genome[1,:] = genes
    
    return genome


#interfaz.xfoil_calculate_population(generation,genome)