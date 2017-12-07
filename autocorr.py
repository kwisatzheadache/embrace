execfile('straight.py')

dire = './demo_data/walk/ryan'

straight = straight_walk(dire, 15)

one = straight[2230:2700]

mag_z = one[:,9]
