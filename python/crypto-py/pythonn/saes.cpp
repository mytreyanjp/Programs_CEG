#include <bits/stdc++.h>
using namespace std;

// --- Step 1: Define S-Box and Inverse S-Box ---
map<int, int> S_BOX = {
    {0x0, 0x9}, {0x1, 0x4}, {0x2, 0xA}, {0x3, 0xB},
    {0x4, 0xD}, {0x5, 0x1}, {0x6, 0x8}, {0x7, 0x5},
    {0x8, 0x6}, {0x9, 0x2}, {0xA, 0x0}, {0xB, 0x3},
    {0xC, 0xC}, {0xD, 0xE}, {0xE, 0xF}, {0xF, 0x7}
};

map<int, int> INV_S_BOX;

// --- Step 2: Helper functions ---
int sub_nibbles(int byte) {
    return (S_BOX[(byte >> 4) & 0xF] << 4) | S_BOX[byte & 0xF];
}

int inv_sub_nibbles(int byte) {
    return (INV_S_BOX[(byte >> 4) & 0xF] << 4) | INV_S_BOX[byte & 0xF];
}

int shift_rows(int word) {
    return ((word & 0xF0) >> 4) | ((word & 0x0F) << 4);
}

int gf_mult(int a, int b) {
    int p = 0;
    for (int i = 0; i < 4; i++) {
        if (b & 1) p ^= a;
        int carry = a & 0x8;
        a = (a << 1) & 0xF;
        if (carry) a ^= 0x3;
        b >>= 1;
    }
    return p & 0xF;
}

int mix_columns(int word) {
    int a0 = (word >> 12) & 0xF;
    int a1 = (word >> 8) & 0xF;
    int a2 = (word >> 4) & 0xF;
    int a3 = word & 0xF;

    int b0 = a0 ^ gf_mult(4, a2);
    int b1 = a1 ^ gf_mult(4, a3);
    int b2 = a2 ^ gf_mult(4, a0);
    int b3 = a3 ^ gf_mult(4, a1);

    return (b0 << 12) | (b1 << 8) | (b2 << 4) | b3;
}

// --- Step 3: Key Expansion (16-bit -> 3 round keys) ---
vector<int> key_expansion(int key) {
    vector<int> w(6);
    w[0] = (key >> 8) & 0xFF;
    w[1] = key & 0xFF;

    int RCON1 = 0x80, RCON2 = 0x30;

    w[2] = w[0] ^ sub_nibbles(shift_rows(w[1])) ^ RCON1;
    w[3] = w[2] ^ w[1];
    w[4] = w[2] ^ sub_nibbles(shift_rows(w[3])) ^ RCON2;
    w[5] = w[4] ^ w[3];

    int k0 = (w[0] << 8) | w[1];
    int k1 = (w[2] << 8) | w[3];
    int k2 = (w[4] << 8) | w[5];

    return {k0, k1, k2};
}

// --- Step 4: AddRoundKey ---
int add_round_key(int state, int key) {
    return state ^ key;
}

// --- Step 5: Encryption ---
int encrypt(int plaintext, int key) {
    vector<int> keys = key_expansion(key);
    int k0 = keys[0], k1 = keys[1], k2 = keys[2];

    int state = add_round_key(plaintext, k0);

    state = (sub_nibbles((state >> 8) & 0xFF) << 8) | sub_nibbles(state & 0xFF);
    state = shift_rows(state);
    state = mix_columns(state);
    state = add_round_key(state, k1);

    state = (sub_nibbles((state >> 8) & 0xFF) << 8) | sub_nibbles(state & 0xFF);
    state = shift_rows(state);
    state = add_round_key(state, k2);

    return state;
}

// --- Step 6: Decryption ---
int decrypt(int ciphertext, int key) {
    vector<int> keys = key_expansion(key);
    int k0 = keys[0], k1 = keys[1], k2 = keys[2];

    int state = add_round_key(ciphertext, k2);
    state = shift_rows(state);
    state = (inv_sub_nibbles((state >> 8) & 0xFF) << 8) | inv_sub_nibbles(state & 0xFF);

    state = add_round_key(state, k1);
    state = mix_columns(state); // same in S-AES
    state = shift_rows(state);
    state = (inv_sub_nibbles((state >> 8) & 0xFF) << 8) | inv_sub_nibbles(state & 0xFF);

    state = add_round_key(state, k0);
    return state;
}

// --- Main Function ---
int main() {
    // build inverse S-BOX
    for (auto &p : S_BOX) {
        INV_S_BOX[p.second] = p.first;
    }

    int plaintext = 0b1101011100101000; // Example 16-bit plaintext
    int key = 0b0100101011110101;       // Example 16-bit key

    cout << "Plaintext : " << bitset<16>(plaintext) << endl;
    int ciphertext = encrypt(plaintext, key);
    cout << "Ciphertext: " << bitset<16>(ciphertext) << endl;
    int decrypted = decrypt(ciphertext, key);
    cout << "Decrypted : " << bitset<16>(decrypted) << endl;

    return 0;
}

This paste expires in <1 hour. Public IP access. Share whatever you see with others in seconds with Context.Terms of ServiceReport this