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
vector<tree_node> AutoTree;
vector<int> color;
vector<vector<int> > clique;
vector<vector<int> > cs;
vector<bool> inc;
vector<vector<int> > triangle; 
vector<pair<int,int> > EL;
vector<int> leaf;
vector<int> depth;
vector<vector<int> > SubTree;
vector<bool> in_st;


int read_graph(char* filename){
	ifstream input(filename);
	input>>nodenum>>edgenum;
	for(int i=0; i<nodenum; i++){
		Graph.push_back(vector<int> (0));
		inc.push_back(false);
		leaf.push_back(-1);
		depth.push_back(-1);
	}
	int u,v;
	while(input>>u>>v){
		Graph[u].push_back(v);
		Graph[v].push_back(u);
		EL.push_back(make_pair(u,v));
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
	cout<<"max_depth "<<max_depth<<endl;
	for(int i=0; i<max_depth+1; i++)
		SubTree.push_back(vector<int> (0));
	for(int i=0; i<AutoTree.size(); i++)
		in_st.push_back(false);
	return 0;
}


int read_color(char* filename){
	ifstream input(filename);
	int u;
	while(input>>u)
		color.push_back(u);
	return 0;
}



int read_clique(char* filename){
	ifstream input(filename);
	int mc;
	input>>mc;
	vector<int> a(mc, -1);
	int u;
	while(input>>u){
		a[0]=u;
		for(int i=1; i<mc; i++)
			input>>a[i];
		clique.push_back(a);
	}
	cout<<"max clique number"<<clique.size()<<endl;
	for(int i=0; i<clique.size(); i++){
		cs.push_back(vector<int>  (0));
	}
	return 0;
}


int vertex_info(){
	for(int i=0; i<AutoTree.size(); i++){
		if(AutoTree[i].children[0]==-1){
			for(auto v: AutoTree[i].vertex_list){
				leaf[v]=i;
				depth[v]=AutoTree[i].depth;
			}
		}
	}
	return 0;
}




int triangle_listing(){
	vector<int> t(3,-1);
	for(int i=0; i<nodenum; i++)
		sort(Graph[i].begin(), Graph[i].end());
	int u,v;
	vector<int>::iterator iter1, iter2;
	for(auto e: EL){
		u=e.first;
		v=e.second;
		for(iter1=Graph[u].begin(), iter2=Graph[v].begin(); iter1!=Graph[u].end() && iter2!=Graph[v].end(); ){
			if(*iter1 < *iter2)
				++iter1;
			else if(*iter1 > *iter2){
				++iter2;
			}
			else{
				if(*iter1>u && *iter1>v){
					t[0]=u;
					t[1]=v;
					t[2]=*iter1;
					triangle.push_back(t);
				}

				++iter1;
				++iter2;
			}
		}
	}
	for(int i=0; i<triangle.size(); i++)
		cs.push_back(vector<int > (0));
	return 0;
}


/*
int sgc(int n, vector<int> s, int k){
 

	if(AutoTree[n].children[0] == -1 || AutoTree[n].vertex_list.size() == s.size()){
	 
		cs[k].push_back(make_pair(AutoTree[n].sig, s.size()));
 
		return 0;
	}
	 
 
	vector<int> vs;
	for(auto v: s)
		inc[v]=true;

	for(auto c: AutoTree[n].children){
		vs.clear();
		for(auto v: AutoTree[c].vertex_list){
			if(inc[v])
				vs.push_back(v);
		} 
		if(!vs.empty()){ 
			sgc(c, vs, k);
		}
	}
	 
	for(auto v: s)
		inc[v]=false;
	return 0;
}



int SGC(vector<int> s, int k){
	for(auto v: s)
		inc[v]=true;
	int nq=0;
	int nn, tn;
	 
	while(true){
		for(auto c: AutoTree[nq].children){
			nn=0;
			for(auto v: AutoTree[c].vertex_list){
				if(inc[v])
					nn++;
			}
			if(nn!=0){
				tn=c;
				break;
			}
		}
		if(nn==s.size()){
			nq=tn;
		}
		else
			break;
		if(AutoTree[nq].children[0] == -1)
			break;
	}
	 
	sgc(nq, s, k);
	 
 	for(auto v: s)
		inc[v]=false;
	return 0;
}
*/

int get_sig(vector<int>& s, int k){
	int maxd=0;
	int mind=max_depth;
	vector<int> visited;
	for(auto v: s){
		if(in_st[leaf[v]]==false){
			SubTree[depth[v]].push_back(leaf[v]);
			in_st[leaf[v]]=true;
			visited.push_back(leaf[v]);
			if(depth[v]>maxd)
				maxd=depth[v];
			if(depth[v]<mind)
				mind=depth[v];
		}
	}
	int u;
	for(auto v: s){
		u=leaf[v];
		while(AutoTree[u].depth != mind){
			u=AutoTree[u].parent;
			if(in_st[u] == false){
				SubTree[AutoTree[u].depth].push_back(u);
				in_st[u]=true;
				visited.push_back(u);
			}
		} 
	}
	for(int i=mind; i>=0; i--){
		if(SubTree[i].size() == 1)
			break;
		else{
			for(auto u: SubTree[i]){
				u=AutoTree[u].parent;
				if(in_st[u] ==false){
					in_st[u]=true;
					SubTree[AutoTree[u].depth].push_back(u);
					visited.push_back(u);
				}
			}
		}
	} 
	for(auto n: visited)
		cs[k].push_back(AutoTree[n].sig);
	sort(cs[k].begin(), cs[k].end());
	for(auto n: visited){
		in_st[n]=false;
	}
	for(int i=0; i<=maxd; i++){
		SubTree[i].clear();
	}
	return 0;
}

 
int SSM(){
	//for(int i=0; i<clique.size(); i++)
	//	get_sig(clique[i], i);
	for(int i=0; i<triangle.size(); i++)
		get_sig(triangle[i], i);
	return 0;
}



int simple_ssm(){
	vector<int> s;
	for(int i=0; i<triangle.size(); i++){
		cs[i].clear();
		for(auto v: triangle[i])
			cs[i].push_back(color[v]);
		sort(cs[i].begin(), cs[i].end());
	}
	return 0;
}
 

int stat(){
	sort(cs.begin(), cs.end());
	vector<int> counts;
	int pre=0;
	int c=1;
	for(int cur=1; cur<cs.size(); cur++){
		if(cs[cur] == cs[pre])
			++c;
		else{
			counts.push_back(c);
			pre=cur;
			c=1;
		}
	}
	counts.push_back(c);
	int max=0;
	for(auto cc: counts){
		if(cc>max)
			max=cc;
	}
	cout<<"counts size "<<counts.size()<<endl
		<<"max count "<<max<<endl;
	return 0;

}


int main(int argc, char** argv){
	read_graph(argv[1]);
	read_AT(argv[2]);
	read_color(argv[3]);
 //	read_clique(argv[4]);
    vertex_info();
    triangle_listing();
    cout<<"triangle "<<triangle.size()<<endl;
     SSM(); 
    stat();
	return 0;
}