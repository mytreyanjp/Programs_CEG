
S_BOX = {
    0x0: 0x9, 0x1: 0x4, 0x2: 0xA, 0x3: 0xB,
    0x4: 0xD, 0x5: 0x1, 0x6: 0x8, 0x7: 0x5,
    0x8: 0x6, 0x9: 0x2, 0xA: 0x0, 0xB: 0x3,
    0xC: 0xC, 0xD: 0xE, 0xE: 0xF, 0xF: 0x7
}
INV_S_BOX = {v: k for k, v in S_BOX.items()}


def gf_mult(a, b):
    a &= 0xF; b &= 0xF
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        carry = a & 0x8
        a = (a << 1) & 0xF
        if carry:
            a ^= 0x3 
        b >>= 1
    return p & 0xF

def sub_nibbles16(state):
    n0 = (state >> 12) & 0xF
    n1 = (state >> 8)  & 0xF
    n2 = (state >> 4)  & 0xF
    n3 =  state        & 0xF
    n0 = S_BOX[n0]; n1 = S_BOX[n1]; n2 = S_BOX[n2]; n3 = S_BOX[n3]
    return (n0 << 12) | (n1 << 8) | (n2 << 4) | n3

def inv_sub_nibbles16(state):
    n0 = (state >> 12) & 0xF
    n1 = (state >> 8)  & 0xF
    n2 = (state >> 4)  & 0xF
    n3 =  state        & 0xF
    n0 = INV_S_BOX[n0]; n1 = INV_S_BOX[n1]; n2 = INV_S_BOX[n2]; n3 = INV_S_BOX[n3]
    return (n0 << 12) | (n1 << 8) | (n2 << 4) | n3

def shift_rows(state):

    n0 = (state >> 12) & 0xF
    n1 = (state >> 8)  & 0xF
    n2 = (state >> 4)  & 0xF
    n3 =  state        & 0xF
    
    return (n0 << 12) | (n3 << 8) | (n2 << 4) | (n1)

def inv_shift_rows(state):

    return shift_rows(state)

def mix_columns(state):

    n0 = (state >> 12) & 0xF
    n1 = (state >> 8)  & 0xF
    n2 = (state >> 4)  & 0xF
    n3 =  state        & 0xF
    b0 = n0 ^ gf_mult(4, n2)
    b1 = n1 ^ gf_mult(4, n3)
    b2 = n2 ^ gf_mult(4, n0)
    b3 = n3 ^ gf_mult(4, n1)
    return (b0 << 12) | (b1 << 8) | (b2 << 4) | b3

def inv_mix_columns(state):
 
    n0 = (state >> 12) & 0xF
    n1 = (state >> 8)  & 0xF
    n2 = (state >> 4)  & 0xF
    n3 =  state        & 0xF
    b0 = gf_mult(9, n0) ^ gf_mult(2, n2)
    b1 = gf_mult(9, n1) ^ gf_mult(2, n3)
    b2 = gf_mult(2, n0) ^ gf_mult(9, n2)
    b3 = gf_mult(2, n1) ^ gf_mult(9, n3)
    return (b0 << 12) | (b1 << 8) | (b2 << 4) | b3

def sub_nibbles8(byte):
    return (S_BOX[(byte >> 4) & 0xF] << 4) | S_BOX[byte & 0xF]

def rot_nibbles8(byte):
    return ((byte & 0x0F) << 4) | ((byte & 0xF0) >> 4)

def key_expansion(key16):
    w0 = (key16 >> 8) & 0xFF
    w1 = key16 & 0xFF
    RCON1, RCON2 = 0x80, 0x30
    w2 = w0 ^ sub_nibbles8(rot_nibbles8(w1)) ^ RCON1
    w3 = w2 ^ w1
    w4 = w2 ^ sub_nibbles8(rot_nibbles8(w3)) ^ RCON2
    w5 = w4 ^ w3
    k0 = (w0 << 8) | w1
    k1 = (w2 << 8) | w3
    k2 = (w4 << 8) | w5
    return k0, k1, k2

def add_round_key(state, key):
    return state ^ key


def encrypt_saes(plaintext, key16):
    k0, k1, k2 = key_expansion(key16)
    print("Expanded key: ",k0,k1,k2)
    s = add_round_key(plaintext, k0)
    print("Block after added round key:",s)
    s = sub_nibbles16(s)
    print("Round 1 -> Sub bytes:",s)
    s = shift_rows(s)
    print("Round 1 -> Shift rows:",s)
    s = mix_columns(s)
    print("Round 1 -> Mix columns:",s)
    s = add_round_key(s, k1)
    print("Round 1 -> Round key k1:",s)
    s = sub_nibbles16(s)
    s = shift_rows(s)
    s = add_round_key(s, k2)
    return s & 0xFFFF


def decrypt_saes(ciphertext, key16):
    k0, k1, k2 = key_expansion(key16)
    s = add_round_key(ciphertext, k2)
    s = inv_shift_rows(s)
    s = inv_sub_nibbles16(s)
    s = add_round_key(s, k1)
    s = inv_mix_columns(s)
    s = inv_shift_rows(s)
    s = inv_sub_nibbles16(s)
    s = add_round_key(s, k0)
    return s & 0xFFFF


if __name__ == "__main__":
    P = int("1101011100101000", 2) 
    K = int("0100101011110101", 2)  
    C = encrypt_saes(P, K)
    D = decrypt_saes(C, K)
    print("Plaintext : ", format(P, "016b"))
    print("Ciphertext:", format(C, "016b"))
    print("Decrypted : ", format(D, "016b"))


#cipher=0b0010010011101100