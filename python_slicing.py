# Python Slicing Examples

# Original string
text = "Hello, GitHub!"

print("Original String:", text)

# Basic slicing
print("First 5 characters:", text[:5])
print("Last 7 characters:", text[-7:])
print("Characters from index 7 to 12:", text[7:13])

# Step slicing
print("Every second character:", text[::2])

# Reverse string
print("Reversed String:", text[::-1])

# List slicing
numbers = [10, 20, 30, 40, 50, 60, 70]

print("\nOriginal List:", numbers)
print("First 3 elements:", numbers[:3])
print("Last 3 elements:", numbers[-3:])
print("Middle elements:", numbers[2:5])
print("Every second element:", numbers[::2])
print("Reversed List:", numbers[::-1])
