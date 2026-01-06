import hashlib
a=input("Enter text to hash:")
hash_object = hashlib.sha256()
hash_object.update(a.encode())
hex_dig = hash_object.hexdigest()
print(hex_dig)