#include<iostream>
#include<fstream>
#include<vector>
#include<set>
#include<map>

using namespace std;

vector<int> Results;
vector<int> orbit;
vector<int> leaf;
struct tree_node{
  vector<int> vertex_list;
  vector<int> children;
  int parent;
  int sig;
  int depth;
};
vector<tree_node> AutoTree;
vector<map<int,int> > lex;
vector<map<int,int> > lcan;
vector<map<int,int> > pex;
vector<map<int,int> > pcan;
vector<bool> leaf_filled;



int read_AutoTree(char* filename){
	ifstream input(filename);
	tree_node tn;
	int s,v;
	while(input>>s){
		tn.vertex_list.clear();
		for(int i=0; i<s; i++){
			input>>v;
			tn.vertex_list.push_back(v);
		}
		input>>s;
		tn.children.clear();
		for(int i=0; i<s; i++){
			input>>v;
			tn.children.push_back(v);
		}
		input>>tn.parent>>tn.sig>>tn.depth;
		AutoTree.push_back(tn);
	}
	cout<<"AutoTree size "<<AutoTree.size()<<endl;
	return 0;
}



int read_orbit(char* filename){
	ifstream input(filename);
	int u,o,l;
	while(input>>u>>o>>l){
	//	cout<<u<<" "<<o<<" "<<l<<endl;
		orbit.push_back(o);
		leaf.push_back(l);
		if(AutoTree[l].children[0]!=-1)
			cout<<"error "<<endl;
	}
	return 0;
}


int read_result(char* filename){
	ifstream input(filename);
	int u;
	while(input>>u){
		Results.push_back(u);
	}
	return 0;
}



double bin(int u, int v){
	double f=1.0;
	for(int i=0; i<v; i++)
		f*=(u-i);
	for(int i=1; i<=v; i++)
		f/=i;
	return f;
}


int estimate(){
	for(int i=0; i<AutoTree.size(); i++){
		lex.push_back(map<int,int> ());
		lcan.push_back(map<int,int> ());
		pex.push_back(map<int,int> ());
		pcan.push_back(map<int,int> ());
		leaf_filled.push_back(false);
	}
	for(auto u: Results){
		int l=leaf[u];
		int o=orbit[u];
		if(lex[l][o]==0){
			lex[l][o]++;
			for(auto v: AutoTree[l].vertex_list){
				if(orbit[v]==o)
					lcan[l][o]++;
			}
		}
		else{
			lex[l][o]++;
		}
	}
	set<int> L;
	for(auto u: Results){
		L.insert(leaf[u]);
		leaf_filled[leaf[u]]=true;
	}
	double num_can=1.0;
	map<int,int>::iterator iter1, iter2;
	for(set<int>::iterator iter=L.begin(); iter!=L.end(); ++iter){
		for(iter1=lcan[*iter].begin(), iter2=lex[*iter].begin(); iter1!=lcan[*iter].end() && iter2!=lex[*iter].end(); ++iter1, ++iter2 ){
			num_can*=bin(iter1->second, iter2->second);
		}
	}

	set<int> P;
	for(set<int>::iterator iter=L.begin(); iter!=L.end(); ++iter){
		int s=AutoTree[*iter].sig;
		int p=AutoTree[*iter].parent;
		P.insert(p);
		if(pex[p][s]==0){
			pex[p][s]++;
			for(auto v: AutoTree[p].children){
				if(AutoTree[v].sig == s)
					pcan[p][s]++;
			}
		}
		else{
			pex[p][s]++;
		}
	}
	for(set<int>::iterator iter=P.begin(); iter!=P.end(); ++iter){
		for(iter1=pcan[*iter].begin(), iter2=pex[*iter].begin(); iter1!=pcan[*iter].end() && iter2!=pex[*iter].end(); ++iter1, ++iter2){
			num_can*=bin(iter1->second, iter2->second);
		}
	}

	cout<<"num_can "<<num_can<<endl;
	return 0;

}



int main(int argc, char** argv){
	cout<<"point 1"<<endl;
	read_AutoTree(argv[1]);
	cout<<"point 2"<<endl;
	read_orbit(argv[2]);
	cout<<"point 3"<<endl;
	read_result(argv[3]);
	cout<<"point 4"<<endl;
	estimate();
	return 0;
}
