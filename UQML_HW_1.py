'''
Olshefski, Kristopher
Uncertainty Quantification and Machine Learning
Homework #1
Python and Latex Basics
'''

# standard library imports
# import tempfile
import os
# import shutil
# import sys

# third party imports
import scipy as sp
import numpy as np
# from scipy.integrate import ode

#python plotting
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


# Define the input file
input_file = './heat.in'
# Function for reading input file
def read_input_data(input_file):
    """ Parse an input file into a dictionary.

    The input file should contain two entries per line separated by
    any number of white space characters or ':' or '='. Comments are
    indicated with '#'. Each non-empty, non-comment, line is stored
    in the output dictionary with the first entry as the key (input name)
    and the second as the argument(input value). Both keys and arguments
    are strings.

    Parameters
    ----------
    input_file : str
        Name of the input file.

    Returns
    -------
    param_dict : dict
        Dictionary containing input names and values.
    """
    param_dict = {}
    try:
        file = open(input_file, "r")
    except IOError:
        print('Cannot open file: {}'.format(input_file))
        sys.exit(1)
    else:
        for line in file:
            # remove comments and trailing/leading whitespace
            line = line.split('#', 1)[0]
            line = line.strip()
            # ignore empty or comment lines
            if not line:
                continue
            # allow ":" and "=" in input file
            line = line.replace(':', ' ').replace('=', ' ')
            # parse into dictionary
            param, value = line.split(None, 1)
            param_dict[param] = value
        file.close()
    return param_dict

#   Create data directories
if not os.path.exists('./postprocessing'):
    os.mkdir('./postprocessing')
#*****************************************
#        Read & Parse Input File
#*****************************************
print('reading input file')
param_dict = read_input_data(input_file)
# Domain size
lx = int(param_dict['Lx'])
ly = int(param_dict['Ly'])
# Mesh Size
nx = int(param_dict['Nx'])
ny = int(param_dict['Ny'])
# Time step
dt = float(param_dict['dt'])
# End Time
t_end = int(param_dict['t_end'])
# Diffusion Coefficient
eps = float(param_dict['eps'])
# Define the grid
x = np.linspace(0,lx,nx)
y = np.linspace(0,ly,ny)
# Grid step size
dx = np.float(nx/lx)
dy = np.float(ny/ly)
# Check stability criteria and adjust timestep (value should be .leq. 0.5)
stab = dt/(dx**2) + dt/(dy**2)
print('Stability value = ', stab)
# Initialize temp array
print('Initializing, Setting ICs, Setting BCs')
u     = np.zeros((nx+2,ny+2))
u_new = np.zeros((nx+2,ny+2))
# Boundary Conditions
u[ 1,:] = u[0, :] # Top Wall
u[-2,:] = u[-1,:] # Btm Wall
u[: ,1] = u[:, 0] # Left Wall
u[:,-2] = u[:,-1] # Right Wall
# Initial Conditions
# for i in range(nx):
#     for j in range(ny):
#         if (i < eps and i > -eps):
#             u[i,j] = 1. / (2.*eps)
#         else:
#             u[i,j] = 0.
# Circular heat concentration
for i in range(nx):
    for j in range(ny):
        if ( (i*dx-50)**2+(j*dy-50)**2 <= 5):
            u[i,j] = 1
        else:
            u[i,j] = 0
# Initialize time for iterating and counter for plotting
t= 0.
cnt = 0
print('Beginning time loop')
while t <= t_end:
    u_new[1:-1, 1:-1] = u[1:-1, 1:-1] + dt*(
                (u[2:, 1:-1] - 2*u[1:-1, 1:-1] + u[:-2, 1:-1])/dx**2 +
                (u[1:-1, 2:] - 2*u[1:-1, 1:-1] + u[1:-1, :-2])/dy**2 )
    time = str(round(t,2))
    u[:,:] = u_new[:,:]
    pct = str(round(t/t_end*100,2))
    if cnt == 0:
        print(pct,'% complete')
        plt.pcolormesh(u[1:-2,1:-2])
        plt.colorbar()
        plt.xlabel('Lx')
        plt.ylabel('Ly')
        plt.title('Heat Equation of 2D Plate')
        plt.savefig('./postprocessing/'+'image_' + pct + '.png')
    elif cnt == int(10*t_end):
        print(pct,'% complete')
        plt.pcolormesh(u[1:-2,1:-2])
        plt.xlabel('Lx')
        plt.ylabel('Ly')
        plt.title('Heat Equation of 2D Plate')
        plt.savefig('./postprocessing/'+'image_' + pct + '.png')
        cnt = 0     # Reset counter
    cnt += 1
    t = t+dt

# final_T = u[50,50]
# u_an = ( 1. / np.sqrt(4. * np.pi * t_end) ) \
# * np.exp(-50**2 / (4 * t_end))
# print('error % = ',str(((u_an-final_T)/u_an)*100))
