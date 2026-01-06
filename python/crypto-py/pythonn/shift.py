word=input("Enter the word: ")
n=int(input("Enter the shift number: "))
word=word.upper()
print("Word: ",word)
res=""
for i in word:
    res+=chr(((ord(i)-65+n)%26)+65)
print("Encrypted:",res)
dec=""
for i in res:
    dec+=chr(((ord(i)-65-n)%26)+65)
print("Decrypted:",dec.lower())