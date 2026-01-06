#include <iostream>

// Base class
class Shape {
public:
    // Virtual function
    virtual double area() const = 0; // Pure virtual function, making Shape an abstract class
    virtual void display() const {
        std::cout << "Shape" << std::endl;
    }
};

// Derived class Rectangle inheriting from Shape
class Rectangle : public Shape {
private:
    double length, width;

public:
    Rectangle(double l, double w) : length(l), width(w) {}

    // Override area() function
    double area() const override {
        return length * width;
    }

    // Override display() function
    void display() const override {
        std::cout << "Rectangle" << std::endl;
    }
};

// Derived class Circle inheriting from Shape
class Circle : public Shape {
private:
    double radius;

public:
    Circle(double r) : radius(r) {}

    // Override area() function
    double area() const override {
        return 3.14 * radius * radius;
    }

    // Override display() function
    void display() const override {
        std::cout << "Circle" << std::endl;
    }
};

// Another base class
class Printable {
public:
    virtual void print() const = 0;
};

// Multiple inheritance
class Square : public Shape, public Printable {
private:
    double side;

public:
    Square(double s) : side(s) {}

    // Override area() function
    double area() const override {
        return side * side;
    }

    // Override display() function
    void display() const override {
        std::cout << "Square" << std::endl;
    }

    // Override print() function
    void print() const override {
        std::cout << "Printing Square" << std::endl;
    }
};

int main() {
    Rectangle rectangle(5, 4);
    Circle circle(3);
    Square square(6);

    // Polymorphic behavior through pointers to base class
    Shape* shapes[] = {&rectangle, &circle, &square};
    for (auto shape : shapes) {
        shape->display();
        std::cout << "Area: " << shape->area() << std::endl;
    }

    // Polymorphic behavior through pointers to Printable base class
    Printable* printables[] = {&rectangle, &circle, &square};
    for (auto printable : printables) {
        printable->print();
    }

    return 0;
}
