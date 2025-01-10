# Create a script to read a text file, count the number of words, and write the results to a new file.


def file_word_count(input_file, output_file):
    try:
        # Read input file
        with open(input_file, "r") as file:
            content = file.read()

        # Count words
        word_count = len(content.split())

        # Write results to output file
        with open(output_file, "w") as file:
            file.write(f"The file '{input_file}' contains {word_count} words.")

        print(f"Word count written to '{output_file}'")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")


file_word_count("input.txt", "output.txt")
