import random
import string

def generate_password():
    """
    Generate a secure password with letters at the start and numbers at the end.

    :return: Generated password as a string
    """
    # Randomly select a length between 7 and 10
    length = random.randint(7, 10)

    # Define the character pools
    letters = string.ascii_letters  # Uppercase and lowercase letters
    digits = string.digits  # Numbers

    # Ensure the password has letters at the start and numbers at the end
    num_letters = random.randint(3, length - 3)  # At least 3 letters
    num_digits = length - num_letters  # Remaining characters are digits

    letters_part = ''.join(random.choices(letters, k=num_letters))
    digits_part = ''.join(random.choices(digits, k=num_digits))

    # Combine letters and numbers
    password = letters_part + digits_part

    return password

# Example usage
if __name__ == "__main__":
    print("Generated Password:", generate_password())
