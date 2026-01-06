# Diffie-Hellman Key Exchange
# No libraries used — only built-in Python math and random functions

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

# Input shared public values
p = int(input("Enter a prime number (p): "))
g = int(input("Enter a primitive root of p (g): "))

# Alice chooses a private key (a)
a = int(input("Enter Alice's private key (a): "))

# Bob chooses a private key (b)
b = int(input("Enter Bob's private key (b): "))

# Compute public keys
A = power(g, a, p)  # Alice sends this to Bob
B = power(g, b, p)  # Bob sends this to Alice

print("\nPublicly shared values:")
print("Prime (p):", p)
print("Base (g):", g)
print("Alice's public key (A):", A)
print("Bob's public key (B):", B)

# Compute the shared secret keys
secret_A = power(B, a, p)
secret_B = power(A, b, p)

print("\nShared secret computed by Alice:", secret_A)
print("Shared secret computed by Bob:  ", secret_B)

# Check if they match
if secret_A == secret_B:
    print("\n✅ Key exchange successful! Shared secret =", secret_A)
else:
    print("\n❌ Keys do not match. Check inputs.")
