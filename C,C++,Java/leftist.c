#include <iostream>

using namespace std;

// Node structure for the leftist heap
struct Node {
    int data;
    int rank; // Rank of the node
    Node* left;
    Node* right;
};

// Function to create a new node
Node* createNode(int data) {
    Node* newNode = new Node;
    newNode->data = data;
    newNode->rank = 1; // Initially, rank is set to 1
    newNode->left = newNode->right = nullptr;
    return newNode;
}

// Function to merge two leftist heaps
Node* merge(Node* a, Node* b) {
    if (!a) return b;
    if (!b) return a;

    // Ensure a has larger root
    if (a->data > b->data)
        swap(a, b);

    // Merge the right subtree of a with b
    a->right = merge(a->right, b);

    // Update rank of a
    if (!a->left || a->left->rank < a->right->rank)
        swap(a->left, a->right);
    if (!a->right) a->rank = 1;
    else a->rank = a->right->rank + 1;

    return a;
}

// Function to insert a new element into the leftist heap
Node* insert(Node* root, int data) {
    Node* newNode = createNode(data);
    return merge(root, newNode);
}

// Function to delete the minimum element (root) from the leftist heap
Node* deleteMin(Node* root) {
    if (!root) return nullptr;
    Node* leftChild = root->left;
    Node* rightChild = root->right;
    delete root;
    return merge(leftChild, rightChild);
}

// Function to print the elements of the leftist heap in in-order traversal
void inOrder(Node* root) {
    if (!root) return;
    inOrder(root->left);
    cout << root->data << " ";
    inOrder(root->right);
}

int main() {
    Node* root = nullptr;
    root = insert(root, 5);
    root = insert(root, 3);
    root = insert(root, 10);
    root = insert(root, 1);

    cout << "In-order traversal of leftist heap after insertion: ";
    inOrder(root);
    cout << endl;

    root = deleteMin(root);

    cout << "In-order traversal of leftist heap after deletion of minimum element: ";
    inOrder(root);
    cout << endl;

    return 0;
}
