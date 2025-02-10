# Script: Soft Bending Actuator Geometry Creation for Dynamic Finite-Element Analysis
# Link to Publication: https://www.researchgate.net/publication/356419093_Dynamic_Finite-Element_analysis_of_a_soft_bending_actuator
# - This script generates the geometry for the soft bending actuator in preparation for dynamic analysis.
# - It creates a semi-circular fiber structure that will be used for the actuator's modeling.
# - The geometry is wrapped and positioned in 3D space to simulate the structure's physical behavior.
# - The actuator is constructed with a user-defined radius, length, and fiber angle.
# - Parameters such as fiber pitch and loop count are computed based on the actuator's dimensions.
# - The script divides the geometry into semi-circular segments for the fiber wrapping.
# - A reference point is defined at the origin for the actuator's fiber wrapping.
# - The actuator's geometry is then translated to a specified position in the assembly.
# - The final model consists of fiber paths wrapped around a semi-circular structure.
# - This script is focused on geometry creation and does not perform dynamic simulation.
# - All Input Required: Make sure to define the necessary parameters before running the script.


# Define parameters for the actuator geometry
Radius_of_Actuator = 10.000     # Radius of the actuator
Smoothen_wrapping = 3.0         # Fiber angle in degrees
Length_of_Actuator = 160.0      # Total actuator length
NODivision = 10                 # Divide Semi Circle into Segments for Radial Points Creation (Should be greater then 10)

#Move the Instance from Origion in Assembly
# If all three components are set to (0,0,0), the "Fiber Wrap" will coincide with global coordinate system of ABAQUS in assembly module
delta_x = 3.0                   # Translate the "Fiber Wrap" instance in Assembly module in Global X-Direction
delta_y = 5.0                   # Translate the "Fiber Wrap" instance in Assembly module in Global Y-Direction
delta_Z = 4.8                   # Translate the "Fiber Wrap" instance in Assembly module in Global Z-Direction

# Import All Libraries
from part import *
import math
import numpy as np
import bisect
from abaqus import *
from abaqusConstants import *

# Draw Point in Point Module (In ABAQUS)
p = mdb.models['Model-1'].Part(name='semi_circular_sp', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
# Assign Reference Point for Fiber
x_Coord, y_Coord, z_Coord = [0.0] * 3                   #This is to define coordinates
p.ReferencePoint(point=(x_Coord, y_Coord, z_Coord))     #This is to generate coordinates
p = mdb.models['Model-1'].parts['semi_circular_sp']     #This is to generate spiral
session.viewports['Myvp1'].setValues(displayedObject=p) #This is to display the generated part

# Rename The Origon (In ABAQUS)
mdb.models['Model-1'].parts['semi_circular_sp'].features.changeKey(fromName='RP', toName='Origin of First Semi Circle')

# Create a list of points in a semi-circle including 0 and 180 degrees
Polar_grid = np.deg2rad(np.arange(0, NODivision * 18 + 1, NODivision))  # Generate angles from 0 to 180 degrees (inclusive)

# Define fiber geometry
# Calculate fiber pitch based on geometry
# Calculate the fiber pitch, which is the distance between adjacent semi_circular_sp along the circumference.
# The formula uses the external radius and the fiber angle to determine the pitch.
fiber_pitch = 2.0 * np.pi * Radius_of_Actuator / np.tan(np.deg2rad(90.0 - Smoothen_wrapping))

# Determines the number of fiber loops fitting within the actuator length
# Calculate the number of fiber loops that can fit within the actuator length.
# This is done by dividing the actuator length by the fiber pitch and adding 1 to ensure full coverage.
num_loops = int(Length_of_Actuator / fiber_pitch) + 1

# Number of semi_circular_sp based on geometry
# Determine the number of semi_circular_sp based on the fiber angle.
# The formula uses a sine function to scale the number of semi_circular_sp and ensures at least one fiber is present.
num_semi_circular_sp = int(np.maximum(13.0 * np.sin(np.deg2rad(Smoothen_wrapping)) + 0.5, 1.0))

# Angular offset between semi_circular_sp
# Calculate the angular offset between each fiber.
# This ensures that semi_circular_sp are evenly spaced around the circumference.
fiber_angular_offset = np.pi / np.float64(num_semi_circular_sp)

# Compute z-offset for each loop based on pitch
# This function calculates the z-offset for each fiber loop.
# The z-offset is determined by multiplying the loop index by the fiber pitch.
# This ensures that each loop is positioned correctly along the z-axis based on its index
def compute_z_offset(loop_index):
    return loop_index * fiber_pitch

def create_fiber_points(fiber_index, sign, fiber_angular_offset, Polar_grid, Radius_of_Actuator, fiber_pitch, num_loops, Length_of_Actuator, compute_z_offset):
    point_vec = []  # List to store fiber points (x, y, z coordinates)
    point_z_coords = []  # List to track z-coordinates of points

    for angle in Polar_grid:
        # Compute coordinates based on sign (positive/negative x-component)
        angle_offset = angle + fiber_index * fiber_angular_offset
        x = sign * Radius_of_Actuator * np.cos(angle_offset)  # x-coordinate with sign adjustment
        y = Radius_of_Actuator * np.sin(angle_offset) if (angle % (2 * np.pi)) < np.pi else 0  # y-coordinate based on semi-circle condition
        z = fiber_pitch * angle / np.pi / 2  # z-coordinate covers only half-pitch for the semi-circle
        point_vec.extend([x, y, z])

    fiber_points = []  # List to store complete fiber geometry

    for loop_index in range(num_loops):
        for point_index in range(len(point_vec) // 3):
            x = point_vec[3 * point_index]
            y = point_vec[3 * point_index + 1]
            z = point_vec[3 * point_index + 2] + compute_z_offset(loop_index)
            fiber_points.append((x, y, z))  # Append computed point coordinates
            point_z_coords.append(z)  # Track z-coordinate

    cutoff_index = np.searchsorted(point_z_coords, Length_of_Actuator)  # Find cutoff index for valid points
    fiber_points = fiber_points[:cutoff_index + 1]  # Truncate points to fit actuator length

    # Create fiber geometry in the model (In ABAQUS)
    mdb.models['Model-1'].parts['semi_circular_sp'].WirePolyLine(points=fiber_points, meshable=ON)
    rotation_name = 'Anti Clock Wise Rotated Wire' if sign > 0 else 'Clock Wise Rotated Wire'
    mdb.models['Model-1'].parts['semi_circular_sp'].features.changeKey(fromName='Wire-1', toName=rotation_name)

# Positive x-component semi_circular_sp
for fiber_index in range(num_semi_circular_sp):
    create_fiber_points(fiber_index, 1, fiber_angular_offset, Polar_grid, Radius_of_Actuator, fiber_pitch, num_loops, Length_of_Actuator, compute_z_offset)

# Negative x-component semi_circular_sp
for fiber_index in range(num_semi_circular_sp):
    create_fiber_points(fiber_index, -1, fiber_angular_offset, Polar_grid, Radius_of_Actuator, fiber_pitch, num_loops, Length_of_Actuator, compute_z_offset)

# Create an instance of Fiber Wrapping (In ABAQUS)
session.viewports['Myvp1'].view.setValues(session.views['Iso'])
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['semi_circular_sp']
a.Instance(name='Fiber Wrap', part=p, dependent=OFF)

# Apply translation
a.translate(instanceList=('Fiber Wrap',), vector=(delta_x, delta_y, delta_z))

# End of script

# About Section:
# # Developer: Tufail Mabood
# GitHub: https://github.com/tufailmab
# Description: This script is developed by Tufail Mabood for generating the geometry of a soft bending actuator 
# in preparation for dynamic finite-element analysis (FEA). The tool wraps fibers 
# around a semi-circular structure (Which is Actuator), and positions the model in 3D space for further analysis.
# Version: 1.0
# Date: 02/10/2025

