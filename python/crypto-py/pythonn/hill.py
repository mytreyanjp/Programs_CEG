import numpy as np

def mod_inv(a, m):
    a = a % m
    for i in range(1, m):
        if (a * i) % m == 1:
            print("Valid key: ",i)
            return i
        
    return None

def hill_encrypt(text, key):
    text = text.upper().replace(" ", "")
    while len(text) % 2 != 0:
        text += 'X'
    res = ""
    for i in range(0, len(text), 2):
        rec = [ord(c) - 65 for c in text[i:i+2]]
        enc = np.dot(key, rec) % 26
        res += ''.join(chr(num + 65) for num in enc)
    return res

def hill_decrypt(cipher, key):
    det = int(round(np.linalg.det(key))) % 26
    inv_det = mod_inv(det, 26)
    if inv_det is None:
        return "Key matrix is not invertible modulo 26, can't decrypt."
    inv_key = np.round(inv_det * np.linalg.inv(key) * det).astype(int) % 26
    res = ""
    for i in range(0, len(cipher), 2):
        rec = [ord(c) - 65 for c in cipher[i:i+2]]
        dec = np.dot(inv_key, rec) % 26
        res += ''.join(chr(num + 65) for num in dec)
    return res

def input_key():
    print("Enter 2x2 key matrix values (integers 0-25) row-wise separated by space:")
    while True:
        try:
            values = input().strip()
            if values == '-1':
                return None
            vals = list(map(int, values.split()))
            if len(vals) != 4 or any(not (0 <= v <= 25) for v in vals):
                print("Please enter exactly 4 integers between 0 and 25.")
                continue
            key_matrix = np.array(vals).reshape(2, 2)
            det = int(round(np.linalg.det(key_matrix))) % 26
            if mod_inv(det, 26) is None:
                print("Key matrix determinant has no modular inverse mod 26. Choose another key.")
                continue
            return key_matrix
        except ValueError:
            print("Invalid input. Enter 4 integers separated by space or -1 to exit.")

def main():
    print("Hill Cipher (2x2 matrix) - Enter '-1' at any prompt to exit.")
    while True:
        op = input("\nChoose operation: 1 for Encrypt, 2 for Decrypt: ").strip()
        if op == '-1':
            print("Exiting.")
            break
        if op not in {'1', '2'}:
            print("Invalid choice. Try again.")
            continue

        key = input_key()
        if key is None:
            print("Exiting.")
            break

        if op == '1':
            plaintext = input("Enter plaintext to encrypt: ").strip()
            if plaintext == '-1':
                print("Exiting.")
                break
            ciphertext = hill_encrypt(plaintext, key)
            print("Encrypted text:", ciphertext)
        else:
            ciphertext = input("Enter ciphertext to decrypt: ").strip()
            if ciphertext == '-1':
                print("Exiting.")
                break
            plaintext = hill_decrypt(ciphertext, key)
            print("Decrypted text:", plaintext)

if __name__ == "__main__":
    main()
