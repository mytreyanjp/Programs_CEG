#include <iostream>
#include <algorithm>
using namespace std;

struct node {
    int key;
    struct node *left;
    struct noed *right;
    int height;

    node(int x) : key(x), left(nullptr), right(nullptr), height(1) {}
};
typedef struct node* n;

int height(n root) {
    if (root == nullptr) return 0;
    return root->height;
}

int getbalance(n root) {
    if (root == nullptr) return 0;
    return height(root->left) - height(root->right);
}

n leftr(n x) {
    n y = x->right;
    n t = y->left;

    y->left = x;
    x->right = t;

    x->height = 1 + max(height(x->left), height(x->right));
    y->height = 1 + max(height(y->left), height(y->right));
    return y;
}

n rightr(n x) {
    n y = x->left;
    n t = y->right;

    y->right = x;
    x->left = t;

    x->height = 1 + max(height(x->left), height(x->right));
    y->height = 1 + max(height(y->left), height(y->right));
    return y;
}

n insert(n root, int x) {
    if (root == nullptr)
        return new node(x);

    if (x < root->key)
        root->left = insert(root->left, x);
    else if (x > root->key)
        root->right = insert(root->right, x);
    else
        return root;

    root->height = 1 + max(height(root->left), height(root->right));
    int balance = getbalance(root);

    if (balance > 1 && x < root->left->key)
        return rightr(root);
    if (balance < -1 && x > root->right->key)
        return leftr(root);
    if (balance > 1 && x > root->left->key) {
        root->left = leftr(root->left);
        return rightr(root);
    }
    if (balance < -1 && x < root->right->key) {
        root->right = rightr(root->right);
        return leftr(root);
    }
    return root;
}

void inorder(n root) {
    if (root != nullptr) {
        inorder(root->left);
        cout << root->key << " ";
        inorder(root->right);
    }
}

int main() {
    n r = nullptr;
    r = insert(r, 10);
    r = insert(r, 50);
    r = insert(r, 30);
    r = insert(r, 60);
    r = insert(r, 20);
    r = insert(r, 90);
    inorder(r);
}
