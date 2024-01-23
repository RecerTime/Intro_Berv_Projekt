import roadster
import matplotlib.pyplot as plt
import numpy as np

n_base = 8
n_stop = 15
route = "roadster/speed_anna.npz"

k = np.array([(2**i) for i in range(0, n_stop)])
n = k*n_base
N = n + 1

x, raw_v = roadster.load_route(route)
x_max = x[-1]

ch = np.array([(roadster.time_to_destination(x_max, route, i) - roadster.time_to_destination(x_max, route, 2*i))/3 for i in n])

print(ch)

fig_v, ax_v = plt.subplots()
fig_v.suptitle('Tid för olika N')
ax_v.set_xlabel('N')
ax_v.set_ylabel('Tid (h)')
ax_v.loglog(n, ch)

'''
consump = np.array([roadster.total_consumption(x_max, route, i) for i in N])

fig_consump, ax_consump = plt.subplots()
fig_consump.suptitle('Konsumption för olika N')
ax_consump.set_xlabel('N')
ax_consump.set_ylabel('Konsumption (W/m^2)')
ax_consump.loglog(n, consump)
'''
plt.show()
