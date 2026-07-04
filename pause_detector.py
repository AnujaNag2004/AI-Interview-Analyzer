import librosa # type: ignore
import numpy as np

audio_path = "audio/answer2.wav"

audio, sr = librosa.load(audio_path)

intervals = librosa.effects.split(
    audio,
    top_db=40
)

print("Detected speech intervals:")
print(intervals)

pause_durations = []

for i in range(1, len(intervals)):
    previous_end = intervals[i - 1][1]
    current_start = intervals[i][0]

    pause_duration = (current_start - previous_end) / sr
    pause_durations.append(pause_duration)

if pause_durations:
    average_pause = np.mean(pause_durations)
    longest_pause = np.max(pause_durations)

    print(f"\nTotal Pauses: {len(pause_durations)}")
    print(f"Average Pause Duration: {average_pause:.2f} seconds")
    print(f"Longest Pause Duration: {longest_pause:.2f} seconds")
else:
    print("\nNo pauses detected.")
