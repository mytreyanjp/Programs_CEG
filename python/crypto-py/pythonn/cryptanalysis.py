# =========================
# Toy Feistel Cipher (S-DES-style) + Brute Force, Linear, Differential Attacks
# =========================
# Block: 8 bits (L||R = 4+4), Master key: 10 bits → two 8-bit round subkeys (K1, K2)
# Rounds: 2 (like S-DES). This is ONLY a teaching cipher, not DES.
# =========================

from collections import Counter
import random

# --- Bit helpers ---
def bits(x, n): return [(x >> i) & 1 for i in reversed(range(n))]
def from_bits(b): 
    v = 0
    for bit in b: v = (v << 1) | (bit & 1)
    return v
def permute(x, in_size, order):
    b = bits(x, in_size)
    return from_bits([b[i-1] for i in order])  # order is 1-indexed

def rot_left(lst, k):
    k %= len(lst)
    return lst[k:] + lst[:k]

# --- S-DES tables (classic teaching values) ---
# Initial / Inverse permutations (same as S-DES teaching cipher)
IP  = [2,6,3,1,4,8,5,7]
IP1 = [4,1,3,5,7,2,8,6]
EP  = [4,1,2,3,2,3,4,1]   # expand 4→8
P10 = [3,5,2,7,4,10,1,9,8,6]
P8  = [6,3,7,4,8,5,10,9]
P4  = [2,4,3,1]

# S-boxes (rows picked by outer bits, cols by inner bits)
S0 = [
    [1,0,3,2],
    [3,2,1,0],
    [0,2,1,3],
    [3,1,3,2],
]
S1 = [
    [0,1,2,3],
    [2,0,1,3],
    [3,0,1,0],
    [2,1,0,3],
]

def sbox_lookup(sbox, x4):  # x4 is 4-bit int
    b = bits(x4, 4)
    row = (b[0] << 1) | b[3]
    col = (b[1] << 1) | b[2]
    return sbox[row][col]  # 2-bit int

# --- Key schedule (10-bit key → K1, K2  (both 8-bit)) ---
def key_schedule(key10):
    b = bits(key10, 10)
    p10 = [b[i-1] for i in P10]
    left, right = p10[:5], p10[5:]
    left = rot_left(left, 1); right = rot_left(right, 1)
    k1 = from_bits([(left+right)[i-1] for i in P8])
    left = rot_left(left, 2); right = rot_left(right, 2)
    k2 = from_bits([(left+right)[i-1] for i in P8])
    return k1, k2

# --- Round function f(R, K): 4 bits in → 4 bits out ---
def f_func(r4, k8):
    # Expand/permutation
    x = permute(r4, 4, EP)  # 8 bits
    x ^= k8
    L4 = (x >> 4) & 0xF
    R4 = x & 0xF
    s0 = sbox_lookup(S0, L4)  # 2 bits
    s1 = sbox_lookup(S1, R4)  # 2 bits
    s_out = (s0 << 2) | s1    # 4 bits
    y = permute(s_out, 4, P4) # 4 bits
    return y

# --- One Feistel round ---
def round_feistel(L4, R4, k8):
    return R4, L4 ^ f_func(R4, k8)

# --- Full encryption (2 rounds, like S-DES) ---
def encrypt_block(p8, key10):
    k1, k2 = key_schedule(key10)
    x = permute(p8, 8, IP)
    L, R = (x >> 4) & 0xF, x & 0xF
    L, R = round_feistel(L, R, k1)
    L, R = round_feistel(L, R, k2)
    pre = (R << 4) | L  # note: final swap in 2-round Feistel
    return permute(pre, 8, IP1)

def decrypt_block(c8, key10):
    # Feistel ⇒ decryption uses subkeys reversed
    k1, k2 = key_schedule(key10)
    x = permute(c8, 8, IP)
    L, R = (x >> 4) & 0xF, x & 0xF
    L, R = round_feistel(L, R, k2)
    L, R = round_feistel(L, R, k1)
    pre = (R << 4) | L
    return permute(pre, 8, IP1)

# =========================
# 1) Brute-force key search (on toy cipher)
# =========================
def brute_force_key(known_pairs):
    """
    known_pairs: list of (P8, C8) integers
    returns: list of keys (0..1023) that satisfy all pairs
    """
    candidates = []
    for k in range(1<<10):
        ok = True
        for p, c in known_pairs:
            if encrypt_block(p, k) != c:
                ok = False
                break
        if ok:
            candidates.append(k)
    return candidates

# =========================
# 2) Linear cryptanalysis demo (score last-round subkey K2)
# =========================
# Build linear approximation table (LAT) for a 4x2 S-box: map input mask -> output mask bias
def build_LAT(sbox):
    # inputs: 4 bits, outputs: 2 bits
    LAT = [[0]*4 for _ in range(16)]  # 16 input masks, 4 output masks (2 bits)
    for a in range(16):     # input mask (4 bits)
        for b in range(4):  # output mask (2 bits)
            cnt = 0
            for x in range(16):
                u = x
                v = sbox_lookup(sbox, x)  # 2-bit
                # parity of masked bits
                in_par  = bin(u & a).count("1") & 1
                out_par = bin(v & b).count("1") & 1
                if in_par == out_par:
                    cnt += 1
            LAT[a][b] = cnt - 8  # bias centered at 0
    return LAT

LAT_S0 = build_LAT(S0)
LAT_S1 = build_LAT(S1)

def linear_attack_last_round(known_PC, try_keys=None):
    """
    known_PC: list of (P8, C8) known plaintext/ciphertext
    Scores K2 (8-bit). Uses a simple linear relation:
      Choose a decent (a,b) per S-box from LAT, partially decrypt last round
      with K2 guess to expose each S-box input, and tally parity matches.
    Returns: Counter of scores per K2, most likely at top.
    """
    if try_keys is None:
        try_keys = range(256)

    # pick input/output masks with decent bias for S0 and S1
    # choose the (a,b) pair with maximum |bias|
    def best_masks(LAT):
        best = (0,0,0)
        for a in range(1,16):
            for b in range(1,4):
                bias = abs(LAT[a][b])
                if bias > abs(best[2]):
                    best = (a,b,LAT[a][b])
        return best  # (a,b,bias)
    a0,b0,_ = best_masks(LAT_S0)
    a1,b1,_ = best_masks(LAT_S1)

    scores = Counter()
    for k2 in try_keys:
        tally = 0
        for P, C in known_PC:
            # Partially decrypt last round to reveal inputs to S-boxes.
            # Undo IP: get pre = (R2||L2) after last swap
            x = permute(C, 8, IP)              # (L2', R2') in Feistel notation for decrypt
            L2, R2 = (x >> 4) & 0xF, x & 0xF
            # One decrypt round with k2:
            # decrypt round: newL = R2, newR = L2 ^ f(R2, k2) → (L1, R1)
            L1 = R2
            R1 = L2 ^ f_func(R2, k2)

            # We want S-box inputs of last encryption round = EP(R1) ^ k2 splitted
            u = permute(R1, 4, EP) ^ k2
            u0 = (u >> 4) & 0xF  # input to S0
            u1 = u & 0xF         # input to S1
            v0 = sbox_lookup(S0, u0)  # 2 bits
            v1 = sbox_lookup(S1, u1)  # 2 bits

            in_par  = ((bin(u0 & a0).count("1") ^ bin(u1 & a1).count("1")) & 1)
            out_par = ((bin(v0 & b0).count("1") ^ bin(v1 & b1).count("1")) & 1)
            tally += 1 if in_par == out_par else 0

        # convert to centered score
        scores[k2] = tally - (len(known_PC)//2)
    return scores

# =========================
# 3) Differential cryptanalysis demo (score last-round subkey K2)
# =========================
def build_DDT(sbox):
    # 4-bit in → 2-bit out
    DDT = [[0]*4 for _ in range(16)]  # input diff (0..15) → output diff (0..3)
    for dx in range(16):
        for x in range(16):
            y  = sbox_lookup(sbox, x)
            y2 = sbox_lookup(sbox, x ^ dx)
            DDT[dx][y ^ y2] += 1
    return DDT

DDT_S0 = build_DDT(S0)
DDT_S1 = build_DDT(S1)

def differential_attack_last_round(pairs, deltaP):
    """
    pairs: list of (P, P^=P^Δ, C, C^) where P^ = P ^ ΔP and C^ = E(P^) with same unknown key
    deltaP: fixed input difference (8-bit)
    Scores K2 by counting how often the observed last-round S-box output diffs
    match the predicted ones for a good characteristic traversing the last round.
    """
    # We only use 1-round projection through last round (classic last-round counting).
    scores = Counter()
    for k2 in range(256):
        count = 0
        for P, P2, C, C2 in pairs:
            # partially decrypt last round with k2 to expose S-box inputs
            x1 = permute(C,  8, IP);   L2, R2  = (x1 >> 4) & 0xF, x1 & 0xF
            x2 = permute(C2, 8, IP);   L2b,R2b = (x2 >> 4) & 0xF, x2 & 0xF

            # invert last round: (L1,R1) = (R2, L2 ^ f(R2,k2))
            L1,  R1  = R2,  L2  ^ f_func(R2,  k2)
            L1b, R1b = R2b, L2b ^ f_func(R2b, k2)

            # inputs to S-boxes of last round: EP(R1) ^ k2 and EP(R1b) ^ k2
            u  = permute(R1,  4, EP) ^ k2
            ub = permute(R1b, 4, EP) ^ k2
            u0, u1   = (u >> 4) & 0xF,  u & 0xF
            u0b, u1b = (ub>> 4) & 0xF, ub & 0xF

            # Compare S-box output differences (observed through partial decryption)
            v0,  v1  = sbox_lookup(S0, u0),  sbox_lookup(S1, u1)
            v0b, v1b = sbox_lookup(S0, u0b), sbox_lookup(S1, u1b)
            dv0, dv1 = v0 ^ v0b, v1 ^ v1b

            # Heuristic: count pairs where both S-box diffs are "likely" for the
            # resulting input diffs (u0^u0b, u1^u1b), i.e., DDT mass is above baseline.
            if DDT_S0[u0 ^ u0b][dv0] > 4 and DDT_S1[u1 ^ u1b][dv1] > 4:
                count += 1

        scores[k2] = count
    return scores

# =========================
# Demo / Usage
# =========================
if __name__ == "__main__":
    random.seed(7)

    # Pick a random 10-bit key and show a quick check
    KEY = random.randrange(1<<10)
    print(f"[Toy cipher] Secret key (10-bit): {KEY:010b} ({KEY})")

    # Generate some random known plaintext/ciphertext pairs
    known = []
    for _ in range(2000):
        p = random.randrange(256)
        c = encrypt_block(p, KEY)
        known.append((p, c))

    # ---- Brute force (on toy cipher) ----
    klist = brute_force_key(known[:3])  # a few pairs usually eliminate all but correct key
    print(f"[Brute force] Candidates with 3 pairs: {len(klist)}")
    if KEY in klist:
        print("  ✓ True key is among candidates.")
    # Tighten with more pairs
    klist = brute_force_key(known[:5])
    print(f"[Brute force] Candidates with 5 pairs: {len(klist)}")
    print(f"  Top few: {klist[:5]}")
    assert KEY in klist

    # ---- Linear cryptanalysis demo (score K2) ----
    lin_scores = linear_attack_last_round(known[:400])
    k2_true = key_schedule(KEY)[1]
    best_k2, best_score = max(lin_scores.items(), key=lambda kv: kv[1])
    print(f"[Linear] Best K2 guess: {best_k2:08b} (score={best_score}), true K2={k2_true:08b}")

    # ---- Differential cryptanalysis demo (score K2, chosen-plaintext model) ----
    # Use a fixed input difference (ΔP) and collect pairs (P, P^, C, C^)
    deltaP = 0x0C  # 00001100 as an example; some values work better than others
    pairs = []
    for _ in range(2000):
        P = random.randrange(256)
        P2 = P ^ deltaP
        C  = encrypt_block(P,  KEY)
        C2 = encrypt_block(P2, KEY)
        pairs.append((P, P2, C, C2))
    diff_scores = differential_attack_last_round(pairs, deltaP)
    best_k2_d, best_cnt = max(diff_scores.items(), key=lambda kv: kv[1])
    print(f"[Differential] Best K2 guess: {best_k2_d:08b} (count={best_cnt}), true K2={k2_true:08b}")

    # Tip: once K2 is recovered, you can search remaining 10-bit keys
    # that yield that K2 via the key schedule, or attack earlier rounds similarly.
