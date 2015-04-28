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
import transcript as trans
import numpy as np
import ambient as ambient


def xfoil_calculate_profile(generation,profile_number, genome, ambient_data, aero_domain):
    
    '''Starts Xfoil and analyzes the given airfoil. Saves the results.
    '''
    
    profile_name = 'gen' + str(generation) + 'prof' + str(profile_number)
    geo_file_name = 'profile' + str(profile_number) + '.txt'
    profile_root = os.path.join('profiles','gen' + str(generation) , geo_file_name )
    data_root = os.path.join("aerodata","data" + profile_name + '.txt')    
    
    aerodynamics = ambient.aero_conditions(ambient_data)
    
    
    commands = ['load',
            profile_root,
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


    perfil = trans.decode_genome(genome)
    

    try:
        os.remove(profile_root)
    except :
        pass
    try:
        os.remove(data_root)
    except :
        pass
   
    
    archivo = open(profile_root, mode = 'x')
    archivo.write(profile_name + '\n')


    for i in np.arange(0,100,1):
        texto = str(round(perfil[i,0],6)) + '   ' + str(round(perfil[i,1],6)) +'\n'
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

def xfoil_calculate_population(generation, ambient_data, aero_domain):
    '''Given a generation number and ambiental conditions, reads the file
    which contains the genome information of the generation, and uses xfoil to
    analyze each airfoil.
    '''
    
    genome_root = os.path.join('genome','generation'+ str(generation) + '.txt')    
    genome_matrix = np.loadtxt(genome_root, skiprows=1)    
    num_pop = genome_matrix.shape[0]
    
    profile_folder = os.path.join('profiles', 'gen' + str(generation))
    if not os.path.exists(profile_folder):
        os.makedirs(profile_folder)
    
    for profile_number in np.arange(1,num_pop+1,1):
        xfoil_calculate_profile(generation, profile_number, genome_matrix[profile_number-1,:], ambient_data, aero_domain)


