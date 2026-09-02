from src.preprocessing import preprocess_text


print("Test 1: Basic preprocessing")

text = "I am feeling very stressed because of my workload!!!"

processed = preprocess_text(text)

print("Original:", text)
print("Processed:", processed)


print("\nTest 2: Positive employee feedback")

text = "I really enjoy working with my team and I feel happy 😊"

processed = preprocess_text(text)

print("Original:", text)
print("Processed:", processed)


print("\nTest 3: Negative employee feedback")

text = "I am extremely frustrated and tired because of my workload 😔"

processed = preprocess_text(text)

print("Original:", text)
print("Processed:", processed)


print("\nTest 4: Neutral employee feedback")

text = "I attended the employee meeting today."

processed = preprocess_text(text)

print("Original:", text)
print("Processed:", processed)


print("\nTest 5: Empty text")

text = ""

processed = preprocess_text(text)

print("Original:", repr(text))
print("Processed:", processed)


print("\nTest 6: Repeated spaces")

text = "I    feel     very     happy     today 😊"

processed = preprocess_text(text)

print("Original:", text)
print("Processed:", processed)


print("\nTest 7: Special characters and emojis")

text = "I am VERY happy!!! 😊🎉 #great @team"

processed = preprocess_text(text)

print("Original:", text)
print("Processed:", processed)

print("\nTest 8: Lemmatization")

text = "Employees are working harder and feeling exhausted."

processed = preprocess_text(text)

print("Original:", text)
print("Processed:", processed)


print("\nTest 9: Negation")

text = "I am not happy with my workload."

processed = preprocess_text(text)

print("Original:", text)
print("Processed:", processed)

print("\nTest 10: Very Short Emotional Text")

text = "Sad."

processed = preprocess_text(text)

print("Original:", text)
print("Processed:", processed)


print("\nTest 11: Long Employee Feedback")

text = """
I have been feeling extremely stressed and anxious because my workload
has increased significantly over the past few weeks. I am finding it
difficult to maintain a healthy work-life balance, and I often feel
exhausted after work. However, I still enjoy working with my team and
I am excited about the upcoming project.
"""

processed = preprocess_text(text)

print("Original:", text)
print("Processed:", processed)