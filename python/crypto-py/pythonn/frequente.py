from collections import Counter

ciphertext = ("DECTOP ESCPLE XZOPW TD ZYP ZQ ESP MPDE ESCPLE XZOPWTYR XPESZOZWZRTPD "
              "LGLTWLMWP TE AFED QZCHLCO L QCLXPHZCV ESLE TD XZDE HTOPWJ FDPO EZ "
              "LNNPDD NJMPCDPNFCTEJTE LWDZ OPXLYOD EZ TOPYETQJ LYO NWLDDTQJ ESCPLED "
              "MJ YLEFCP ZQ ESPTC LEELNV FYOPC SPLOD YLXPWJ DAZZQTYRELXAPCTYRCPAFOTLETZYTYQZCXLETZY "
              "OTDNWZDFCPOPYTLW ZQDPCGTNPOZDLYO PWPGLETZY ZQ ACTGTWPRP. NJMPC PIAPCED NSZZDP ESP "
              "DECTOP ESCPLE XZOPW LMZGP XLYJ ZESPC ESCPLE XZOPWTYR LAACZLNSPD MPNLFDP ZQ TED XLYJ MPYPQTED")


cleaned_text = ''.join(filter(str.isalpha, ciphertext.upper()))
freq = Counter(cleaned_text)
most_common_cipher_letter, _ = freq.most_common(1)[0]

shift = (ord(most_common_cipher_letter) - ord('E')) % 26

def decrypt(text, shift):
    decrypted = []
    for char in text:
        if char.isalpha():
            base = ord('A')
            new_char = chr((ord(char) - base - shift) % 26 + base)
            decrypted.append(new_char)
        else:
            decrypted.append(char)
    return ''.join(decrypted)

decrypted_text = decrypt(ciphertext, shift)

print(f"Most frequent letter in ciphertext: '{most_common_cipher_letter}'")
print(f"Assumed shift: {shift}")
print("\nDecrypted text:\n")
print(decrypted_text)
