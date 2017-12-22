execfile('functions.py')

# dire = './demo_data/walk'
straight, index = straight_walk(dire, 15)
longest = longest_walk(straight, index)

df = DataFrame(longest)
cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z'] 
df.columns = cols

acc_mag, mag_mag, mag_gy = get_mags(df)
reduced_acc = reduce_signal(acc_mag)
reduced_mag = reduce_signal(mag_mag)
reduced_gy = reduce_signal(mag_gy)

acc = [make_auto(acc_mag), make_auto(reduced_acc)]
mag = [make_auto(mag_mag), make_auto(reduced_mag)]
gy = [make_auto(mag_gy), make_auto(reduced_gy)]

plt.plot(gy[0])
plt.plot(gy[1])
plt.show()
