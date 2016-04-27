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
import algoritmo.testing as test
import shutil


class Airfoil(object):
    '''This object represents a single airfoil'''
    results_root = ''
    
    def __init__(self, genome):
        self.genome = genome
    def copy_data(self, gen, num):
        airfoil_name = 'gen' + str(gen) + 'airf' + str(num)
        new_root = os.path.join("aerodata","data" + airfoil_name + '.txt')
        shutil.copy(self.results_root, new_root)
        self.results_root = new_root
        self.name = airfoil_name
    def copy_winner(self, num):
        new_root = os.path.join("results","data", 'winner '+str(num) + 'aerodata.txt')
        shutil.copy(self.results_root, new_root)
        self.results_root = new_root
        
        
def start_pop(pop_num):
    '''Creates a randomly generated population of the size (pop_num)
    '''
    
    population = []
        
    
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
                  
                  
    for airfoil in range(pop_num):
        genome = np.zeros(16)
        deviation = 0.7 * np.random.randn(16) * gen_deviation
        genome = genes + deviation
        while not(test.airfoil_test(genome)):
            
            # Here we check that our airfoil actually makes sense        
            deviation = 0.7 * np.random.randn(16) * gen_deviation
            genome = genes + deviation
        airfoil = Airfoil(genome)
        population.append(airfoil)

    
       
    genome_root = os.path.join('genome','generation0.txt')
    title = 'generation 0 genome'
    
    try:
        os.remove(genome_root)
    except :
        pass
    archivo = open(genome_root, mode = 'x')
    archivo.write(title + '\n')
    
    for airfoil in population:
        line = ''
        genome = airfoil.genome
        for gen in genome:
            line = line + str(gen) +'    '
        line = line + '\n'
        archivo.write(line)
    
    return population


