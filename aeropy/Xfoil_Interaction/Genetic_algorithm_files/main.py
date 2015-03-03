'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is the main program. It will call the different submodules
and manage the data transfer between them in order to achieve the
genetic optimization of the profile.

'''




import os
import interfaz as interfaz
import numpy as np
import initial as initial
import genetics as genetics

if not os.path.exists('aerodata'):
        os.makedirs('aerodata')
        
if not os.path.exists('genome'):
        os.makedirs('genome')


####---------Primary Variables-----


generation = 0
airfoils_per_generation = 30
total_generations = 15
num_parent = 4
ambient_data = ('Earth', 0.1, 3, 'mach', 0.1)

# We give the algorithm the conditions at wich we want to optimize our airofil
# through the "ambient data" tuple. The first position is for the planet,
# only 'Mars' and 'Earth are available at the moment.
# The second position is for the lenght of the airfoil, in metres.
# The third is for the flying height, in kilometers, above sea level 
# on Earth and avobe the zero reference in Mars. 
# The fourth especifies the type of speed we are introducing, and can
# have the values 'speed' or 'mach'.
# The last one is for the value of the parameter selected in the previous one.


####--------Secondary Variables------
#-- Analysis domain
start_alpha_angle = 0
finish_alpha_angle = 20
alpha_angle_step = 1

aero_domain = (start_alpha_angle, finish_alpha_angle, alpha_angle_step)
#-- Optimization objectives

lift_coefficient_weight = 0.3
efficiency_weight = 0.7

weighting_parameters = (lift_coefficient_weight, efficiency_weight)

####--- Starting the population, analysis of the starting population


genome = initial.start_pop(airfoils_per_generation)

interfaz.xfoil_calculate_population(generation, ambient_data, aero_domain)


##--- Genetic Algorithm


for generation in np.arange(0,total_generations,1):
    
    genome = genetics.genetic_step(generation,num_parent, weighting_parameters)
    
    interfaz.xfoil_calculate_population(generation + 1, ambient_data, aero_domain)
    
    
    
    
    
    