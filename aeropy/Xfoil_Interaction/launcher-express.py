# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 18:52:51 2016

@author: Usuario
"""

import algoritmo.main as main

airfoils_per_generation = 3
total_generations = 2
num_parent = 1

# We give the algorithm the conditions at wich we want to optimize our airofil
# through the "ambient data" tuple. 

planet = 'Mars' # For the moment we have 'Earth' and 'Mars'
chord_length = 0.1 # In metres
altitude = -7.5 # In Kilometres above sea level or reference altitude
speed_parameter = 'speed' # 'speed' or 'mach'
speed_value = 18 # Value of the previous magnitude (speed - m/s)
ambient_data = (planet, chord_length, altitude, speed_parameter, speed_value)



####--------Secondary Variables------
#-- Analysis domain

start_alpha_angle = 0
finish_alpha_angle = 20
alpha_angle_step = 2

aero_domain = (start_alpha_angle, finish_alpha_angle, alpha_angle_step)


#-- Optimization objectives

lift_coefficient_weight = 0.3
efficiency_weight = 0.7

weighting_parameters = (lift_coefficient_weight, efficiency_weight)

#-- Final results options

num_winners = 1
draw_winners = True
draw_polars = True
draw_evolution = True
compare_naca_standard = True
compare_naca_custom = True #Work in progress
create_report = True       #Work in progress

end_options = (draw_winners, draw_polars, draw_evolution, 
           compare_naca_standard, compare_naca_custom, 
           create_report)
         
         
         
all_parameters = (airfoils_per_generation, total_generations, num_parent,
                  num_winners, weighting_parameters, end_options,
                  ambient_data, aero_domain )   


main.main_program(all_parameters)    