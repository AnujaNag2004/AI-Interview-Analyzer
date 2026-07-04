filler_words = ["um", "uh", "like", "actually", "basically", "you know"]

answer = input("Enter transcript: ").lower()

count = 0

for word in filler_words:
    count += answer.count(word)

print(f"\nFiller words used: {count}")

if count == 0:
    print("Excellent communication confidence")
elif count <= 3:
    print("Good communication confidence")
elif count <= 6:
    print("Average communication confidence")
else:
    print("Too many filler words detected")