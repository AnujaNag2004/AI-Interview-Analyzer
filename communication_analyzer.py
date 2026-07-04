import wave

transcript = """
Machine learning is a subset of artificial intelligence that enables computers to learn from data.
"""

word_count = len(transcript.split())

audio_file = wave.open("audio/answer2.wav", "r")

frames = audio_file.getnframes()
rate = audio_file.getframerate()

duration = frames / float(rate)

wpm = (word_count / duration) * 60

print(f"Words Spoken: {word_count}")
print(f"Duration: {duration:.2f} seconds")
print(f"Speaking Speed: {wpm:.2f} WPM")

if wpm < 100:
    print("Candidate speaks slowly.")
elif wpm <= 160:
    print("Candidate speaks at an ideal pace.")
else:
    print("Candidate speaks too fast.")