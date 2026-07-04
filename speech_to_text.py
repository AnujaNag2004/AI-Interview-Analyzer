import whisper # type: ignore

print("Loading Whisper model...")
model = whisper.load_model("base")

print("Converting speech to text...")
result = model.transcribe("audio/answer2.wav", language="en")

print("\nTranscript:")
print(result["text"])