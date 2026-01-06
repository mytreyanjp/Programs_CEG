import random

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, int(n**0.5)+1, 6):
        if n % i == 0 or n % (i+2) == 0:
            return False
    return True

def generate_large_prime(start=1000, end=5000):
    while True:
        p = random.randint(start, end)
        if is_prime(p):
            return p

def mod_inverse(a, p):
    return pow(a, -1, p)

def generate_keys():
    p = generate_large_prime()
    g = random.randint(2, p - 1)
    x = random.randint(2, p - 2)
    y = pow(g, x, p)
    return (p, g, y), x

def encrypt(p, g, y, m):
    k = random.randint(2, p - 2)
    a = pow(g, k, p)
    b = (m * pow(y, k, p)) % p
    return a, b

def decrypt(p, x, a, b):
    s = pow(a, x, p)
    s_inv = mod_inverse(s, p)
    m = (b * s_inv) % p
    return m

if __name__ == "__main__":
    public_key, private_key = generate_keys()
    p, g, y = public_key
    x = private_key

    message = 1234  # Must be less than p
    a, b = encrypt(p, g, y, message)
    decrypted = decrypt(p, x, a, b)

    print(f"Public key: p={p}, g={g}, y={y}")
    print(f"Private key: x={x}")
    print(f"Original message: {message}")
    print(f"Encrypted: a={a}, b={b}")
    print(f"Decrypted message: {decrypted}")