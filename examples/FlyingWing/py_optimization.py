# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:02:46 2022

@author: Parina
"""

# twist = 2
# dz = -16

import json 
import machupX as MX
import numpy as np
from scipy.optimize import minimize
import os
import matplotlib.pyplot as plt


#Objective function to calculate lift force when given twist and height above ground. 
def obj_fun(twist,dz):
    
    with open('flying_wing.json', 'r') as openfile:
        
        flying_wing_mod = json.load(openfile)
    
    flying_wing_mod["wings"]["main_wing"]["twist"] = float(twist)
    flying_wing_mod["wings"]["main_wing"]["connect_to"]["dz"] = float(dz)
    
    flying_wing_mod["wings"]["mirrored_wing"]["twist"] = float(-twist)
    flying_wing_mod["wings"]["mirrored_wing"]["connect_to"]["dz"] = float(-dz)
    
    with open("flying_wing_c.json", "w") as outfile:
        
      json.dump(flying_wing_mod, outfile)
      
    input_file = "flying_wing_input.json"
    
    my_scene = MX.Scene(input_file)
    
    FM_results = my_scene.solve_forces(dimensional=True, non_dimensional=False, verbose=True, report_by_segment = True)
    
    fl = FM_results["flying_wing"]["inviscid"]["FL"]["main_wing_left"] + FM_results["flying_wing"]["inviscid"]["FL"]["main_wing_right"]
    
    fd = FM_results["flying_wing"]["inviscid"]["FD"]["main_wing_left"] + FM_results["flying_wing"]["inviscid"]["FD"]["main_wing_right"]
    
    return fl

FL = obj_fun(2, -100)
print("Lift Force:", FL)

# #Plot for lift force as a function of h/b
# dz = np.linspace(0.1, 16, 30)
# results = []
# for value in dz:
#     lift_force = obj_fun(2,-value)
#     results.append(lift_force)
# plt.plot(dz, results)
# plt.xlabel('dz')
# plt.ylabel('Lift Force')
# plt.title("Lift Force as a Function of h/b")

# # Plot for lift force as function of twist angle
# fl = np.linspace(2,100,10)
# fl_res = []
# for i in fl:
#     FL_2 = obj_fun(i, -100)
#     fl_res.append(FL_2)
# plt.plot(fl, fl_res)
# plt.xlabel('Twist Angle')
# plt.ylabel('Lift Force')
# plt.title("Lift Force as a Function of Twist Angle")  

#Notes:
#In flying_wing.json 
#Main Wing: twist = 10, dz = -0.1
#Mirrored Wing: twist = -10, dz = 0.1

#Optimization 

FL_0 = 16.055
xstar = []
fstar = []

for dz in np.linspace(0.8, 16, 10):
    dz = -dz
    fun = lambda tw: (obj_fun(tw, dz) - FL_0) ** 2

    sol = minimize(fun, 2.0, args=(), method='trust-constr', jac=None, hess=None, hessp=None,
                    bounds=[(-10,10)], constraints=(), tol=1e-18, callback=None, options=None)
    
    x, f = sol.x, sol.fun
    xstar.append(x)
    fstar.append(f)
    
plt.plot(xstar, fstar)
plt.xlabel("h/b")
plt.ylabel("Lift Force")
plt.title("Lift force as a function of height above ground")
plt.show()


