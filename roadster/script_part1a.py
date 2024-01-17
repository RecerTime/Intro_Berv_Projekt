#!/usr/bin/env python3
import numpy as np
import roadster
import matplotlib.pyplot as plt

speed_kmph = np.linspace(1., 200., 1000)
consumption_Whpkm = roadster.consumption(speed_kmph)

route = 'speed_elsa.npz'
x, raw_v = roadster.load_route(route)
v = roadster.velocity(x, route)

consump_fig, consump_ax = plt.subplots()
consump_ax.plot(speed_kmph, consumption_Whpkm)

route_fig, route_ax = plt.subplots()
route_ax.plot(x, raw_v, 'bo')
route_ax.plot(x, v)

plt.show()