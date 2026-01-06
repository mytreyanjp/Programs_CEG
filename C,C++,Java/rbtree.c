#include <iostream>

using namespace std;

enum Color { RED, BLACK };

class Node {
public:
    int key;
    Node* left;
    Node* right;
    Node* parent;
    Color color;

    Node(int k, Node* p = nullptr, Color c = RED) {
        key = k;
        left = right = nullptr;
        parent = p;
        color = c;
    }
};

class RedBlackTree {
private:
    Node* root;
    Node* nil;

    void leftRotate(Node* x) {
        Node* y = x->right;
        x->right = y->left;
        if (y->left!= nil)
            y->left->parent = x;
        y->parent = x->parent;
        if (x->parent == nullptr)
            root = y;
        else if (x == x->parent->left)
            x->parent->left = y;
        else
            x->parent->right = y;
        y->left = x;
        x->parent = y;
    }

    void rightRotate(Node* x) {
        Node* y = x->left;
        x->left = y->right;
        if (y->right!= nil)
            y->right->parent = x;
        y->parent = x->parent;
        if (x->parent == nullptr)
            root = y;
        else if (x == x->parent->right)
            x->parent->right = y;
        else
            x->parent->left = y;
        y->right = x;
        x->parent = y;
    }

    void fixInsert(Node* k) {
        Node* u;
        while (k->parent->color == RED) {
            if (k->parent == k->parent->parent->right) {
                u = k->parent->parent->left;
                if (u->color == RED) {
                    u->color = BLACK;
                    k->parent->color = BLACK;
                    k->parent->parent->color = RED;
                    k = k->parent->parent;
                } else {
                    if (k == k->parent->left) {
                        k = k->parent;
                        rightRotate(k);
                    }
                    k->parent->color = BLACK;
                    k->parent->parent->color = RED;
                    leftRotate(k->parent->parent);
                }
            } else {
                u = k->parent->parent->right;

                if (u->color == RED) {
                    u->color = BLACK;
                    k->parent->color = BLACK;
                    k->parent->parent->color = RED;
                    k = k->parent->parent;
                } else {
                    if (k == k->parent->right) {
                        k = k->parent;
                        leftRotate(k);
                    }
                    k->parent->color = BLACK;
                    k->parent->parent->color = RED;
                    rightRotate(k->parent->parent);
                }
            }
            if (k == root)
                break;
        }
        root->color = BLACK;
    }

    void fixDelete(Node* x) {
        Node* s;
        while (x!= root && x->color == BLACK) {
            if (x == x->parent->left) {
                s = x->parent->right;
                if (s->color == RED) {
                    s->color = BLACK;
                    x->parent->color = RED;
                    leftRotate(x->parent);
                    s = x->parent->right;
                }

                if (s->left->color == BLACK && s->right->color == BLACK) {
                    s->color = RED;
                    x = x->parent;
                } else {
                    if (s->right->color == BLACK) {
                        s->left->color = BLACK;
                        s->color = RED;
                        rightRotate(s);
                        s = x->parent->right;
                    }

                    s->color = x->parent->color;
                    x->parent->color = BLACK;
                    s->right->color = BLACK;
                    leftRotate(x->parent);
                    x = root;
                }
            } else {
                s = x->parent->left;
                if (s->color == RED) {
                    s->color = BLACK;
                    x->parent->color = RED;
                    rightRotate(x->parent);
                    s = x->parent->left;
                }

                if (s->right->color == BLACK && s->left->color == BLACK) {
                    s->color = RED;
                    x = x->parent;
                } else {
                    if (s->left->color == BLACK) {
                        s->right->color = BLACK;
                        s->color = RED;
                        leftRotate(s);
                        s = x->parent->left;
                    }

                   s->color = x->parent->color;
                    x->parent->color = BLACK;
                    s->left->color = BLACK;
                    rightRotate(x->parent);
                    x = root;
                }
            }
        }
        x->color = BLACK;
    }

public:
    RedBlackTree() {
        nil = new Node(INT_MIN);
        nil->color = BLACK;
        root = nil;
    }

    Node* search(int key) {
        Node* x = root;
        while (x != nil && x->key != key) {
            if (key < x->key)
                x = x->left;
            else
                x = x->right;
        }
        return x;
    }

    void insert(int key) {
        Node* x = root;
        Node* y = nil;
        Node* z = new Node(key);

        while (x != nil) {
            y = x;
            if (z->key < x->key)
                x = x->left;
            else
                x = x->right;
        }

        z->parent = y;

        if (y == nil)
            root = z;
        else if (z->key < y->key)
            y->left = z;
        else
            y->right = z;

        fixInsert(z);
    }

    void remove(int key) {
        Node* x = search(key);
        if (x == nil)
            return;

        Node* y = x;
        Node* z;
        Color yOrigColor = y->color;

        if (x->left == nil) {
            z = x->right;
            transplant(x, x->right);
        } else if (x->right == nil) {
            z = x->left;
            transplant(x, x->left);
        } else {
            y = minimum(x->right);
            yOrigColor = y->color;
            z = y->right;
            if (y->parent == x) {
                z->parent = y;
            } else {
                transplant(y, y->right);
                y->right = x->right;
                y->right->parent = y;
            }
            transplant(x, y);
            y->left = x->left;
            y->left->parent = y;
            y->color = x->color;
        }

        if (yOrigColor == BLACK)
            fixDelete(z);
    }

    void inorder() {
        inorder(root);
        cout << endl;
    }

private:
    void inorder(Node* x) {
        if (x == nil)
            return;

        inorder(x->left);
        cout << x->key << " ";
        inorder(x->right);
    }

    void transplant(Node* u, Node* v) {
        if (u->parent == nullptr)
            root = v;
        else if (u == u->parent->left)
            u->parent->left = v;
        else
            u->parent->right = v;
        v->parent = u->parent;
    }

    Node* minimum(Node* x) {
        while (x->left != nil)
            x = x->left;
        return x;
    }
};

int main() {
    RedBlackTree rbt;

    rbt.insert(10);
    rbt.insert(20);
    rbt.insert(30);
    rbt.insert(40);
    rbt.insert(50);

    rbt.inorder();

    rbt.remove(30);

    rbt.inorder();

    return 0;
}