# This script is for me to test the functionality of whatever I'm working on at the moment.
import machupX as MX
import json
import numpy as np
import subprocess as sp
import matplotlib.pyplot as plt
from stl import mesh
from mpl_toolkits import mplot3d

if __name__=="__main__":
    
    # Specify input
    input_dict = {
        "solver" : {
            "type" : "nonlinear",
        }
    }

    # Specify airplane
    airplane_dict = {
        "CG" : [0.0, 0.0, 0.0],
        "weight" : 50.0,
        "controls" : {
            "aileron" : {
                "is_symmetric" : False
            },
            "elevator" : {
                "is_symmetric" : True
            },
            "rudder" : {
                "is_symmetric" : False
            }
        },
        "airfoils" : {
            "NACA_4410" : "test/NACA_4410.json",
            "NACA_0010" : "test/NACA_0010.json"
        },
        "wings" : {
            "main_wing" : {
                "ID" : 1,
                "side" : "both",
                "is_main" : True,
                "semispan" : 4.0,
                "airfoil" : "NACA_0010",
                "ac_offset" : "kuchemann",
                "dihedral" : [[0.0, 20.0],
                              [0.3, 20.0],
                              [0.7, -20.0],
                              [1.0, -20.0]],
                "sweep" : [[0.0, 20.0],
                              [1.0, -20.0]],
                "control_surface" : {
                    "chord_fraction" : 0.1,
                    "root_span" : 0.5,
                    "control_mixing" : {
                        "aileron" : 1.0
                    }
                },
                "grid" : {
                    "N" : 40,
                    "reid_corrections" : True
                }
            },
            "h_stab" : {
                "ID" : 2,
                "side" : "both",
                "is_main" : False,
                "connect_to" : {
                    "ID" : 1,
                    "location" : "root",
                    "dx" : -3.0
                },
                "semispan" : 2.0,
                "airfoil" : "NACA_0010",
                "twist" : -2.1,
                "ac_offset" : "kuchemann",
                "sweep" : 45.0,
                "control_surface" : {
                    "chord_fraction" : 0.5,
                    "control_mixing" : {
                        "elevator" : 1.0
                    }
                },
                "grid" : {
                    "N" : 40,
                    "reid_corrections" : True
                }
            },
            "v_stab" : {
                "ID" : 3,
                "side" : "right",
                "is_main" : False,
                "connect_to" : {
                    "ID" : 1,
                    "location" : "root",
                    "dx" : -3.0,
                    "dz" : -0.1
                },
                "semispan" : 2.0,
                "dihedral" : 90.0,
                "airfoil" : "NACA_0010",
                "ac_offset" : "kuchemann",
                "sweep" : 45.0,
                "control_surface" : {
                    "chord_fraction" : 0.5,
                    "control_mixing" : {
                        "rudder" : 1.0
                    }
                },
                "grid" : {
                    "N" : 40,
                    "reid_corrections" : True
                }
            }
        }
    }

    # Specify state
    state = {
        "velocity" : 100.0,
        "alpha" : 5.0,
        "beta" : 0.0
    }
    control_state = {
        "elevator" : 0.0,
        "aileron" : 0.0,
        "rudder" : 0.0
    }

    # Load scene with Jackson's corrections
    scene = MX.Scene(input_dict)
    scene.add_aircraft("plane", airplane_dict, state=state, control_state=control_state)

    scene.display_wireframe(show_vortices=True)

    # Solve forces
    FM = scene.solve_forces(non_dimensional=False, verbose=True)
    print(json.dumps(FM["plane"]["total"], indent=4))

    ## Get derivatives
    #derivs = scene.aircraft_derivatives(wind_frame=False)
    #print(json.dumps(derivs["plane"], indent=4))