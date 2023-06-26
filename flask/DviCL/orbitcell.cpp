#include<iostream>
#include<fstream>
#include<vector>
#include<map>


using namespace std;

int max_cell;
vector<int> cell_size;


int read_orbit(char* filename){
	ifstream input(filename);
	max_cell=0;
	int u,v;
	while(input>>u>>v){
		if(v>max_cell)
			max_cell=v;
	}
	max_cell++;
	for(int i=0; i<max_cell; i++ )
		cell_size.push_back(0);
	return 0;
}



int count(char* filename){
	ifstream input(filename);
	int u,v;
	while(input>>u>>v){
		cell_size[v]++;
	}
	int e=0;
	int s=0;
	for(int i=0; i<cell_size.size(); i++){
		if(cell_size[i]>0)
			e++;
		if(cell_size[i]==1)
			s++;
	}
	cout<<"max_cell "<<max_cell<<endl
		<<"cell num "<<e<<endl
		<<"singleton num "<<s<<endl;
	return 0;
}


int main(int argc, char** argv){
	read_orbit(argv[1]);
	count(argv[1]);
	return 0;
}