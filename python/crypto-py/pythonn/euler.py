def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def phi(n):
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
        i += 1
    if n > 1:
        result -= result // n
    return result


def mod_exp(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result


if __name__ == "__main__":
    a, n = map(int, input("Enter a and n: ").split())
    ph = phi(n)
    print(f"phi({n}) = {ph}")
    if gcd(a, n) == 1:
        print(f"{a}^{ph} mod {n} = {mod_exp(a, ph, n)}")
    else:
        print("a and n are not coprime")