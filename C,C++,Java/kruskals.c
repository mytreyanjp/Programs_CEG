#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Edge {
    int src, dest, weight;
};

bool compare(Edge a, Edge b) {
    return a.weight < b.weight;
}

int find(vector<int>& parent, int i) {
    if (parent[i] == -1)
        return i;
    return find(parent, parent[i]);
}

void Union(vector<int>& parent, int x, int y) {
    parent[x] = y;
}

void KruskalMST(vector<Edge>& edges, int V) {
    sort(edges.begin(), edges.end(), compare);
    vector<int> parent(V, -1);

    cout << "Edges in the MST:\n";
    int edgeCount = 0;
    for (auto edge : edges) {
        int x = find(parent, edge.src);
        int y = find(parent, edge.dest);

        if (x != y) {
            cout << edge.src << " - " << edge.dest << "  Weight: " << edge.weight << endl;
            Union(parent, x, y);
            edgeCount++;
            if (edgeCount == V - 1)
                break;
        }
    }
}

int main() {
    int V = 4;
    vector<Edge> edges = { {0, 1, 10}, {0, 2, 6}, {0, 3, 5},
                           {1, 3, 15}, {2, 3, 4} };

    KruskalMST(edges, V);

    return 0;
}
