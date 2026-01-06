class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        self.identity = Point(None, None) # Point at infinity

    def is_on_curve(self, point):
        if point == self.identity:
            return True
        return (point.y**2 - (point.x**3 + self.a * point.x + self.b)) % self.p == 0

    def inverse_mod(self, k):
        # Extended Euclidean Algorithm for modular inverse
        if k == 0:
            raise ZeroDivisionError("Cannot invert 0")
        return pow(k, self.p - 2, self.p) # Fermat's Little Theorem

    def point_add(self, P1, P2):
        if P1 == self.identity:
            return P2
        if P2 == self.identity:
            return P1

        if P1.x == P2.x and P1.y != P2.y: # P1 + (-P1) = O
            return self.identity

        if P1.x == P2.x and P1.y == P2.y: # Point doubling
            if P1.y == 0: # Tangent is vertical
                return self.identity
            slope = (3 * P1.x**2 + self.a) * self.inverse_mod(2 * P1.y) % self.p
        else: # Point addition for distinct points
            slope = (P2.y - P1.y) * self.inverse_mod(P2.x - P1.x) % self.p

        x3 = (slope**2 - P1.x - P2.x) % self.p
        y3 = (slope * (P1.x - x3) - P1.y) % self.p
        return Point(x3, y3)

    def scalar_multiply(self, k, P):
        if k == 0:
            return self.identity
        if k < 0: # Handle negative scalar multiplication
            P_neg = Point(P.x, (-P.y) % self.p)
            return self.scalar_multiply(-k, P_neg)

        result = self.identity
        addend = P

        while k > 0:
            if k & 1: # If k is odd
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1 # k = k // 2
        return result

# Example Usage
if __name__ == "__main__":
    # Define an elliptic curve: y^2 = x^3 + ax + b (mod p)
    # Example curve: y^2 = x^3 + 7 (mod 17)
    a = 0
    b = 7
    p = 17
    curve = EllipticCurve(a, b, p)

    # A point on the curve (5, 8)
    G = Point(5, 8)
    print(f"Is G on curve? {curve.is_on_curve(G)}")

    # Scalar multiplication: 2 * G
    two_G = curve.scalar_multiply(2, G)
    print(f"2 * G = {two_G}")

    # Scalar multiplication: 3 * G
    three_G = curve.scalar_multiply(3, G)
    print(f"3 * G = {three_G}")

    # Scalar multiplication: 5 * G
    five_G = curve.scalar_multiply(5, G)
    print(f"5 * G = {five_G}")

    # Adding two distinct points
    P1 = Point(5, 8)
    P2 = Point(16, 13) # Another point on the curve
    print(f"Is P2 on curve? {curve.is_on_curve(P2)}")
    P1_plus_P2 = curve.point_add(P1, P2)
    print(f"P1 + P2 = {P1_plus_P2}")