import nltk
from nltk.corpus import words
from collections import Counter
import re

ciphertext="DECTOP ESCPLE XZOPW TD ZYP ZQ ESP MPDE ESCPLE XZOPWTYR XPESZOZWZRTPD LGLTWLMWP TE AFED QZCHLCO L QCLXPHZCV ESLE TD XZDE HTOPWJ FDPO EZ LNNPDD NJMPCDPNFCTEJTE LWDZ OPXLYOD EZ TOPYETQJ LYO NWLDDTQJ ESCPLED MJ YLEFCP ZQ ESPTC LEELNV FYOPC SPLOD YLXPWJ DAZZQTYRELXAPCTYRCPAFOTLETZYTYQZCXLETZY OTDNWZDFCPOPYTLW ZQDPCGTNPOZDLYO PWPGLETZY ZQ ACTGTWPRP. NJMPC PIAPCED NSZZDP ESP DECTOP ESCPLE XZOPW LMZGP XLYJ ZESPC ESCPLE XZOPWTYR LAACZLNSPD MPNLFDP ZQ TED XLYJ MPYPQTED"

def caesar_decrypt(text, shift):

    decrypted_text = ""
    for char in text:
        if 'A' <= char <= 'Z':
            decrypted_text += chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
        elif 'a' <= char <= 'z':
            decrypted_text += chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
        else:
            decrypted_text += char
    return decrypted_text

def calculate_word_validity(text):

    words_in_text = re.findall(r'\b[A-Za-z]+\b', text.lower())
    if not words_in_text:
        return 0

    valid_word_count = 0
    for word in words_in_text:
        if word in words.words():
            valid_word_count += 1
    return (valid_word_count / len(words_in_text)) * 100


def analyze_with_wordnet(ciphertext):
    print("\n--- 1. Ciphertext Only Attack using WordNet (Caesar Cipher) ---")
    best_shift = -1
    highest_validity = 0.0
    potential_plaintexts = []

    for shift in range(26):
        decrypted_text = caesar_decrypt(ciphertext, shift)
        validity = calculate_word_validity(decrypted_text)

        if validity > highest_validity:
            highest_validity = validity
            best_shift = shift
            potential_plaintexts = [(decrypted_text, shift, validity)]
        elif validity == highest_validity and validity > 0:
            potential_plaintexts.append((decrypted_text, shift, validity))

    if best_shift != -1:
        print(f"Best potential shift(s) found with highest word validity ({highest_validity:.2f}%):")
        for pt, shift, validity in potential_plaintexts:
            print(f"  Shift: {shift}, Key: {chr(ord('A') + (26 - shift) % 26)} (Caesar reverse shift)")
            print(f"  Decrypted Sample (first 200 chars): {pt[:200]}...")
            print("-" * 30)
    else:
        print("No meaningful decryption found using Caesar cipher and WordNet validity.")



if __name__ == "__main__":
    analyze_with_wordnet(ciphertext)
