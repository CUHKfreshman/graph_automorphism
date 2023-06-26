#include<iostream>
#include<fstream>
#include<vector>
#include<string>


using namespace std;

vector<int> T;


 

int read(char* filename){
	ifstream input(filename);
	string s;
	char c;
	int i,total, mhb, mheb, msb;
	getline(input, s);
	getline(input, s);
	cout<<s<<endl;
	while(input>>c){
		if(c=='s'){
			getline(input, s);
			getline(input, s);
			getline(input, s);

			input>>s>>c>>mhb
				 >>s>>c>>mheb
				 >>s>>c>>msb;
			 
			total=mhb+mheb+msb;
			T.push_back(total);
		}
		else
			getline(input, s);
	}
	return 0;
}



int main(int argc ,char** argv){
	read(argv[1]);
	int max=0;
	for(auto t: T)
		if(t>max)
			max=t;
	cout<<"max memory "<<max/(1024*1024)<<endl
		<<T.size()<<endl;
	return 0;
}