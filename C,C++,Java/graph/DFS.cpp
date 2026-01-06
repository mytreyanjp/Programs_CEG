#include <iostream>
#include <vector>
#include <stack>
#include <fstream>
using namespace std;

class Graph
{
    int V;
    vector<vector<int>> adjList;

public:
    Graph(int v) : V(v)
    {
        adjList.resize(v);
    }

    void addEdge(int u, int v)
    {
        adjList[u].push_back(v);
    }

    void dfs(int source)
    {
        vector<bool> visited(V, false);
        stack<int> path;

        path.push(source);

        cout << "DFS traversal : " << endl;

        while (!path.empty())
        {
            int n = path.top();
            path.pop();

            if (!visited[n])
            {
                visited[n] = true;
                cout << n << " ";
                for (int w : adjList[n])
                {
                    if (!visited[w])
                    {
                        path.push(w);
                    }
                }
            }
        }
    }
};

int main()
{
    Graph g(8);

    ifstream file("bfs.txt");

    int a, b;

    while (file >> a >> b)
    {
        g.addEdge(a, b);
    }

    int source = 0;
    g.dfs(source);
}