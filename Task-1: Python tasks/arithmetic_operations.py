# Write a program to perform addition, subtraction, multiplication, and division of two numbers provided by the user.


def arithmetic_operations():
    try:
        # Taking user input
        num1 = float(input("Enter the first number -> "))
        num2 = float(input("Enter the second number -> "))

        # Perform operations
        addition = num1 + num2
        subtraction = num1 - num2
        multiplication = num1 * num2
        division = num1 / num2 if num2 != 0 else "Error: Cannot divide by zero"

        # Display results
        print("Results - >")
        print(f"\tAddition: {addition}")
        print(f"\tSubtraction: {subtraction}")
        print(f"\tMultiplication: {multiplication}")
        print(f"\tDivision: {division}")
    except ValueError:
        print("Invalid input. Please enter numeric values.")


arithmetic_operations()
