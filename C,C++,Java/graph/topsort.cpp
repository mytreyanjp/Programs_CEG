#include <iostream>
#include <vector>
#include <queue>
#include <fstream>
using namespace std;

class Graph{
    private:
        int V;
        vector<vector<int>> adj;

    public:
        Graph(int v):V(v){
            adj.resize(v);
        }

        void addEdge(int u,int v){
            adj[u].push_back(v);
        }

        void topologicalOrder(){
            vector<int> inDegree(V,0);

            for(int i=0;i<V;i++){
                for(int u : adj[i]){
                    inDegree[u]++;
                }
            }

            queue<int> q;
            for(int i=0;i<V;i++){
                if(inDegree[i]==0){
                    q.push(i);
                }
            }

            int visited=0;

            vector<int> topOrder;

            while(!q.empty()){
                int v=q.front();
                q.pop();
                topOrder.push_back(v);

                for(int u:adj[v]){
                    if(--inDegree[u]==0){
                        q.push(u);
                    }
                }

                visited++;
            }

            if(visited!=V){
                cout<<"Graph has cycle "<<endl;
            }

            for(int v:topOrder){
                cout<<v<<" ";
            }
            cout<<endl;

        }

};

int main(){

    Graph g(6);

    int a,b;

    ifstream file("top.txt");

    while(file >> a >> b){
        g.addEdge(a,b);
    }

    /*g.addEdge(5, 2);
    g.addEdge(5, 0);
    g.addEdge(4, 0);
    g.addEdge(4, 1);
    g.addEdge(2, 3);
    g.addEdge(3, 1);*/

    g.topologicalOrder();

    return 0;
}