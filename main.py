import math


def caesar_cipher_encrypt(plaintext, key):
    # Ensure key is integer
    try:
        shift = int(key)
    except ValueError:
        print("Key must be an integer for Caesar cipher.")
        return None
    result = ""
    for char in plaintext:
        if char.isalpha():
            # Shift character by shift positions
            char_code = ord(char.upper())
            shifted = ((char_code - 65 + shift) % 26) + 65
            result += chr(shifted)
        else:
            # Keep non-alphabetic characters as is
            result += char
    return result


def vigenere_cipher_encrypt(plaintext, key):
    # Ensure key contains only letters
    if not key.isalpha():
        print("Key must only contain letters for Vigenere cipher.")
        return None
    key = key.upper()
    result = ""
    key_length = len(key)
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            # Shift character by the amount represented by key letter
            char_code = ord(char.upper()) - 65
            key_code = ord(key[key_index % key_length]) - 65
            shifted = (char_code + key_code) % 26
            result += chr(shifted + 65)
            key_index += 1
        else:
            result += char
    return result


def affine_cipher_encrypt(plaintext, key_a, key_b):
    try:
        a = int(key_a)
        b = int(key_b)
    except ValueError:
        print("Keys must be integers for Affine cipher.")
        return None
    if math.gcd(a, 26) != 1:
        print("Key 'a' must be coprime with 26 for Affine cipher.")
        return None
    result = ""
    for char in plaintext:
        if char.isalpha():
            char_code = ord(char.upper()) - 65
            encrypted_code = (a * char_code + b) % 26
            result += chr(encrypted_code + 65)
        else:
            result += char
    return result


def get_hill_cipher_key():
    print("Enter the key matrix for Hill cipher (2x2 matrix).")
    key_matrix = []
    for i in range(2):
        row = input(f"Enter row {i + 1} (2 integers separated by space): ")
        row_values = row.strip().split()
        if len(row_values) != 2:
            print("Each row must contain exactly 2 numbers.")
            return None
        try:
            row_ints = [int(x) % 26 for x in row_values]
        except ValueError:
            print("Matrix values must be integers.")
            return None
        key_matrix.append(row_ints)
    # Now check if determinant is invertible modulo 26
    det = (key_matrix[0][0] * key_matrix[1][1] - key_matrix[0][1] * key_matrix[1][0]) % 26
    if math.gcd(det, 26) != 1:
        print("The determinant of the key matrix is not invertible modulo 26.")
        return None
    return key_matrix


def hill_cipher_encrypt(plaintext, key_matrix):
    # Convert plaintext to uppercase letters
    plaintext = ''.join([c.upper() for c in plaintext if c.isalpha()])
    # Pad plaintext if necessary
    if len(plaintext) % 2 != 0:
        plaintext += 'X'  # Padding character
    result = ''
    for i in range(0, len(plaintext), 2):
        pair = plaintext[i:i + 2]
        vector = [ord(pair[0]) - 65, ord(pair[1]) - 65]
        # Multiply key matrix with vector
        encrypted_vector = [
            (key_matrix[0][0] * vector[0] + key_matrix[0][1] * vector[1]) % 26,
            (key_matrix[1][0] * vector[0] + key_matrix[1][1] * vector[1]) % 26
        ]
        result += chr(encrypted_vector[0] + 65) + chr(encrypted_vector[1] + 65)
    return result


def substitution_cipher_encrypt(plaintext, key):
    key = key.upper()
    if len(key) != 26 or not key.isalpha():
        print("Key must be a permutation of 26 letters for Substitution cipher.")
        return None
    if len(set(key)) != 26:
        print("Key must contain 26 unique letters for Substitution cipher.")
        return None
    # Create substitution mapping
    substitution_mapping = {chr(65 + i): key[i] for i in range(26)}
    result = ""
    for char in plaintext:
        if char.isalpha():
            result += substitution_mapping[char.upper()]
        else:
            result += char
    return result


def otp_encrypt(plaintext, key):
    # Remove non-alphabetic characters from plaintext
    plaintext_alpha = ''.join([c.upper() for c in plaintext if c.isalpha()])
    if len(key) != len(plaintext_alpha):
        print("Key must be the same length as the plaintext (after removing non-alphabetic characters) for OTP.")
        return None
    if not key.isalpha():
        print("Key must only contain letters for OTP.")
        return None
    key = key.upper()
    result = ''
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            char_code = ord(char.upper()) - 65
            key_code = ord(key[key_index]) - 65
            encrypted_code = (char_code + key_code) % 26
            result += chr(encrypted_code + 65)
            key_index += 1
        else:
            result += char
    return result


def main():
    while True:
        print("\nAvailable ciphers:")
        print("1. Caesar Cipher")
        print("2. Vigenere Cipher")
        print("3. Affine Cipher")
        print("4. Hill Cipher (2x2)")
        print("5. Substitution Cipher")
        print("6. One-Time Pad (OTP)")
        print("7. Exit")
        choice = input("Enter the number corresponding to the cipher you want to use: ")
        if choice == '7':
            print("Exiting the program.")
            break
        elif choice not in ['1', '2', '3', '4', '5', '6']:
            print("Invalid choice. Please enter a number between 1 and 7.")
            continue
        plaintext = input("Enter the plaintext to encrypt: ")
        if choice == '1':
            # Caesar Cipher
            key = input("Enter the key (integer shift amount): ")
            result = caesar_cipher_encrypt(plaintext, key)
        elif choice == '2':
            # Vigenere Cipher
            key = input("Enter the key (a word or phrase): ")
            result = vigenere_cipher_encrypt(plaintext, key)
        elif choice == '3':
            # Affine Cipher
            key_a = input("Enter key 'a' (must be coprime with 26): ")
            key_b = input("Enter key 'b': ")
            result = affine_cipher_encrypt(plaintext, key_a, key_b)
        elif choice == '4':
            # Hill Cipher
            key_matrix = get_hill_cipher_key()
            if key_matrix is None:
                result = None
            else:
                result = hill_cipher_encrypt(plaintext, key_matrix)
        elif choice == '5':
            # Substitution Cipher
            key = input("Enter the key (a permutation of 26 unique letters): ")
            result = substitution_cipher_encrypt(plaintext, key)
        elif choice == '6':
            # One-Time Pad (OTP)
            # Remove non-alphabetic characters from plaintext
            plaintext_alpha = ''.join([c for c in plaintext if c.isalpha()])
            key = input(f"Enter the key (must be {len(plaintext_alpha)} letters): ")
            result = otp_encrypt(plaintext, key)
        if result is None:
            retry = input("Invalid input detected. Do you want to retry? (Y/N): ").upper()
            if retry != 'Y':
                print("Exiting the program.")
                break
            else:
                continue  # Go back to the start of the loop
        else:
            print(f"Encrypted text: {result}")
        # Ask the user if they want to encrypt another message
        retry = input("Do you want to encrypt another message? (Y/N): ").upper()
        if retry != 'Y':
            print("Exiting the program.")
            break


if __name__ == "__main__":
    main()
