from pydub import AudioSegment
from pydub.playback import play

######### IASI to change
path_audio = "" # modify this and listen to generated audio
#########

sound = AudioSegment.from_wav(path_audio)
play(sound)
