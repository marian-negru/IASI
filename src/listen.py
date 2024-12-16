from pydub import AudioSegment
from pydub.playback import play

path_audio = '../output.wav'  # modify this if needed
sound = AudioSegment.from_wav(path_audio)
play(sound)
