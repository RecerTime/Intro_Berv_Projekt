#!/usr/bin/env python3
import numpy as np
import roadster
import matplotlib.pyplot as plt

speed_kmph = np.linspace(1.0, 200.0, 1000)
consumption_Whpkm = roadster.consumption(speed_kmph)

route = "speed_anna.npz"
x, raw_v = roadster.load_route(route)
v = roadster.velocity(x, route)

consump_fig, consump_ax = plt.subplots()
consump_ax.plot(speed_kmph, consumption_Whpkm)
consump_ax.set_xlabel("Hastighet (km/h)")
consump_ax.set_ylabel("Konsumption (W/m^2)")
consump_fig.suptitle("Konsumption beroende på hastighet")
route_fig, route_ax = plt.subplots()
route_ax.plot(x, raw_v, "ro")
route_ax.plot(x, v, color="red")
route_ax.set_xlabel("Position (km)")
route_ax.set_ylabel("Hastighet (km/h)")
route_fig.suptitle("Rutt Anna")
plt.show()
