%% how to run a python file from matlab
%wing_example = pyrunfile('flying_wing_example.py', 'wing_example', input1 = 5, input2 = 7);

%% How to do repeated optimizations for different height above ground (dz or h)
FL_0 = 16.055; %with twist =2 and dz =-100
options = optimoptions('fmincon','Display','iter');

xstar = [];
fstar = [];

for dz = linspace(0.8, 16, 10) % from h/b 0.1 to 2 with 10 total values
    dz = -dz; % python script expects negative value
    %twist = -twist; % python script expects negative value
    obj_fun = @(tw) (pyrunfile('objective_fun.py', 'FL', twist = tw, dz = dz) - FL_0)^2;

    [xstar, fstar] = fmincon(obj_fun,2,[],[],[],[],-10,10);
    
    % save values to list/array
    % expect fstar values to be =0
    xstar.append(xstar)
    fstar.append(fstar)

end





