import inspect
import numpy as np

def VisVivaVelocitySquared(gravitationalParameter, r, a):
    return gravitationalParameter * (2 / r - 1 / a)

def gravitationalParameter_from_Mass(mass, gravitationalConstant):
    return mass * gravitationalConstant

def gravitationalParameter_from_Radius(gravity, radius):
    return gravity * radius ** 2

def VelocityCircularOrbit(gravitationalParameter, radius):
    return np.sqrt(gravitationalParameter / radius)


def keplersThirdLaw_radius_from_period(period, gravitationalParameter):
    return np.cbrt(gravitationalParameter * period ** 2 / (4 * np.pi ** 2))

# moved this from leeLibs to here
def varprint(var, name = None):
    if name is None:
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        name =  [var_name for var_name, var_val in callers_local_vars if var_val is var]
        varprint(var, name[0])
    else:
        print(name, "=", var)