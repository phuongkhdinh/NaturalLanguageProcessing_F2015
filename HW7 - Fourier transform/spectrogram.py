import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import matplotlib.cm as cm


def get_spectro(filename):
	wav_file = wave.open(filename, 'r')
	timeStep = (wav_file.getnframes()-400) / 160
	spectroArray = np.zeros(shape=(timeStep,400)) #spectroArray[t][k] = 10*log10(fourier_amplitude)

	window = wav_file.readframes(400)
	n = 0
	while wav_file.tell() + 160 < wav_file.getnframes(): #spacing of window = 10ms = 160 frames
		signal = np.fromstring(window, "int16")
		fourier_transformed = np.fft.fft(signal)
		# print(fourier_transformed)
		# sys.exit()
		spectroArray[n] = 10*np.log10(np.sqrt(np.square(fourier_transformed.real) + np.square(fourier_transformed.imag)))
		#print(n,"--------------")
		#print(spectroArray[n])
		n += 1
		wav_file.setpos(160 * n)		
		window = wav_file.readframes(400)

	#Draw it
	spectroArray = spectroArray.T
	plt.imshow(spectroArray, origin = "lower", cmap = cm.Greys, extent=[0,n/100,0,16000], aspect='auto') 
	# longitude_top_left,longitude_top_right,latitude_bottom_left,latitude_top_left
	# erm, don't know which axis is which! timee need to be divided by 100
	# don't know how to scale k back to frequency (by times 400)
	# don't know how to make sure bigger is darker

	plt.show()

	# plt.figure(1)
	# plt.title('Signal Wave...')
	# plt.plot(signal)
	#plt.show()
	#userInput = input()


def main():

	wav_file = get_spectro("./timitwav/sx14.wav")


if __name__ == "__main__":
	main()