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
import algoritmo.interfaz as interfaz
import numpy as np
import algoritmo.initial as initial
import algoritmo.genetics as genetics
import algoritmo.analyze as analyze
import algoritmo.selection as selection
import matplotlib.pyplot as plt
import algoritmo.transcript as transcript
import algoritmo.ambient as ambient
import subprocess
#import algoritmo.ender_report


def finish (all_parameters):
    
    
    generation = all_parameters[1]
    num_winners = all_parameters[3]
    weights = all_parameters[4]
    end_options = all_parameters[5]    
    ambient_data = all_parameters[6]
    aero_domain = all_parameters[7]
    
    must_draw_winners = end_options[0]
    must_draw_polars = end_options[1]
    must_draw_evolution = end_options[2]
    must_compare_naca_standard = end_options[3]
    must_compare_naca_custom = end_options[4]
    must_create_report = end_options[5]
    
    analyze_final(generation, num_winners, weights)
    
    compare = must_compare_naca_standard
    final_xfoil(generation, ambient_data, aero_domain, compare)
    analyze_winners(generation, num_winners, weights)
    calculate_evolution(generation, num_winners, compare)
    if (must_draw_winners):
        draw_winners(compare)
    if (must_draw_polars):
        draw_aero_comparison(num_winners, compare)
    if (must_draw_evolution):
        draw_evolution(compare, aero_domain)
    #if (must_create_report):
    #    ender_report.create_report(all_parameters)


def analyze_final(generation, num_winners, weights):
    '''Analyze the data of the last generation
    '''
    file_parent_name = 'generation'+ str(generation) + '.txt'
    genome_parent_root = os.path.join('genome', file_parent_name)    
    genome = np.loadtxt(genome_parent_root, skiprows=1)
    num_pop = genome.shape[0]
    results_data = analyze.pop_analice(generation, num_pop)
    
    scores = analyze.score(generation,num_pop, weights)
    winners = selection.selection(scores, genome, num_winners)
    
    
    
    
    file_name = 'winners.txt'
    genome_root = os.path.join('genome', file_name)
    title = 'winners genome'
    
    results_name = 'results_data_generation'+ str(generation) + '.txt'
    results_root = os.path.join('results', 'data', results_name )
    results_title = 'generation' + str(generation) + 'results:'
    
    
    try:
        os.remove(genome_root)
    except:
        pass
    
    try:
        os.remove(results_root)
    except :
        pass
    
    genome_file = open(genome_root, mode = 'x')
    results_file = open(results_root, mode = 'x')
    genome_file.write(title + '\n')
    results_file.write(results_title + '\n')
    results_file.write('Cl max   Eficciency      Score' + '\n')
    
    for profile in np.arange(0, num_pop, 1):
        result = str(results_data[profile, 0]) + '   ' 
        result = result + str(results_data[profile, 1]) + '   '
        result = result + str(scores[profile]) + '\n'
        results_file.write(result)
    for profile in np.arange(0, num_winners, 1):
        line = ''
        for gen in np.arange(0, 16,1):
            line = line + str(winners[profile, gen]) +'    '
        line = line + '\n'
        genome_file.write(line)
    genome_file.close()
    results_file.close()


def analyze_winners(generation, num_winners, weights):
    '''Analyze the data of the winners
    '''
    
    results = np.zeros([num_winners, 3])
    
    for i in np.arange(0, num_winners, 1):
        dataname = 'datagen' + str(generation) + 'prof' + str(i + 1) + '.txt'
        data_root = os.path.join('aerodata', dataname)
        data = np.loadtxt(data_root, skiprows = 12, usecols=[1,2])
        clmax = max(data[:,0])
        efimax = max(data[:,0] / data[:,1])
        results[i, 0:2] = [clmax, efimax]
        
    cl_score = analyze.adimension(results[:,0])
    efic_score = analyze.adimension(results[:,1])
    results[:,2] = weights[0] * cl_score + weights[1] * efic_score
    
    
    results_name = 'results_winners.txt'
    results_root = os.path.join('results', 'data', results_name )
    results_title = 'Winners results:'
    
    
    try:
        os.remove(results_root)
    except :
        pass
    
    results_file = open(results_root, mode = 'x')
    results_file.write(results_title + '\n')
    results_file.write('Cl max   Eficciency      Score' + '\n')
    
    for profile in np.arange(0, num_winners, 1):
        result = str(results[profile, 0]) + '   ' 
        result = result + str(results[profile, 1]) + '   '
        result = result + str(results[profile, 2]) + '\n'
        results_file.write(result)

#--- Drawing Airfoils


        
def draw_winners(options):
    
    winners_root = os.path.join('genome', 'winners.txt')
    winners_genome = np.loadtxt(winners_root, skiprows=1)
    
    num_winners = winners_genome.shape[0]
    
    for winner in np.arange(0, num_winners, 1):
        
        graph_name = 'winner ' + str(winner + 1)
        graph_root = os.path.join('results','graphics',graph_name + '.png')
        point_data = transcript.decode_genome(winners_genome[winner,:])
        draw_figure(graph_name, graph_root, point_data)
    
    if (options):
        graph_name = 'NACA 5615'
        graph_root = os.path.join('results','graphics',graph_name + '.png')
        data_root = os.path.join('profiles','winners',graph_name + '.txt')
        point_data = np.loadtxt(data_root, skiprows = 1)
        draw_figure(graph_name, graph_root, point_data)
        
        graph_name = 'NACA 5603'
        graph_root = os.path.join('results','graphics',graph_name + '.png')
        data_root = os.path.join('profiles','winners',graph_name + '.txt')
        point_data = np.loadtxt(data_root, skiprows = 1)
        draw_figure(graph_name, graph_root, point_data)
        

def draw_figure(graph_name, graph_root, point_data):
    try:
        os.remove(graph_root)
    except :
        pass
        
    plt.figure(num=None, figsize=(15, 5), dpi=80, facecolor='w', edgecolor='k')
    plt.title (graph_name)
    plt.ylim(-0.15, 0.15)
    plt.xlim(-0.05, 1.05)
    plt.plot(point_data[:,0], point_data[:,1])
    plt.gca().set_aspect(1)
        
        
    plt.savefig(graph_root)


# Running Xfoil for more detailed analysis of the winners

def xfoil_calculate_profile(profile_name, profile_root,
                            ambient_data, aero_domain,
                            profile_type):
    
    '''Starts Xfoil and analyzes the given airfoil. Saves the results.
    '''
 
    data_root = os.path.join("results","data" , profile_name + 'aerodata.txt')    
    
    aerodynamics = ambient.aero_conditions(ambient_data)
    
    
    commands = [profile_type,
            profile_root]
    commands2 = ['oper',
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
    if (profile_type == 'NACA'):
        naca_root = os.path.join('profiles', 'winners', profile_name + '.txt')
        commands.extend(['save',naca_root])
    commands.extend(commands2)


    
    try:
        os.remove(data_root)
    except :
        pass
   
    
    
    p = subprocess.Popen(["xfoil",],
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE)

    for command in commands:
        p.stdin.write((command + '\n').encode())
     

    p.stdin.close()
    for line in p.stdout.readlines():
        print(line.decode(), end='')

def final_xfoil(total_generations, ambient_data, aero_domain, compare):
    
    profile_folder = os.path.join('profiles','winners')    
    if not os.path.exists(profile_folder):
        os.makedirs(profile_folder) 
        
    genome_root = os.path.join('genome','winners.txt')
    genome_matrix = np.loadtxt(genome_root, skiprows=1)    
    num_winners = genome_matrix.shape[0]
    
    
    for profile in np.arange(0, num_winners, 1):
        genome = genome_matrix[profile,:]
        profile_name = 'winner ' + str(profile + 1)
        profile_root = os.path.join('profiles','winners', profile_name + '.txt')
        
        perfil = transcript.decode_genome(genome)
        try:
            os.remove(profile_root)
        except :
            pass 
   
    
        archivo = open(profile_root, mode = 'x')
        archivo.write(profile_name + '\n')
        for i in np.arange(0,100,1):
            texto = str(round(perfil[i,0],6)) + '   ' + str(round(perfil[i,1],6)) +'\n'
            archivo.write(texto)
        archivo.close()
        
        xfoil_calculate_profile(profile_name, profile_root,
                                ambient_data, aero_domain,
                                'load')
    if (compare):
        
        profile_name = 'NACA 5615'
        profile_root = '5615'
        
        try:
            os.remove(os.path.join('profiles','winners', profile_name + '.txt'))
        except :
            pass 
        
        xfoil_calculate_profile(profile_name, profile_root,
                                ambient_data, aero_domain,
                                'NACA')
                                
        profile_name2 = 'NACA 5603'
        profile_root2 = '5603'
        
        try:
            os.remove(os.path.join('profiles','winners', profile_name2 + '.txt'))
        except :
            pass 
        
        xfoil_calculate_profile(profile_name2, profile_root2,
                                ambient_data, aero_domain,
                                'NACA')

# Drawing polars

def draw_alpha(data): 
    
    if not os.path.exists(os.path.join('results','graphics')):
        os.makedirs(os.path.join('results','graphics'))
    graph_name = 'Cl_vs_Alpha_Graphic'
    graph_root = os.path.join('results','graphics',graph_name + '.png')
        
    root = data[:,1]
    name = data[:,0]
    
    num_prof = root.shape[0]
    
    plt.figure(num=None, figsize=(15, 8), dpi=80, facecolor='w', edgecolor='k')
    plt.rc('font', size = 20)
    plt.title (graph_name)
    
    ideal = np.array([[0,0],
                      [15, (15*np.pi/180)*np.pi*2]])
        
    plt.plot(ideal[:,0], ideal[:,1], label = ' ideal, cl alpha = 2$\pi$')
    for i in np.arange(0,num_prof,1):
       
        profile_root = root[i] 
        profile_name = name[i]
        datos = np.loadtxt(profile_root, skiprows=12, usecols=[0,1])
        read_dim = np.array(datos.shape)
        if ((read_dim.shape[0]) == 2):
            plt.plot(datos[:,0], datos[:,1], label = profile_name)
    
    
    
        
    plt.legend(loc = 2, fontsize =14)  
    plt.grid() 
    plt.minorticks_on()
    plt.xlabel('Attack angle')  
    plt.ylabel('Lift coefficient')
    plt.savefig(graph_root)

def draw_polar(data): 
    
    if not os.path.exists(os.path.join('results','graphics')):
        os.makedirs(os.path.join('results','graphics'))
    graph_name = 'Cl_vs_Cd_Graphic'
    graph_root = os.path.join('results','graphics',graph_name + '.png')
        
    root = data[:,1]
    name = data[:,0]
    
    num_prof = root.shape[0]
    
    plt.figure(num=None, figsize=(15, 8), dpi=80, facecolor='w', edgecolor='k')
    plt.rc('font', size = 20)
    plt.title (graph_name)
    
    for i in np.arange(0,num_prof,1):
       
        profile_root = root[i] 
        profile_name = name[i]
        datos = np.loadtxt(profile_root, skiprows=12, usecols=[1,2])
        read_dim = np.array(datos.shape)        
        if ((read_dim.shape[0]) == 2):
            plt.plot(datos[:,1], datos[:,0], label = profile_name)
    
    
    
    plt.xlim(xmin=0)    
    plt.legend(loc = 4, fontsize =14)  
    plt.grid() 
    plt.minorticks_on()
    plt.xlabel('Drag coefficient')  
    plt.ylabel('Lift coefficient')
    plt.savefig(graph_root)


def draw_aero_comparison(num_winners, compare):
    
    num_profiles = num_winners
    if (compare):
        num_profiles = num_profiles + 1
        
    data = []
    
    for i in np.arange(0, num_winners, 1):
        name = 'winner ' + str(i + 1)
        root = os.path.join('results','data', name + 'aerodata.txt')
        data.append([name, root])
    if compare :
        name = 'NACA 5615'
        root = os.path.join('results','data', name + 'aerodata.txt')
        data.append([name, root])
        
        name = 'NACA 5603'
        root = os.path.join('results','data', name + 'aerodata.txt')
        data.append([name, root])
        
    data = np.array(data) 
    draw_alpha(data)
    draw_polar(data)
    
    
# Drawing the Evolution Diagrams

def calculate_evolution(max_generations, num_winners, options):
    lift = []
    effic = []
    
   
    
    for gen in np.arange(0,max_generations + 1,1):
        lift.append([])
        effic.append([])
        data_root = os.path.join('results','data','results_data_generation'+ str(gen) + '.txt')
        data = np.loadtxt(data_root, skiprows = 2)
        invscore = 1- data[:, 2]
        positions = np.argsort(invscore)
        for win in np.arange(0, num_winners, 1):
            win_cl = data[positions[win], 0]
            win_effic = data[positions[win], 1]
            lift[gen].append(win_cl)
            effic[gen].append(win_effic)
                        
    lift = np.array(lift)
    effic = np.array(effic)
    
    lift_name = 'lift history.txt'
    lift_root = os.path.join('results', 'data', lift_name )
    effic_name = 'efficiency history.txt'
    effic_root = os.path.join('results', 'data', effic_name )
    
    
    
    try:
        os.remove(lift_root)
    except :
        pass
    try:
        os.remove(effic_root)
    except :
        pass
    
    lift_file = open(lift_root, mode = 'x')
    lift_file.write('Values of Cl of the best airfoils of each generation\n')
    lift_file.write('generation   ')
    for i in np.arange(1, num_winners + 1, 1):
        lift_file.write('winner ' + str(i) + '     ')
    lift_file.write('\n')
    
    for gen in np.arange(0, max_generations + 1, 1):
        lift_file.write('    '+ str(gen) + '        ')
        
        for win in np.arange(0, num_winners, 1):
            lift_file.write(str(lift[gen,win])+ '       ')
        lift_file.write('\n')
        
    lift_file.close()
    
    effic_file = open(effic_root, mode = 'x')
    effic_file.write('Values of efficiency of the best airfoils of each generation\n')
    effic_file.write('generation   ')
    for i in np.arange(1, num_winners + 1, 1):
        effic_file.write('winner ' + str(i) + '          ')
    effic_file.write('\n')
    
    for gen in np.arange(0, max_generations + 1, 1):
        effic_file.write('    '+ str(gen) + '      ')
        
        for win in np.arange(0, num_winners, 1):
            effic_file.write(str(effic[gen,win])+ '     ')
        effic_file.write('\n')
        
    effic_file.close()

def draw_evolution(options, aero_domain):
    
    if options :
        naca_root = os.path.join('results','data','NACA 5615aerodata.txt')
        naca_data = np.loadtxt(naca_root, skiprows = 12, usecols=[1,2])
        max_angle = 1 + 2 * round((aero_domain[1]-aero_domain[0])/aero_domain[2])
        naca_cl = max(naca_data[0:max_angle,0])
        naca_effic = max(naca_data[0:max_angle,0] / naca_data[0:max_angle,1])
        
        naca_root2 = os.path.join('results','data','NACA 5603aerodata.txt')
        naca_data2 = np.loadtxt(naca_root2, skiprows = 12, usecols=[1,2])
        max_angle = 1 + 2 * round((aero_domain[1]-aero_domain[0])/aero_domain[2])
        naca_cl2 = max(naca_data2[0:max_angle,0])
        naca_effic2 = max(naca_data2[0:max_angle,0] / naca_data2[0:max_angle,1])
        
    lift_name = 'lift history.txt'
    lift_root = os.path.join('results', 'data', lift_name )
    lift_data = np.loadtxt(lift_root, skiprows = 2)
    
    effic_name = 'efficiency history.txt'
    effic_root = os.path.join('results', 'data', effic_name )
    effic_data = np.loadtxt(effic_root, skiprows = 2)
    
    
    if not os.path.exists(os.path.join('results','graphics')):
        os.makedirs(os.path.join('results','graphics'))
        
    # Draw the history of lift coefficient
    graph_name = 'History of lift coefficient'
    graph_root = os.path.join('results','graphics',graph_name + '.png')
        
    num_winners = lift_data.shape[1] - 1
    
    plt.figure(num=None, figsize=(15, 8), dpi=80, facecolor='w', edgecolor='k')
    plt.rc('font', size = 20)
    plt.title (graph_name)
    
    for i in np.arange(0,num_winners,1):
        label = 'winner' + str(i + 1)       
        plt.plot(lift_data[:,0], lift_data[:,i + 1], label = label)
    if options :
        label = 'NACA 5615' 
        value = naca_cl * np.ones_like(effic_data[:,0])
        plt.plot(lift_data[:,0], value, label = label)
        
        label = 'NACA 5603' 
        value = naca_cl2 * np.ones_like(effic_data[:,0])
        plt.plot(lift_data[:,0], value, label = label)
    
    
        
    plt.legend(loc = 4, fontsize =14)  
    plt.grid() 
    plt.minorticks_on()
    plt.xlabel('Generation')  
    plt.ylabel('Lift coefficient')
    plt.savefig(graph_root)
    
    # Draw the history of efficiency
    graph_name = 'History of efficiency'
    graph_root = os.path.join('results','graphics',graph_name + '.png')
        
    num_winners = effic_data.shape[1] - 1
    
    plt.figure(num=None, figsize=(15, 8), dpi=80, facecolor='w', edgecolor='k')
    plt.rc('font', size = 20)
    plt.title (graph_name)
    
    for i in np.arange(0,num_winners,1):
        label = 'winner' + str(i + 1)       
        plt.plot(effic_data[:,0], effic_data[:,i + 1], label = label)
    if options :
        label = 'NACA 5615' 
        value = naca_effic * np.ones_like(effic_data[:,0])
        plt.plot(effic_data[:,0], value, label = label)
        
        label = 'NACA 5603' 
        value = naca_effic2 * np.ones_like(effic_data[:,0])
        plt.plot(effic_data[:,0], value, label = label)
    
    
        
    plt.legend(loc = 4, fontsize =14)  
    plt.grid() 
    plt.minorticks_on()
    plt.xlabel('Generation')  
    plt.ylabel('Efficiency')
    plt.savefig(graph_root)
  






if __name__ == '__main__':

####---------Primary Variables-----


    airfoils_per_generation = 30
    total_generations = 30
    num_parent = 4

# We give the algorithm the conditions at wich we want to optimize our airofil
# through the "ambient data" tuple. 

    planet = 'Mars' # For the moment we have 'Earth' and 'Mars'
    chord_length = 0.4 # In metres
    altitude = -7.5 # In Kilometres above sea level or reference altitude
    speed_parameter = 'speed' # 'speed' or 'mach'
    speed_value = 28.284 # Value of the previous magnitude (speed - m/s)
    ambient_data = (planet, chord_length, altitude, speed_parameter, speed_value)



####--------Secondary Variables------
#-- Analysis domain

    start_alpha_angle = 0
    finish_alpha_angle = 20
    alpha_angle_step = 2

    aero_domain = (start_alpha_angle, finish_alpha_angle, alpha_angle_step)
    
    
#-- Optimization objectives

    lift_coefficient_weight = 0.0
    efficiency_weight = 1.0

    weighting_parameters = (lift_coefficient_weight, efficiency_weight)

#-- Final results options

    num_winners = 3
    vdraw_winners = True
    vdraw_polars = True
    vdraw_evolution = True
    vcompare_naca_standard = True
    vcompare_naca_custom = True #Work in progress
    vcreate_report = True       #Work in progress

    end_options = (vdraw_winners, vdraw_polars, vdraw_evolution, 
               vcompare_naca_standard, vcompare_naca_custom, 
               vcreate_report,
               ambient_data, aero_domain)
             
             
             
    all_parameters = (airfoils_per_generation, total_generations, num_parent,
                      num_winners, weighting_parameters, end_options )   


    finish(all_parameters)    