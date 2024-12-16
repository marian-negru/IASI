import sounddevice as sd
from scipy.io.wavfile import write

########## IASI to change
fs = None  #  # Sample rate
channels = 100 # number of audio channels
seconds = 1000000  # Duration of recording, in seconds
path_audio = ""  # audio save path
########## 


myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=channels)
print(f'You can speak now!')
sd.wait()  # Wait until recording is finished
print(f'Recording has now stopped, saving file...')
write(path_audio, fs, myrecording)  # Save as WAV file 
print(f'Program finished succesfully!')
