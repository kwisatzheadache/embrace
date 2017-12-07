execfile('straight.py')

dire = './demo_data/walk/ryan'

straight = straight_walk(dire, 15)

cols = ['id', 'acc_x', 'acc_y', 'acc_z', 'gy_x', 'gy_y', 'gy_z', 'mag_x', 'mag_y', 'mag_z'] 

one = straight[2230:2700]
one_df = DataFrame(one)
one_df.columns = cols

mag_z = pd.Series(one[:,9])
acc_mag, mag_mag, mag_gy = get_mags(one_df)

auto = []
for i in range(500):
    auto.append(mag_z.autocorr(i))

def make_auto(feature):
    series = pd.Series(feature)
    auto = []
    for i in range(500):
        auto.append(series.autocorr(i))
    return auto

acc = make_auto(acc_mag)
mag = make_auto(mag_mag)
gy = make_auto(mag_gy)
