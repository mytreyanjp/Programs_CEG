#include "splay_tree.h"

template <typename T>
SplayTree<T>::SplayTree() : root(nullptr) {}

template <typename T>
SplayTree<T>::~SplayTree() {
    destroyTree(root);
}

template <typename T>
void SplayTree<T>::rightRotate(Node*& node) {
    Node* newRoot = node->left;
    node->left = newRoot->right;
    newRoot->right = node;
    node = newRoot;
}

template <typename T>
void SplayTree<T>::leftRotate(Node*& node) {
    Node* newRoot = node->right;
    node->right = newRoot->left;
    newRoot->left = node;
    node = newRoot;
}

template <typename T>
void SplayTree<T>::splay(Node*& node, const T& value) {
    if (!node || node->data == value) return;

    if (node->data > value) {
        if (!node->left) return;
        if (node->left->data > value) {
            splay(node->left->left, value);
            rightRotate(node);
        } else if (node->left->data < value) {
            splay(node->left->right, value);
            if (node->left->right) leftRotate(node->left);
        }
        if (node->left) rightRotate(node);
    } else {
        if (!node->right) return;
        if (node->right->data > value) {
            splay(node->right->left, value);
            if (node->right->left) rightRotate(node->right);
        } else if (node->right->data < value) {
            splay(node->right->right, value);
            leftRotate(node);
        }
        if (node->right) leftRotate(node);
    }
}

template <typename T>
void SplayTree<T>::inOrderTraversal(Node* node, std::stringstream& ss) const {
    if (!node) return;
    inOrderTraversal(node->left, ss);
    ss << node->data.toString() << "\n";
    inOrderTraversal(node->right, ss);
}

template <typename T>
void SplayTree<T>::destroyTree(Node* node) {
    if (!node) return;
    destroyTree(node->left);
    destroyTree(node->right);
    delete node;
}

template <typename T>
void SplayTree<T>::insert(const T& value) {
    if (!root) {
        root = new Node(value);
        return;
    }
    splay(root, value);
    if (root->data == value) return;
    Node* newNode = new Node(value);
    if (root->data > value) {
        newNode->right = root;
        newNode->left = root->left;
        root->left = nullptr;
    } else {
        newNode->left = root;
        newNode->right = root->right;
        root->right = nullptr;
    }
    root = newNode;
}

template <typename T>
void SplayTree<T>::remove(const T& value) {
    if (!root) return;
    splay(root, value);
    if (!(root->data == value)) return;
    if (!root->left) {
        Node* temp = root;
        root = root->right;
        delete temp;
    } else {
        Node* newRoot = root->left;
        splay(newRoot, value);
        newRoot->right = root->right;
        delete root;
        root = newRoot;
    }
}

template <typename T>
typename SplayTree<T>::Node* SplayTree<T>::find(const T& value) {
    if (!root) return nullptr;
    splay(root, value);
    return (root->data.id == value.id) ? root : nullptr;
}

template <typename T>
void SplayTree<T>::display() const {
    std::stringstream ss;
    inOrderTraversal(root, ss);
    std::cout << ss.str();
}

template <typename T>
std::string SplayTree<T>::getTasksAsString() const {
    std::stringstream ss;
    inOrderTraversal(root, ss);
    return ss.str();
}

template <typename T>
typename SplayTree<T>::Node* SplayTree<T>::getRoot() const {
    return root;
}
