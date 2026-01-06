#ifndef SPLAY_TREE_H
#define SPLAY_TREE_H

#include <sstream>

template <typename T>
class SplayTree {
private:
    struct Node {
        T data;
        Node* left;
        Node* right;

        Node(const T& value) : data(value), left(nullptr), right(nullptr) {}
    };

    Node* root;

    void rightRotate(Node*& node);
    void leftRotate(Node*& node);
    void splay(Node*& node, const T& value);
    void inOrderTraversal(Node* node, std::stringstream& ss) const;
    void destroyTree(Node* node);

public:
    SplayTree();
    ~SplayTree();
    void insert(const T& value);
    void remove(const T& value);
    Node* find(const T& value);
    void display() const;
    std::string getTasksAsString() const;
    Node* getRoot() const;
};

#include "splay_tree.cpp" // Template class implementation included here

#endif // SPLAY_TREE_H
