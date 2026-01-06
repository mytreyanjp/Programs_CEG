import base64

def ksa(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def prga(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def rc4(key, plaintext):
    key = [ord(c) for c in key]
    S = ksa(key)
    keystream = prga(S)
    
    res = []
    for char in plaintext:
        x = next(keystream)
        val = ord(char) ^ x
        print((char), "->", ord(char), "XOR", x, "=", val, " (", hex(val), ")")
        res.append(val)
    
    return bytes(res)

key = "secretkey"
plaintext = "Hello, RC4!"

ciphertext_bytes = rc4(key, plaintext)

cipher_b64 = base64.b64encode(ciphertext_bytes).decode('utf-8')
print("\nBase64 Encoded Ciphertext:", cipher_b64)

decoded_ciphertext = base64.b64decode(cipher_b64)
decrypted_bytes = rc4(key, decoded_ciphertext.decode('latin1'))
print("\nDecrypted text:", decrypted_bytes.decode())
