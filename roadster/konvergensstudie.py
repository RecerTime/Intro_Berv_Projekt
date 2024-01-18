import roadster
import matplotlib.pyplot as plt

n = 1
N_stop = 16
N = [(2**i)*n + 1 for i in range(0, N_stop)]
O = 1
route = "speed_anna.npz"

x, raw_v = roadster.load_route(route)
x_max = x[-1]

v = [roadster.time_to_destination(x_max, route, i) for i in N]
consumption = [roadster.total_consumption(x_max, route, i) for i in N]

p = [O/(1/i) for i in N]

fig_v, ax_v = plt.subplots()
fig_v.suptitle('Time')
ax_v.loglog(N, v)
ax_v.plot(N, p)

fig_consumption, ax_consumption = plt.subplots()
fig_consumption.suptitle('Consumption')
ax_consumption.loglog(N, consumption)
plt.show()