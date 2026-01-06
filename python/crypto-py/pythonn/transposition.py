import math

def keyless_encrypt(plaintext, num_columns=2):
    plaintext = plaintext.replace(" ", "") 
    num_rows = math.ceil(len(plaintext) / num_columns)
    grid = ['' for _ in range(num_columns)]

    for i, char in enumerate(plaintext):
        col = i % num_columns
        grid[col] += char

    ciphertext = ''.join(grid)
    return ciphertext

def keyless_decrypt(ciphertext, num_columns=2):
    num_rows = math.ceil(len(ciphertext) / num_columns)
    num_full_cols = len(ciphertext) % num_columns
    if num_full_cols == 0:
        num_full_cols = num_columns

    col_lengths = [num_rows if i < num_full_cols else num_rows - 1 for i in range(num_columns)]
    
    index = 0
    columns = []
    for length in col_lengths:
        columns.append(ciphertext[index:index+length])
        index += length

    plaintext = ''
    for r in range(num_rows):
        for c in range(num_columns):
            if r < len(columns[c]):
                plaintext += columns[c][r]

    return plaintext

def keyed_encrypt(plaintext, key):
    col=len(key)
    order=sorted(range(col),key=lambda x:key[x])
    rows=[plaintext[i:i+col] for i in range(0,len(plaintext),col)]
    while len(rows[-1])<col: rows[-1]+='X' 
    return ''.join(''.join(row[i] for row in rows) for i in order)

def keyed_decrypt(ciphertext, key):
    col=len(key)
    row=len(ciphertext)//col
    order=sorted(range(col),key=lambda x:key[x])
    cols=['']*col
    idx=0
    for i in order:
        cols[i]=ciphertext[idx:idx+row]
        idx+=row
    return ''.join(''.join(x) for x in zip(* cols))

def combination_encrypt(plaintext, key, num_columns=5):
    return keyed_encrypt( keyless_encrypt(plaintext, num_columns), key)

def combination_decrypt(ciphertext, key, num_columns=5):
    return keyless_decrypt(keyed_decrypt(ciphertext, key), num_columns)



print("Transposition Cipher Program")
while True:
    print("Choose method:")
    print("0. Exit")
    print("1. Key-based")
    print("2. Keyless")
    print("3. Combination (Keyless + Key-based)")
    method = input("Enter choice (0/1/2/3): ").strip()

    if method not in {'0', '1', '2', '3'}:
        print("Invalid method choice.")
        continue

    if method=='0':
        break

    print("\nChoose operation:")
    print("1. Encrypt")
    print("2. Decrypt")
    operation = input("Enter choice (1/2): ").strip()
    if operation not in {'1', '2'}:
        print("Invalid operation choice.")
        continue

    if operation == '1':
        text = input("\nEnter plaintext to encrypt: ").strip()
    else:
        text = input("\nEnter ciphertext to decrypt: ").strip()

    key = None
    num_columns = 2

    if method in {'1', '3'}:
        key = input("Enter key (for key-based): ").strip()
        if not key:
            print("Key cannot be empty.")
            continue

    if method in {'2', '3'}:
        col_input = input("Enter number of columns for keyless (default 2): ").strip()
        if col_input.isdigit() and int(col_input) > 0:
            num_columns = int(col_input)
        else:
            print("Using default number of columns = 2")

    if method == '1': 
        if operation == '1':
            result = keyed_encrypt(text.replace(" ", ""), key)
            print("\nEncrypted ciphertext:", result.upper())
        else:
            result = keyed_decrypt(text, key)
            print("\nDecrypted plaintext:", result.lower())

    elif method == '2': 
        if operation == '1':
            result = keyless_encrypt(text, num_columns)
            print("\nEncrypted ciphertext:", result.upper())
        else:
            result = keyless_decrypt(text, num_columns)
            print("\nDecrypted plaintext:", result.lower())

    else:  
        if operation == '1':
            result = combination_encrypt(text.replace(" ", ""), key, num_columns)
            print("\nEncrypted ciphertext:", result.upper())
        else:
            result = combination_decrypt(text, key, num_columns)
            print("\nDecrypted plaintext:", result.lower())

