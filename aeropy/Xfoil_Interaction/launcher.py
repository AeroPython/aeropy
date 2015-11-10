'''

Created on Wed Nov 4 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is a command prompt launcher.

'''




import algoritmo.main as main



####---------Primary Variables-----


def cuestionario(min_x):
    correct = False
    while not correct:
        x = input()
        try:
            x = int(x)
        except:
            print('Por favor, introduzca un número válido')
            continue
        if x < min_x:
            print('número demasiado bajo, vuelva a intentarlo')
        else:
            correct = True
    return x
def cuestionario_float(min_x):
    correct = False
    while not correct:
        x = input()
        try:
            x = float(x)
        except:
            print('Por favor, introduzca un número válido')
            continue
        if x < min_x:
            print('número demasiado bajo, vuelva a intentarlo')
        else:
            correct = True
    return x
       
def cuestionario_s_n():
    correct = False
    while not correct:
        x = input()
        try:
            x = str(x)
        except:
            continue
        if x == 's' or x == 'y' or x == 'S' or x == 'Y':
            r = True
            correct = True
        elif x =='n' or x =='N':
            r = False
            correct = True
        else:
            print('Por favor, responda con "s" o "n"')
            correct = False
    return r
    
print()
print('--- Parámetros del algoritmo genético ---')
print()
print('introduzca un número de perfiles por generación')
airfoils_per_generation = cuestionario(2)
print('introduzca un número de generaciones')
total_generations = cuestionario(2)
print('introduzca un número de parents')
num_parent = cuestionario(1)

# We give the algorithm the conditions at wich we want to optimize our airofil
# through the "ambient data" tuple. 
print()
print('--- Parámetros ambientales ---')
print()

print('¿En qué planeta desea otimizar? Mars / Earth')
correct = False
while not correct:
    x = input()
    try:
        x = str(x)
    except:
        continue
    if not(x == 'Earth' or x == 'Mars'):
        print('planeta incorrecto, elija "Earth" o "Mars"')
    else:
        correct = True
planet = x # For the moment we have 'Earth' and 'Mars'
print('introduzca la longitud de la cuerda (en metros)')
chord_length = cuestionario_float(0) # In metres
print('introduzca la altitud de vuelo (en kilómetros)')
if planet == 'Earth':
    altitude = cuestionario_float(0)
else:
    altitude = cuestionario_float(-7.5)# In Kilometres above sea level or reference altitude
print('¿Cómo va a introducir la velocidad? speed / mach')
correct = False
while not correct:
    x = input()
    try:
        x = str(x)
    except:
        continue
    if not(x == 'speed' or x == 'mach'):
        print('parámetro de velocidad incorrecto')
    else:
        correct = True
speed_parameter = x # 'speed' or 'mach'
if speed_parameter == 'speed':
    print('Introduzca el valor de la velocidad (m/s)')
    speed_value = cuestionario_float(0) # Value of the previous magnitude (speed - m/s)
else:
    print('Introduzca el valor del número de Mach')
    speed_value = cuestionario_float(0)
ambient_data = (planet, chord_length, altitude, speed_parameter, speed_value)



####--------Secondary Variables------
#-- Analysis domain
print()
print('--- Dominio Aerodinámico ---')
print()
print('Ángulo de ataque inicial(grados):')
start_alpha_angle = cuestionario_float(-20)
print('Ángulo de ataque final:')
finish_alpha_angle = cuestionario_float(start_alpha_angle)
print('Espaciado entre ángulos de ataque de estudio:')
alpha_angle_step = cuestionario_float(0)

aero_domain = (start_alpha_angle, finish_alpha_angle, alpha_angle_step)
    
    
#-- Optimization objectives
print()
print('--- Objetivos de optimización ---')
print()
print('Importancia del coeficiente de sustentación:')
lift_coefficient_weight = cuestionario_float(-1)
print('Importancia de la eficiencia aerodinámica:')
efficiency_weight = cuestionario_float(-1)

weighting_parameters = (lift_coefficient_weight, efficiency_weight)

#-- Final results options
print()
print('--- Dominio Aerodinámico ---')
print()
print('Número de ganadores del algoritmo')
num_winners = cuestionario(1)
print('Desea generar dibujos de los ganadores? (s/n)')
draw_winners = cuestionario_s_n()
print('Desea generar gráficas de las polares? (s/n)')
draw_polars = cuestionario_s_n()
print('Desea generar gráficas de la evolución? (s/n)')
draw_evolution = cuestionario_s_n()
print('Desea comparar los resultados con dos perfiles NACA?')
compare_naca_standard = cuestionario_s_n()
print()
compare_naca_custom = True #Work in progress
create_report = True       #Work in progress

end_options = (draw_winners, draw_polars, draw_evolution, 
           compare_naca_standard, compare_naca_custom, 
               create_report)
             
             
             
all_parameters = (airfoils_per_generation, total_generations, num_parent,
                      num_winners, weighting_parameters, end_options,
                      ambient_data, aero_domain )   
                      
print()
print('--- Iniciando algoritmo ---')
print()

main.main_program(all_parameters)

