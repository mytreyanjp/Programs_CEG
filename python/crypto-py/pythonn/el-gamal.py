# -------------------------------
# Diffie–Hellman Key Exchange
# -------------------------------
import random

# Function for modular exponentiation
def power(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

# Example small prime and primitive root
p = 23      # prime number
g = 5       # primitive root modulo 23

print("Publicly shared values:")
print("Prime (p):", p)
print("Primitive root (g):", g)

# Alice's private and public keys
a = random.randint(1, p-2)
A = power(g, a, p)

# Bob's private and public keys
b = random.randint(1, p-2)
B = power(g, b, p)

print("\nAlice sends public key A =", A)
print("Bob sends public key B =", B)

# Shared secret calculation
secret_A = power(B, a, p)
secret_B = power(A, b, p)

print("\nShared secret (Alice):", secret_A)
print("Shared secret (Bob):", secret_B)
