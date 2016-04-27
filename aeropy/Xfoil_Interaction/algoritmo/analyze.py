'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is the analysis subprogram. Its objective is to assign a score to
every airfoil by reading the aerodynamic characteristics that XFoil
has calculated.

'''




import numpy as np
import os




def pop_analice (generation, population, num_parent):
    '''For a given generation and number of airfoils, returns an array which
    contains the maximun Lift Coefficient and Maximum Aerodinamic Efficiency
    for every airfoil.
    '''
    pop_len = len(population)
    for airfoil_number in range(1, pop_len+1):
        airfoil = population[airfoil_number - 1] 
        if not hasattr(airfoil, 'clmax'):
            airfoil_analice(generation, airfoil_number, airfoil)
    
   
    
    
def airfoil_analice (generation, airfoil_number, airfoil):
    '''For a given generation and airfoil, searches for the results of the
    aerodynamic analysis made in Xfoil. Then, searches for the maximum
    values of the Lift Coefficient and Aerodynamic Efficiency.
    '''    
    airfoil_name = airfoil.name
    data_root = os.path.join("aerodata","data" + airfoil_name + '.txt')
    datos = np.loadtxt(data_root, skiprows=12, usecols=[1,2])
    
    #Chequear integridad de los datos
    read_dim = np.array(datos.shape)
    if ((read_dim.shape[0]) != 2):
        datos = np.zeros([2,2])
    
    
    pos_clmax = np.argmax(datos[:,0])
    clmax = datos[pos_clmax,0]
    efic = datos[:,0] / datos[:,1]
    pos_maxefic = np.argmax(efic)
    maxefic = efic[pos_maxefic]
    airfoil.clmax = clmax
    airfoil.maxefic = maxefic
    
def score(generation, population, weights):
    '''
    
    '''
    max_cl = -100
    max_efic = -100
    
    for airfoil in population:
        max_cl = max(airfoil.clmax, max_cl)
        max_efic = max(airfoil.maxefic, max_efic)
    for airfoil in population:
        cl_score = airfoil.clmax / max_cl
        efic_score = airfoil.maxefic / max_efic
        total_score = weights[0] * cl_score + weights[1] * efic_score
        airfoil.score = total_score
    
