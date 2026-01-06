#include <iostream>
#include<bits/stdc++.h>
#include <vector>
#include <queue>
#include <fstream>
using namespace std;

#define infinity  numeric_limits<int>::max()

class Graph{
    private:
        struct vertex{
            int dist;
            bool known;
            //int path;
        };
        int V;
        vector<vertex>vertices;
        vector<vector<pair<int,int>>>adjList;
        //vector<int> path;

    public:
        Graph(int v):V(v){
            adjList.resize(v);
            vertices.resize(v);
            //path.resize(v);
            for(int i=0;i<V;i++){
                vertices[i].dist=infinity;
                vertices[i].known=false;
            }

        }

        void addEdge(int u,int v,int weight){
            adjList[u].push_back(make_pair(v,weight));
            adjList[v].push_back(make_pair(u,weight));
        }


        // Dijkstra's algorithm
        void dijkstra(int source){
            
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

                    if(!vertices[v].known && vertices[minIndex].dist+weight < vertices[v].dist){
                        vertices[v].dist=vertices[minIndex].dist+weight;
                    }
                }

            }
            cout<<"distance from the source : "<<source<<"\n";
            
            for(int i=0;i<V;i++){
                cout<<"vertex "<<i<<" : "<<vertices[i].dist<<endl;
            }

        }

};

int main(){

    Graph g(6);

    int a,b,c;

    ifstream file("Dijkstra.txt");

    while(file >> a >> b >> c){
        g.addEdge(a,b,c);
    }

    /*g.addEdge(5, 2);
    g.addEdge(5, 0);
    g.addEdge(4, 0);
    g.addEdge(4, 1);
    g.addEdge(2, 3);
    g.addEdge(3, 1);*/
    int source=0;

    g.dijkstra(source);


    return 0;
}
