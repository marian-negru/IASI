import sounddevice as sd
from scipy.io.wavfile import write

fs = 16000  # Sample rate
channels = 1 # mono audio
seconds = 10  # Duration of recording, in seconds
path_audio = '../output.wav'  # modify this if needed

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=channels)
print(f'You can speak now!')
sd.wait()  # Wait until recording is finished
print(f'Recording has now stopped, saving file...')
write(path_audio, fs, myrecording)  # Save as WAV file 
print(f'Program finished succesfully!')
