relevance_score = 82.97
filler_words = 2
wpm = 120
average_pause = 0.8

# Relevance contributes 50%
technical_score = relevance_score * 0.5

# Filler words contribute 20%
if filler_words == 0:
    filler_score = 20
elif filler_words <= 3:
    filler_score = 15
elif filler_words <= 6:
    filler_score = 10
else:
    filler_score = 5

# Speaking speed contributes 20%
if 100 <= wpm <= 160:
    speed_score = 20
else:
    speed_score = 10

# Pause contributes 10%
if average_pause < 0.5:
    pause_score = 10
elif average_pause < 1.5:
    pause_score = 8
else:
    pause_score = 5

final_score = (
    technical_score +
    filler_score +
    speed_score +
    pause_score
)

print(f"Final Interview Score: {final_score:.2f}/100")