# -*- coding: utf-8 -*-
'''
Created on Fri Feb 20 20:57:16 2015

@author: Juan Luis Cano, Alberto Lorenzo, Siro Moreno

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
import os
import algoritmo.transcript as trans
import numpy as np
import algoritmo.ambient as ambient


def xfoil_calculate_profile(generation, airfoil_number,
                            airfoil, ambient_data, aero_domain):
    
    '''Starts Xfoil and analyzes the given airfoil. Saves the results.
    '''
    
    airfoil_name = 'gen' + str(generation) + 'airf' + str(airfoil_number)
    geo_file_name = 'airfoil' + str(airfoil_number) + '.txt'
    airfoil_root = os.path.join('airfoils','gen' + str(generation) , geo_file_name )
    data_root = os.path.join("aerodata","data" + airfoil_name + '.txt')    
    airfoil.name = airfoil_name
    airfoil.results_root = data_root
    
    aerodynamics = ambient.aero_conditions(ambient_data)
    
    
    commands = ['load',
            airfoil_root,
            'oper',
            'mach ' + str(aerodynamics[0]),
            're ' + str(aerodynamics[1]),
            'visc',
            'pacc',
            data_root,
            '',
            'aseq',
            str(aero_domain[0]),
            str(aero_domain[1]),
            str(aero_domain[2]),
            '',
            'quit']


    genome = airfoil.genome    
    airf_points = trans.decode_genome(genome)
    

    try:
        os.remove(airfoil_root)
    except :
        pass
    try:
        os.remove(data_root)
    except :
        pass
   
    
    archivo = open(airfoil_root, mode = 'x')
    archivo.write(airfoil_name + '\n')

    for i in np.arange(0,100,1):
        texto = str(round(airf_points[i,0],6))
        texto += '   ' + str(round(airf_points[i,1],6)) +'\n'
        archivo.write(texto)
    archivo.close()

    p = subprocess.Popen(["xfoil",],
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE)

    for command in commands:
        p.stdin.write((command + '\n').encode())
     

    p.stdin.close()
    for line in p.stdout.readlines():
        print(line.decode(), end='')

def xfoil_calculate_population(generation, population,
                               ambient_data, aero_domain,
                               num_parent = 0):
    '''Given a generation number and ambiental conditions, reads the file
    which contains the genome information of the generation, and uses xfoil to
    analyze each airfoil.
    '''
    
    
    pop_len = len(population)
    
    airfoils_folder = os.path.join('airfoils', 'gen' + str(generation))
    if not os.path.exists(airfoils_folder):
        os.makedirs(airfoils_folder)
    
    for airfoil_number in range(num_parent, pop_len):
        xfoil_calculate_profile(generation, airfoil_number,
                                population[airfoil_number],
                                ambient_data, aero_domain)


