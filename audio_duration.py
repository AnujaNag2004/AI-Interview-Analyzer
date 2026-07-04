import wave

audio_file = wave.open("audio/answer2.wav", "r")

frames = audio_file.getnframes()
rate = audio_file.getframerate()

duration = frames / float(rate)

print(f"Audio Duration: {duration:.2f} seconds")
