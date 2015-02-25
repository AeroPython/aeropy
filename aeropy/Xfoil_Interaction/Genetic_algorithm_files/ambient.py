'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is the main program. It will call the different submodules
and manage the data transfer between them in order to achieve the
genetic optimization of the profile.

'''




import numpy as np





def ventana (x, inicio=0, fin=1, f=1.):
    _1 = (np.sign(x-inicio))
    _2 = (np.sign(-x+fin))
    return 0.25 * (_1+1) * (_2+1) * f
    
def etc (x, inicio=0, f=1.):
    _1 = (np.sign(x-inicio))
    return 0.5 * (_1+1) * f

def earth_conditions():
    heights = np.array([-1.000,
                        11.019,
                        20.063,
                        32.162,
                        47.350,
                        51.413,
                        71.802,
                        86.000,
                        90.000])
  

    # an es el gradiente válido entre H(n-1) y H(n)
    temp_gradient = np.array([-6.49,
                               0,
                               0.99,
                               2.77,
                               0,
                              -2.75,
                              -1.96,
                               0,
                               0])
     

    
    atm_layer = temp_gradient.shape[0]
    
    temp_points = np.zeros([atm_layer])
    temp_points[0] = 294.64
    for layer in np.arange(1, atm_layer, 1):
        temp_points[layer] = temp_points[layer-1] + temp_gradient[layer-1]*(heights[layer]-heights[layer-1])
    gravity = 9.8
    gas_R = 287
    planet_radius = 6371
    p0 = 113922
    
    conditions = (heights, temp_gradient, temp_points, gravity, gas_R, planet_radius, p0)
    
    return conditions
    
    
def temperatura(h, conditions, dT = 0):
        '''Calcula la temperatura a una altura h en Km sobre el nivel del mar'''
        grad = 0
        heights = conditions[0]
        gradient = conditions[1]
        atm_layer = gradient.shape[0]
        temp_points = conditions[2]
        
        
        
        for layer in np.arange(0, atm_layer-1,1):
            increase = temp_points[layer] + gradient[layer] * (h - heights[layer])
            grad = grad + ventana(h, heights[layer],heights[layer+1], increase)
        grad = grad + etc(h, heights[atm_layer-1],temp_points[atm_layer-1] + gradient[atm_layer-1]*(h - heights[atm_layer-1]))
        return grad + dT
     
        
def segmento_presion_1(z, pi, z0, dT, conditions):
        '''calcula la presión en un segmento de atmósfera de temperatura constante'''
        g = conditions[3]
        R = conditions[4]
        radius = conditions[5]
        h  = (radius * z) /(radius + z)
        h0 = (radius * z0)/(radius + z0)
        _ = 1000*(h-h0) * g / (R * temperatura(z, conditions, dT))
        return pi * np.e ** -_
            
def segmento_presion_2(z, pi, Ti, a, dT, conditions):
        '''calcula la presión en un segmento de atmósfera con gradiente de temperatura "a" '''
        g = conditions[3]
        R = conditions[4]
        _ = g / (a*R/1000)
        return pi * (temperatura(z, conditions, dT)/(Ti + dT)) ** -_
                
def presion (h, conditions,  dT = 0):
        '''Calcula la presion en Pa a una altura h en m sobre el nivel del mar'''
        
        heights = conditions[0]
        gradient = conditions[1]
        temp_points = conditions[2]
        atm_layer = gradient.shape[0]
        #Primero, calculamos la presion de cada punto de cambio de capa para la condición de dT pedida
        #Suponemos que la presión es siempre constante a 101325 Pa a nivel del mar
        
        
        pressure_points = np.zeros([atm_layer])
        pressure_points[0] = conditions[6]
        
        for layer in np.arange(1, atm_layer, 1):
            if (abs(gradient[layer-1]) < 1e-8):
                pressure_points[layer] = segmento_presion_1(heights[layer],
                                                            pressure_points[layer - 1],
                                                            heights[layer - 1],
                                                            dT, conditions)
            else:
                pressure_points[layer] = segmento_presion_2(heights[layer],
                                                            pressure_points[layer - 1],
                                                            temp_points[layer - 1],
                                                            gradient[layer-1],
                                                            dT, conditions)
#        
        
        #A partir de estos datos, construímos la atmósfera en cada capa
        
        grad = 0
        for layer in np.arange(1, atm_layer, 1):
            if (abs(gradient[layer-1]) < 1e-8):
                funcion = segmento_presion_1(h,
                                             pressure_points[layer - 1],
                                             heights[layer - 1],
                                             dT, conditions)
            else:
                funcion = segmento_presion_2(h,
                                             pressure_points[layer - 1],
                                             temp_points[layer - 1],
                                             gradient[layer-1],
                                             dT, conditions)
            grad = grad + ventana(h, heights[layer-1], heights[layer], funcion)
        if (abs(gradient[layer-1])< 10e-8):
            funcion = segmento_presion_1(h,
                                         pressure_points[layer - 1],
                                         heights[layer - 1],
                                         dT, conditions)
        else:
            funcion = segmento_presion_2(h,
                                         pressure_points[layer - 1],
                                         temp_points[layer - 1],
                                         gradient[layer-1],
                                         dT, conditions)
        
        grad = grad + etc(h, heights[atm_layer - 1], funcion)
        return grad
    

def densidad(h, conditions, dT = 0):
        '''Calcula la densidad a una altura h en m sobre el nivel del mar'''
        R = conditions[4]
        return presion(h, conditions, dT)/(R * temperatura(h, conditions, dT))
        
        
def mars_conditions():
    heights = np.array([-8.3,
                         8.85,
                         30]) 

    # an es el gradiente válido entre H(n-1) y H(n)
    temp_gradient = np.array([-2.22,
                              -0.998,
                              -0.998])    

    
    atm_layer = temp_gradient.shape[0]
    
    temp_points = np.zeros([atm_layer])
    temp_points[0] = 268.77
    for layer in np.arange(1, atm_layer, 1):
        temp_points[layer] = temp_points[layer-1] + temp_gradient[layer-1]*(heights[layer]-heights[layer-1])
    gravity = 3.711
    gas_R = 192.1
    planet_radius = 3389
    p0 = 1131.67
    
    conditions = (heights, temp_gradient, temp_points, gravity, gas_R, planet_radius, p0)
    
    return conditions
    


def viscosidad(temp, planet):
    if (planet == 'Earth'):
        c = 120
        lamb = 1.512041288
    elif(planet == 'Mars'):
        c = 240
        lamb =  	1.572085931
        
    visc = lamb * temp**1.5 / (temp + c)
    return visc   
    
    
def Reynolds(dens, longitud, vel, visc):
    re = 1000000 * dens * longitud * vel / visc
    return re

            
def aero_conditions(ambient_data):
    (planet, chord, height, speed_type, speed) = ambient_data
    planet_dic = {'Mars':mars_conditions(), 'Earth':earth_conditions()}
       
    
    sound = (1.4 *presion(height, planet_dic[planet]) / densidad(height,planet_dic[planet]))**0.5
    
    if (speed_type == 'mach'):
        mach = speed
        vel = mach * sound
    elif (speed_type == 'speed'):
        mach = speed / sound
        vel = speed
    else:
        print('error in the data, invalid speed parameter')
        
    
    
    re = Reynolds(densidad(height, planet_dic[planet]), chord, vel, viscosidad(temperatura(height, planet_dic[planet]), planet))
    
  
    
    return [mach, re]
#
#ambient_data = ('Earth', 03.0003, 11, 'speed', 30.1) 
#
#result = aero_conditions(('Earth', 0.03, 11, 'mach', 0.1))       
#print(result)      