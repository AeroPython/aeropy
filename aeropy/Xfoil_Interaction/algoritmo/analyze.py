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




def pop_analice (generation, num_pop):
    '''For a given generation and number of airfoils, returns an array which
    contains the maximun Lift Coefficient and Maximum Aerodinamic Efficiency
    for every airfoil.
    '''
    pop_results = np.zeros([num_pop,2])
    for profile_number in np.arange(1,num_pop+1,1):
       pop_results[profile_number - 1, :] = profile_analice (generation, profile_number)
    
    return pop_results
    
    
def profile_analice (generation, profile_number):
    '''For a given generation and profile, searches for the results of the
    aerodynamic analysis made in Xfoil. Then, searches for the maximum
    values of the Lift Coefficient and Aerodynamic Efficiency and returns them
    as an 1x2 array.
    '''    
    profile_name = 'datagen' + str(generation) + 'prof' + str(profile_number)+ '.txt'
    data_root = os.path.join("aerodata", profile_name)
    datos = np.loadtxt(data_root, skiprows=12, usecols=[1,2])
    
    read_dim = np.array(datos.shape)
    #print('read_dim = ', read_dim, read_dim.shape)
    if ((read_dim.shape[0]) != 2):
        return np.array ([0,0])
    
    
    pos_clmax = np.argmax(datos[:,0])
    clmax = datos[pos_clmax,0]
    efic = datos[:,0] / datos[:,1]
    pos_maxefic = np.argmax(efic)
    maxefic = efic[pos_maxefic]
    return np.array([clmax , maxefic])
    
def adimension(array):
    '''Adimensionalyzes an array with its maximun value
    '''
    max_value = max(array)
    adim = array / max_value
    return adim
    
def score(generation, num_pop, weights):
    '''For a given generation, number of airfoils and weight parameters, returns
    an array of the scores of all airfoils.
    '''
    pop_results = pop_analice (generation, num_pop)
    cl_score = adimension(pop_results[:,0])
    efic_score = adimension(pop_results[:,1])
    total_score = weights[0] * cl_score + weights[1] * efic_score
    return total_score
