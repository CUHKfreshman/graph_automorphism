#include "option.h"
#include "hypergraph.hpp"
#include "sfmt/SFMT.h"
#include <iostream>
#include <ctime>
#include <cmath>

using namespace std;

bool calculateInfluence(HyperGraph & hg, Graph & g, vector<int> & seeds, int t, double & deg, float epsilon, float delta, int m, long long int maxSamples, int iter){
	long long  counter = 0;
	int n = g.getSize();
	unsigned k = seeds.size();
	vector<unsigned int> link(n + 1, seeds.size());
	double f = (log(6/delta)+lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1))*n/(k*log(6*log2(n)/delta));
	double lambda1 = 1+(1+epsilon)*(2+2*epsilon/3)*log(3*log2(f)/delta)/(epsilon*epsilon);
	double degree=0;
	for (unsigned int i = 0; i < k;++i){
		link[seeds[i]] = i;
	}
	vector<bool> maxSeed(t, false);

	omp_set_num_threads(t);
	#pragma omp parallel
	{
		vector<bool> visit(n+1,false);
		vector<int> visit_mark(n,0);
		int id = omp_get_thread_num();

		if (m == 0){
			while(counter < maxSamples){
        		       	maxSeed[id]=hg.pollingLT2(g,link,k,visit,visit_mark);
				#pragma omp critical
				{
					counter += 1;
					if (maxSeed[id]){
						degree++;
					}
				}
               	        }
		} else {
			while(counter < maxSamples){
				maxSeed[id]=hg.pollingIC2(g,link,k,visit,visit_mark);
                                #pragma omp critical
                                {
					counter += 1;
                                        if (maxSeed[id]){
                                                degree++;
                                        }
                                }
                        }
                }
	}
//	cout << "Degree: " << degree << " " << counter << endl;

        if (degree >= lambda1){
		double epsilon_1 = (deg*n/maxSamples)/(degree*n/counter) - 1;
		cout << "Epsilon_1 = " << epsilon_1 << endl;
                double epsilon_2 = epsilon*sqrt(n*(1+epsilon)/(degree*n*pow(2,iter-1)/counter));
		cout << "Epsilon_2 = " << epsilon_2 << " " << epsilon*sqrt(n*(1+epsilon)/(degree*n*pow(2,iter-1)/counter)) << " " << pow(2,iter-1) << " " << pow(3,iter-1) << endl;
		double epsilon_3 = epsilon*sqrt(n*(1+epsilon)*(1-1/exp(1)-epsilon)/((1+epsilon/3)*degree*n*pow(2,iter-1)/counter));
		cout << "Epsilon_3 = " << epsilon_3 << endl;
		cout << "Epsilon_t = " << (epsilon_1 + epsilon_2 + epsilon_1*epsilon_2)*(1-1/exp(1)-epsilon) + epsilon_3*(1-1/exp(1)) << endl;

                if ((epsilon_1 + epsilon_2 + epsilon_1*epsilon_2)*(1-1/exp(1)-epsilon) + epsilon_3*(1-1/exp(1)) <= epsilon){
			return true;
                }
        }

	hg.updateDeg();
	return false;
}

int main(int argc, char ** argv)
{
	srand(time(NULL));

	OptionParser op(argc, argv);
	if (!op.validCheck()){
		printf("Parameters error, please check the readme.txt file for correct format!\n");
		return -1;
	}
	char * inFile = op.getPara("-i");
	if (inFile == NULL){
		inFile = (char*)"network.bin";
	}

	char * outFile = op.getPara("-o");
	if (outFile == NULL){
		outFile = (char*)"network.seeds";
	}

        char * model = op.getPara("-m");
        if (model == NULL)
                model = (char *) "LT";

	Graph g;
	if (strcmp(model, "LT") == 0){
		g.readGraphLT(inFile);
	} else if (strcmp(model, "IC") == 0){
		g.readGraphIC(inFile);
	} else {
		printf("Incorrect model option!");
		return -1;
	}

	int n = g.getSize();

	char * tmp = op.getPara("-epsilon");
	float epsilon = 0.1;
	if (tmp != NULL){
		epsilon = atof(tmp);
	}

	float delta = 1.0/n;
	tmp = op.getPara("-delta");
        if (tmp != NULL){
                delta = atof(tmp);
        }

	double k = n;
	
	tmp = op.getPara("-k");
	if (tmp != NULL){
		k = atof(tmp);
	}	

	int t = 1;
	tmp = op.getPara("-t");
	if (tmp != NULL){
		t = atoi(tmp);
	}
	
	HyperGraph hg(n);
	vector<double> degree(k+1,0);

	vector<int> seeds;

	double f = (log(6/delta)+lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1))*n/(k*log(6*log2(n)/delta));

	double lambda = (2+2*epsilon/3)*log(3*log2(f)/delta)/(epsilon*epsilon);

	long long int totalSamples = (long long int)lambda;
	cout << lambda << " " << totalSamples << endl;

	int mo = 0;
	if (strcmp(model, "IC") == 0)
		mo = 1;

	int iter = 1;

	addHyperedge(g,hg,t,totalSamples,mo);
	double nmax = (2+2*epsilon/3)*(lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1) + log(6/delta))*n/(epsilon*epsilon*k);
	
	clock_t start = clock();
	cout << totalSamples << " " << nmax << " " << lgamma(n+1) << " " << lgamma(k+1) << " " << lgamma(n-k+1) << endl;

	while (totalSamples < nmax){
		seeds.clear();
		totalSamples = hg.getNumEdge();
		cout << "Total Samples: " << totalSamples << endl;
		buildSeedSet(hg,seeds,n,k,degree);
		if (calculateInfluence(hg,g,seeds,t,degree[k],epsilon,delta,mo,totalSamples,iter)){
                       	break;
                }
		iter++;
	}
	cout << "Seed Nodes: ";
	ofstream out(outFile);
	for (unsigned int i = 0; i < seeds.size(); ++i){
		cout << seeds[i] << " ";
		out << seeds[i] << endl;
	}
	out.close();
	cout << endl;
 	printf("Influence: %0.2lf\n",(double)degree[k]*n/totalSamples);
	cout << "Time: " << (float)(clock()-start)/CLOCKS_PER_SEC << "s" << endl;
	cout << "Memory: " << getCurrentMemoryUsage() << " MB" << endl;
}
