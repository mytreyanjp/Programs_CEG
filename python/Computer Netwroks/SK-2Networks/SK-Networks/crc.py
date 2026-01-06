def xor(a, b):
    # Ensure both strings are the same length by padding with '0'
    length = max(len(a), len(b))
    a = a.zfill(length)
    b = b.zfill(length)
    return ''.join('1' if a[i] != b[i] else '0' for i in range(length))

def crc_encode(data, divisor):
    n = len(divisor)
    padded_data = data + '0' * (n - 1)
    remainder = padded_data[:n]

    for i in range(len(data)):
        if remainder[0] == '1':
            remainder = xor(remainder, divisor) + (padded_data[n + i] if n + i < len(padded_data) else '')
        else:
            remainder = xor(remainder, '0' * n) + (padded_data[n + i] if n + i < len(padded_data) else '')
        remainder = remainder[1:]  # Drop the first bit

    # Handle the final remainder processing
    if remainder[0] == '1':
        remainder = xor(remainder, divisor)
    else:
        remainder = xor(remainder, '0' * n)

    return remainder[1:]

def crc_check(data_with_crc, divisor):
    n = len(divisor)
    remainder = data_with_crc[:n]

    for i in range(len(data_with_crc) - n + 1):
        if remainder[0] == '1':
            remainder = xor(remainder, divisor) + (data_with_crc[n + i] if n + i < len(data_with_crc) else '')
        else:
            remainder = xor(remainder, '0' * n) + (data_with_crc[n + i] if n + i < len(data_with_crc) else '')
        remainder = remainder[1:]  # Drop the first bit

    return remainder == '0' * (n - 1)

# User Input
data = input("Enter binary data: ")
divisor = input("Enter divisor (binary): ")

crc_code = crc_encode(data, divisor)
data_with_crc = data + crc_code

print(f"Encoded Data with CRC: {data_with_crc}")

received_data = input("Enter received data to check: ")
if crc_check(received_data, divisor):
    print("No errors detected.")
else:
    print("Error detected in data.")


# Enter binary data: 1101011011
# Enter divisor (binary): 10011
# Encoded Data with CRC: 11010110111110
# Enter received data to check: 11010110111110