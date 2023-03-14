# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:02:46 2022

@author: Parina
"""

#from pyDOE import lhs
import matplotlib.pyplot as plt
import json 
import numpy as np
import machupX as MX

with open('flying_wing_c.json', 'r') as openfile:
    
    flying_wing_mod = json.load(openfile)

fd = []
fl = []
      
for i in range(-1,35):
    flying_wing_mod["wings"]["main_wing"]["dihedral"] = i

    with open("flying_wing.json", "w") as outfile:
      json.dump(flying_wing_mod, outfile)
      
    # The input file will contain the path to the aircraft file.
    input_file = "flying_wing_input.json"

    # Initialize Scene object.
    my_scene = MX.Scene(input_file)

    #To make sure we know where each lifting surface 
    # is, we'll set show_legend to true.
    my_scene.display_wireframe(show_legend=True)

    # Let's see what forces are acting on the airplane. We'll output just the total
    # dimensional forces and moments acting on the airplane.
    FM_results = my_scene.solve_forces(dimensional=True, non_dimensional=False, verbose=True)
    print(json.dumps(FM_results["flying_wing"]["total"], indent=4))

    # MachUpX will default to using the 'elevator' control to trim out the airplane. We can use set_trim_state 
    # to have MachUpX set the trim state to be the new state of the airplane.
    trim_state = my_scene.pitch_trim(set_trim_state=True, verbose=True)
    print(json.dumps(trim_state["flying_wing"], indent=4))

    # Now that we're trimmed, let's see what our aerodynamic derivatives are.
    derivs = my_scene.derivatives()
    print(json.dumps(derivs["flying_wing"], indent=4)) 
    
    fd.append(FM_results["flying_wing"]["total"]["FD"])
    fl.append(FM_results["flying_wing"]["total"]["FL"])

print("Drag Force:", fd)
print("Lift Force:", fl)    

dihedral = list(range(-1,35))

# plt.scatter(fd, fl)
# plt.xlabel("Drag Force")
# plt.ylabel("Lift Force")
# plt.title("Drage Force vs. Lift Force")

plt.plot(dihedral, fd)
plt.xlabel("Dihedral(\u03C9)")
plt.ylabel("Drag Force")
plt.title("Dihedral vs. Drag Force")

# plt.plot(dihedral, fl)
# plt.xlabel("Dihedral (\u03C9)")
# plt.ylabel("Lift Force")
# plt.title("Dihedral vs. Lift Force")