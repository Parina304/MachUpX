# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:02:46 2022

@author: Parina
"""

twist = 2
dz = -100

import json 
import machupX as MX
import numpy as np
from scipy.optimize import minimize

def obj_fun(twist, dz):
    
    with open('flying_wing_c.json', 'r') as openfile:
    
        flying_wing_mod = json.load(openfile)
    
    flying_wing_mod["wings"]["main_wing"]["twist"] = twist
    flying_wing_mod["wings"]["main_wing"]["connect_to"]["dz"] = dz
    
    flying_wing_mod["wings"]["mirrored_wing"]["twist"] = -twist
    flying_wing_mod["wings"]["mirrored_wing"]["connect_to"]["dz"] = -dz
    
    with open("flying_wing_c.json", "w") as outfile:
        
      json.dump(flying_wing_mod, outfile)
      
    input_file = "flying_wing_input.json"
    
    my_scene = MX.Scene(input_file)
    
    FM_results = my_scene.solve_forces(dimensional=True, non_dimensional=False, verbose=True, report_by_segment = True)
    
    fl = FM_results["flying_wing"]["inviscid"]["FL"]["main_wing_left"] + FM_results["flying_wing"]["inviscid"]["FL"]["main_wing_right"]
    
    fd = FM_results["flying_wing"]["inviscid"]["FD"]["main_wing_left"] + FM_results["flying_wing"]["inviscid"]["FD"]["main_wing_right"]
    
    return fl

FL_0 = 16.055; # with twist=2 and dz=100

xstar = [];
fstar = [];

for dz in np.linspace(0.8, 16, 10): # from h/b 0.1 to 2 with 10 total values
    dz = -dz; # python script expects negative value
    fun = lambda tw: (obj_fun(tw,dz) - FL_0)**2

    x, f = minimize(fun, 16.055, args=(), method='trust-constr', constraints=(), tol = 0.000000000000000001) 
    
    xstar.append(xstar) #save values to list/array
    fstar.append(fstar) #expect fstar values to be =0