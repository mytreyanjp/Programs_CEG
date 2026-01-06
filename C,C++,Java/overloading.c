#include <iostream>

class Complex {
private:
    double real, imag;

public:
    Complex(double real = 0.0, double imag = 0.0) : real(real), imag(imag) {}

    // Overloading output operator using std::ostream
    friend std::ostream& operator<<(std::ostream& os, const Complex& c) {
        os << c.real << " + " << c.imag << "i";
        return os;
    }

    // Overloading input operator using std::istream
    friend std::istream& operator>>(std::istream& is, Complex& c) {
        std::cout << "Enter real part: ";
        is >> c.real;
        std::cout << "Enter imaginary part: ";
        is >> c.imag;
        return is;
    }
};

int main() {
    Complex c1, c2;

    std::cout << "Enter complex number c1:" << std::endl;
    std::cin >> c1;

    std::cout << "Enter complex number c2:" << std::endl;
    std::cin >> c2;

    // Overloading output operator using std::ostream
    std::cout << "c1: " << c1 << std::endl;
    std::cout << "c2: " << c2 << std::endl;

    return 0;
}
