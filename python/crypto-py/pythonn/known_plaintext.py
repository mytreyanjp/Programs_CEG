def caesar_decrypt(ciphertext, key):
    decrypted = ''
    for char in ciphertext:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            decrypted += chr((ord(char) - shift - key) % 26 + shift)
        else:
            decrypted += char
    return decrypted

def known_plaintext_attack(ciphertext, known_plaintext):
    for key in range(26):
        decrypted = caesar_decrypt(ciphertext, key)
        if known_plaintext in decrypted:
            print(f"[+] Key found: {key}")
            print(f"[+] Decrypted text: {decrypted}")
            return key, decrypted
    print("[-] No matching key found.")
    return None, None

# Example usage
ciphertext = "Wklv lv d whvw phvvdjh"  # Encrypted with Caesar cipher (key = 3)
known_plaintext = "test message"

known_plaintext_attack(ciphertext, known_plaintext)

print("-----------------------------------------------------------------")

from math import gcd

# Encrypt using Affine Cipher
def affine_encrypt(plaintext, a, b):
    m = 26
    encrypted = ''
    for char in plaintext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            x = ord(char) - offset
            y = (a * x + b) % m
            encrypted += chr(y + offset)
        else:
            encrypted += char
    return encrypted

# Decrypt using Affine Cipher
def affine_decrypt(ciphertext, a, b):
    m = 26
    a_inv = mod_inverse(a, m)
    if a_inv is None:
        return None
    decrypted = ''
    for char in ciphertext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            y = ord(char) - offset
            x = (a_inv * (y - b)) % m
            decrypted += chr(x + offset)
        else:
            decrypted += char
    return decrypted

# Modular inverse using brute-force
def mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

# Known Plaintext Attack
def known_plaintext_attack(ciphertext, known_plaintext):
    m = 26
    for a in range(1, m):
        if gcd(a, m) != 1:
            continue
        for b in range(m):
            decrypted = affine_decrypt(ciphertext, a, b)
            if decrypted and known_plaintext.lower() in decrypted.lower():
                print(f"[+] Key found: a={a}, b={b}")
                print(f"[+] Decrypted text: {decrypted}")
                return a, b, decrypted
    print("[-] No matching key found.")
    return None, None, None

# Example usage

    # Step 1: Encrypt a known plaintext
plaintext = "hello world, this is an simple message"
a, b = 5, 8
ciphertext = affine_encrypt(plaintext, a, b)
print(f"Encrypted: {ciphertext}")

# Step 2: Run known plaintext attack
known_plaintext = "hello"
known_plaintext_attack(ciphertext, known_plaintext)