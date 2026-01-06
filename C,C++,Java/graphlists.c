#include <iostream>
#include <vector>
#include <list>

using namespace std;

class GraphList {
    int V;
    vector<list<int>> adjList;

public:
    GraphList(int vertices) : V(vertices), adjList(vertices) {}

    void addEdge(int u, int v) {
        adjList[u].push_back(v);
        adjList[v].push_back(u); // For undirected graph
    }

    void removeEdge(int u, int v) {
        adjList[u].remove(v);
        adjList[v].remove(u); // For undirected graph
    }

    void printGraph() {
        for (int i = 0; i < V; i++) {
            cout << "Vertex " << i << ":";
            for (int v : adjList[i]) {
                cout << " -> " << v;
            }
            cout << endl;
        }
    }
};

int main() {
    GraphList g(5);

    g.addEdge(0, 1);
    g.addEdge(0, 4);
    g.addEdge(1, 2);
    g.addEdge(1, 3);
    g.addEdge(1, 4);
    g.addEdge(2, 3);
    g.addEdge(3, 4);

    cout << "Adjacency List:" << endl;
    g.printGraph();

    return 0;
}
