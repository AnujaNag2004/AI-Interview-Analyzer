transcript = input("Enter transcript: ")

duration_seconds = float(
    input("Enter duration of answer in seconds: ")
)

word_count = len(transcript.split())

wpm = (word_count / duration_seconds) * 60

print(f"\nWords Spoken: {word_count}")
print(f"Speaking Speed: {wpm:.2f} WPM")

if wpm < 100:
    print("Speaking pace is slow.")
elif wpm <= 160:
    print("Speaking pace is ideal.")
else:
    print("Speaking pace is too fast.")