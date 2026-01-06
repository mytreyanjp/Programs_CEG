#include <iostream>
#include <vector>
#include <queue>
#include <climits>
using namespace std;

void addEdge(vector<pair<int, int>> adj[], int u, int v, int w) {
    adj[u].emplace_back(v, w);
    adj[v].emplace_back(u, w); // For undirected graph
}

void shortestPathDijkstra(vector<pair<int, int>> adj[], int V, int src) {
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    vector<int> dist(V, INT_MAX);

    pq.emplace(0, src);
    dist[src] = 0;

    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();

        for (const auto &neighbor : adj[u]) {
            int v = neighbor.first;
            int weight = neighbor.second;

            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.emplace(dist[v], v);
            }
        }
    }

    cout << "Vertex \t Distance from Source " << src << endl;
    for (int i = 0; i < V; ++i)
        cout << i << " \t " << dist[i] << endl;
}

int main() {
    int V = 9;
    vector<pair<int, int>> adj[V];
    addEdge(adj, 0, 1, 4);
    addEdge(adj, 0, 7, 8);
    addEdge(adj, 1, 2, 8);
    addEdge(adj, 1, 7, 11);
    addEdge(adj, 2, 3, 7);
    addEdge(adj, 2, 8, 2);
    addEdge(adj, 2, 5, 4);
    addEdge(adj, 3, 4, 9);
    addEdge(adj, 3, 5, 14);
    addEdge(adj, 4, 5, 10);
    addEdge(adj, 5, 6, 2);
    addEdge(adj, 6, 7, 1);
    addEdge(adj, 6, 8, 6);
    addEdge(adj, 7, 8, 7);

    int src = 0;
    shortestPathDijkstra(adj, V, src);

    return 0;
}
