#include <iostream>
#include <vector>
#include <queue>
#include <fstream>
using namespace std;

struct Edge{

    int u,v,weight;

    Edge(int u,int v,int weight):u(u),v(v),weight(weight){}

    bool operator<(const Edge& other) const {
        return weight > other.weight;
    }

};

class DisjSets{

    vector<int> parent;

    public:
        DisjSets(int v):parent(v){
            for(int i=0;i<v;i++){
                parent[i]=i;
            }
        }

        int find(int u){
            if(parent[u]!=u){
                parent[u]=find(parent[u]);
            }
            return parent[u];
        }

        void Union(int u,int v){
            parent[find(u)]=find(v);
        }

};

vector<Edge> kruskal(vector<Edge>& edge,int vertices){
    DisjSets ds(vertices);

    priority_queue<Edge> pq;

    for(Edge e : edge){
        pq.push(e);
    }

    vector<Edge> mst;

    while(mst.size()!=vertices-1){
        Edge ed=pq.top();
        pq.pop();

        int uset=ds.find(ed.u);
        int vset=ds.find(ed.v);
        if(uset!=vset){
            mst.push_back(ed);
            ds.Union(uset,vset);
        }
    }

    return mst;

}

int main(){

    vector<Edge> edges;

    ifstream file("dijkstra.txt");

    int a,b,c;

    while(file >> a >> b >> c){
        Edge ed(a,b,c);
        edges.push_back(ed);
    }

    vector<Edge> ans=kruskal(edges,6);

    for(Edge e:ans){
        cout<< e.u <<" - " << e.v << " - weight - " << e.weight<<endl;
    }


    return 0;
}