from src.sentiment import analyze_sentiment


print("Test 1: Positive sentiment")

text = "I really enjoy my work and feel happy with my team 😊"

result = analyze_sentiment(text)

print("Text:", text)
print("Result:", result)


print("\nTest 2: Negative sentiment")

text = "I am feeling very stressed because of my workload 😔"

result = analyze_sentiment(text)

print("Text:", text)
print("Result:", result)


print("\nTest 3: Neutral sentiment")

text = "I attended the employee meeting today."

result = analyze_sentiment(text)

print("Text:", text)
print("Result:", result)


print("\nTest 4: Strong positive sentiment")

text = "I am extremely excited and happy about the amazing new project! 🎉"

result = analyze_sentiment(text)

print("Text:", text)
print("Result:", result)


print("\nTest 5: Strong negative sentiment")

text = "I am extremely frustrated, exhausted and unhappy with my workload."

result = analyze_sentiment(text)

print("Text:", text)
print("Result:", result)


print("\nTest 6: Empty input")

text = ""

result = analyze_sentiment(text)

print("Text:", repr(text))
print("Result:", result)


print("\nTest 7: Negation")

text = "I am not happy with my workload."

result = analyze_sentiment(text)

print("Text:", text)
print("Result:", result)