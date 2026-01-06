#include <iostream>
#include <vector>
#include <queue>
#include <fstream>
using namespace std;

class Graph{
    int V;
    vector<vector<int>> adjList;

    public:

        Graph(int v):V(v){
            adjList.resize(v);
        }

        void addEdge(int u,int v){
            adjList[u].push_back(v);
        }

        void bfs(int source){
            vector<bool> visited(V,false);
            queue<int> path;
            int visitedcount=1;

            path.push(source);

            while(!path.empty()){
                int n=path.front();
                if(visited[n]==false){
                    path.pop();
                }
                visited[n]=true;
                cout<<n<<" ";

                for(int w:adjList[n]){
                    if(!visited[w]){
                        path.push(w);
                    }
                }

                visitedcount++;
            }

            if(visitedcount!=V){
                cout<<"cycle found!!\n";
            }


        }
};

int main(){
    Graph g(8);

    ifstream file("bfs.txt");

    int a,b;

    while(file >> a >> b){
        g.addEdge(a,b);
    }

    int source=0;
    g.bfs(source);
}