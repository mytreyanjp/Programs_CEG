def xor(a, b):
    # Perform XOR operation on two binary strings
    result = []
    for i in range(1, len(b)):
        result.append('1' if a[i] != b[i] else '0')
    return ''.join(result)
def crc_encode(data, divisor):
    n = len(divisor)
    padded_data = data + '0' * (n - 1)
    remainder = padded_data[:n]

    for i in range(len(data)):
        if remainder[0] == '1':
            remainder = xor(remainder, divisor) + padded_data[n + i]
        else:
            remainder = xor(remainder, '0' * n) + padded_data[n + i]
        remainder = remainder[1:]

    return remainder

def crc_check(data_with_crc, divisor):
    n = len(divisor)
    remainder = data_with_crc[:n]

    for i in range(len(data_with_crc) - n + 1):
        if remainder[0] == '1':
            remainder = xor(remainder, divisor) + data_with_crc[n + i]
        else:
            remainder = xor(remainder, '0' * n) + data_with_crc[n + i]
        remainder = remainder[1:]

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