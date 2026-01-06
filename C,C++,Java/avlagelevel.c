#include <iostream>
#include <fstream>
#include <string>

// AVL Node structure
struct AVLNode {
    std::string name;
    int age;
    int height;
    AVLNode* left;
    AVLNode* right;
};

// Function to get height of a node
int height(AVLNode* node) {
    if (node == nullptr)
        return 0;
    return node->height;
}

// Function to get maximum of two integers
int max(int a, int b) {
    return (a > b) ? a : b;
}

// Function to create a new AVL node
AVLNode* newNode(std::string name, int age) {
    AVLNode* node = new AVLNode();
    node->name = name;
    node->age = age;
    node->height = 1;
    node->left = nullptr;
    node->right = nullptr;
    return node;
}

// Function to perform right rotation
AVLNode* rightRotate(AVLNode* y) {
    AVLNode* x = y->left;
    AVLNode* T2 = x->right;

    // Perform rotation
    x->right = y;
    y->left = T2;

    // Update heights
    y->height = max(height(y->left), height(y->right)) + 1;
    x->height = max(height(x->left), height(x->right)) + 1;

    // Return new root
    return x;
}

// Function to perform left rotation
AVLNode* leftRotate(AVLNode* x) {
    AVLNode* y = x->right;
    AVLNode* T2 = y->left;

    // Perform rotation
    y->left = x;
    x->right = T2;

    // Update heights
    x->height = max(height(x->left), height(x->right)) + 1;
    y->height = max(height(y->left), height(y->right)) + 1;

    // Return new root
    return y;
}

// Function to get balance factor of a node
int getBalance(AVLNode* node) {
    if (node == nullptr)
        return 0;
    return height(node->left) - height(node->right);
}

// Function to insert a node into AVL tree
AVLNode* insert(AVLNode* node, std::string name, int age) {
    // Perform normal BST insertion
    if (node == nullptr)
        return newNode(name, age);

    if (age < node->age)
        node->left = insert(node->left, name, age);
    else if (age > node->age)
        node->right = insert(node->right, name, age);
    else // Duplicate ages are not allowed
        return node;

    // Update height of this ancestor node
    node->height = 1 + max(height(node->left), height(node->right));

    // Get the balance factor of this ancestor node to check whether this node became unbalanced
    int balance = getBalance(node);

    // If the node becomes unbalanced, then there are four cases

    // Left Left Case
    if (balance > 1 && age < node->left->age)
        return rightRotate(node);

    // Right Right Case
    if (balance < -1 && age > node->right->age)
        return leftRotate(node);

    // Left Right Case
    if (balance > 1 && age > node->left->age) {
        node->left = leftRotate(node->left);
        return rightRotate(node);
    }

    // Right Left Case
    if (balance < -1 && age < node->right->age) {
        node->right = rightRotate(node->right);
        return leftRotate(node);
    }

    // Return the unchanged node pointer
    return node;
}

// Function to traverse the AVL tree and print nodes with age above 18
void printNodesAboveAge(AVLNode* node, int level = 1) {
    if (node == nullptr)
        return;

    // In-order traversal
    printNodesAboveAge(node->left, level + 1);

    if (node->age > 18)
        std::cout << "Name: " << node->name << ", Age: " << node->age << ", Level: " << level << std::endl;

    printNodesAboveAge(node->right, level + 1);
}

int main() {
    std::ifstream inputFile("names.txt");
    if (!inputFile) {
        std::cerr << "Error opening file." << std::endl;
        return 1;
    }

    AVLNode* root = nullptr;
    std::string name;
    int age;

    // Read names and ages from file and insert into AVL tree
    while (inputFile >> name >> age) {
        root = insert(root, name, age);
    }

    // Print nodes with age above 18
    std::cout << "Names with age above 18:" << std::endl;
    printNodesAboveAge(root);

    inputFile.close();

    return 0;
}
