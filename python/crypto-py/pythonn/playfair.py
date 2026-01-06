def generate_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" 
    key = key.upper().replace("J", "I")
    matrix = []
    used = set()

    for char in key:
        if char not in used and char in alphabet:
            matrix.append(char)
            used.add(char)

    for char in alphabet:
        if char not in used:
            matrix.append(char)
            used.add(char)

    return [matrix[i*5:(i+1)*5] for i in range(5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None

def prepare_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    prepared = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = ''
        if i+1 < len(text):
            b = text[i+1]
        else:
            b = 'X'  

        if a == b:
            prepared += a + 'X'
            i += 1
        else:
            prepared += a + b
            i += 2

    if len(prepared) % 2 != 0:
        prepared += 'X'

    return prepared

def playfair_encrypt(plaintext, key):
    matrix = generate_matrix(key)
    text = prepare_text(plaintext)
    ciphertext = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2: 
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2: 
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else: 
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]

    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = generate_matrix(key)
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:  
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:  
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]

    return ''.join([i for i in plaintext if i!='X'])

key = input("Enter key:")
plaintext = input("ENTER WORD: ")
plaintext.upper()
encrypted = playfair_encrypt(plaintext, key)
print("Encrypted:", encrypted)

decrypted = playfair_decrypt(encrypted, key)
print("Decrypted:", decrypted.lower())
