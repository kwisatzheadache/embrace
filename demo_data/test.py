import embrace_setup as ep
from fft_funcs import *
import break_on_lics as bol
import matplotlib.pyplot as plt


vals = ep.get_lists("5step.csv")

ac_mag = vals[4]

x = []
y = []
z = []

for s_s in range(50):
    for i in range(1,11):
        lics, hics = bol.get_lics(ac_mag,s_s,i*.1)
        x.append(s_s)
        y.append(i)
        z.append(len(hics))

plt.plot_surface(x,y,z)
plt.show()



