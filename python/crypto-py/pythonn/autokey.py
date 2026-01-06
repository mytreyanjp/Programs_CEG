def format_text(text):
    return ''.join(filter(str.isalpha, text.upper()))

def generate_key_encrypt(plaintext, keyword):
    return (keyword + plaintext)[:len(plaintext)]

def autokey_encrypt(plaintext, keyword):
    plaintext = format_text(plaintext)
    key = generate_key_encrypt(plaintext, keyword.upper())
    ciphertext = ''

    for p_char, k_char in zip(plaintext, key):
        encrypted_char = chr(((ord(p_char) - 65 + ord(k_char) - 65) % 26) + 65)
        ciphertext += encrypted_char

    return ciphertext

def autokey_decrypt(ciphertext, keyword):
    ciphertext = format_text(ciphertext)
    key = keyword.upper()
    plaintext = ''

    for i in range(len(ciphertext)):
        k_char = key[i]
        decrypted_char = chr(((ord(ciphertext[i]) - ord(k_char) + 26) % 26) + 65)
        plaintext += decrypted_char
        key += decrypted_char 

    return plaintext

# Example Usage
plaintext = input("Enter input: ")
plaintext.upper()
keyword = "KEY"

cipher = autokey_encrypt(plaintext, keyword)
print("Encrypted:", cipher)

decrypted = autokey_decrypt(cipher, keyword)
print("Decrypted:", decrypted.lower())
