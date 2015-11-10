'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is the testing subprogramme. Its objective is to check if a 
new airfoil genome would make a real, viable one. In ordr to do so,
it runs 3 test in increasing level of complexity.

'''




import algoritmo.transcript as transcript
import numpy as np
from scipy import interpolate

def increasing_test(array):
    '''Checks wheter a certain array is monotone increasing.
    '''
    numele = np.shape(array)[0]
    if np.array_equal(np.argsort(array), np.arange(0, numele, 1)):
        return True
    else:
        return False
    

def decreasing_test(array):
    '''Checks wheter a certain array is monotone decreasing.
    '''
    numele = np.shape(array)[0]
    if np.array_equal(np.argsort(array), np.arange(numele-1, -1, -1)):
        return True
    else:
        return False
    
def x_coordinate_test(genome):
    '''Cheks wheter the x coordinate of the points that a given genome
    would generate get smaller at the airfoil upper side, as we go
    from the tail to the nose, and viceversa for the lower side.
    '''
    perfil = transcript.decode_genome(genome[:])
    test1 = decreasing_test(perfil[0:25, 0])
    test2 = decreasing_test(perfil[25:50, 0])
    test3 = increasing_test(perfil[50:75, 0])
    test4 = increasing_test(perfil[75:100, 0])
    
    if (test1 * test2 * test3 * test4):
        return True
    else:
        return False
        
def test_simple (genome):
    '''Test simple genome characteristics, such as the upper surface point
    being above the lower surface point.
    '''
    test1 = (genome[14] - genome [0]) > (5*np.pi/180)
    test2 = genome[3] > genome[10]
    test3 = genome[7] > 0.01
    test4 = genome[8] > 0.01
    test5 = genome[1] > 0.01
    test6 = genome[15] > 0.01
    test7 = genome[0] > (np.pi * 0.6)
    test8 = genome[0] < (np.pi * 1.4)
    
    if (test1 * test2 * test3 * test4 * test5 * test6 * test7 * test8):
        return True
    else:
        return False
        
def collision_test(genome):
    '''Interpolates two curves for the upper and the lower surfaces. 
    Then, check that the distance between them is larger than 0.01 times 
    the chord.
    '''
    
    
    perfil = transcript.decode_genome(genome[:])

    extrax = np.append(perfil[40:25:-1,0],perfil[24:5:-1,0])
    extray = np.append(perfil[40:25:-1,1],perfil[24:5:-1,1])

    intrax = np.append(perfil[60:74,0],perfil[75:98,0])
    intray = np.append(perfil[60:74,1],perfil[75:98,1])

    extrados = interpolate.InterpolatedUnivariateSpline(extrax, extray, k=1)
    intrados = interpolate.InterpolatedUnivariateSpline(intrax, intray, k=1)

    ver = np.linspace(0.1, 0.9, 50)
    very = extrados(ver) - intrados(ver)
    
    return (very > 0.01 ). all()
        
def airfoil_test(genome):
    '''Run 3 test of increasing complexity to detect inviable airfoils
    '''
    if test_simple(genome):
        if x_coordinate_test(genome):
            if collision_test(genome):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
    
    