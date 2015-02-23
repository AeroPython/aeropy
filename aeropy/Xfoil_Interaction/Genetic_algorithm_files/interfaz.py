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
import sys
import os
import transcript as trans
import numpy as np


def xfoil_calculate_profile(generation,profile_number,genome):
    
    profile_root = 'profiles\gen' + str(generation) + '\profile' + str(profile_number) + '.txt'
    profile_name = 'gen' + str(generation) + 'prof' + str(profile_number)
    
    
    commands = ['load',
            profile_root,
            'oper',
            'mach 0.2',
            're 3500',
            'visc',
            'pacc',
            "aerodata\data" + profile_name + '.txt',
            '',
            'aseq',
            '0',
            '20',
            '1',
            '',
            'quit']


    perfil = trans.decode_genome(genome)
    
    if not os.path.exists('profiles\gen' + str(generation)):
        os.makedirs('profiles\gen' + str(generation))
    try:
        os.remove(profile_root)
    except :
        pass
    try:
        os.remove("aerodata\data" + profile_name + '.txt')
    except :
        pass
    
    
    
    archivo = open(profile_root, mode = 'x')
    archivo.write(profile_name + '\n\n\n')


    for i in np.arange(0,100,1):
        texto = str(round(perfil[i,0],6)) + '   ' + str(round(perfil[i,1],6)) +'\n'
        archivo.write(texto)
    archivo.close()

    p = subprocess.Popen(["xfoil.exe",],
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE)

    for command in commands:
        p.stdin.write((command + '\n').encode())
     
    p.stdin.write("\nquit\n".encode())
    p.stdin.close()
    for line in p.stdout.readlines():
        print(line.decode(), end='')

def xfoil_calculate_population(generation, genome_matrix):
    num_pop = genome_matrix.shape[0]
    for profile_number in np.arange(1,num_pop+1,1):
        xfoil_calculate_profile(generation, profile_number, genome_matrix[profile_number-1,:])


