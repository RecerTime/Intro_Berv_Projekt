import roadster
import matplotlib.pyplot as plt
import numpy as np

route = "roadster/speed_anna.npz"

n = 8*np.array([(2**i) for i in range(0, 20)])

x, raw_v = roadster.load_route(route)

T = lambda n: roadster.time_to_destination(x[-1], route, n)
c2h2 = [np.abs(T((2*i) + 1) - T(i + 1))/3 for i in n]

fig_v, ax_v = plt.subplots()
fig_v.suptitle('Error för olika n')
ax_v.set_xlabel('n')
ax_v.set_ylabel('Error')
ax_v.loglog(n, c2h2)
plt.show()
