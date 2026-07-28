"""
Arithmetic Calculator
---------------------
A simple Python program that performs basic arithmetic operations
based on user input.

Operations Supported:
- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Division (/)

Author: Your Name
GitHub: https://github.com/your-username
"""

def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b


def divide(a, b):
    """Return the quotient of two numbers."""
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b


def main():
    """Main function to execute the calculator."""

    print("=" * 40)
    print("      BASIC ARITHMETIC CALCULATOR")
    print("=" * 40)

    try:
        first_number = float(input("Enter the first number: "))
        second_number = float(input("Enter the second number: "))

        print("\nChoose an operation:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            result = add(first_number, second_number)
            operation = "+"
        elif choice == "2":
            result = subtract(first_number, second_number)
            operation = "-"
        elif choice == "3":
            result = multiply(first_number, second_number)
            operation = "*"
        elif choice == "4":
            result = divide(first_number, second_number)
            operation = "/"
        else:
            print("Invalid choice. Please run the program again.")
            return

        print("\n" + "-" * 40)
        print(f"Result: {first_number} {operation} {second_number} = {result}")
        print("-" * 40)

    except ValueError:
        print("Error: Please enter valid numeric values.")


if __name__ == "__main__":
    main()
