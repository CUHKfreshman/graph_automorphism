#include "rwgraph.h"
#include <vector>
#include <iostream>
#include <fstream>
#include <queue>
#include <cstdlib>
#include <unistd.h>
#include <sstream>

using namespace std;


const vector<int> & Graph::operator [] (int u) const
{
	return adjList[u];
}


const vector<int> & Graph::operator [] (int u)
{
	return adjList[u];
}


const vector<UI> & Graph::getWeight (int u) const
{
        return weights[u];
}

const vector<UI> & Graph::getWeight (int u)
{
        return weights[u];
}

/*
* get degree of node u
*/
int Graph::getDegree(int u) const
{
	return adjList[u].size();
}

/*
* get the number of nodes
*/
int Graph::getSize() const
{
	return numNodes;
}

/*
* get the number of edges
*/
int Graph::getEdge() const
{
	return numEdges;
}

/*
* read binary graph input for LT model
* difference between LT and IC is for LT we accumulate the weights for fast choosing a random node
*/
void Graph::readGraphLT(const char* filename)
{
	FILE * pFile;
        pFile = fopen(filename, "rb");
        fread(&numNodes, sizeof(int), 1, pFile);
        fread(&numEdges, sizeof(long long), 1, pFile);
        node_deg=vector<int>(numNodes + 1);
        dart = vector<bool>(numNodes+1,false);
        fread(&node_deg[1], sizeof(int), numNodes, pFile);

        vector<int> a;
        vector<UI> b;
        adjList.push_back(a);
        weights.push_back(b);

        for (unsigned int i = 1; i <= numNodes; ++i){
                vector<int> tmp(node_deg[i]);
                fread(&tmp[0], sizeof(int), node_deg[i], pFile);

                adjList.push_back(tmp);
        }

	for (unsigned int i = 1; i <= numNodes; ++i){
		vector<float> tmp(node_deg[i] + 1, 0);
                vector<UI> tmp1(node_deg[i] + 1, 0);
                fread(&tmp[1], sizeof(float), node_deg[i], pFile);

                for(int j = 1;j < node_deg[i] + 1; ++j){
                        tmp[j] += tmp[j-1];
                        if (tmp[j] >= 1){
                                tmp1[j] = UI_MAX;
                        } else {
                                tmp1[j] = tmp[j]*UI_MAX;
                        }
                }

                weights.push_back(tmp1);
                node_deg[i]++;
        }
}

/*
* read input graph for IC model
*/
void Graph::readGraphIC(const char* filename)
{
    	FILE * pFile;
    	pFile = fopen(filename, "rb");
    	fread(&numNodes, sizeof(int), 1, pFile);
    	fread(&numEdges, sizeof(long long), 1, pFile);
    	node_deg=vector<int>(numNodes + 1);
    	fread(&node_deg[1], sizeof(int), numNodes, pFile);
        
	vector<int> a;
	vector<UI> b;
    	adjList.push_back(a);
    	weights.push_back(b);
	
        for (unsigned int i = 1; i <= numNodes; ++i){
                vector<int> tmp(node_deg[i]);
                fread(&tmp[0], sizeof(int), node_deg[i], pFile);
                adjList.push_back(tmp);
        }

        for (unsigned int i = 1; i <= numNodes; ++i){
                vector<float> tmp(node_deg[i] + 1, 0);
		vector<UI> tmp1(node_deg[i] + 1, 0);
                fread(&tmp[1], sizeof(float), node_deg[i], pFile);

                for(int j = 1;j < node_deg[i] + 1; ++j){
                        tmp1[j] = tmp[j]*UI_MAX;
                }

		if (tmp1[node_deg[i]] <= 0)
                        tmp1[node_deg[i]] = UI_MAX;
		
                weights.push_back(tmp1);
        }
}

void Graph::writeToFile(const char * filename)
{/*
	ofstream output(filename);
	for (unsigned int i = 0; i < numNodes; ++i){
		for (unsigned int j = 0; j < adjList[i].size(); ++j){
			if (adjList[i][j] > i){
				output << adjList[i][j] << " " << i << " " << weights[i][j] << endl;
			}
		}
	}
	output.close();
*/	
}

// choose a random edge in LT model based on linear search
inline int HyperGraph::randIndex_lin(const vector<UI> &w, unsigned int si)
{
        UI ranNum = sfmt_genrand_uint32(&sfmtSeed);
        if (si <= 1 || ranNum > w[si - 1])
                return -1;

        for (unsigned int i = 1; i < si; ++i){
                if (ranNum <= w[i])
                        return i;
        }
        return -1;
}

// choose a random live edge in LT model based on binary search
inline int HyperGraph::randIndex_bin(const vector<UI> &w, unsigned int si)
{
	UI ran = sfmt_genrand_uint32(&sfmtSeed);
	if (si <= 1 || ran > w[si - 1])
                return -1;
        int left = 1;
        int right = si - 1;
        int prob;
        for (unsigned int i = 0; i < si; ++i){
                prob = (left + right)/2;
                if (w[prob - 1] > ran){
                        right = prob - 1;
                        continue;
                }
                if (w[prob] <= ran){
                        left = prob + 1;
                        continue;
                }
                break;
        }
        return prob;
}

inline int HyperGraph::randIndex_dart(const vector<UI> &w, unsigned int si)
{
        int prob = 0;
        while (prob == 0){
                UI ran = sfmt_genrand_uint32(&sfmtSeed)%si;
                UI ran2 = sfmt_genrand_uint32(&sfmtSeed);
                if (w[ran] >= ran2)
                        prob = ran;
        }
        return prob;
}

HyperGraph::HyperGraph(unsigned int n)
{
	sfmt_init_gen_rand(&sfmtSeed, rand());
	node_edge = vector<vector<int> >(n+1);
	maxDegree = 0;
	numNodes = n;
	curEdge=0;
}

void HyperGraph::updateDeg(){
	unsigned int num=edge_node.size();
	for (unsigned int i = curEdge; i < num; ++i){
		unsigned int num2 = edge_node[i].size();
		for (unsigned int j=0;j<num2;++j){
			node_edge[edge_node[i][j]].push_back(i);
		}
	}
	curEdge = edge_node.size();
}

void HyperGraph::updateEdge(){
	curEdge = edge_node.size();
}

/*
* Add a hyperedge into the hypergraph
*/
void HyperGraph::addEdge(vector<int> & edge)
{
	edge_node.push_back(edge);
	unsigned int ind = edge_node.size() - 1;
	for (unsigned int i = 0; i < edge.size(); ++i)
		node_edge[edge[i]].push_back(ind);
}

/*
* Add a hyperedge into the hypergraph while keeping track of the node with max degree
*/
void HyperGraph::addEdgeD(vector<int> & edge)
{
        edge_node.push_back(edge);
        int ind = edge_node.size() - 1;
        for (unsigned int i = 0; i < edge.size(); ++i){
                node_edge[edge[i]].push_back(ind);
		if (node_edge[edge[i]].size() > maxDegree)
			maxDegree = node_edge[edge[i]].size();
	}
}

/*
* get an edge from the hypergraph
*/
const vector<int> & HyperGraph::getEdge(int e) const{
	return edge_node[e];
}

const vector<int> & HyperGraph::getEdge(int e){
	return edge_node[e];
}

/*
* get the list of hyperedges incident to node n
*/
const vector<int> & HyperGraph::getNode(int n) const{
	return node_edge[n];
}

const vector<int> & HyperGraph::getNode(int n){
	return node_edge[n];
}

/*
* get the number of hyperedges
*/
int HyperGraph::getNumEdge() const
{
        return edge_node.size();
}

/*
* get the maximum degree
*/
int HyperGraph::getMaxDegree()
{
	return maxDegree;
}

/*
* remove all the hyperedges
*/
void HyperGraph::clearEdges()
{
	edge_node.clear();
	node_edge.clear();
	cout << "clear edges!" << endl;
       maxDegree = 0;
}

/*
* polling process under LT model
*/ 
bool HyperGraph::pollingLT2(Graph &g, vector<unsigned int> & link, unsigned int k, vector<bool> &visit, vector<int> &visit_mark)
{	
	unsigned int i;
	bool t = false;
        unsigned int gSize = g.getSize();
        unsigned int cur = sfmt_genrand_uint32(&sfmtSeed)%gSize+1;
        unsigned int num_marked = 0;
        for (i = 0; i < gSize; ++i){
                if (visit[cur] == true) break;
                visit[cur] = true;
                visit_mark[num_marked] = cur;
		num_marked++;
		if (link[cur] < k)
			t=true;
                int ind;
		if (g.weights[cur].size() >= 32)
                        ind = randIndex_bin(g.weights[cur],g.node_deg[cur]);
                else
                        ind = randIndex_lin(g.weights[cur],g.node_deg[cur]);

                if (ind == -1)
                        break;

                cur = g.adjList[cur][ind-1];
        }
	edge_node.push_back(vector<int>(visit_mark.begin(),visit_mark.begin()+num_marked));
        for (i = 0; i < num_marked; ++i){
                visit[visit_mark[i]]=false;
        }
	return t;
}

bool HyperGraph::pollingLT(Graph &g, vector<unsigned int> & link, unsigned int k, vector<bool> &visit, vector<int> &visit_mark)
{
        unsigned int i;
        bool t = false;
        unsigned int gSize = g.getSize();
        unsigned int cur = sfmt_genrand_uint32(&sfmtSeed)%gSize+1;
        unsigned int num_marked = 0;
        for (i = 0; i < gSize; ++i){
		if (link[cur] < k){
                        t=true;
			break;
                }
                if (visit[cur] == true) break;
                visit[cur] = true;
                visit_mark[num_marked] = cur;
		num_marked++;
		int ind;

                if (g.weights[cur].size() >= 32)
                        ind = randIndex_bin(g.weights[cur],g.node_deg[cur]);
                else
                        ind = randIndex_lin(g.weights[cur],g.node_deg[cur]);
                
                if (ind == -1)
                        break;

                cur = g.adjList[cur][ind-1];
        }
        for (i = 0; i < num_marked; ++i){
                visit[visit_mark[i]]=false;
        }
        return t;
}


void HyperGraph::pollingLT1(Graph &g, vector<bool> &visit, vector<int> &visit_mark)
{
        unsigned int i;
        unsigned int gSize = g.getSize();
        unsigned int cur = sfmt_genrand_uint32(&sfmtSeed)%gSize+1;
        unsigned int num_marked = 0;
        for (i = 0; i < gSize; ++i){
                if (visit[cur] == true) break;
                visit[cur] = true;
                visit_mark[num_marked] = cur;
		num_marked++;
                const vector<int> &neigh = g[cur];
                int ind;

                if (g.weights[cur].size() >= 32)
                        ind = randIndex_bin(g.weights[cur],g.node_deg[cur]);
                else
                        ind = randIndex_lin(g.weights[cur],g.node_deg[cur]);

                if (ind == -1)
                        break;

                cur = neigh[ind-1];
        }
	edge_node.push_back(vector<int>(visit_mark.begin(),visit_mark.begin()+num_marked));
        for (i = 0; i < num_marked; ++i){
                visit[visit_mark[i]]=false;
        }
}

void HyperGraph::pollingIC1(Graph &g, vector<bool> &visit, vector<int> &visit_mark)
{
        int i;
        unsigned int cur = sfmt_genrand_uint32(&sfmtSeed)%(g.getSize())+1;
        int num_marked=1;
	int curPos=0;
        visit[cur] = true;
        visit_mark[0] = cur;
        while(curPos < num_marked){
                cur = visit_mark[curPos];
		curPos++;
                const vector<UI> &w=g.getWeight(cur);
                const vector<int> &neigh = g[cur];
                for (i = 0; i < g.node_deg[cur]; ++i){
                        if (sfmt_genrand_uint32(&sfmtSeed) <  w[i+1]){
                        	if (!visit[neigh[i]]){
                                        visit[neigh[i]] = true;
                                        visit_mark[num_marked]=neigh[i];
					num_marked++;
                                }
                        }
                }
        }
	edge_node.push_back(vector<int>(visit_mark.begin(),visit_mark.begin()+num_marked));
        for(i = 0; i < num_marked;++i){
                visit[visit_mark[i]]=false;
        }
}

/*
* polling process under IC model
*/
bool HyperGraph::pollingIC2(Graph &g, vector<unsigned int> & link, unsigned int k, vector<bool> &visit, vector<int> &visit_mark)
{
        int i;
        unsigned int cur = sfmt_genrand_uint32(&sfmtSeed)%(g.getSize())+1;
	int curPos=0;
        int num_marked=1;
	visit[cur] = true;
	visit_mark[0] = cur;
	bool t = false;
        while(curPos < num_marked){
		cur = visit_mark[curPos];
		curPos++;
		if (link[cur] < k)
	               t=true;
		const vector<UI> &w=g.getWeight(cur);
                const vector<int> &neigh = g[cur];
		for (i = 0; i < g.node_deg[cur]; ++i){
			if (sfmt_genrand_uint32(&sfmtSeed) <  w[i+1]){
				if (!visit[neigh[i]]){
					visit[neigh[i]] = true;
					visit_mark[num_marked]=neigh[i];
					num_marked++;
				}
			}
		}
        }
        edge_node.push_back(vector<int>(visit_mark.begin(),visit_mark.begin()+num_marked));

	for(i = 0; i < num_marked;++i){
		visit[visit_mark[i]]=false;
	}
	return t;
}

bool HyperGraph::pollingIC(Graph &g, vector<unsigned int> & link, unsigned int k, vector<bool> &visit, vector<int> &visit_mark)
{
        int i;
        unsigned int cur = sfmt_genrand_uint32(&sfmtSeed)%(g.getSize())+1;
	int curPos=0;
        int num_marked=1;
        visit[cur] = true;
        visit_mark[0] = cur;
        bool t = false;
        while(curPos < num_marked){
                cur = visit_mark[curPos];
		curPos++;
                if (link[cur] < k){
                        t=true;
			break;
		}
                const vector<UI> &w=g.getWeight(cur);
                const vector<int> &neigh = g[cur];
                for (i = 0; i < g.node_deg[cur]; ++i){
                        if (sfmt_genrand_uint32(&sfmtSeed) <  w[i+1]){
                        	if (!visit[neigh[i]]){
                                        visit[neigh[i]] = true;
                                        visit_mark[num_marked]=neigh[i];
					num_marked++;
                                }
                        }
                }
        }
        for(i = 0; i < num_marked;++i){
                visit[visit_mark[i]]=false;
        }
        return t;
}


/*
* convert from an integer to a string
*/
string intToStr(int i) {
        stringstream ss;
        ss << i;
        return ss.str();
}

/*
* convert from a strong to an integer
*/
unsigned int strToInt(string s) {
        unsigned int i;
        istringstream myStream(s);

        if (myStream>>i) {
                return i;
        } else {
                cout << "String " << s << " is not a number." << endl;
                return atoi(s.c_str());
        }
        return i;
}

/*
* measure the consumed memory
*/
float getCurrentMemoryUsage() {

        string pid = intToStr(unsigned(getpid()));
        string outfile = "tmp_" + pid + ".txt";
        string command = "pmap " + pid + " | grep -i Total | awk '{print $2}' > " + outfile;
        system(command.c_str());

        string mem_str;
        ifstream ifs(outfile.c_str());
        std::getline(ifs, mem_str);
        ifs.close();

        mem_str = mem_str.substr(0, mem_str.size()-1);
        float mem = (float)strToInt(mem_str);

	command = "rm " + outfile;
        system(command.c_str());

        return mem/1024;

        return 0;
}
