
# coding: utf-8


import numpy as np

#las funciones Ventana y Etc se usan para modular las funciones parciales,
#ya que el modelo ISA está definido a trozos

def ventana (x, inicio=0, fin=1, f=1.):
    '''
    Devuelve una función que es f en el intervalo entre inicio y fin,
    y 0 en el resto. en inicio y fin exactamente, devuelve f/2 '''    
    _1 = (np.sign(x-inicio))
    _2 = (np.sign(-x+fin))
    return 0.25 * (_1+1) * (_2+1) * f

def etc (x, inicio=0, f=1.):
    '''
    Devuelve una función que es f desde inicio en adelante,
    y 0 desde -infinito a inicio'''
    _1 = (np.sign(x-inicio))
    return 0.5 * (_1+1) * f



#Definición de parámetros clave del modelo ISA: 
#Altura de cambio de capas (en metros)
#Gradiente de temperatura en cada capa (en k/metro)
#Temperatura al inicio de cada capa (calculada a partir de laas anteriores)

H0 =     0
H1 = 11019
H2 = 20063
H3 = 32162
H4 = 47350
H5 = 51413
H6 = 71802
H7 = 86000
H8 = 90000 #límite de validez aproximado del modelo (aproximado, pendiente de comprobación)

# an es el gradiente válido entre H(n-1) y H(n)
a1 = -6.49 /1000
a2 =  0
a3 =  0.99 /1000
a4 =  2.77 /1000
a5 =  0
a6 = -2.75 /1000
a7 = -1.96 /1000
a8 = 0
aext = 0 #Para permitir que las operaciones continúen fuera del rango de validez del modelo,
         #propagamos las condiciones del último tramo de manera indefinida (modelo falso)

T0 = 288.15
T1 = T0 + a1 *  H1
T2 = T1 + a2 * (H2-H1)
T3 = T2 + a3 * (H3-H2)
T4 = T3 + a4 * (H4-H3)
T5 = T4 + a5 * (H5-H4)
T6 = T5 + a6 * (H6-H5)
T7 = T6 + a7 * (H7-H6)
T8 = T7 + a8 * (H8-H7)

#Con estos datos, ya podemos construir la función de temperaturas:

def temperatura (h, dT = 0):
    '''Calcula la temperatura a una altura h en m sobre el nivel del mar,
    para una atmósfera ISA con una temperatura + dt'''
    
    grad =        ventana (h, H0, H1, T0 + a1*(h - H0)) #Troposfera
    grad = grad + ventana (h, H1, H2, T1 + a2*(h - H1)) #Tropopausa
    grad = grad + ventana (h, H2, H3, T2 + a3*(h - H2)) #Estratosfera baja
    grad = grad + ventana (h, H3, H4, T3 + a4*(h - H3)) #Estratosfera alta
    grad = grad + ventana (h, H4, H5, T4 + a5*(h - H4)) #Estratopausa
    grad = grad + ventana (h, H5, H6, T5 + a6*(h - H5)) #Mesosfera baja
    grad = grad + ventana (h, H6, H7, T6 + a7*(h - H6)) #Mesosfera alta
    grad = grad + ventana (h, H7, H8, T7 + a8*(h - H7)) #Mesopausa (límite sin comprobar)
    grad = grad + etc     (h, H8,     T8 + aext*(h - H8)) #Modelo sin completar más allá de la mesopausa
    return grad + dT

#La función de presión también está definida a trozos. En cada trozo se usa una de
#las dos siguientes funciones, dependiendo de si la temperatura en el segmento es
#constante o no.

def segmento_presion_1(z, pi, z0, dT):
    '''calcula la presión en un segmento de atmósfera de temperatura constante
    
    z es la altura en m sobre el nivel del mar del punto cuya presión 
    queremos calcular.
    
    z0 es la altura de la que se tienen datos, a partir de la que se 
    calculan todos los demás puntos. Normalmente es el punto en el que
    comienza la capa actual.
    
    pi es la presión en el punto z0
    
    dt es el modificador de la temperatura ISA, en grados centígrados o kelvin'''
    g = 9.8066
    R = 287
    h  = (6371000 * z) /(6371000 + z)
    h0 = (6371000 * z0)/(6371000 + z0)
    _ = (h-h0) * g / (R * temperatura(z, dT))
    return pi * np.e ** -_

def segmento_presion_2(z, pi, Ti, a, dT):
    '''calcula la presión en un segmento de atmósfera con gradiente de temperatura "a"
    
    z es la altura en m sobre el nivel del mar del punto cuya presión 
    queremos calcular.
    
    De manera implícita, se asume que existe una z0, que
    es la altura de la que se tienen datos, a partir de la que se 
    calculan todos los demás puntos. Normalmente es el punto en el que
    comienza la capa actual. La altura de este punto no entra como argumento,
    pero sí las condiciones de presión y temperatura en dicho punto. 
    La distancia entre z0 y el punto que estamos calculando se resuelve 
    de manera implícita mediante la diferencia de temperaturas entre ambos,
    conocido el gradiente "a".
    
    pi es la presión en el punto z0.
    
    Ti es la temperatura en el punto z0
    
    a es el gradiente de temperatura en el segmento actual, en ºC o kelvin / metro
    
    dt es el modificador de la temperatura ISA, en grados centígrados o kelvin '''
    g = 9.8066
    R = 287
    h = (6371000 * z)/(6371000 + z)
    _ = g / (a*R)
    return pi * (temperatura(z, dT)/(Ti + dT)) ** -_


#Con estas dos funciones, ya podemos construir la función completa de presiones:



def presion (h, dT = 0):
    '''Calcula la presion en Pa a una altura h en m sobre el nivel del mar,
    para una atmósfera ISA con una temperatura + dt'''
    
    #Primero, calculamos la presion de cada punto de cambio de capa para la condición de dT pedida
    #Suponemos que la presión es siempre constante a 101325 Pa a nivel del mar
    
    p0 = 101325
    p1 = segmento_presion_2(H1, p0,    T0, a1, dT)
    p2 = segmento_presion_1(H2, p1, H1,        dT)
    p3 = segmento_presion_2(H3, p2,    T2, a3, dT)
    p4 = segmento_presion_2(H4, p3,    T3, a4, dT)
    p5 = segmento_presion_1(H5, p4, H4       , dT)
    p6 = segmento_presion_2(H6, p5,    T5, a6, dT)
    p7 = segmento_presion_2(H7, p6,    T6, a7, dT)
    p8 = segmento_presion_1(H8, p7, H7       , dT)
    
    #A partir de estos datos, construímos la atmósfera en cada capa
    
    grad =        ventana (h, H0, H1, segmento_presion_2(h, p0,    T0, a1, dT)) #Troposfera
    grad = grad + ventana (h, H1, H2, segmento_presion_1(h, p1, H1,        dT)) #Tropopausa
    grad = grad + ventana (h, H2, H3, segmento_presion_2(h, p2,    T2, a3, dT)) #Estratosfera baja
    grad = grad + ventana (h, H3, H4, segmento_presion_2(h, p3,    T3, a4, dT)) #Estratosfera alta
    grad = grad + ventana (h, H4, H5, segmento_presion_1(h, p4, H4       , dT)) #Estratopausa
    grad = grad + ventana (h, H5, H6, segmento_presion_2(h, p5,    T5, a6, dT)) #Mesosfera baja
    grad = grad + ventana (h, H6, H7, segmento_presion_2(h, p6,    T6, a7, dT)) #Mesosfera alta
    grad = grad + ventana (h, H7, H8, segmento_presion_1(h, p7, H7       , dT)) #Mesopausa (límite sin comprobar)
    grad = grad + etc     (h, H8,     segmento_presion_1(h, p8, H8       , dT)) #Modelo sin completar más allá de la mesopausa
    return grad



#Mediante la ecuación de los gases perfectos, es fácil hallar le densidad
#a partir de la presión y la temperatura.

def densidad(h, dT = 0):
    '''Calcula la densidad a una altura h en m sobre el nivel del mar,
    para una atmósfera ISA con una temperatura + dt'''
    R = 287
    return presion(h)/(R * temperatura(h, dT))

#Por último, combinamos las tres funciones en una única función que devuelve los
#tres parámetros:

def atm(h, dT = 0):
    '''Calcula la temperatura en kelvin, la presión en Pascales y la densidad en
    Kg/metro cúbico, para un punto a una altura h en metros sobre el nivel del mar,
    para una atmósfera ISA+dt'''
    
    return temperatura(h, dT), presion(h, dT), densidad(h, dT)


#get_ipython().run_cell_magic('timeit', '', 'temperatura(np.linspace(0, 86, 10000))')
