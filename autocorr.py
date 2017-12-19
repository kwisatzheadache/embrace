execfile('straight.py')

def make_auto(feature):
    series = pd.Series(feature)
    auto = []
    for i in range(500):
        auto.append(series.autocorr(i))
    return auto

<<<<<<< HEAD
# dire = './demo_data/walk'
=======
>>>>>>> ca1f1667bd388caa6d2aaa22a653d6f7088f8c71
straight, index = straight_walk(dire, 15)
longest = longest_walk(straight, index)

df = DataFrame(longest)
cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z'] 
df.columns = cols

acc_mag, mag_mag, mag_gy = get_mags(df)

acc = make_auto(acc_mag)
mag = make_auto(mag_mag)
gy = make_auto(mag_gy)

plt.plot(acc)
plt.show()

autos = []
for i in df.columns:
    autos.append([make_auto(i)])
