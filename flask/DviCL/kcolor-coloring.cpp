#include<iostream>
#include<vector>
#include<map>
#include<unordered_map>
#include <unistd.h>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <fstream>
#include <set>
#include <algorithm>

using namespace std;

 
int nodenum,edgenum,MaxCore,MaxColor;
vector<vector<int> > Graph;
vector<int> core;
vector<map<int,int> > ncolor;
vector<int> color;
vector<int> rcolor;
vector<int> num_color;
vector<int> Verts;
vector<int> temp_;
vector<int> mark_;
vector<int> kcore_node;
vector<int> kcore_edge;
vector<int> kcolor_node;
vector<int> kcolor_edge;
int max_kcolor;
int max_color;
vector<int> mbin;
vector<int> cn;
vector<int> kclique;


int read_graph(char* filename){
	ifstream input(filename);
	input>>nodenum>>edgenum;
	for(int i=0; i<nodenum; i++){
		Graph.push_back(vector<int> (0));
		core.push_back(0);
		ncolor.push_back(map<int,int> ());
		num_color.push_back(0);
		color.push_back(-1);
		Verts.push_back(i);
		temp_.push_back(0);
		mark_.push_back(0);
	}
	int u,v;
	while(input>>u>>v){
		Graph[u].push_back(v);
		Graph[v].push_back(u);
	}
	return 0;
}


int read_clique(char* filename){
	ifstream input(filename);
	int u,v;
	while(input>>u>>v){
		kclique.push_back(v);
	}
	return 0;
}



int CoreDecomposition(const vector<vector<int> > & graph, vector<int>& verts){
	int max_deg=0;
	auto& deg=core;
	for(auto v: verts){
		deg[v]=graph[v].size();
		if(deg[v]>max_deg)
			max_deg=deg[v];
	}
	vector<int> bin(max_deg+1, 0);
	for(auto v: verts)
		++bin[deg[v]];
	int start=0;
	for(int i=0; i<=max_deg; ++i){
		int tmp=bin[i];
		bin[i]=start;
		start+=tmp;
	}
	vector<int> order(verts.size());
	auto& pos=temp_;
	for(auto v: verts){
		pos[v] = bin[deg[v]];
		order[pos[v]]=v;
		++bin[deg[v]];
	}
	for(int i=max_deg; i>0; --i){
		bin[i]=bin[i-1];
	}
	bin[0]=0;

	for(int i=0; i<order.size(); ++i){
		int v=order[i];
		for(auto u: graph[v]){
			if(deg[u]>deg[v]){
				const int pw=bin[deg[u]];
				const int pu=pos[u];
				if(pw != pu){
					const int w=order[pw];
					pos[w]=pu;
					order[pos[w]]=w;
					pos[u]=pw;
					order[pos[u]]=u;
				}
				++bin[deg[u]];
				--deg[u];
			}
		}
	}


	for(auto v: verts)
		temp_[v]=0;
 
	verts.clear();
	while(!order.empty()){
		verts.push_back(order.back());
		order.pop_back();
	}
 	


	return 0;
}

 

int Coloring(vector<vector<int> >& graph, vector<int>& verts){
	int Num_color=0;
	for(auto v: verts){
		int i;
		map<int,int>::iterator iter;
		color[v]=-1;
		for(iter=ncolor[v].begin(), i=0; iter!=ncolor[v].end(); ++iter, ++i){
			if(iter->first != i){
				color[v] = i;
				break;
			}
		}
		color[v]=i;
		 
		if(color[v]>Num_color)
			Num_color=color[v];
 
 		for(auto u: graph[v])
 			ncolor[u][color[v]]++;
	}
	max_color=Num_color+1;


	return Num_color+1;
}

 


int ColorDecomposition(vector<vector<int> >& graph, vector<int>& verts){
	int max_color=0;
	for(auto v: verts){
		num_color[v] = ncolor[v].size();
		if(num_color[v] > max_color)
			max_color=num_color[v];
	} 
	 

	vector<int> bin(max_color+1, 0);
	for(auto v: verts)
		++bin[num_color[v]];
	int start=0;
	for(int i=0; i<=max_color; ++i){
		int tmp=bin[i];
		bin[i]=start;
		start+=tmp;
	}
	vector<int> order(verts.size());
	auto& pos=temp_;
	/*for(auto v: verts){
		pos[v]=bin[num_color[v]];
		order[pos[v]]=v;
		++bin[num_color[v]];
	}*/
	for(int i=verts.size()-1; i>=0; i--){
		int v=verts[i];
		pos[v]=bin[num_color[v]];
		order[pos[v]]=v;
		++bin[num_color[v]];
	}

	for(int i=max_color; i>0; --i)
		bin[i]=bin[i-1];
	bin[0]=0;

	for(int i=0; i<order.size(); ++i){
		int v=order[i];
		for(auto u: graph[v]){
			if(num_color[u] > num_color[v]){
				ncolor[u][color[v]]--;
				if(ncolor[u][color[v]] == 0){
					const int pw=bin[num_color[u]];
					const int pu=pos[u];
					if(pw != pu){
						const int w=order[pw];
						pos[w]=pu;
						order[pos[w]]=w;
						pos[u]=pw;
						order[pos[u]]=u;
					}
					++bin[num_color[u]];
					num_color[u]--;
				}
			}
		}
	}

	max_kcolor=num_color[order.back()];
	cout<<"max_kcolor, the supposed coloring number  "<<max_kcolor<<endl;
 
	for(auto v: verts)
		temp_[v]=0;

	verts.clear();
	while(!order.empty()){
		verts.push_back(order.back());
		order.pop_back();
	}

	return 0;
}




 
int ColorDecomposition_dyn(vector<vector<int> >& graph, vector<int>& verts){
	int max_color=0;
	for(auto v: verts){
		num_color[v] = ncolor[v].size();
		if(num_color[v] > max_color)
			max_color=num_color[v];
	} 

	for(auto v: verts){
		sort(graph[v].begin(), graph[v].end(), [](const int& v1, const int& v2){
			if(num_color[v1] < num_color[v2])
				return true;
			else if(num_color[v1] == num_color[v2] && color[v1] < color[v2])
				return true;
			else 
				return false;
		});
	} 
	 
	vector<int> bin(max_color+1, 0);
	for(auto v: verts)
		++bin[num_color[v]];
	int start=0;
	for(int i=0; i<=max_color; ++i){
		int tmp=bin[i];
		bin[i]=start;
		start+=tmp;
	}
	vector<int> order(verts.size());
	auto& pos=temp_;
 
	for(int i=verts.size()-1; i>=0; i--){
		int v=verts[i];
		pos[v]=bin[num_color[v]];
		order[pos[v]]=v;
		++bin[num_color[v]];
	}

	for(int i=max_color; i>0; --i)
		bin[i]=bin[i-1];
	bin[0]=0;

	int pw, pu, w;


	for(int i=0; i<order.size(); ++i){
		int v=order[i];
	 
		for(auto u: graph[v]){
			if(num_color[u] > num_color[v]){
				 
				ncolor[u][color[v]]--;
				if(ncolor[u][color[v]] ==0){
					pw=bin[num_color[u]];
					pu=pos[u];
					if(pw != pu){
						w=order[pw];
						pos[w]=pu;
						order[pos[w]]=w;
						pos[u]=pw;
						order[pos[u]]=u;
					}
					++bin[num_color[u]];
					num_color[u]--;

				 	if(color[v] < color[u]){
						 
						 for(auto x: graph[u]){
						 	if(num_color[x] <= num_color[v])
						 		continue;
						 	ncolor[x][color[u]]--;
						 	ncolor[x][color[v]]++;
						 	if(ncolor[x][color[u]] == 0 && ncolor[x][color[v]]>1){
						 		pw=bin[num_color[x]];
						 		pu=pos[x];
						 		if(pw != pu ){
						 			w=order[pw];
						 			pos[w]=pu;
						 			order[pos[w]]=w;
						 			pos[x]=pw;
						 			order[pos[x]]=x;
						 		}
						 		++bin[num_color[x]];
						 		num_color[x]--;
						 	}
						 	else if(ncolor[x][color[u]] == 0 && ncolor[x][color[v]]==1)
						 		;
						 	else if(ncolor[x][color[u]] >0 && ncolor[x][color[v]] >1)
						 		;
						 	else{
						 		pw=bin[num_color[x]+1]-1;
						 		pu=pos[x];
						 		if(pw != pu){
						 			w=order[pw];
						 			pos[w]=pu;
						 			order[pos[w]]=w;
						 			pos[x]=pw;
						 			order[pos[x]]=x;
						 		}
						 		--bin[num_color[x]+1];
						 		++num_color[x];
						 	}
						 }
						 color[u]=color[v];
					} 
					 
				}
			}
		}
	}

	max_kcolor=num_color[order.back()];
	cout<<"max_kcolor, the supposed coloring number  "<<max_kcolor<<endl;
 
	for(auto v: verts)
		temp_[v]=0;

	verts.clear();
	while(!order.empty()){
		verts.push_back(order.back());
		order.pop_back();
	}

	return 0;
}
 
 




int recoloring(vector<vector<int> >& graph, vector<int>& verts){
	vector<int> order(verts.size());
	vector<bool> update(verts.size(), false);
	int i;
	map<int,int>::iterator iter;

	for(i=0; i<verts.size(); i++){
		int v=verts[i];
		order[v]=i;
		ncolor[v].clear();
	}

	int Num_color=0;
	for(auto v: verts){
		if(color[v]<=max_kcolor && !update[v]){
			if(color[v] > Num_color)
				Num_color=color[v];
			continue;
		}
		int ori=color[v];
		color[v]=-1;
		for(auto u: graph[v]){
			if(order[u]<order[v]){
				ncolor[v][color[u]]++;
			}
		}
		for(i=0, iter=ncolor[v].begin(); iter!=ncolor[v].end(); ++iter, ++i){
			if(iter->first !=i){
				color[v]=i;
				break;
			}
		}
		color[v]=i;
		if(color[v]>Num_color)
			Num_color=color[v];
		if(color[v] > max_kcolor)
			cout<<"*********  "<<v<<"	"<<color[v]<<"	"<<ncolor[v].size()<<"  "<<num_color[v]<<"	"<<update[v]<<"  "<<ori<<endl;
		for(auto u: graph[v]){
			if(order[u] > order[v] && color[u] == color[v])
				update[u]=true;
		}
	}
	cout<<"recoloring with colors "<<Num_color+1<<endl;
	return Num_color+1;

}



 
int recolor(vector<vector<int> >& graph, vector<int>& verts){
	vector<int> order(verts.size());
	vector<bool> update(verts.size(), false);
	int i;
	map<int,int>::iterator iter;

	for(i=0; i<verts.size(); i++){
		int v=verts[i];
		order[v]=i;
		ncolor[v].clear();
	}

	int cn=Coloring(graph, verts);

	cout<<"recolor  with colors "<<cn<<endl;
	return cn;
}


int check(vector<vector<int> >& graph, vector<int>& verts){
	set<int> c;
	int i;
	set<int>::iterator iter;
	for(auto v: verts){
		c.clear();
		for(auto u: graph[v]){
			c.insert(color[u]);
		}
		for(i=0, iter=c.begin(); iter!=c.end(); ++iter, ++i){
			if(*iter != i)
				break;
		}
		if(i != color[v])
			cout<<"//////////// error "<<endl;
	}
	return 0;
}



int cc(vector<vector<int> >& graph, vector<int>& verts){
	set<int> c;
	int i;
	set<int>::iterator iter;
	vector<int> order(verts.size());
	for(i=0; i<verts.size(); i++){
		int v=verts[i];
		order[v]=i;
	}
	for(auto v: verts){
		c.clear();
		for(auto u: graph[v]){
			if(order[u]<order[v])
				c.insert(color[u]);
		}
		if(c.size() > num_color[v])
			cout<<"?????? "<<v<<"	"<<num_color[v]<<"	"<<c.size()<<endl;
	}
	return 0;

}



int stat( ){
	int max_diff=0; 
	int min_diff=nodenum;
	long double diff_total=0;
	int change_total=0;
	MaxColor=0;
	int min_ncolor=nodenum;
	int Max_color=0;
	int Min_color=nodenum;
	for(int i=0; i<nodenum; i++){
		int diff=core[i]-num_color[i];
		if(diff > max_diff)
			max_diff=diff;
		if(diff < min_diff)
			min_diff=diff;
		diff_total+=diff;
		if(diff>0)
			change_total++;
		if(num_color[i] > MaxColor)
			MaxColor=num_color[i];
		if(num_color[i] < min_ncolor)
			min_ncolor=num_color[i];
	}
	cout<<"nodenum "<<nodenum<<endl
		<<"min_diff "<<min_diff<<endl
		<<"max_diff "<<max_diff<<endl
		<<"change_total "<<change_total<<endl
		<<"ave diff "<<diff_total/nodenum<<endl
		<<"act ave diff "<<diff_total/change_total<<endl
		<<"MaxColor "<<MaxColor<<endl
		<<"min_ncolor "<<min_ncolor<<endl;
	return 0;
}

 


int stat_k(vector<vector<int> >& graph){
	for(int i=0; i<=MaxCore; i++){
		kcore_node.push_back(0);
		kcore_edge.push_back(0);
	}
	for(int i=0; i<=MaxColor; i++){
		kcolor_node.push_back(0);
		kcolor_edge.push_back(0);
	}
	for(int i=0; i<nodenum; i++){
		kcore_node[core[i]]++;
		kcolor_node[num_color[i]]++;
		for(auto v: graph[i]){
			if(core[v] < core[i])
				kcore_edge[core[v]]++;
			else
				kcore_edge[core[i]]++;

			if(num_color[v] < num_color[i])
				kcolor_edge[num_color[v]]++;
			else
				kcolor_edge[num_color[i]]++;
		}
	}
	int start_n=0;
	int start_e=0;
	for(int i=MaxCore; i>=0; i--){
		start_n+=kcore_node[i];
		kcore_node[i]=start_n;
		start_e+=kcore_edge[i];
		kcore_edge[i]=start_e/2;
	}
	start_n=0;
	start_e=0;
	for(int i=MaxColor; i>=0; i--){
		start_n+=kcolor_node[i];
		kcolor_node[i]=start_n;
		start_e+=kcolor_edge[i];
		kcolor_edge[i]=start_e/2;
	}
	cout<<"MaxCore "<<MaxCore<<"	with node "<<kcore_node[MaxCore]<<"	with edges "<<kcore_edge[MaxCore]<<endl
		<<"MaxColor "<<MaxColor<<"	with node "<<kcolor_node[MaxColor]<<"	with edges "<<kcolor_edge[MaxColor]<<endl;

	return 0;

}


int map_new(vector<vector<int> >& graph, vector<int>& verts){
	mbin.clear();
	vector<int> brc;
	for(int i=0; i<max_color; i++){
		mbin.push_back(0);
		brc.push_back(i);
	}
	for(auto v: verts){
		mbin[color[v]]++;
	}
	sort(brc.begin(), brc.end(), [](const int& v1, const int& v2){
		if(mbin[v1]>mbin[v2])
			return true;
		else if(mbin[v1] == mbin[v2] && v1 < v2)
			return true;
		else
			return false;
	});
	vector<int> rc(max_color, -1);
	for(int i=0; i<brc.size(); i++){
		rc[brc[i]]=i;
		cout<<"&&&&&&&&&&&&&&&&&&&&&& "<<i<<"	"<<brc[i]<<endl;
	}

	vector<int> ori_c=color;
	vector<int> ori_kc=num_color;

	int min=nodenum;
	int max=-1;

	cout<<"####################### before recolor "<<endl;
	for(auto v: verts){
		if(color[v]>max)
			max=color[v];
		if(color[v] < min)
			min=color[v];
	}

	cout<<"#######################  with min "<<min<<"	and max  "<<max<<endl; 

	min=nodenum;
	max=-1;

	cout<<"######################## after recolor  "<<endl;
	for(auto v: verts){
		color[v]=rc[color[v]];
		ncolor[v].clear();
		if(color[v] > max)
			max=color[v];
		if(color[v]<min)
			min=color[v];
	}

	cout<<"######################## with new min "<<min<<"  and max "<<max<<endl;
	for(auto v: verts){
		for(auto u: graph[v]){
			ncolor[u][color[v]]++;
		}
	}

	 

	ColorDecomposition(graph, verts);

	for(auto v: verts){
		if(num_color[v] != ori_kc[v])
			cout<<" &&&&&&&&& "<<v<<"	"<<num_color[v]<<"	"<<ori_kc[v]<<endl;
	 }
	return 0;
}




int map_recolor(vector<vector<int> >& graph, vector<int>& verts){
	vector<int> rc(max_color, -1);
	int oc=0;

	for(auto v: verts){
		if(rc[color[v]]==-1){
			rc[color[v]]=oc;
			oc++;
		}
		 
	}
	 
	vector<int> ori_c=color;
	vector<int> ori_kc=num_color;

	int min=nodenum;
	int max=-1;

	cout<<"####################### before recolor "<<endl;
	for(auto v: verts){
		if(color[v]>max)
			max=color[v];
		if(color[v] < min)
			min=color[v];
	}

	cout<<"#######################  with min "<<min<<"	and max  "<<max<<endl; 

	min=nodenum;
	max=-1;

	cout<<"######################## after recolor  "<<endl;
	for(auto v: verts){
		color[v]=rc[color[v]];
		ncolor[v].clear();
		if(color[v] > max)
			max=color[v];
		if(color[v]<min)
			min=color[v];
	}


	cout<<"recolor "<<endl;
 	int i;
	map<int,int>::iterator iter;
 	for(auto v: verts){
 		if(num_color[v] != max_kcolor){
 			color[v]=-1;
 			for(iter=ncolor[v].begin(), i=0; iter!=ncolor[v].end(); ++iter, ++i){
 				if(iter->first !=i){
 					color[v]=i;
 					break;
 				}
 			}
 			color[v]=i;
 		}
 		for(auto u: graph[v])
 			ncolor[u][color[v]]++;
 	}

 	cout<<"recolor "<<endl;






	cout<<"///////////////// check num_color with different regin "<<endl;

 
	vector<int> MAX(max_kcolor+1, 0);
	for(auto v: verts){
		if(color[v] > MAX[num_color[v]]){
			MAX[num_color[v]]=color[v];
		}
	}

	cout<<"//////////////// "<<endl;
	for(int i=0; i<MAX.size(); i++){
		cout<<i<<"	"<<MAX[i]<<endl;
	}

	cout<<"///////////////////"<<endl;

/*
	cout<<"######################## with new min "<<min<<"  and max "<<max<<endl;
	for(auto v: verts){
		for(auto u: graph[v]){
			ncolor[u][color[v]]++;
		}
	}

	 

	ColorDecomposition(graph, verts);

	for(auto v: verts){
		if(num_color[v] != ori_kc[v])
			cout<<" &&&&&&&&& "<<v<<"	"<<num_color[v]<<"	"<<ori_kc[v]<<endl;
	 }  

*/
	return 0;

}


int adjust(vector<vector<int> >& graph, vector<int>& verts){
	for(auto v: verts){
		ncolor[v].clear();
	}

	int Num_color=0;
	int i;
	map<int,int>::iterator iter;
	for(auto v: verts){
		for(iter=ncolor[v].begin(), i=0; iter!=ncolor[v].end(); ++iter, ++i){
			if(iter->first !=i){
				if(color[v] !=i){
//cout<<"!!!!!!!!!!!! adjust, with original "<<color[v]<<" changed to new "<<i<<endl;
					color[v]=i;
				}
				break;
			}
		}
		if(color[v] !=i){
			//cout<<"!!!!!!!!!!!! adjust, with original "<<color[v]<<" changed to new "<<i<<endl;
			color[v]=i;
		}
		if(color[v] > Num_color)
			Num_color=color[v];
		for(auto u: graph[v])
			ncolor[u][color[v]]++;
	}
	max_color=Num_color+1;
	return max_color;
}
 





int adjust_new(vector<vector<int> >& graph, vector<int>& verts){
	vector<int> bin(max_color, 0);
	vector<int> order(verts.size(), -1);
	for(auto v: verts)
		bin[color[v]]++;

	for(int i=0; i<bin.size(); i++)
		cout<<i<<" 	"<<bin[i]<<endl;
	cout<<" num nodes with largest color "<<bin[max_color-1]<<endl;
	int start=0;
	for(int i=0; i<max_color; i++){
		int tmp=bin[i];
		bin[i]=start; 
		start+=tmp;
	}
	for(auto v: verts){
		order[bin[color[v]]]=v;
		bin[color[v]]++;
	}

	verts=order;

	for(int i=0; i<verts.size()-1; i++){
		if(verts[i]==-1 || verts[i+1]==-1)
			cout<<"##########  -1"<<endl;
		if(color[verts[i]]>color[verts[i+1]] )
			cout<<"###########  not sorted "<<i<<"	"<<verts[i]<<"  "<<color[verts[i]]<<",   "<<verts[i+1]<<"	"<<color[verts[i+1]]<<endl;
	}



	for(auto v: verts){
		ncolor[v].clear();
	}

	int Num_color=0;
	int i;
	map<int,int>::iterator iter;
	for(auto v: verts){
		for(iter=ncolor[v].begin(), i=0; iter!=ncolor[v].end(); ++iter, ++i){
			if(iter->first !=i){
				if(color[v] !=i){
					//if(color[v]==max_color-1)
  						cout<<"!!!!!!!!!!!! adjust, with original "<<color[v]<<" changed to new "<<i<<endl;
					color[v]=i;
				}
				break;
			}
		}
		if(color[v] !=i){
		//	if(color[v]==max_color-1)
			 	cout<<"!!!!!!!!!!!! adjust, with original "<<color[v]<<" changed to new "<<i<<endl;
			color[v]=i;
		}
		if(color[v] > Num_color)
			Num_color=color[v];
		for(auto u: graph[v])
			ncolor[u][color[v]]++;
	}
	max_color=Num_color+1;
	return max_color;
}	








/*


int main(int argc, char** argv){
	read_graph(argv[1]);
	auto core_beg= std::chrono::steady_clock::now();
	CoreDecomposition(Graph, Verts);
	auto core_end= std::chrono::steady_clock::now();
	auto core_diff= core_end - core_beg;
	printf("CoreDecomposition %f ms used.\n",
         std::chrono::duration<double, std::milli>(core_diff).count());
	cout<<"max core "<<core[Verts[0]]<<endl;

	MaxCore=core[Verts[0]];

	auto color_beg= std::chrono::steady_clock::now();
	int nc=Coloring(Graph, Verts);
	auto color_end= std::chrono::steady_clock::now();
	auto color_diff= color_end - color_beg;
	printf("Coloring %f ms used.\n",
         std::chrono::duration<double, std::milli>(color_diff).count());
	cout<<"******************  coloring number "<<nc<<endl;
 

	auto colordec_beg= std::chrono::steady_clock::now();
	ColorDecomposition_dyn(Graph, Verts);
	auto colordec_end= std::chrono::steady_clock::now();
	auto colordec_diff= colordec_end - colordec_beg;
	printf("ColorDecomposition %f ms used.\n",
         std::chrono::duration<double, std::milli>(colordec_diff).count());
 
 
  
 
 	map_recolor(Graph, Verts);


 
	return 0;
}
*/


int read_cn(char* filename){
	ifstream input(filename);
	int u,c;
	while(input>>u>>c)
		cn.push_back(c);
	int diff=0;
	double total=0;
	for(int i=0; i<nodenum; i++){
		if(num_color[i] != cn[i]-1){
			diff++;
			total+=(num_color[i]-cn[i]+1);
		}
		if(num_color[i]+1 < cn[i]){
			cout<<"error "<<endl;
		}
	}
	cout<<"comparing kcolor and kclique"<<endl<<"diff perc	"<<100.0*diff/nodenum<<endl<<"avg "<<total/diff<<endl;

	diff=0;
	total=0;
	for(int i=0; i<nodenum; i++){
		if(core[i] !=cn[i]-1){
			diff++;
			total+=(core[i]+1-cn[i]);
		}
		if(core[i]+1 < cn[i])
			cout<<"core < cn"<<endl;
	}
	cout<<"comparing core and clique"<<endl<<"diff perc "<<100.0*diff/nodenum<<endl<<"avg "<<total/diff<<endl;


	return 0;

}

//v1 is kcolor/kcore and v2 is kclique
int bound(vector<int>& v1, vector<int>& v2){
	int total=0;
	for(int i=0; i<nodenum; i++){
		for(auto j: Graph[i]){
			if(v1[i]+1 < v2[j])
				++total;
		}
	}
	cout<<total<<"	"<<edgenum<<"	"<<(1.0)*total/edgenum<<endl;
	return 0;
}


int check(){
	int error=0;
	for(int i=0; i<nodenum; i++){
		if(num_color[i]+1 < kclique[i])
			error++;
	}
	cout<<"error "<<error<<endl;
	return 0;
}


int main(int argc, char** argv){
	read_graph(argv[1]);
	CoreDecomposition(Graph, Verts);
	read_clique(argv[2]);

	vector<int> RV(nodenum, -1);
	for(int i=0; i<nodenum; i++)
		RV[i]=Verts[nodenum-i-1];

	int nc=Coloring(Graph, Verts);
	cout<<"******************  coloring number "<<nc<<endl;

	ColorDecomposition(Graph, Verts);

	cout<<"core and clique "<<endl;
	bound(core, kclique);

	cout<<"kcolor and clique "<<endl;
	bound(num_color, kclique);

	check();

	for(auto v: Verts)
		ncolor[v].clear();

	sort(Verts.begin(), Verts.end(),[](const int& v1, const int& v2){
		if(kclique[v1] > kclique[v2])
			return true;
		else if(kclique[v1] == kclique[v2] && core[v1] >= core[v2])
			return true;
		else
			return false;
	});

	cn=Coloring(Graph, Verts);




	/*read_cn(argv[2]);


 	vector<int> kcolor=num_color;

	for(auto v: RV){
		ncolor[v].clear();
	}
	int rnc=Coloring(Graph, RV);
	cout<<"****************** reverse coloring "<<rnc<<endl;
	ColorDecomposition(Graph, Verts);

	int larger=0;
	int smaller=0;
	for(int i=0; i<nodenum; i++){
		if( num_color[i]>kcolor[i]){
			larger+=(num_color[i] - kcolor[i]);
		}
		else if(num_color[i] < kcolor[i])
			smaller+=(kcolor[i]-num_color[i]);
	}
	cout<<"reverse vs core, larger	"<<larger<<endl
		<<"reverse vs core, smaller	"<<smaller<<endl; */

	return 0;  
}
