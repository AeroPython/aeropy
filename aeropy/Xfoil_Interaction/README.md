aeropy - Xfoil Interaction tool
======

Python tools for Aeronautical calculations.

Genetic Optimization Algorithm in progress (python 3.4, xfoil 6.99)

Includes:

-Minimal working interface between Python and Xfoil

-Interactive Ipython notebook showing how the genome-to-profile decodification works (in progress). 

-Ipython notebook that can easily be used to save drawings of the airfoils generate. (Must be placed with the .py genetic algorithm files)

Genetic algorithm modules:

-interfaz

-transcript

-testing

-main 

-initial 

-genetics

-analice

-cross

-mutation

-selection

-ambient

All 11 files must be in the same folder as xfoil.exe. 

Execute the main.py file in order to start the algorithm. The main control paraparameters are defined here, and secondary parameters will be automatically calculated. 

It will randomly generate 30 profiles and test if they are viable, those wich aren't will be regenerated until they are.

They will be analiced with xfoil, and scored and sorted depending on the values they achieve.

Then, the best 3 will be selected as parents for the next generation.

More info: 
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

You can download Xfoil for free from its official page:
http://web.mit.edu/drela/Public/web/xfoil/