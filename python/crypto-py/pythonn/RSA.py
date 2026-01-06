import math

def gcd(a, b):
    """Computes the greatest common divisor of a and b."""
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(num):
    """Checks if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_key_pair(p, q):
    """Generates RSA public and private key pairs."""
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    if p == q:
        raise ValueError("p and q cannot be equal.")

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e (public exponent) such that 1 < e < phi and gcd(e, phi) = 1
    e = 2
    while e < phi:
        if gcd(e, phi) == 1:
            break
        e += 1

    # Calculate d (private exponent) such that d*e ≡ 1 (mod phi)
    d = 0
    for k in range(1, phi):
        if (k * phi + 1) % e == 0:
            d = (k * phi + 1) // e
            break

    return (e, n), (d, n)  # Public key (e, n), Private key (d, n)

def encrypt(public_key, plaintext):
    """Encrypts a message using the public key."""
    e, n = public_key
    cipher_text = [pow(ord(char), e, n) for char in plaintext]
    return cipher_text

def decrypt(private_key, ciphertext):
    """Decrypts a message using the private key."""
    d, n = private_key
    decrypted_message = [chr(pow(char, d, n)) for char in ciphertext]
    return "".join(decrypted_message)

# Example Usage
if __name__ == "__main__":
    p = 61
    q = 53
    public_key, private_key = generate_key_pair(p, q)

    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    message = "Hello RSA!"
    print(f"Original Message: {message}")

    encrypted_message = encrypt(public_key, message)
    print(f"Encrypted Message: {encrypted_message}")

    decrypted_message = decrypt(private_key, encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")