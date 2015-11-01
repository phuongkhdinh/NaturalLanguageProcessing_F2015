'''
	spectrogram.py
	By Phuong Dinh and Julia Kroll
	1 Nov 2015
	Draw spectrogram of a wav file
'''
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import matplotlib.cm as cm


def get_spectro(filename):
	try:
		wav_file = wave.open(filename, 'r')
	except:
		print("ERROR: CANNOT OPEN INPUT FILE AS WAV FILE.")
		sys.exit(1)
		
	timeStep = (wav_file.getnframes()-400) / 160
	spectroArray = np.zeros(shape=(timeStep,400)) #spectroArray[t][k] = 10*log10(fourier_amplitude)

	window = wav_file.readframes(400)
	n = 0
	while wav_file.tell() + 160 < wav_file.getnframes(): #spacing of window = 10ms = 160 frames
		signal = np.fromstring(window, "int16")
		fourier_transformed = np.fft.fft(signal)
		spectroArray[n] = 10*np.log10(np.sqrt(np.square(fourier_transformed.real) + np.square(fourier_transformed.imag)))

		n += 1
		wav_file.setpos(160 * n)		
		window = wav_file.readframes(400)

	#Draw it
	spectroArray = spectroArray.T
	fig = plt.figure() 

	# We will only display half of the frequency, for the upper half is vertical mirror image of the lower one
	plt.imshow(spectroArray[:len(spectroArray)/2], origin = "lower", cmap = cm.Greys, extent=[0,n/100,0,16000/2], aspect='auto') 
	plt.xlabel("Time/s")
	plt.ylabel("Frequency/Hz")
	fig.suptitle('Spectrogram for ' + filename, fontsize=15)

	plt.show()



def main():

	if len(sys.argv) == 2:
		filename = sys.argv[1]
		wav_file = get_spectro(filename)
	else:
		print("ERROR: INPUT WAV FILE IS MISSING.")

if __name__ == "__main__":
	main()