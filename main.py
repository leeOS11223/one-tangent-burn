import matplotlib.pyplot as plt # for plotting
import numpy as np #for plotting & maths
from matplotlib.patheffects import withStroke # for plotting
import spaceEquations as se # for the space equations
ll = se

def PlotCircle(x, y, r, color, label):
    # Create a circle
    theta_circle = np.linspace(0, 2 * np.pi, 100)
    x_circle = r * np.cos(theta_circle) + x
    y_circle = r * np.sin(theta_circle) + y
    plt.plot(x_circle/1000, y_circle/1000, c=color, label=label)

def PlotEllipse(x, y, a, b, color, label):
    # Create an ellipse
    theta_ellipse = np.linspace(-np.pi/2, -2*np.pi/2, 100)
    x_ellipse = a * np.cos(theta_ellipse) + x
    y_ellipse = b * np.sin(theta_ellipse) + y
    plt.plot(x_ellipse/1000, y_ellipse/1000,"--", c=color, label=label)

def PlotPoint(x, y, color, label):
    # Create a scatter plot with a single dot
    plt.scatter(x/1000, y/1000, c=color, marker='o', label=label, zorder=3)

def PlotArrow(x, y, dx, dy, color, label, arrowthickness=2):
    # Create an arrow
    plt.arrow(x/1000, y/1000, dx/1000, dy/1000,head_width=arrowthickness, head_length=arrowthickness, color=color, zorder=2)
    label_text = plt.text((x+dx/2)/1000, (y+dy/2)/1000, label, fontsize=16, zorder=2, color=color, ha='center', va='center')
    outline_effect = withStroke(linewidth=6, foreground='white')
    label_text.set_path_effects([outline_effect])


# Given parameters
R_earth = 6371  # Radius of Earth in km
M_earth = 5.972e24  # Mass of Earth in kg
gravity_earth = 9.81  # Gravity of Earth in m/s^2

h_parking = 410  # Altitude of circular parking orbit in km
h_geostationary = 35786  # Altitude of geostationary orbit in km

a_transfer = 60000  # Semi-major axis of transfer ellipse in km

# Calculate circular parking orbit radius and geostationary orbit radius
r_parking = R_earth + h_parking
r_geostationary = R_earth + h_geostationary

ll.varprint(r_parking)


b_transfer = np.sqrt(a_transfer ** 2 - r_geostationary ** 2)  # Semi-minor axis of transfer ellipse in km

# draw diagram
if False:
    # Plotting
    plt.figure(figsize=(8,8))

    PlotCircle(0, 0, r_parking, 'black', 'Circular Parking Orbit')
    PlotCircle(0, 0, r_geostationary, 'orange', 'Geostationary Orbit')
    PlotEllipse(a_transfer-r_parking, 0, a_transfer, b_transfer, 'blue', 'Transfer Ellipse')

    # Mark the satellite position in the parking orbit
    PlotPoint(-r_parking, 0, 'red', 'Satellite')
    PlotPoint(0, 0, 'green', 'Earth')

    # Mark arrows
    PlotArrow(-r_parking, 0, 0, -10000, 'red', '$\Delta v_\pi$')

    by_eye_intersection = [21500,-36300]
    PlotArrow(by_eye_intersection[0],by_eye_intersection[1], 15000, -6000, 'red', '$v_{intercept}$')
    PlotArrow(by_eye_intersection[0],by_eye_intersection[1], 10000, 6000, 'purple', '$v_{r_2,cir}$')
    PlotArrow(by_eye_intersection[0]+16000, by_eye_intersection[1]-6000, -3400, 11300, 'green', '$v_{burn}$')

    # Mark radius'
    PlotArrow(0, 0, 0, r_parking, 'black', '$r_1$', arrowthickness=0)
    PlotArrow(0, 0, 0, r_geostationary, 'black', '$r_2$', arrowthickness=0)

    # Set equal aspect ratio and labels
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('Distance (megametres)')
    plt.ylabel('Distance (megametres)')
    plt.title('Circular Parking Orbit to Geostationary Orbit Transfer \nusing One-Tangent Burn')
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()



# Used to convert to meters
r_1 = r_parking *1000
r_2 = r_geostationary *1000
a_transfer*=1000
R_earth *= 1000 #m
r_3 = a_transfer - r_parking # not used.  just for reference


Earth_GravitationalParameter = se.gravitationalParameter_from_Radius(gravity_earth, R_earth)
ll.varprint(Earth_GravitationalParameter)

# derive geostationary orbit radius
# to be geostationary, the satellite must have a period of 24 hours
# use kepler's third law to find the radius
# T^2 = 4pi^2 / mu * a^3
ll.varprint(r_geostationary, "r_geostationary(from google)")
ll.varprint(24*60*60, "Time Period (s)")
r_geostationary = se.keplersThirdLaw_radius_from_period(24*60*60, Earth_GravitationalParameter)/1000 #km
ll.varprint(r_geostationary)


#some default values that i know the answer to.  used for testing
if False: #Expected result of these test values is delta_v_total = 5959 m/s
    r_1 = 6.7*10**6 #m
    r_2 = 42.238*10**6 #m
    r_3 = 91.176*10**6 #m
    a_transfer = (r_1+r_3)/2 #m



#1. \Delta v_\pi = v_\pi - v_cir_r_1
# first find \Delta v_\pi
v_pi = np.sqrt(se.VisVivaVelocitySquared(Earth_GravitationalParameter, r_1, a_transfer)) #m/s
ll.varprint(v_pi)
v_cir_r_1 = se.VelocityCircularOrbit(Earth_GravitationalParameter, r_1) #m/s
ll.varprint(v_cir_r_1)
delta_v_pi = v_pi - v_cir_r_1 #m/s
ll.varprint(delta_v_pi)

#2. \Delta v_int^2 = v_cir_r_2^2 - v_int^2 - 2v_cir_r_2 * v_int * cos(\theta)
# find v_intercept
v_intercept = np.sqrt(se.VisVivaVelocitySquared(Earth_GravitationalParameter, r_2, a_transfer)) #m/s
ll.varprint(v_intercept)

# find v_r_2,cir
v_cir_r_2 = se.VelocityCircularOrbit(Earth_GravitationalParameter, r_2) #m/s
ll.varprint(v_cir_r_2)

# use conservation of momentum to find the component of the intercept velocity in the direction of the circular orbit
# h = r_1*v_pi = r_2*v_int_perp
v_int_perp = (r_1/r_2)*v_pi #m/s
ll.varprint(v_int_perp)

# use the law of cosines to find the angle between v_r_2_cir and v_intercept
theta = np.arccos(v_int_perp/v_intercept) #rad
ll.varprint(theta*180/np.pi, "angle between v_r_2_cir and v_intercept in degrees")

# \Delta v_int^2
delta_v_int_squared = v_cir_r_2**2 + v_intercept**2 - 2*v_cir_r_2*v_intercept*np.cos(theta) #m/s
delta_v_int = np.sqrt(delta_v_int_squared) #m/s
ll.varprint(delta_v_int)

#3. \Delta v_total = |\Delta v_\pi| + |\Delta v_int|
# \Delta v_Total
delta_v_total = np.abs(delta_v_pi) + np.abs(delta_v_int) #m/s
ll.varprint(delta_v_total)
