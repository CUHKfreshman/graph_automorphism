#include<iostream>
#include<fstream>
#include<vector>
#include<algorithm>

using namespace std;


int nodenum, edgenum;
vector<vector<int> > Graph;
vector<int> H;

int read_graph(char* filename){
	ifstream input(filename);
	input>>nodenum>>edgenum;
	for(int i=0; i<nodenum; i++){
		Graph.push_back(vector<int> (0));
		H.push_back(-1);
	}
	int u,v;
	while(input>>u>>v){
		Graph[u].push_back(v);
		Graph[v].push_back(u);
	}
	return 0;
}


int read_H(char* filename){
	ifstream input(filename);
	int u,v;
	while(input>>u>>v){
		H[u]=v;
	}
	return 0;
}


int remap(char* filename){
	vector<pair<int,int> > EL;
	int pu,pv;
	for(int i=0; i<nodenum; i++){
		pu=H[i];
		for(auto v: Graph[i]){
			pv=H[v];
			if(pu<pv)
				EL.push_back(make_pair(pu, pv));

		}
	}
	sort(EL.begin(), EL.end());
	ofstream output(filename);
	output<<nodenum<<endl<<edgenum<<endl;
	for(auto e: EL){
		output<<e.first<<" "<<e.second<<endl;
	}
	return 0;
}


int main(int argc, char**argv){
	read_graph(argv[1]);
	read_H(argv[2]);
	remap(argv[3]);
	return 0;
}