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
    # Check input ok?
    assert np.min(x) >= 0, "x must be non-negative"
    assert np.max(x) <= distance_km[-1], "x must be smaller than route length"
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

### PART 3A ###
def distance(T, route):
    pos, vel = load_route(route)
    #assert np.all(T <= time_to_destination(pos[-1], route, 20)), "T too large"
    xTest = 0.4
    m = 1
    tolerance = 0.00001
    err = 1
    zero = time_to_destination(xTest, route, 20) - T
    while (zero != 0) and (np.abs(err) > tolerance):
        dy = time_to_destination(xTest + tolerance, route, 20) - time_to_destination(xTest, route, 20)
        dx = tolerance
        err = (zero) / (dy/dx)

        xTest = xTest - m * err
        if xTest > pos[-1]:
            xTest = pos[-1]
        print("x", xTest)
        print("error", np.abs(err))
    return xTest


### PART 3B ###
def reach(C, route):
    # REMOVE THE FOLLOWING LINE AND WRITE YOUR SOLUTION
    raise NotImplementedError("reach not implemented yet!")


if __name__ == "__main__":
    x, v = load_route("speed_anna.npz")
    print(time_to_destination(x[-1], "speed_anna.npz", 10))
    #x, v = load_route("speed_anna.npz")
    #print(time_to_destination(x[-1], "speed_anna.npz", 10))
    distance(1, "roadster/speed_anna.npz")
    #x, v = load_route("speed_anna.npz")
    #print(time_to_destination(x[-1], "speed_anna.npz", 10))
    distance(1, "roadster/speed_anna.npz")