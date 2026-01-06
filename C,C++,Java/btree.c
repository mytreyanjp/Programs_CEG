#include <iostream>
#include <vector>

using namespace std;

const int MAX_KEYS = 4; // Maximum number of keys in a node

// Node structure for the B-tree
struct BTreeNode {
    vector<int> keys; // Vector to store keys
    vector<BTreeNode*> children; // Vector to store child pointers
    bool leaf; // True if node is a leaf, false otherwise

    BTreeNode(bool leafNode) : leaf(leafNode) {}

    // Function to find the key index or child index where the key could be present
    int findKeyIndex(int key) {
        int index = 0;
        while (index < keys.size() && keys[index] < key)
            ++index;
        return index;
    }

    // Function to insert a new key into the node
    void insertNonFull(int key) {
        int index = keys.size() - 1;

        // If this is a leaf node, find the right position for the new key
        if (leaf) {
            while (index >= 0 && keys[index] > key) {
                keys[index + 1] = keys[index];
                --index;
            }
            keys[index + 1] = key;
        } else { // If this is not a leaf, find the child to insert into
            while (index >= 0 && keys[index] > key)
                --index;
            if (children[index + 1]->keys.size() == MAX_KEYS) {
                splitChild(index + 1, children[index + 1]);
                if (keys[index + 1] < key)
                    ++index;
            }
            children[index + 1]->insertNonFull(key);
        }
    }

    // Function to split a child node into two nodes
    void splitChild(int index, BTreeNode* y) {
        BTreeNode* z = new BTreeNode(y->leaf);
        z->keys.resize(MAX_KEYS / 2);
        z->children.resize(MAX_KEYS / 2 + 1);

        for (int j = 0; j < MAX_KEYS / 2; ++j)
            z->keys[j] = y->keys[j + MAX_KEYS / 2];
        
        if (!y->leaf) {
            for (int j = 0; j < MAX_KEYS / 2 + 1; ++j)
                z->children[j] = y->children[j + MAX_KEYS / 2];
        }

        y->keys.resize(MAX_KEYS / 2);
        if (!y->leaf)
            y->children.resize(MAX_KEYS / 2 + 1);

        for (int j = keys.size(); j >= index + 1; --j)
            children[j + 1] = children[j];
        
        children[index + 1] = z;

        for (int j = keys.size() - 1; j >= index; --j)
            keys[j + 1] = keys[j];
        
        keys[index] = y->keys[MAX_KEYS / 2];
    }

    // Function to traverse the subtree rooted with this node
    void traverse() {
        int i;
        for (i = 0; i < keys.size(); ++i) {
            if (!leaf)
                children[i]->traverse();
            cout << " " << keys[i];
        }

        if (!leaf)
            children[i]->traverse();
    }
};

// B-tree class
class BTree {
    BTreeNode* root; // Pointer to the root node
public:
    BTree() : root(nullptr) {}

    // Function to traverse the B-tree
    void traverse() {
        if (root != nullptr)
            root->traverse();
    }

    // Function to insert a key into the B-tree
    void insert(int key) {
        if (root == nullptr) {
            root = new BTreeNode(true);
            root->keys.push_back(key);
        } else {
            if (root->keys.size() == MAX_KEYS) {
                BTreeNode* s = new BTreeNode(false);
                s->children.push_back(root);
                s->splitChild(0, root);
                int i = 0;
                if (s->keys[0] < key)
                    ++i;
                s->children[i]->insertNonFull(key);
                root = s;
            } else {
                root->insertNonFull(key);
            }
        }
    }
};

int main() {
    BTree tree;

    tree.insert(10);
    tree.insert(20);
    tree.insert(5);
    tree.insert(6);
    tree.insert(12);
    tree.insert(30);
    tree.insert(7);
    tree.insert(17);

    cout << "Traversal of the constucted B-tree is ";
    tree.traverse();
    cout << endl;

    return 0;
}
