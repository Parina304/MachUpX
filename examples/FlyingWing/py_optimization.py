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
# import os
import matplotlib.pyplot as plt

# import sys
# sys.path.append('c:/users/parina/documents/machupx')

#%%

# Objective function to calculate an output when given twist and HAG. 
def obj_fun(twist,dz, output='CL'): #add extra input to decide what value is output
    
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
    
    # FM_results = my_scene.solve_forces(dimensional=True, non_dimensional=False, verbose=True, report_by_segment = True)
    
    # fl = FM_results["flying_wing"]["inviscid"]["FL"]["main_wing_left"] + FM_results["flying_wing"]["inviscid"]["FL"]["main_wing_right"]
    
    # fd = FM_results["flying_wing"]["inviscid"]["FD"]["main_wing_left"] + FM_results["flying_wing"]["inviscid"]["FD"]["main_wing_right"]
    
    FM_results = my_scene.solve_forces(dimensional=False, non_dimensional=True, verbose=True, report_by_segment = True)
    
    distributions_for_CDi = my_scene.distributions(dimensional=False, non_dimensional=True, verbose=True, report_by_segment = True)
    
    cd_i = sum(distributions_for_CDi["flying_wing"]["main_wing_left"]["CD_i"] + distributions_for_CDi["flying_wing"]["main_wing_right"]["CD_i"])
    
    cl = FM_results["flying_wing"]["inviscid"]["CL"]["main_wing_left"] + FM_results["flying_wing"]["inviscid"]["CL"]["main_wing_right"]
    
    cd = FM_results["flying_wing"]["inviscid"]["CD"]["main_wing_left"] + FM_results["flying_wing"]["inviscid"]["CD"]["main_wing_right"]
    
    if output=="CL": #Coefficient of lift
        return cl 
    elif output=="CD": #Coefficient of drag
        return cd 
    elif output=="CD_i": #Induced drag
        return cd_i
    else:
        print('error')
    
CL_0 = obj_fun(2, -100)
print("CL:", CL_0)

#%%   Main figure 1 (constant angle of attack, how does CL change as we get close to the ground?)

#Plot for lift force as a function of h/b
dz = np.linspace(0.1, 16, 30)
results = []
for value in dz:
    lift_force = obj_fun(2,-value)
    results.append(lift_force)

plt.figure()
plt.plot(dz/8, results)
plt.xlabel('h/b') # b=8 (wing span)
plt.ylabel('CL')
# plt.title("Lift Force as a Function of h/b")

#%%

# Plot for lift force as function of twist angle
alpha = np.linspace(-10,10,20)
fl_res = []
for i in alpha:
    FL_2 = obj_fun(i, -100)
    fl_res.append(FL_2)

plt.figure()
plt.plot(alpha, fl_res)
plt.xlabel('Twist Angle')
plt.ylabel('CL')
plt.title("(no ground effect)")  

#Notes:
#In flying_wing.json 
#Main Wing: twist = 10, dz = -0.1
#Mirrored Wing: twist = -10, dz = 0.1

#%% Optimization 

# CL_0 = 0.08443422032568976 # calculated above
xstar = []
fstar = []

dz = np.linspace(0.8, 16, 40)

for ii in dz:
    fun = lambda tw: (obj_fun(tw, -ii) - CL_0) ** 2

    sol = minimize(fun, 2.0, args=(), method='trust-constr', jac=None, hess=None, hessp=None,
                    bounds=[(-10,10)], constraints=(), tol=1e-18, callback=None, options=None)
    
    x, f = sol.x, sol.fun
    xstar.append(x)
    fstar.append(f)

#%%    Main figure 2 (if we allow angle of attack to change, can we match the ground effect CL with CL high above ground at angle of attack=2deg)

#Plot for Lift Force as a function of HAB with angle of attack held constant
# dz = np.linspace(0.8, 16, 40) # no need to redefine this

plt.figure()
plt.plot(dz/8, fstar)
plt.xlabel("h/b") # b=8 (wing span)
plt.ylabel(r"$(\Delta CL)^2$") # actually plotting the squared error here (want zero)
# plt.title("Lift force as a Function of Height Above Ground")
plt.show()


#%%    Main figure 3 (corresponding to the previous figure, what are the AoA values?)

plt.figure()
plt.plot(dz/8, xstar)
plt.xlabel("h/b") # b=8 (wing span)
plt.ylabel(r"$\alpha$")


#%%    Main figure 4 (corresponding to the previous two figures, what is the induced drag?)

CD_i = []

for ii in range(len(xstar)):
    CD_i.append(obj_fun(xstar[ii], -dz[ii], output='CD_i'))


plt.figure()
plt.plot(dz/8, CD_i)
plt.xlabel("h/b") # b=8 (wing span)
plt.ylabel(r"$CD_i$")












#%%   I think everything below here is old



# #Graph with heatmap

# FL_0 = 16.055
# dz_vals = np.linspace(0.8, 16, 40)
# tw_vals = np.linspace(-10, 10, 21)
# lift_vals = np.zeros((len(dz_vals), len(tw_vals)))

# for i, dz in enumerate(dz_vals):
#     for j, tw in enumerate(tw_vals):
#         fun = lambda tw: (obj_fun(tw, -dz) - FL_0) ** 2
#         sol = minimize(fun, tw, bounds=[(-10, 10)])
#         lift_vals[i, j] = sol.fun

# fig, ax = plt.subplots()
# im = ax.imshow(lift_vals.T, cmap='coolwarm', origin='lower', extent=[min(dz_vals), max(dz_vals), min(tw_vals), max(tw_vals)])
# cbar = ax.figure.colorbar(im, ax=ax)
# cbar.ax.set_ylabel('Lift Force', rotation=-90, va="bottom")
# ax.set_xlabel('Height Above Ground (m)')
# ax.set_ylabel('Angle of Attack (deg)')
# ax.set_title('Optimized Lift Force')
# plt.show()

# #%%
# Graph with lift force and HAB

# FL_0 = 16.055
# xstar = []
# fstar = []

# for dz in np.linspace(0.8, 16, 40):
#     dz = -dz
#     fun = lambda tw: (obj_fun(tw, dz) - FL_0) ** 2

#     sol = minimize(fun, 2.0, args=(), method='trust-constr', jac=None, hess=None, hessp=None,
#                     bounds=[(-10,10)], constraints=(), tol=1e-18, callback=None, options=None)
    
#     x, f = sol.x, sol.fun
#     xstar.append(x)
#     fstar.append(f)

# dz = np.linspace(0.8, 16, 40)
# plt.plot(xstar, fstar)
# plt.plot(dz, [FL_0] * len(dz))
# plt.xlabel("Height Above Ground")
# plt.ylabel("Lift Force")
# plt.title("Optimized lift Force as a Function of Height Above Ground")
# plt.show()

# #%%

# FL_0 = 16.055
# dz_vals = np.linspace(0.8, 16, 10)
# tw_vals = np.linspace(-10, 10, 21)
# lift_vals = np.zeros((len(dz_vals), len(tw_vals)))
# tw_opt_vals = np.zeros(len(dz_vals))

# for i, dz in enumerate(dz_vals):
#     for j, tw in enumerate(tw_vals):
#         fun = lambda tw: (obj_fun(tw, -dz) - FL_0) ** 2
#         sol = minimize(fun, tw, bounds=[(-10, 10)])
#         lift_vals[i, j] = sol.fun
#     j_opt = np.argmin(lift_vals[i, :])
#     tw_opt_vals[i] = tw_vals[j_opt]

# fig, ax = plt.subplots()
# ax.plot(dz_vals, tw_opt_vals, 'o-')
# ax.set_xlabel('Height Above Ground (m)')
# ax.set_ylabel('Angle of Attack (deg)')
# ax.set_title('Optimized Angle of Attack for Minimum Lift Force')
# plt.show()
