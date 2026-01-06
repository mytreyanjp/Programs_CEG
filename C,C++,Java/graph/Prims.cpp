#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <fstream>

using namespace std;

#define infinity numeric_limits<int>::max()

class Graph{
    struct vertex{
        int dist;
        bool known;
        int path;
    };

    int V;
    vector<vector<pair<int,int>>> adjList;
    vector<vertex> vertices;

    public:

        Graph(int v):V(v){
            adjList.resize(v);
            vertices.resize(v);

            for(int i=0;i<v;i++){
                vertices[i].dist=infinity;
                vertices[i].known=false;
                vertices[i].path=-1;
            }
        }

        void addEdge(int u,int v,int weight){
            adjList[u].push_back(make_pair(v,weight));
            adjList[v].push_back(make_pair(u,weight));
        }

        

        void prim(int source){

            vertices[source].dist=0;

            for(int i=0;i<V-1;i++){

                int minDist=infinity;
                int minIndex=-1;

                for(int j=0;j<V;j++){
                    if(!vertices[j].known && vertices[j].dist < minDist){
                        minDist=vertices[j].dist;
                        minIndex=j;
                    }
                }

                vertices[minIndex].known=true;

                for(const auto& w:adjList[minIndex]){
                    int v=w.first;
                    int weight=w.second;

                    if(!vertices[v].known && vertices[v].dist > weight){
                        vertices[v].dist=weight;
                        vertices[v].path=minIndex;
                    }
                }
            }

            cout<<"Edges of minimum spanning tree:"<<endl;
            for(int i=1;i<V;i++){
                cout<<"Edge : "<< vertices[i].path << " - " << i <<"  Weight : "<<vertices[i].dist<<endl;
            }

        }
};

int main(){
    Graph g(6);

    int a,b,c;

    ifstream file("dijkstra.txt");


    while(file >> a >> b >> c){
        g.addEdge(a,b,c);
    }

    int source=0;
    g.prim(source);

    return 0;
}