import nltk
from nltk.corpus import words
def mod_inverse(a,m):
    for x in range (1,m):
        if (a*x)%m==1:
            return x
    return -1

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

for i in range(27):
    if mod_inverse(i,26)>0:
        for j in range(27):
            ans=affine_decrypt("ZHTGSHR DXJBGSJDSDUTWBIHJCSGBLRTSUVQXOPKSVFOTKUP",i,-j)
            if ans.split(' ')[0] in words.words():
                print(mod_inverse(i,26),j,":", ans.replace(" ",""))