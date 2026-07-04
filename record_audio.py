import sounddevice as sd # type: ignore
from scipy.io.wavfile import write # type: ignore
import numpy as np

fs = 16000
seconds = 10

print("Recording starts in 3 seconds...")
sd.sleep(3000)

print("Speak now...")

audio = sd.rec(
    int(seconds * fs),
    samplerate=fs,
    channels=1,
    dtype=np.int16
)

sd.wait()

write("audio/answer2.wav", fs, audio)

print("Recording saved successfully!")