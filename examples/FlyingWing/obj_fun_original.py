# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:02:46 2022

@author: Parina
"""

twist = 2
dz = -100

import json 
import machupX as MX

with open('flying_wing_c.json', 'r') as openfile:
    
    flying_wing_mod = json.load(openfile)
 
# Instead of dihedral, change twist value and dz value 
 # Check signs when calling in Matlab     

# twist = flying_wing_mod["wings"]["main_wing"]["twist"] 
# dz = flying_wing_mod["wings"]["main_wing"]["dz"] 

# -twist = flying_wing_mod["wings"]["mirrored_wing"]["twist"] 
# -dz = flying_wing_mod["wings"]["mirrored_wing"]["dz"]

flying_wing_mod["wings"]["main_wing"]["twist"] = twist
flying_wing_mod["wings"]["main_wing"]["connect_to"]["dz"] = dz

flying_wing_mod["wings"]["mirrored_wing"]["twist"] = -twist
flying_wing_mod["wings"]["mirrored_wing"]["connect_to"]["dz"] = -dz

with open("flying_wing_c.json", "w") as outfile:
  json.dump(flying_wing_mod, outfile)
  
input_file = "flying_wing_input.json"

my_scene = MX.Scene(input_file)

# my_scene.display_wireframe(show_legend=True)

FM_results = my_scene.solve_forces(dimensional=True, non_dimensional=False, verbose=True, report_by_segment = True)

# trim_state = my_scene.pitch_trim(set_trim_state=True, verbose=True)

# derivs = my_scene.derivatives()

fl = FM_results["flying_wing"]["inviscid"]["FL"]["main_wing_left"] + FM_results["flying_wing"]["inviscid"]["FL"]["main_wing_right"]

fd = FM_results["flying_wing"]["inviscid"]["FD"]["main_wing_left"] + FM_results["flying_wing"]["inviscid"]["FD"]["main_wing_right"]