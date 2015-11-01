'''
	spectrogram.py
	By Phuong Dinh and Julia Kroll
	1 Nov 2015
	Draws the spectrogram of a wav file
'''
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import matplotlib.cm as cm


def get_spectro(filename):
	'''Takes in a file name, performs a Fourier transformation, and graphs the spectrogram of the result.'''

	# Open the file
	try:
		wav_file = wave.open(filename, 'r')
	except:
		print("ERROR: CANNOT OPEN INPUT FILE AS WAV FILE.")
		sys.exit(1)
		
	# Create an array with a size equal to the number of 25-ms (400-sample) time steps	
	num_time_steps = (wav_file.getnframes()-400) / 160 
	spectro_array = np.zeros(shape=(num_time_steps,400)) #spectro_array[t][k] = 10*log10(fourier_amplitude)

	# Iterate to perform a Fourier transform on each window
	window = wav_file.readframes(400)
	n = 0
	while wav_file.tell() + 160 < wav_file.getnframes(): # Window spacing = 10 ms = 160 frames
		signal = np.fromstring(window, "int16")
		fourier_transformed = np.fft.fft(signal)
		spectro_array[n] = 10*np.log10(np.sqrt(np.square(fourier_transformed.real) + np.square(fourier_transformed.imag)))
		n += 1
		wav_file.setpos(160 * n)		
		window = wav_file.readframes(400)

	# Draw the spectrogram
	spectro_array = spectro_array.T # Transpose the x/y dimensions of the array
	fig = plt.figure(facecolor="white") 

	# We will only display half of the frequency, for the upper half is vertical mirror image of the lower one
	plt.imshow(spectro_array[:len(spectro_array)/2], origin = "lower", cmap = cm.Greys, extent=[0,n/100,0,16000/2], aspect='auto') 
	plt.xlabel("Time (seconds)")
	plt.ylabel("Frequency (Hz)\n")
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