#include <iostream>
#include<bits/stdc++.h>
#include <vector>
#include <queue>
#include <fstream>
using namespace std;

#define infinity INT_MAX

class Graph{
    private:
        struct vertex{
            int dist;
            bool known;
            int path;
        };
        int V;
        vector<vertex>vertices;
        vector<vector<int>>adjList;
        vector<int> path;

    public:
        Graph(int v):V(v){
            adjList.resize(v);
            vertices.resize(v);
            path.resize(v);

        }

        void addEdge(int u,int v){
            adjList[u].push_back(v);
        }


        void unweighted(int start){

            for(int i=0;i<V;i++){
                vertices[i].dist=infinity;
                vertices[i].path=-1;
                vertices[i].known=false;
            }
            vertices[start].dist=0;

            for(int currDist=0;currDist<V;currDist++){
                for(int i=0;i<V;i++){
                    if(!vertices[i].known && vertices[i].dist==currDist){
                        vertices[i].known=true;
                        for(int w:adjList[i]){
                            if(vertices[w].dist==infinity){
                                vertices[w].dist=currDist+1;
                                vertices[w].path=i;
                            }
                        }
                    }
                }
            }

        }

        void shortestPath(int start,int end){
            vector<int> path;

            if(vertices[end].dist==infinity){
                return;
            }

            int curr=end;
            while(curr!=start){
                path.push_back(curr);
                curr=vertices[curr].path;
            }

            path.push_back(start);

            reverse(path.begin(),path.end());

            for(int i:path){
                cout<<i<<" ";
            }
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

    g.unweighted(5);
    g.shortestPath(5,1);


    return 0;
}
