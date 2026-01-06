#include <stdio.h>
#include <stdlib.h>

// Structure for a binary tree node
struct node {
    int key;
    struct node *left;
    struct node *right;
};

// Function to create a new node
struct node* createNode(int key) {
    struct node* newNode = (struct node*)malloc(sizeof(struct node));
    newNode->key = key;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

// Function to print spaces
void printSpaces(int n) {
    for (int i = 0; i < n; i++)
        printf(" ");
}

// Function to print a tree with root at given level
void printTree(struct node* root, int level) {
    if (root == NULL)
        return;

    // Print right child
    printTree(root->right, level + 1);

    // Print current node
    printSpaces(4 * level);
    printf("%d\n", root->key);

    // Print left child
    printTree(root->left, level + 1);
}

// Function to print a tree as a tree
void printTreeAsTree(struct node* root) {
    printTree(root, 0);
}

int main() {
    // Constructing the tree
    struct node* root = createNode(1);
    root->left = createNode(2);
    root->right = createNode(3);
    root->left->left = createNode(4);
    root->left->right = createNode(5);
    root->right->left = createNode(6);
    root->right->right = createNode(7);

    // Print the tree
    printf("Tree:\n");
    printTreeAsTree(root);

    return 0;
}
