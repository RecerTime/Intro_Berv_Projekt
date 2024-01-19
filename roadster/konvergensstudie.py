import roadster
import matplotlib.pyplot as plt
import numpy as np

n_base = 10
n_stop = 18
route = "speed_anna.npz"

n = np.array([(2**i)*n_base for i in range(0, n_stop)])
N = n + 1

x, raw_v = roadster.load_route(route)
x_max = x[-1]

v = np.array([roadster.time_to_destination(x_max, route, i) for i in N])
consump = np.array([roadster.total_consumption(x_max, route, i) for i in N])

v_error = np.abs(v-v[-1])
consump_error = np.abs(consump-consump[-1])

for i, val in enumerate(v_error):
    print(f'{n[i]} : {val}')

fig_v, ax_v = plt.subplots()
fig_v.suptitle('Tid för olika N')
ax_v.set_xlabel('N')
ax_v.set_ylabel('Tid (h)')
ax_v.loglog(n, v_error)

fig_consump, ax_consump = plt.subplots()
fig_consump.suptitle('Konsumption för olika N')
ax_consump.set_xlabel('N')
ax_consump.set_ylabel('Konsumption (W/m^2)')
ax_consump.loglog(n, consump_error)
plt.show()
