'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is the main program. It will call the different submodules
and manage the data transfer between them in order to achieve the
genetic optimization of the profile.

'''



import subprocess
import sys
import os
import interfaz as interfaz
import numpy as np
import initial as initial



#generation = 0
#starting_profiles = 20
#
#genome = initial.start_pop(starting_profiles)
#
#interfaz.xfoil_calculate_population(generation,genome)
#
#num_pop = genome_matrix.shape[0]

def pop_analice (generation, num_pop):
    pop_results = np.zeros([num_pop,2])
    for profile_number in np.arange(1,num_pop+1,1):
       pop_results[profile_number - 1, :] = profile_analice (generation, profile_number)
    
    return pop_results
    
    
def profile_analice (generation, profile_number):    
    profile_name = 'gen' + str(generation) + 'prof' + str(profile_number)
    data_root = "aerodata\data" + profile_name + '.txt'
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
    max_value = max(array)
    adim = array / max_value
    return adim
    
def score(generation, num_pop):
    
    pop_results = pop_analice (generation, num_pop)
    cl_score = adimension(pop_results[:,0])
    efic_score = adimension(pop_results[:,1])
    total_score = 0.3 * cl_score + 0.7 * efic_score
    return total_score
