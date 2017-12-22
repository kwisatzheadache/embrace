dire = './demo_data/walk'
execfile('autocorr.py')
lag_acc = lag(df['acc_x'], 100)
fft = []
for i in lag_acc:
	fft.append(get_fft(i))
fft.shape
len(fft)
fft[1]
doms = []
for i in fft:
	doms.append(get_dom_freq(
for i, j in fft:
	doms.append(get_dom_freq(i, j, 37))
doms[1]
reduced = []
for i, j in doms:
	reduced.append(i, j, 100)
for i, j in doms:
	reduced.append(get_reduced_signal(i, j, 100))
reduced
len(reduced)
reduced
len(reduced[1])
plt.plot(lagged[0])
plt.plot(lag[0])
lag
plt.plot(lagged[0])
plt.plot(lag_ac[0])
plt.plot(lag_acc[0])
plt.show()
plt.plot(reduced[0])
plt.show()
import readline
readline.write_history_file('./repl_12_21.py')
auto_lag0 = make_auto(reduced[0])
plt.plot(auto_lag0)
plt.show()
plt.plot(auto_lag0)
auto_acc_lag0 = make_auto(lag_acc[0])
plt.plot(auto_acc_lag0)
plt.show()
fft = []
fft = get_fft(acc_mag)
doms = []
doms = get_dom_freq(fft[0], fft[1], 100)
doms
len(fft[0])
reduced = get_reduced_signal(doms[0], doms[1], 100\
reduced = get_reduced_signal(doms[0], doms[1], 100)
reduced
len(reduced)
len(acc_mag)
reduced = get_reduced_signal(doms[0], doms[1], 1881)
len(reduced)
auto_red = make_auto(reduced)
plt.plot(auto_red)
plt.show()
plt.plot(acc)
plt.show()
plt.plot(mag)
plt.show()
plt.plot(gy)
plt.show()
plt.plot(acc)
plt.show()
execfile('functions.py')
execfile('autocorr.py')
len(acc)
plt.plot(acc[0])
plt.plot(acc[1])
plt.show()
plt.plot(gy[0])
plt.plot(gy[1])
plt.show()
plt.plot(acc[1])
plt.plot(gy[1])
plt.show()
plt.plot(reduced_acc)
plt.show(0
plt.show()
plt.plot(acc_mag)
plt.show()
len(acc_mag)
len(reduced_acc)
plt.plot(acc[1])
plt.show()
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('graph.pdf')
plot1 = plt.plot(acc[1])
pp.savefig(plot1)
plt.figure()
plt.show()
plt.plot(acc[0])
plt.show()
plt.plot(acc[1])
plt.show()
plt.plot(gy[1])
plt.show()
plt.plot(acc[1])
plt.show()
plt.plot(gy[1])
plt.show()
plt.plot(gy[1])
plt.savefig('reduced_gy_magnitude_autocorr.pdf')
from peakdetect import peakdetect
import peakutils
indexes = peakutils.indexes(gy[1])
indedes
indexes
len(gy[1])
findpeaks
from scipy.signal import find_peaks_cwt
indexes = find_peaks_cwt(gy[1], np.arange(1, 500))
indexes
len(gy[0])
execfile('functions.py')
trial = make_auto(reduced_gy)
len(trial)
plt.plot(trial)
plt.show()
indexes = find_peaks_cwt(trial, np.arange(1, len(trial))
)
len(indexes)
indexes = find_peaks_cwt(trial, np.arange(1, 500))
indexes
trial
len(indexes)
indexes = find_peaks_cwt(trial)
indexes = find_peaks_cwt(trial, np.arange(1, 200))
indexes
trial
plt.plot(trial)
plt.show()
ind
ind = find_peaks_cwt(trial, np.arange(1, 550))
ind
ind = find_peaks_cwt(gy[1], np.arange(1, 550))
ind
import peakutils
ind = peakutils.indexes(trial, min_dist = 30)
ind = peakutils.indexes(trial, thres = 0.02/max(trial), min_dist = 30)
ind
type(trial)
type(gy[0])
trial[:10]
gy[1, :10]
gy[1][:10]
ind = peakutils.indexes(trial[:1000], thres = 0.02/max(trial), min_dist = 30)
arr = np.array(trial)
ind = find_peaks_cwt(arr, np.arange(1, 550))
ind
ind.shape
arr.shape
np.array(gy[1]).shape
indexes
ind = find_peaks_cwt(gy[1], np.arange(1, 200))
ind
plt.plot(gy[1])
plt.plot(ind)
plt.show()
plt.plot(gy[1])
plt.show()
execfile('peakdet.py')
outs = peakdet(trial, .01)
outs
len(outs)
len(outs[0])
outs[0]
outs[1]
len(trial)(
len(trial)
plt.plot(trial)
plt.show()
execfile('peakdet.py')
plt.savefig('reduced_gy_magnitude_autocorr.pdf')
import readline
readline.write_history_file('./repl_12_21.py')
