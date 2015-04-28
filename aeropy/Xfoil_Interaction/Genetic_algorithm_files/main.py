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
import ender as ender

#First, the main function is defined. This allows us to call it from a future
#different starting file (like a PyQT graphic interface).

#If this is the starting file, it will call the main function with the 
#parameters described below.



def main_program(all_parameters):
    '''The main function of the program, calls ir order all the rest'''
    
    airfoils_per_generation = all_parameters[0]
    total_generations = all_parameters[1]
    num_parent = all_parameters[2]
#    num_winners = all_parameters[3]
    weighting_parameters = all_parameters[4]
#    end_options = all_parameters[5]

    
###--- Creating work directories
    
    if not os.path.exists('aerodata'):
        os.makedirs('aerodata')
        
    if not os.path.exists('genome'):
        os.makedirs('genome')
        
    if not os.path.exists('results'):
        os.makedirs('results')

    if not os.path.exists(os.path.join('results', 'graphics')):
        os.makedirs(os.path.join('results', 'graphics'))
        
    if not os.path.exists(os.path.join('results', 'data')):
        os.makedirs(os.path.join('results', 'data'))




####--- Starting the population, analysis of the starting population


    generation = 0


    initial.start_pop(airfoils_per_generation)

    interfaz.xfoil_calculate_population(generation, ambient_data, aero_domain)


####--- Genetic Algorithm


    for generation in np.arange(0,total_generations,1):
    

        genetics.genetic_step(generation,num_parent, weighting_parameters)
    
        interfaz.xfoil_calculate_population(generation + 1, ambient_data, aero_domain)
    
   

    ender.finish(all_parameters)    
    


#If this is the file from which we are starting, we define here the parameters:

if __name__ == '__main__':

####---------Primary Variables-----


    airfoils_per_generation = 3
    total_generations = 3
    num_parent = 1

# We give the algorithm the conditions at wich we want to optimize our airofil
# through the "ambient data" tuple. 

    planet = 'Mars' # For the moment we have 'Earth' and 'Mars'
    chord_length = 0.2 # In metres
    altitude = -7.5 # In Kilometres above sea level or reference altitude
    speed_parameter = 'speed' # 'speed' or 'mach'
    speed_value = 30 # Value of the previous magnitude (speed - m/s)
    ambient_data = (planet, chord_length, altitude, speed_parameter, speed_value)



####--------Secondary Variables------
#-- Analysis domain

    start_alpha_angle = 0
    finish_alpha_angle = 15
    alpha_angle_step = 1

    aero_domain = (start_alpha_angle, finish_alpha_angle, alpha_angle_step)
    
    
#-- Optimization objectives

    lift_coefficient_weight = 0.3
    efficiency_weight = 0.7

    weighting_parameters = (lift_coefficient_weight, efficiency_weight)

#-- Final results options

    num_winners = 3
    draw_winners = True
    draw_polars = True
    draw_evolution = True
    compare_naca_standard = True
    compare_naca_custom = True #Work in progress
    create_report = True       #Work in progress

    end_options = (draw_winners, draw_polars, draw_evolution, 
               compare_naca_standard, compare_naca_custom, 
               create_report,
               ambient_data, aero_domain)
             
             
             
    all_parameters = (airfoils_per_generation, total_generations, num_parent,
                      num_winners, weighting_parameters, end_options )   


    main_program(all_parameters)    