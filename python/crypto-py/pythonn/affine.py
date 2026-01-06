def mod_inverse(a,m):
    for x in range (1,m):
        if (a*x)%m==1:
            return x
    return -1
def affine_encrypt(text,a,b):
    result=""
    for char in text:
        if char.isalpha():
            base=ord('A') if char.isupper() else ord('a')
            x=ord(char)-base
            result+=chr((a*x+b)%26+base)
        else:
            result+=char
    return result.upper()

def affine_decrypt(cipher,a_inv,b):
    result=""
    for char in cipher:
        if char.isalpha():
            base=ord('A') if char.isupper() else ord('a')
            y=ord(char)-base
            result+=chr((a_inv*(y+b))%26+base)
        else:
            result+=char
    return result.lower()

while True:
    n=int(input("1 for Encrypt, 2 for Decrypt, -1 to Exit: "))
    if n==1:
        while True:
            a=int(input("Enter multiplicative key: "))
            l=mod_inverse(a,26)
            if l>0:
                print("Valid inverse key exists: ",l)
                break
            print("Please enter a valid key")
        b=int(input("Enter Addiive key:"))
        word=input("Enter word to encrypt:")
        word.upper()
        res=affine_encrypt(word,a,b)
        print("Cipher word:",res)

    elif n==2:
        while True:
            a_inv=int(input("Enter multiplicative inverse key: "))
            l=mod_inverse(a_inv,26)
            if l>0:
                print("Valid key exists: ",l)
                break
            print("Please enter a valid key")
        b=int(input("Enter Addiive inverse key:"))
        cipher=input("Enter a cipher to decrypt: ")
        print("Decrypted word: ",affine_decrypt(cipher,a_inv,b))
        
    elif n==-1:
        break

    else:
        print("Invalid input")


