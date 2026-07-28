Python 3.12.1 (tags/v3.12.1:2305ca5, Dec  7 2023, 22:03:25) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> # Taking input from user
... name = input("Enter a string: ")
... 
... # String slicing
... print("Slicing (0 to 4):", name[0:5])
... 
... # String casting
... num = "123"
... print("Casting string to integer:", int(num))
... 
... # String functions
... print("Upper case:", name.upper())
... print("Lower case:", name.lower())
... print("Length:", len(name))
... print("Replace a with x:", name.replace('a', 'x'))
... print("Find 'a':", name.find('a'))
