
def permute(bits, table):
    return [bits[i] for i in table]

def left_shift(bits, shift):
    return bits[shift:] + bits[:shift]

def sbox_lookup(bits, sbox):
    row = int(f"{bits[0]}{bits[3]}", 2) 
    col = int(f"{bits[1]}{bits[2]}", 2)  
    val = sbox[row][col]
    return [int(b) for b in f"{val:02b}"]

def generate_keys(key10):
    p10_table = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
    key10 = permute(key10, p10_table)

    left, right = key10[:5], key10[5:]

    left = left_shift(left, 1)
    right = left_shift(right, 1)
    p8_table = [5, 2, 6, 3, 7, 4, 9, 8]
    k1 = permute(left + right, p8_table)

    left = left_shift(left, 2)
    right = left_shift(right, 2)
    k2 = permute(left + right, p8_table)

    return k1, k2

def fk(bits, subkey):

    left, right = bits[:4], bits[4:]

    ep_table = [3, 0, 1, 2, 1, 2, 3, 0]
    right_expanded = permute(right, ep_table)

    xor_result = [r ^ k for r, k in zip(right_expanded, subkey)]

    s0 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ]
    s1 = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
    ]
    left_sbox = sbox_lookup(xor_result[:4], s0)
    right_sbox = sbox_lookup(xor_result[4:], s1)
    p4_table = [1, 3, 2, 0]
    p4_result = permute(left_sbox + right_sbox, p4_table)

    left_result = [l ^ p for l, p in zip(left, p4_result)]


    return left_result + right 

def encrypt(plaintext8, key10):
    k1, k2 = generate_keys(key10)
    print("Key1: ",k1,"Key2: ",k2)
    ip_table = [1, 5, 2, 0, 3, 7, 4, 6]
    bits = permute(plaintext8, ip_table)

    bits = fk(bits, k1)

    bits = bits[4:] + bits[:4]

    bits = fk(bits, k2)

    ip_inv_table = [3, 0, 2, 4, 6, 1, 7, 5]
    ciphertext = permute(bits, ip_inv_table)
    return ciphertext

def decrypt(ciphertext8, key10):
    k1, k2 = generate_keys(key10)

    ip_table = [1, 5, 2, 0, 3, 7, 4, 6]
    bits = permute(ciphertext8, ip_table)

    bits = fk(bits, k2)

    bits = bits[4:] + bits[:4]

    bits = fk(bits, k1)

    ip_inv_table = [3, 0, 2, 4, 6, 1, 7, 5]
    plaintext = permute(bits, ip_inv_table)


    return plaintext

key10 = [1, 0, 1, 1, 0, 0, 0, 0, 1, 0]
plaintext8 = [1, 0, 1, 1, 1, 0, 1, 0]
print("Plaintext:",plaintext8)
cipher = encrypt(plaintext8, key10)
print("Ciphertext:", cipher)

plain = decrypt(cipher, key10)
print("Decrypted:", plain)