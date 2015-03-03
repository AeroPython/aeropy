'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script creates the initial population for the genetic algorithm.
It does so by adding a random deviation to a default profile genome.

'''




import os
import numpy as np
import testing as test


def start_pop(pop_num):
    '''Creates a randomly generated population of the size (pop_num)
    '''
    
    genome = np.zeros([pop_num,16])    
    
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
                  190*np.pi/180, #ang s2
                  0.2])          #dist s2


    
    
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
        while not(test.airfoil_test(genome[profile,:])):
            
            # Here we check tat our airfoil actually makes sense
        
            deviation = 0.7 * np.random.randn(16) * gen_deviation
            genome[profile,:] = genes + deviation
        

    
    profile_number = genome.shape[0]    
    genome_root = 'genome\generation0.txt'
    title = 'generation 0 genome'
    
    try:
        os.remove(genome_root)
    except :
        pass
    archivo = open(genome_root, mode = 'x')
    archivo.write(title + '\n')
    
    for profile in np.arange(0, profile_number, 1):
        line = ''
        for gen in np.arange(0, 16,1):
            line = line + str(genome[profile, gen]) +'    '
        line = line + '\n'
        archivo.write(line)
    
    return genome


