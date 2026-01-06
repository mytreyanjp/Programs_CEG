#include <stdio.h>
#include <stdlib.h>

struct node {
    int key;
    struct node *left;
    struct node *right;
};

typedef struct node Node;

Node* createNode(int key) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->key = key;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

Node* rightRotate(Node* x) {
    Node* y = x->left;
    x->left = y->right;
    y->right = x;
    return y;
}

Node* leftRotate(Node* x) {
    Node* y = x->right;
    x->right = y->left;
    y->left = x;
    return y;
}

Node* splay(Node* root, int key) {
    if (root == NULL || root->key == key)
        return root;

    if (root->key > key) {
        if (root->left == NULL)
            return root;

        if (root->left->key > key) {
            root->left->left = splay(root->left->left, key);
            root = rightRotate(root);
        } else if (root->left->key < key) {
            root->left->right = splay(root->left->right, key);
            if (root->left->right != NULL)
                root->left = leftRotate(root->left);
        }

        return (root->left == NULL) ? root : rightRotate(root);
    } else {
        if (root->right == NULL)
            return root;

        if (root->right->key > key) {
            root->right->left = splay(root->right->left, key);
            if (root->right->left != NULL)
                root->right = rightRotate(root->right);
        } else if (root->right->key < key) {
            root->right->right = splay(root->right->right, key);
            root = leftRotate(root);
        }

        return (root->right == NULL) ? root : leftRotate(root);
    }
}

Node* insert(Node* root, int key) {
    if (root == NULL)
        return createNode(key);

    root = splay(root, key);

    if (root->key == key)
        return root;

    Node* newNode = createNode(key);

    if (root->key > key) {
        newNode->right = root;
        newNode->left = root->left;
        root->left = NULL;
    } else {
        newNode->left = root;
        newNode->right = root->right;
        root->right = NULL;
    }

    return newNode;
}

Node* delete(Node* root, int key) {
    if (root == NULL)
        return root;

    root = splay(root, key);

    if (root->key != key)
        return root;

    Node* temp;

    if (root->left == NULL) {
        temp = root;
        root = root->right;
    } else {
        temp = root;
        root = splay(root->left, key);
        root->right = temp->right;
    }

    free(temp);
    return root;
}

void printInorder(Node* root) {
    if (root != NULL) {
        printInorder(root->left);
        printf("%d ", root->key);
        printInorder(root->right);
    }
}

int main() {
    Node* root = createNode(100);
    root->left = createNode(50);
    root->right = createNode(200);
    root->left->left = createNode(40);
    root->left->right = createNode(70);

    printf("Inorder traversal before insertion: ");
    printInorder(root);
    printf("\n");

    int keyToInsert = 80;
    root = insert(root, keyToInsert);

    printf("Inorder traversal after insertion of %d: ", keyToInsert);
    printInorder(root);
    printf("\n");

    int keyToDelete = 70;
    root = delete(root, keyToDelete);

    printf("Inorder traversal after deletion of %d: ", keyToDelete);
    printInorder(root);
    printf("\n");

    return 0;
}
