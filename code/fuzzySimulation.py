import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from Controller2 import Controller

'''
    Plots a mesh with a simulation for both variables of Controller2.py
'''

con = Controller()
ls, rs = np.meshgrid(con.sonar_interval, con.sonar_interval)
t = np.zeros_like(ls)
v = np.zeros_like(ls)

for i in range(len(ls)):
    for j in range(len(rs)):
        con.sim.input['lsonar'] = ls[i, j]
        con.sim.input['rsonar'] = rs[i, j]
        
        con.sim.compute()
        
        t[i, j] = con.sim.output['theta']
        v[i, j] = con.sim.output['v_x']

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

go = 't'

if go is 't':
    tsurf = ax.plot_surface(ls, rs, t, rstride=1, cstride=1, cmap='viridis',
                            linewidth=0.4, antialiased=True)

    cset = ax.contourf(ls, rs, t, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
    cset = ax.contourf(ls, rs, t, zdir='x', offset=3, cmap='viridis', alpha=0.5)
    cset = ax.contourf(ls, rs, t, zdir='y', offset=3, cmap='viridis', alpha=0.5)

if go is  'v':
    vsurf = ax.plot_surface(ls, rs, v, rstride=1, cstride=1, cmap='viridis',
                            linewidth=0.4, antialiased=True)

    cset = ax.contourf(ls, rs, v, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
    cset = ax.contourf(ls, rs, v, zdir='x', offset=3, cmap='viridis', alpha=0.5)
    cset = ax.contourf(ls, rs, v, zdir='y', offset=3, cmap='viridis', alpha=0.5)

ax.view_init(30, 200)
plt.show()
