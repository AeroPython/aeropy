# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is the python script that contains those functions that are necesary 
in order to get a xfoil-compatible description of a profile from the 
genetic information provided by the interface script.

When this spript is run independly, will return an draw of a profile
calculated from an example genome.

When used inside the algorithm, the interface will import these functions
and call the "decode_genome" function with an array of genes. The function shall
return an xfoil-compatible description.

The complete Genetic Algorithm here used is explained at:
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

"""


import numpy as np


def bernstein(u):
    '''This function returns a 4x2 array. Both columns are equal.
    In each row, the value of a 3rd degree Bernstein polinome is 
    calculated for the given value of the parameter u.
    This structure allows the result array to be multiplied element
    by element with another 4x2 array containing the coordinates
    of the control points.
    '''
    b = np.zeros([4,2])
    b[0,:] =         (1-u)**3
    b[1,:] = (u    * (1-u)**2)*3
    b[2,:] = (u**2 * (1-u)   )*3
    b[3,:] =  u**3
    
    return b

                 
def punto_pendiente(a,dist,ang):
    '''Given a point "a", calculates the coordinates of another one
    placed at a distance "dist" in the direction"ang" (in radians).
    '''
    punto = np.array(a)+ np.array(dist,dist)* [np.cos(ang),np.sin(ang)]
    return punto


def generador_puntos(genes):
    '''This function is the first step decoding the profile genome:
    it generates the 13x2 coordinates of the points used in the 4
    bezier curves that describe the profile.
    '''
    puntos = np.zeros([13,2])
    puntos[0,:] = [1,0]
    puntos[1,:] = punto_pendiente([1,0],genes[1],genes[0])
    puntos[2,:] = punto_pendiente([genes[2],genes[3]],genes[5],genes[4])
    puntos[3,:] = [genes[2],genes[3]]
    puntos[4,:] = punto_pendiente([genes[2],genes[3]],genes[6],genes[4]+np.pi)
    puntos[5,:] = [0, genes[7]]
    puntos[6,:] = [0,0]
    puntos[7,:] = [0, -genes[8]]
    puntos[8,:] = punto_pendiente([genes[9],genes[10]], genes[12], genes[11]+np.pi)
    puntos[9,:] = [genes[9],genes[10]]
    puntos[10,:] = punto_pendiente([genes[9],genes[10]], genes[13], genes[11])
    puntos[11,:] = punto_pendiente([1,0], genes[15], genes[14])
    puntos[12,:] = [1,0]
    return puntos

def bezier(num, puntos_control):
    '''This function calculates a Bezier curve using as control 
    points those given in the imput, with a resolution of "num" points.
    '''
   
    parametro_u = np.linspace(0,1,num)
    curva = np.zeros([num,2])

    for contador in np.arange(num):
        _ = bernstein(parametro_u[contador])*puntos_control
        curva[contador,] = sum (_)
    return curva

def profile(num, puntos_control):
    
    '''This is the second stage of the decoding process.
    This will return a line made of 4 bezier curves whose control points
    are given in the imput. 
    Each curve will have a number of points equal to "num", so the total 
    number of points will be 4 * num'''
    
    perfil = np.zeros([(4*num), 2])

    perfil[0:num,:] = bezier(num,puntos_control[0:4,:])
    perfil[num:2*num,:] = bezier(num,puntos_control[3:7,:])
    perfil[2*num:3*num,:] = bezier(num,puntos_control[6:10,:])
    perfil[3*num:4*num,:] = bezier(num,puntos_control[9:13,:])
    
    return perfil
def decode_genome(genome):
    '''
    '''
    num = 25
    epsilon = 0.001
    profile_points = profile(num, generador_puntos(genome))
    
    profile_points[0, 1] = epsilon 
    profile_points[4*num-1,1] = -epsilon
    return profile_points

'''
The following code contains an example and will be used with test purposes only,
when this script is run whole and won't be used in the standard function of the 
genetic algorithm.
'''
#
#import matplotlib.pyplot as plt
#
#  
#genes = np.array([150*np.pi/180, #ang s1
#                  0.2,           #dist s1
#                  0.5,           #x 1
#                  0.12,          #y 1
#                  0,             #ang 1
#                  0.2,           #dist b1
#                  0.2,           #dist c1
#                  0.1,           #dist a1
#                  0.05,          #dist a2
#                  0.4,           #x 2
#                  0.05,          #y 2
#                  5*np.pi/180,   #ang 2
#                  0.2,           #dist b2 
#                  0.2,           #dist c2
#                  160*np.pi/180, #ang s2
#                  0.2])          #dist s2
#

#
#perfil = decode_genome(genes)
#
#
#plt.figure(num=None, figsize=(18, 6), dpi=80, facecolor='w', edgecolor='k')
#plt.plot(perfil[:,0],perfil[:,1])
#plt.gca().set_aspect(1)
