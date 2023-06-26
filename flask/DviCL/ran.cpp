#include<iostream>
#include<fstream>
#include<vector>
#include<ctime>
#include<cstdlib>
#include<set>
#include<map>
#include<climits>

using namespace std;


int nodenum, edgenum;
vector<int> order;
vector<vector<int> > Graph;
vector<int> pos;


int read_graph(char* filename){
	ifstream input(filename);
	input>>nodenum>>edgenum;
	for(int i=0; i<nodenum; i++){
		Graph.push_back(vector<int> (0));
		order.push_back(i);
		pos.push_back(-1);
	}
	int u,v;
	while(input>>u>>v){
		Graph[u].push_back(v);
		Graph[v].push_back(u);
	}
	return 0;
}



int ran(){
	srand((unsigned) time(NULL));
	for(int i=0; i<10; i++){
		for(int j=0; j<nodenum; j++){
			int w=rand()%nodenum;
			int tmp=order[j];
			order[j]=order[w];
			order[w]=tmp;
		}
	}
	for(int i=0; i<nodenum; i++){
		pos[order[i]]=i;
	}
	return 0;
}

int print(char* filename){
	ofstream output(filename);
	output<<nodenum<<endl<<edgenum<<endl;
	for(int i=0; i<nodenum; i++){
		int pu=pos[i];
		for(auto v: Graph[i]){
			int pv=pos[v];
			if(pu<pv)
				output<<pu<<"	"<<pv<<endl;
		}
	}
	return 0;
}

int main(int argc, char** argv){
	read_graph(argv[1]);
	ran();
	print(argv[2]);
	return 0;
}