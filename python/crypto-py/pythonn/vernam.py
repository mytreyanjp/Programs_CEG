import os

def encrypt(plaintext,key):
    plaintext_bytes=plaintext.encode()
    cipher=bytes([p^k for p,k in zip(plaintext_bytes,key)])
    return cipher

def decrypt(cipher,key):
    decrypted=bytes([c^k for c,k in zip(cipher,key)])
    return decrypted.decode()

msg="Hello Lab"
key=os.urandom(len(msg))
print(key)
a=encrypt(msg,key)
print("Encrypted:",a)

b=decrypt(a,key)
print("Decrypted:",b)