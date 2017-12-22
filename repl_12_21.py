dire = './demo_data/walk'
execfile('autocorr.py')
lag_acc = lag(df['acc_x'], 100)


fft = []
for i in lag_acc:
	fft.append(get_fft(i))


doms = []
for i, j in fft:
	doms.append(get_dom_freq(i, j, 37))


reduced = []
for i, j in doms:
	reduced.append(get_reduced_signal(i, j, 100))


plt.plot(lag_acc[0])
plt.show()
plt.plot(reduced[0])
plt.show()

auto_lag0 = make_auto(reduced[0])
auto_acc_lag0 = make_auto(lag_acc[0])
