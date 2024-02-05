import numpy as np
from scipy import interpolate

def load_route(route):
    """
    Get speed data from route .npz-file. Example usage:

      distance_km, speed_kmph = load_route('speed_anna.npz')

    The route file should contain two arrays, distance_km and
    speed_kmph, of equal length with position (in km) and speed
    (in km/h) along route. Those two arrays are returned by this
    convenience function.
    """
    # Read data from npz file
    if not route.endswith(".npz"):
        route = f"{route}.npz"
    data = np.load(route)
    distance_km = data["distance_km"]
    speed_kmph = data["speed_kmph"]
    return distance_km, speed_kmph

def save_route(route, distance_km, speed_kmph):
    """
    Write speed data to route file. Example usage:

      save_route('speed_olof.npz', distance_km, speed_kmph)

    Parameters have same meaning as for load_route
    """
    np.savez(route, distance_km=distance_km, speed_kmph=speed_kmph)

### PART 1A ###
def consumption(v):
    assert np.all(v >= 0)
    return 546.8 * v ** (-1) + 50.31 + 0.2594 * v + 0.008210 * v**2

### PART 1B ###
def velocity(x, route):
    # ALREADY IMPLEMENTED!
    """
    Interpolates data in given route file, and evaluates the function
    in x
    """
    # Load data
    distance_km, speed_kmph = load_route(route)
    # Interpolate
    v = interpolate.pchip_interpolate(distance_km, speed_kmph, x)
    return v

### PART 2A ###
def time_to_destination(x, route, N):
    h = x / (N - 1)
    fx = 1 / velocity(np.linspace(0, x, N), route)
    return h * (2 * np.sum(fx) - fx[-1] - fx[0]) / 2

### PART 2B ###
def total_consumption(x, route, N):
    h = x / (N - 1)
    fx = consumption(velocity(np.linspace(0, x, N), route))
    return h * (2 * np.sum(fx) - fx[-1] - fx[0]) / 2

def newtons_method(fx, fx_prime, tolerance, x_max):
    x = x_max/2
    for i in range(10000):
        x1 = x - fx(x)/fx_prime(x)
        
        if np.abs(x1-x) <= tolerance:
            break

        if x1 > x_max:
            return x_max
        
        x = x1
    return x1

### PART 3A ###
def distance(T, route):
    time = lambda x: time_to_destination(x, route, 10000001) - T
    vel = lambda x: 1/velocity(x, route)
    return newtons_method(time, vel, 1e-4, load_route(route)[0][-1])

### PART 3B ###
def reach(C, route):
    tot_consump = lambda x: total_consumption(x, route, 10000001) - C
    consump = lambda x: consumption(velocity(x, route))
    return newtons_method(tot_consump, consump, 1e-4, load_route(route)[0][-1])
