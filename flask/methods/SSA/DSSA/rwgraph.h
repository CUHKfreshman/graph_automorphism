#ifndef _RWGRAPH_H
#define _RWGRAPH_H
#include <vector>
#include <random>
#include "sfmt/SFMT.h"

typedef uint32_t UI;
typedef uint64_t ULL;


// Graph class defines fundamental operators on graph
class Graph
{
	friend class HyperGraph;
	private:
		UI UI_MAX = 4294967295U;
		ULL ULL_MAX = 18446744073709551615ULL;

		// number of nodes
		unsigned int numNodes;
		// number of edges
		unsigned int numEdges;
		// adjacency list
		std::vector<std::vector<int> > adjList;
		std::vector<int> node_deg;
		std::vector<std::vector<UI> > weights;
		std::vector<bool> dart;
	
	public:
		// get a vector of neighbours of node u
		const std::vector<int> & operator [] (int u) const;
		// return weights of neighbours of node u
		const std::vector<UI> & getWeight(int u) const;

		// get a vector of neighbours of node u
		const std::vector<int> & operator [] (int u);
		// return weights of neighbours of node u
		const std::vector<UI> & getWeight(int u);

		// get degree of node u
		int getDegree(int u) const;
		// get size of the graph
		int getSize() const;
		// get number of edges
		int getEdge() const;
		// read graph from a file
		void readGraphLT(const char * filename);
		// read graph from a file
		void readGraphIC(const char * filename);
		// write the graph to file
		void writeToFile(const char * filename);
		
};

class HyperGraph
{
	private:
		// store the edges that a node is incident to
		std::vector<std::vector<int> > node_edge;
		// store hyperedges
		std::vector<std::vector<int> > edge_node;
		unsigned int curEdge;
		unsigned int maxDegree;
		unsigned int numNodes;
		sfmt_t sfmtSeed;
		// randomly selects a node in a list according to the weight distribution
		inline int randIndex_bin(const std::vector<UI> &w, unsigned int si);
		inline int randIndex_lin(const std::vector<UI> &w, unsigned int si);
		inline int randIndex_dart(const std::vector<UI> &w, unsigned int si);
	public:
		HyperGraph(unsigned int n);
		void updateDeg();
		void updateEdge();
		void addEdge(std::vector<int> & edge);
		void addEdgeD(std::vector<int> & edge);
		int getMaxDegree();
		const std::vector<int> & getEdge(int e) const;
		const std::vector<int> & getEdge(int e);
		const std::vector<int> & getNode(int n) const;
		const std::vector<int> & getNode(int n);
                int getNumEdge() const;
		void clearEdges();

		// different polling processes for different purposes: model and returned output
		void pollingLT1(Graph &g, std::vector<bool> &visit, std::vector<int> &mark_visit);
		bool pollingLT2(Graph &g, std::vector<unsigned int> & link, unsigned int k, std::vector<bool> &visit, std::vector<int> &mark_visit);
		bool pollingLT(Graph &g, std::vector<unsigned int> & link, unsigned int k, std::vector<bool> &visit, std::vector<int> &mark_visit);
		void pollingIC1(Graph &g, std::vector<bool> &visit, std::vector<int> &visit_mark);
		bool pollingIC2(Graph &g, std::vector<unsigned int> & link, unsigned int k, std::vector<bool> &visit, std::vector<int> &visit_mark);
		bool pollingIC(Graph &g, std::vector<unsigned int> & link, unsigned int k, std::vector<bool> &visit, std::vector<int> &visit_mark);
};

float getCurrentMemoryUsage();

#endif
