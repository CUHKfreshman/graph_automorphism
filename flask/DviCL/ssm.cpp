#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <cassert>
#include "timer.hh" 
#include <fstream>
#include <iostream>
#include <algorithm>
#include <queue>
#include <map>
#include <set>
#include <string>
#include <chrono>


using namespace std;


struct tree_node{
	vector<int> vertex_list;
	vector<int> labeling;
	vector<int> children;
	int parent;
	int sig;
	int depth;
};



int nodenum, edgenum, max_depth;
vector<vector<int> > Graph;
vector<int> seed;
vector<tree_node> AutoTree;
vector<int> in_leaf;
vector<int> depth;
vector<vector<int> > SubTree;
vector<int> is_seed;
vector<int> color;


int read_graph(char* filename){
	ifstream input(filename);
	input>>nodenum>>edgenum;
	for(int i=0; i<nodenum; i++){
		Graph.push_back(vector<int> (0));
		in_leaf.push_back(-1);
		depth.push_back(-1);
		is_seed.push_back(0);
	}
	int u,v;
	while(input>>u>>v){
		Graph[u].push_back(v);
		Graph[v].push_back(u);
	}
	return 0;
}


int read_seed(char* filename){
	ifstream input(filename);
	int u,v;
	while(input>>v>>u){
		is_seed[u]=1;
		seed.push_back(u);
	}
	return 0;
}


int read_AT(char* filename){
	ifstream input(filename);
	tree_node n;
	int num,u;
	max_depth=0;
	while(input>>num){
		n.vertex_list.clear();
		n.labeling.clear();
		n.children.clear();

		for(int i=0;i<num;i++){
			input>>u;
			n.vertex_list.push_back(u);
		}
		for(int i=0; i<num;i++){
			input>>u;
			n.labeling.push_back(u);
		}
		input>>num;
		for(int i=0; i<num;i++){
			input>>u;
			n.children.push_back(u);
		}
		input>>n.parent>>n.sig>>n.depth;
		if(n.depth>max_depth)
			max_depth=n.depth;
		AutoTree.push_back(n);
	}
	for(int i=0; i<max_depth+1; i++)
		SubTree.push_back(vector<int> (0));
	return 0;
}


int index(){
	for(int i=0; i<AutoTree.size(); i++){
		auto a=AutoTree[i];
		if(a.children[0]==-1){
			for(auto v: a.vertex_list){
				in_leaf[v]=i;
				depth[v]=a.depth;
			}
		}
	}
	return 0;
}


int read_color(char* filename){
	ifstream input(filename);
	int u;
	while(input>>u)
		color.push_back(u);
	return 0;
}


long double bin(int n, int k){
	if(n==k)
		return 1;
	long double d=1;
	for(int i=0; i<k; i++)
		d*=(n-i);
	for(int i=1; i<=k; i++)
		d/=i;
	return d;
}


long double sm(int n, vector<int>  s){
	 map<int,int> counter1, counter2;
	 for(auto v: AutoTree[n].vertex_list)
	 	counter1[color[v]]++;
	 for(auto v: s)
	 	counter2[color[v]]++;
	 long double d=1;
	 for(map<int,int>::iterator iter=counter2.begin(); iter!=counter2.end(); ++iter){
	 	d*=bin(counter1[iter->first], iter->second);
	 }	
	 return d;
}

 


long double ssm(int n, vector<int>  s){
	vector<pair<int,long double> > cl;
 	vector<int> vs;

 	if(AutoTree[n].vertex_list.size() == s.size())
 		return 1;
 	if(AutoTree[n].children[0] == -1)
 		return sm(n, s);
 
 
	for(auto c: AutoTree[n].children){
		vs.clear();
		for(auto v:AutoTree[c].vertex_list){
			if(is_seed[v])
				vs.push_back(v);
		}
		if(!vs.empty()){
			int np=ssm(c, vs);
			cl.push_back(make_pair(c, np));
		}
	}

	long double d=1;
	map<int,int> counter1, counter2;
	for(auto c: AutoTree[n].children)
		counter1[AutoTree[c].sig]++;
	for(auto c: cl)
		counter2[AutoTree[c.first].sig]++;
	 
	for(auto c: cl){
		int s=AutoTree[c.first].sig;
		d*=bin(counter1[s], counter2[s]);
		d*=c.second;
	}
	return d;

}
 

long double SSM(){
	int nq=0;
	int nn;
	int tn;
	while(true){
		for(auto c: AutoTree[nq].children){
			nn=0;
			for(auto v: AutoTree[c].vertex_list){
				if(is_seed[v])
					nn++;
			}
			if(nn!=0){
				tn=c;
				break;
			}
		}
		if(nn==seed.size()){
			nq=tn;
		}
		else
			break;
	}
	long double np=ssm(nq, seed);
	int p=AutoTree[nq].parent;
	if(p == -1)
		return np;
	int d=0;
	for(auto c: AutoTree[p].children){
		if(AutoTree[c].sig == AutoTree[nq].sig)
			d++;
	}
	return d*np;
}






int main(int argc, char** argv){
	read_graph(argv[1]);
	
	read_AT(argv[2]);
	read_color(argv[3]);
	read_seed(argv[4]);
 	
 	cout<<"seed size "<<seed.size()<<endl;

 	auto core_beg= std::chrono::steady_clock::now();
	long double d=SSM();

	auto core_end= std::chrono::steady_clock::now();
	auto core_diff= core_end - core_beg;
	printf("time %f ms used.\n",
         std::chrono::duration<double, std::milli>(core_diff).count());
 
  

	cout<<d<<endl;
	return 0;
}