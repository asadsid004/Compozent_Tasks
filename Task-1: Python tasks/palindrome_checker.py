# Write a function to check if a given string is a palindrome.


def is_palindrome(s):
    # Remove spaces and convert to lowercase for uniformity
    cleaned = "".join(s.split()).lower()
    # cleaned[::-1] to reverse the string
    return cleaned == cleaned[::-1]


word = input("Enter a string to check if it is a palindrome: ")
print("Result ->")
print(f"\tIs '{word}' a palindrome -> {is_palindrome(word)}")
