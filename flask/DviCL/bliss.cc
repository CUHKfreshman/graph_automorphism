#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <cassert>
#include "defs.hh"
#include "graph.hh"
#include "timer.hh"
#include "utils.hh"
#include <fstream>
#include <iostream>
#include <algorithm>
#include <queue>
#include <map>
#include <set>
#include <string>


using namespace std;



/* Input file name */
static const char* infilename = 0;

static bool opt_directed = false;
static bool opt_canonize = true;
static const char* opt_output_can_file = 0;
static const char* opt_splitting_heuristics = "fsm";
static bool opt_use_failure_recording = true;
static bool opt_use_component_recursion = true;


/* Verbosity level and target stream */
static unsigned int verbose_level = 1;
static FILE* verbstr = stdout;


 


vector<int> sepos;
int nodenum, edgenum;
vector<vector<int> > Graph;
vector<vector<int> > CGraph;
vector<pair<int, vector<int> > > SEList;
vector<int> se;
vector<int> L; 
vector<int> pos;
vector<int> tn_pos_count;
vector<bool> unique_;
vector<pair<vector<int>, int > > signature;
vector<bool> sub_uni;
vector<bool> visited;
vector<int> node_hashing;
vector<int> perm;
vector<int> pos_node;
vector<bool> in_CGraph;

struct tree_node{
  vector<int> vertex_list;
  vector<int> children;
  int parent;
  vector<int> labeling;
  //vector<vector<int>  > orbit_partition;
  vector<pair<int,int> > EL;
  int depth;
  int nof_nodes_s;
  int max_level_s;
};

vector<tree_node> DecTree;

bliss::Graph::SplittingHeuristic shs_undirected;
int divides_error, dividep_error;



static void
usage(FILE* const fp, const char* argv0)
{
  const char* program_name;
  
  program_name = rindex(argv0, '/');
  
  if(program_name) program_name++;
  else program_name = argv0;  
  if(!program_name or *program_name == 0) program_name = "bliss";

 // fprintf(fp, "bliss version %s (compiled "__DATE__")\n", bliss::version);
 // fprintf(fp, "Copyright 2003-2015 Tommi Junttila\n");
 /* fprintf(fp,
"\n"
"Usage: %s [options] [<graph file>]\n"
"\n"
"  -directed   the input graph is directed\n"
"  -can        compute canonical form\n"
"  -ocan=f     compute canonical form and output it in file f\n"
"  -v=N        set verbose level to N [N >= 0, default: 1]\n"
"  -sh=X       select splitting heuristics, where X is\n"
"                f    first non-singleton cell\n"
"                fl   first largest non-singleton cell\n"
"                fs   first smallest non-singleton cell\n"
"                fm   first maximally non-trivially connected\n"
"                     non-singleton cell\n"
"                flm  first largest maximally non-trivially connected\n"
"                     non-singleton cell\n"
"                fsm  first smallest maximally non-trivially connected\n"
"                     non-singleton cell [default]\n"
"  -fr=X       use failure recording? [X=y/n, default: y]\n"
"  -cr=X       use component recursion? [X=y/n, default: y]\n"
"  -version    print the version number and exit\n"
"  -help       print this help and exit\n"
          ,program_name
    );
    */
}



static void
parse_options(const int argc, const char** argv)
{
  unsigned int tmp;
  for(int i = 1; i < argc; i++)
    {
      if(strcmp(argv[i], "-can") == 0)
  opt_canonize = true;
      else if((strncmp(argv[i], "-ocan=", 6) == 0) and (strlen(argv[i]) > 6))
  {
    opt_canonize = true;
    opt_output_can_file = argv[i]+6;
  }
      else if(sscanf(argv[i], "-v=%u", &tmp) == 1)
  verbose_level = tmp;
      else if(strcmp(argv[i], "-directed") == 0)
  //opt_directed = true;
        opt_directed = false;
      else if(strcmp(argv[i], "-fr=n") == 0)
  opt_use_failure_recording = false;
      else if(strcmp(argv[i], "-fr=y") == 0)
  opt_use_failure_recording = true;
      else if(strcmp(argv[i], "-cr=n") == 0)
  opt_use_component_recursion = false;
      else if(strcmp(argv[i], "-cr=y") == 0)
  opt_use_component_recursion = true;
      else if((strncmp(argv[i], "-sh=", 4) == 0) and (strlen(argv[i]) > 4))
  {
    opt_splitting_heuristics = argv[i]+4;
  }
      else if(strcmp(argv[i], "-version") == 0)
  {
    fprintf(stdout, "bliss version %s\n", bliss::version);
    exit(0);
  }
      else if(strcmp(argv[i], "-help") == 0)
  {
    usage(stdout, argv[0]);
    exit(0);
  }
      else if(argv[i][0] == '-')
  {
    fprintf(stderr, "Unknown command line argument `%s'\n", argv[i]);
    usage(stderr, argv[0]);
    exit(1);
  }
      else
  {
    if(infilename)
      {
        fprintf(stderr, "Too many file arguments\n");
        usage(stderr, argv[0]);
        exit(1);
      }
    else
      {
        infilename = argv[i];
      }
  }
    }
}



/**
 * The hook function that prints the found automorphisms.
 * \a param must be a file descriptor (FILE *).
 */
static void
report_aut(void* param, const unsigned int n, const unsigned int* aut)
{
  /*
  assert(param);
  fprintf((FILE*)param, "Generator: ");
  bliss::print_permutation((FILE*)param, n, aut, 1);
  fprintf((FILE*)param, "\n");*/
  ;
}



/* Output an error message and exit the whole program */
static void
_fatal(const char* fmt, ...)
{
  va_list ap;
  va_start(ap, fmt);
  vfprintf(stderr, fmt, ap); fprintf(stderr, "\n");
  va_end(ap);
  exit(1);
}



//***********************************************************************



int read_graph(const char* filename){
  ifstream input(filename);
  input>>nodenum>>edgenum;
  for(int i=0; i<nodenum; i++){
    Graph.push_back(vector<int> (0));
    CGraph.push_back(vector<int> (0));
    se.push_back(-1);
    sepos.push_back(-1);
    pos.push_back(-1);
    unique_.push_back(false);
//****************
     L.push_back(-1); 
    sub_uni.push_back(false);
    visited.push_back(false);
    node_hashing.push_back(-1);
    tn_pos_count.push_back(0);
    perm.push_back(-1);
    pos_node.push_back(-1);

  }
  int u,v;
  while(input>>u>>v){
    Graph[u].push_back(v);
    Graph[v].push_back(u);
  }
  for(int i=0; i<nodenum; i++)
    sort(Graph[i].begin(), Graph[i].end());
  return 0;
}



int structural_equivalent(){
  signature.clear();
  for(int i=0; i<nodenum; i++){
    signature.push_back(make_pair(Graph[i], i));
  }
  sort(signature.begin(), signature.end());

  int pre=0;
  int cur;
  vector<int> sel;
  sel.clear();

  for(cur=1; cur<signature.size(); cur++){
    if(signature[cur].first == signature[pre].first){
      se[signature[cur].second]=signature[pre].second;
      sel.push_back(signature[cur].second);
    }
    else{
      if(!sel.empty()){
        SEList.push_back(make_pair(signature[pre].second, sel));
        se[signature[pre].second]=-2;
        sepos[signature[pre].second]=SEList.size()-1;
      }
      sel.clear();
      pre=cur;
    }
  }
  if(pre!=cur-1){
    SEList.push_back(make_pair(signature[pre].second, sel));
    se[signature[pre].second]=-2;
    sepos[signature[pre].second]=SEList.size()-1;
  }

  return 0;
}


  
int encode_degree(){
  signature.clear();
  pair<vector<int>, int> p;
  for(int i=0; i<nodenum; i++){
    if(se[i]>=0)
      continue;
    p.first.clear();
    p.second=i;
    for(auto u: Graph[i]){
      p.first.push_back(Graph[u].size());
    }
    sort(p.first.begin(), p.first.end());
    signature.push_back(p);
  }
  sort(signature.begin(), signature.end());
  return 0;
}
 


int encode_nei_pos(int start, int end ){
  for(int i=start; i<end; i++){
    signature[i].first.clear();
    int v=signature[i].second;
    for(auto u : Graph[v]){
      if(se[u] >=0)
        signature[i].first.push_back(pos[se[u]]);
      else
        signature[i].first.push_back(pos[u]);
    }
    sort(signature[i].first.begin(), signature[i].first.end());  
  }
  sort(signature.begin()+start, signature.begin()+end);
  return 0;
}

 
 
int partition(){
  vector<bool> nsc_to_refine(nodenum, false);
  vector<int> pos2nsc(nodenum, -1);
  vector<int> start_nsc(nodenum, -1);
  vector<int> end_nsc(nodenum, -1);
  int next_nsc=0;
  vector<int> ToRef_cur, ToRef_next;

  encode_degree();
  int pre=0;
  int cur;
  pos[signature[pre].second]=pre;
  for(cur=1; cur<signature.size(); ++cur){
    if(signature[cur].first == signature[pre].first)
      pos[signature[cur].second]=pre;
    else{
      if(cur==pre+1){
        unique_[signature[pre].second]=true;
      }
      else{
        nsc_to_refine[next_nsc]=true;
        start_nsc[next_nsc]=pre;
        end_nsc[next_nsc]=cur;
        ToRef_next.push_back(next_nsc);
        pos2nsc[pre]=next_nsc;
        next_nsc++;
      }
      pre=cur;
      pos[signature[pre].second]=pre;
    }
  }
  if(cur==pre+1)
    unique_[signature[pre].second]=true;
  else{
    nsc_to_refine[next_nsc]=true;
    start_nsc[next_nsc]=pre;
    end_nsc[next_nsc]=cur;
    ToRef_next.push_back(next_nsc);
    pos2nsc[pre]=next_nsc;
    next_nsc++;
  }

  int round=0;
  bool new_nsc;

  while(!ToRef_next.empty()){
    ToRef_cur=ToRef_next;
    ToRef_next.clear();
    ++round;
    

    for(auto c: ToRef_cur){
      int start=start_nsc[c];
      int end=end_nsc[c];
      nsc_to_refine[c]=false;
      encode_nei_pos(start, end);

      if(signature[start].first != signature[end-1].first){
        new_nsc=false;
        pre=start;
        pos[signature[pre].second]=pre;
        for(cur=pre+1; cur<end; ++cur){
          if(signature[cur].first == signature[pre].first){
            pos[signature[cur].second]=pre;
          }
          else{
            if(cur==pre+1){
              unique_[signature[pre].second]=true;
              if(new_nsc==false){
                new_nsc=true;
                end_nsc[c]=cur;
              }
            }
            else{
              if(new_nsc==false){
                new_nsc=true;
                end_nsc[c]=cur;
                if(nsc_to_refine[c]==false){
                  nsc_to_refine[c]=true;
                  ToRef_next.push_back(c);
                }
              }
              else{
                start_nsc[next_nsc]=pre;
                end_nsc[next_nsc]=cur;
                pos2nsc[pre]=next_nsc;
                ToRef_next.push_back(next_nsc);
                ++next_nsc;
              }
              
            }
            for(auto p: signature[pre].first){
              if(pos2nsc[p]!=-1 &&  end_nsc[pos2nsc[p]]-start_nsc[pos2nsc[p]]>1  && nsc_to_refine[pos2nsc[p]]==false){
                nsc_to_refine[pos2nsc[p]]=true;
                ToRef_next.push_back(pos2nsc[p]);
              }
            }
            pre=cur;
            pos[signature[pre].second]=pre;
          }
        }
        if(cur==pre+1){
          unique_[signature[pre].second]=true;
          if(new_nsc==false){
            new_nsc=true;
            end_nsc[c]=cur;
          }
        }
        else{
          if(new_nsc==false){
            new_nsc=true;
            end_nsc[c]=cur;
            if(nsc_to_refine[c]==false){
              nsc_to_refine[c]=true;
              ToRef_next.push_back(c);
            }
          }
          else{
            start_nsc[next_nsc]=pre;
            end_nsc[next_nsc]=cur;
            pos2nsc[pre]=next_nsc;
            ToRef_next.push_back(next_nsc);
            ++next_nsc;
          }
        }
        for(auto p: signature[pre].first){
          if(pos2nsc[p]!=-1 && end_nsc[pos2nsc[p]]-start_nsc[pos2nsc[p]]>1  && nsc_to_refine[pos2nsc[p]]==false){
            nsc_to_refine[pos2nsc[p]]=true;
            ToRef_next.push_back(pos2nsc[p]);
          }
        }
      } 
    }
  }

  int order=0;
  pre=0;
  pos[signature[pre].second]=order;
  for(cur=1; cur<signature.size(); cur++){
    if(signature[cur].first == signature[pre].first){
      pos[signature[cur].second]=order;
    }
    else{
      for(int i=pre; i<cur; i++){
        order++;
        if(se[signature[i].second]==-2){
          order+=SEList[sepos[signature[i].second]].second.size();
          for(auto v: SEList[sepos[signature[i].second]].second)
            pos[v]=pos[signature[i].second];
        }
      }
      pre=cur;
      pos[signature[pre].second]=order;
    }
  }
  for(int i=pre; i<cur; i++){
    if(se[signature[i].second]==-2){
      for(auto v: SEList[sepos[signature[i].second]].second)
        pos[v]=pos[signature[i].second];
    }
  }
  return 0;
}



/*

int partition(){
  vector<bool> nsc_to_refine(nodenum, false);
  vector<int> start_nsc(nodenum, -1);
  vector<int> end_nsc(nodenum, -1);
  int next_nsc=0;

  encode_degree();
   

  int pre, cur;
  pre=0; 
  pos[signature[pre].second]=pre;
  for(cur=1; cur<signature.size(); cur++){
    if(signature[cur].first == signature[pre].first){
      pos[signature[cur].second]=pre;
    }
    else{
      if(cur == pre+1){
        unique_[signature[pre].second]=true;
      }
      else{
        nsc_to_refine[next_nsc]=true;
        start_nsc[next_nsc]=pre;
        end_nsc[next_nsc]=cur;
        next_nsc++;
      }
      pre=cur;
      pos[signature[pre].second]=pre;
    }
  }
  if(cur == pre+1){
    unique_[signature[pre].second]=true;
  }
  else{
    nsc_to_refine[next_nsc]=true;
    start_nsc[next_nsc]=pre;
    end_nsc[next_nsc]=cur;
    next_nsc++;
  }

  bool refined=true;
  int round=0;
  bool new_nsc;

  while(refined){ 

    ++round;
    int start, end;
    refined=false;
    int nsc_size=next_nsc;
    for(int i=0; i<nsc_size; i++){

      start=start_nsc[i];
      end=end_nsc[i];
      if(end==start+1)
        continue;
      encode_nei_pos(start, end );
      if(signature[start].first != signature[end-1].first){
        refined=true;
        new_nsc=false;
        pre=start;
        pos[signature[pre].second]=pre;
        for(cur=pre+1; cur<end; ++cur){

          if(signature[cur].first == signature[pre].first){
            pos[signature[cur].second]=pre;
          }
          else{
            if(cur==pre+1){
              unique_[signature[pre].second]=true;
              if(new_nsc == false){
                new_nsc=true;
                end_nsc[i]=cur;
              }
            }
            else{
              if(new_nsc==false){
                new_nsc=true;
                end_nsc[i]=cur;
              }
              else{
                start_nsc[next_nsc]=pre;
                end_nsc[next_nsc]=cur;
                ++next_nsc;
              }
            }
            pre=cur;
            pos[signature[pre].second]=pre;
          }

          }
        if(cur == pre+1){
          unique_[signature[pre].second]=true;
          if(new_nsc == false){
                new_nsc=true;
                end_nsc[i]=cur;
              }
        }
        else{
          if(new_nsc==false){
                new_nsc=true;
                end_nsc[i]=cur;
              }
              else{
                start_nsc[next_nsc]=pre;
                end_nsc[next_nsc]=cur;
                ++next_nsc;
              }
        }
      }
    }
  }
 
  int order=0;
  pre=0;
  pos[signature[pre].second]=order;
  for(cur=1; cur<signature.size(); cur++){
    if(signature[cur].first == signature[pre].first){
      pos[signature[cur].second]=order;
    }
    else{
      for(int i=pre; i<cur; i++){
        order++;
        if(se[signature[i].second]==-2){
          order+=SEList[sepos[signature[i].second]].second.size();
          for(auto v: SEList[sepos[signature[i].second]].second)
            pos[v]=pos[signature[i].second];
        }
      }
      pre=cur;
      pos[signature[pre].second]=order;
    }
  }
  for(int i=pre; i<cur; i++){
    if(se[signature[i].second]==-2){
          
          for(auto v: SEList[sepos[signature[i].second]].second)
            pos[v]=pos[signature[i].second];
        }
  }
  return 0;
}
 
*/
 
 
 
 
int simplify_graph(){
  for(int i=0; i<nodenum; i++)
    in_CGraph.push_back(false);
  for(int i=0; i<nodenum; i++){
    if(se[i]<0 && !unique_[i])
      in_CGraph[i]=true;
  }
  for(int i=0; i<nodenum; i++){
    if(in_CGraph[i]){
      for(auto j: Graph[i]){
        if(in_CGraph[j]){
          CGraph[i].push_back(j);
        }
      }
    }
  }
  return 0;
}


 

int bfs(int v, vector<int> &l){
  queue<int> q;
  q.push(v);
  visited[v]=true;
  int u;
  while(!q.empty()){
    u=q.front();
    q.pop();
    l.push_back(u);
    for(int j: CGraph[u]){
      if(!visited[j]){
        q.push(j);
        visited[j]=true;
      }
    }
  }
 // sort(l.begin(), l.end());
  return 0;
}



int construct_root(){  
  DecTree.clear();
  tree_node rn, cn;
  rn.vertex_list.push_back(-1);
  rn.parent=-1;
  rn.depth=0;
  DecTree.push_back(rn);
  for(int i=0; i<nodenum;i++){
    cn.vertex_list.clear();
    cn.children.clear();
    cn.labeling.clear();

    if(se[i]>=0){
       continue;
    }
    else if(unique_[i]){
      cn.vertex_list.push_back(i);
      cn.children.push_back(-1);
      cn.parent=0;
      cn.depth=1;
     
      DecTree.push_back(cn);
      DecTree[0].children.push_back(DecTree.size()-1);
    }
    else{
      if(visited[i]==false){
        bfs(i, cn.vertex_list);
        if(cn.vertex_list.size()==1)
          cn.children.push_back(-1);
        cn.parent=0;
        cn.depth=1;
        DecTree.push_back(cn);
        DecTree[0].children.push_back(DecTree.size()-1);
      }
    } 
  }

  for(int i=0; i<nodenum; i++)
    visited[i]=false;

  return 0;
}



int simplify_sgraph(vector<int> &sg){
  int temp;
  for(auto u: sg){
    if(sub_uni[u]){
      CGraph[u].clear();
      continue;
    }
    temp=0;
    for(int i=0; i<CGraph[u].size(); i++){
      if(!sub_uni[CGraph[u][i]]){
        CGraph[u][temp]=CGraph[u][i];
        temp++;
      }
    }
    while(CGraph[u].size()!=temp)
      CGraph[u].pop_back();
  }
  return 0;

}


 
int DivideP(vector<int>& sg, vector<vector<int> >& s){
  s.clear();
  map<int,int> count;
  for(auto u: sg){
    count[pos[u]]++;
  }
  vector<int> a;
  for(auto u: sg){
    if(count[pos[u]] == 1){
      a.clear(); a.push_back(u);
      s.push_back(a);
      sub_uni[u]=true;    
    }
  }
  if(s.size() ==0 )
    return 0;
  simplify_sgraph(sg);
  for(auto u: sg){
    if(!sub_uni[u] && !visited[u]){
      a.clear();
      bfs(u, a);
      s.push_back(a);
    }
  }
  for(auto u: sg){
    sub_uni[u]=false;
    visited[u]=false;
  }

  return 0;
} 



int simplify_sgraph_e(vector<int>& vl, vector<int>& ll){
  for(auto u: ll)
    sub_uni[u]=true;
  for(auto u: vl){
    int temp=0;
    for(int i=0; i<CGraph[u].size();i++){
      int v=CGraph[u][i];
      if(!sub_uni[pos[v]]){
        CGraph[u][temp]=v;
        ++temp;
      }
    }
    while(CGraph[u].size() != temp)
      CGraph[u].pop_back();
  }
  for(auto u: ll)
    sub_uni[u]=false;
  return 0;
}




int DivideS(vector<int>& sg, vector<vector<int> >& s){

  s.clear();
  sort(sg.begin(), sg.end(), [](const int &v1, const int &v2){
    if(pos[v1]<pos[v2])
      return true;
    else if(pos[v1] == pos[v2] && v1<v2)
      return true;
    else 
      return false;
  });

  vector<vector<int> > part;
  vector<int> labels, a;


  int pre=pos[sg[0]];
  labels.push_back(pre);
  a.push_back(sg[0]);
  for(int i=1; i<sg.size(); i++){
    if(pos[sg[i]] == pre){
      a.push_back(sg[i]);
    }
    else{
      part.push_back(a);
      a.clear();
      pre=pos[sg[i]];
      labels.push_back(pre);
      a.push_back(sg[i]);
    }
  }
  part.push_back(a);



  map<int,int> count_s;
  vector<int> e_remove;
  vector<pair<int, vector<int> > > To_Remove;

  for(int i=0; i<labels.size(); i++){
    int u=part[i][0];
    count_s.clear();
    count_s[pos[u]]++;
    for(auto v: CGraph[u]){
      count_s[pos[v]]++;
    }
    e_remove.clear();
    for(int j=0; j<labels.size(); j++){
      if(count_s[labels[j]] == part[j].size())
        e_remove.push_back(labels[j]);
    }
    if(!e_remove.empty())
      To_Remove.push_back(make_pair(i, e_remove));
  }

  if(To_Remove.empty())
    return 0;
  
  else{
    

    for(auto p: To_Remove){
      simplify_sgraph_e(part[p.first], p.second);
    }
  }

   
  for(auto v: sg){
    if(!visited[v]){
      a.clear();
      bfs(v, a);
      s.push_back(a);
    }
  }


  for(auto v: sg)
    visited[v]=false;

  

  return 0;
}

 
 
 
int CombineCL(int tree_id){
  sort(DecTree[tree_id].vertex_list.begin(), DecTree[tree_id].vertex_list.end(), [](const int& v1, const int& v2){
    if(pos[v1] < pos[v2])
      return true;
    else if(pos[v1] == pos[v2] && perm[node_hashing[v1]] < perm[node_hashing[v2]])
      return true;
    else 
      return false;
  });

  bool to_add=false;
  for(auto u: DecTree[tree_id].vertex_list){
    if(se[u]==-2){
      to_add=true;
      break;
    }
  }
  if(to_add){
    vector<int> vl;
    vl.clear();
    for(auto u: DecTree[tree_id].vertex_list){
      vl.push_back(u);
      if(se[u]==-2){
        for(auto v: SEList[sepos[u]].second)
          vl.push_back(v);
      }
    }
    DecTree[tree_id].vertex_list=vl;
  }
  int pre=pos[DecTree[tree_id].vertex_list[0]];
  int count=0;
  int cur;
  for(auto u: DecTree[tree_id].vertex_list){
    cur=pos[u];
    if(cur == pre){
      L[u]=pre+count;
      DecTree[tree_id].labeling.push_back(L[u]);
      count++;
    }
    else{
      pre=cur;
      count=0;
      L[u]=pre+count;
      DecTree[tree_id].labeling.push_back(L[u]);
      count++;
    }
  } 
  DecTree[tree_id].EL.clear();
  int pu, pv;
  for(auto u: DecTree[tree_id].vertex_list) 
    sub_uni[u]=true;
  for(auto u: DecTree[tree_id].vertex_list){
    pu=L[u];
    for(auto v: Graph[u]){
      if(sub_uni[v]){
        pv=L[v];
        if(pu < pv)
          DecTree[tree_id].EL.push_back(make_pair(pu, pv));
      }
    }
  }
  sort(DecTree[tree_id].EL.begin(), DecTree[tree_id].EL.end());
  for(auto u: DecTree[tree_id].vertex_list)
    sub_uni[u]=false;
  return 0;
}
 
 

int CombineST(int tree_id){
  sort(DecTree[tree_id].children.begin(), DecTree[tree_id].children.end(), [](const int& v1, const int& v2){
    if(DecTree[v1].EL < DecTree[v2].EL)
      return true;
    else if(DecTree[v1].EL == DecTree[v2].EL && v1 < v2)
      return true;
    else 
      return false;
  });
  set<int> pos_list;
  DecTree[tree_id].vertex_list.clear();
  for(auto c: DecTree[tree_id].children){
    for(auto u: DecTree[c].vertex_list){
      DecTree[tree_id].vertex_list.push_back(u);
      pos_list.insert(pos[u]);
      L[u]=pos[u]+tn_pos_count[pos[u]];
      DecTree[tree_id].labeling.push_back(L[u]);
      tn_pos_count[pos[u]]++; 
    }
  }
  for(auto v: pos_list)
    tn_pos_count[v]=0;
  DecTree[tree_id].EL.clear();

  int pu, pv;
  for(auto u: DecTree[tree_id].vertex_list) 
    sub_uni[u]=true;
  for(auto u: DecTree[tree_id].vertex_list){
    pu=L[u];
    for(auto v: Graph[u]){
      if(sub_uni[v]){
        pv=L[v];
        if(pu<pv)
          DecTree[tree_id].EL.push_back(make_pair(pu, pv));
      }
    }
  }
  sort(DecTree[tree_id].EL.begin(), DecTree[tree_id].EL.end());
  for(auto u: DecTree[tree_id].vertex_list)
    sub_uni[u]=false;

  return 0;

}
 

 
int cr(int tree_id){
  tree_node cn;
  vector<vector<int> > s;
  vector<pair<int,int> > node_color;
  vector<pair<int,int> > edgelist;

  bliss::Stats stats;
   

  if(DecTree[tree_id].vertex_list.size()==1){
     
    int u=DecTree[tree_id].vertex_list[0];
    L[u]=pos[u];
    DecTree[tree_id].labeling.push_back(L[u]);
    DecTree[tree_id].EL.clear();
    DecTree[tree_id].EL.push_back(make_pair(L[u], L[u]));

    if(se[u]==-2){
      for(auto v: SEList[sepos[u]].second){
        cn=DecTree[tree_id];
        cn.vertex_list[0]=v;
        L[v]=L[u];
        DecTree.push_back(cn);
        DecTree[cn.parent].children.push_back(DecTree.size()-1);
      }
    } 
    ;
  }
  else{ 
    DivideP(DecTree[tree_id].vertex_list, s);

    if(s.size()>0){
      for(int i=0; i<s.size(); i++){
        cn.vertex_list.clear();
        cn.children.clear();
        cn.labeling.clear();
        cn.vertex_list=s[i];
        cn.depth=DecTree[tree_id].depth+1;
        cn.parent=tree_id;
        if(s[i].size()==1)
          cn.children.push_back(-1);
        DecTree.push_back(cn);
        DecTree[tree_id].children.push_back(DecTree.size()-1);
        cr(DecTree.size()-1);
      }
       CombineST(tree_id);
    }
    else{
      DivideS(DecTree[tree_id].vertex_list, s);
      if(s.size()>1){
        
        for(int i=0; i<s.size(); i++){
          cn.vertex_list.clear();
          cn.children.clear();
          cn.labeling.clear();
          cn.vertex_list=s[i];
          cn.depth=DecTree[tree_id].depth+1;
          cn.parent=tree_id;
          if(s[i].size() ==1)
            cn.children.push_back(-1);
          DecTree.push_back(cn);
          DecTree[tree_id].children.push_back(DecTree.size()-1);
          cr(DecTree.size()-1);
        }
        CombineST(tree_id);  
      }
      else{  
        DecTree[tree_id].children.clear();
        DecTree[tree_id].children.push_back(-1);

      

        node_color.clear();
        edgelist.clear();
        for(int i=0; i<DecTree[tree_id].vertex_list.size(); i++){
          node_hashing[DecTree[tree_id].vertex_list[i]]=i;
        }
        for(auto u: DecTree[tree_id].vertex_list){
          node_color.push_back(make_pair(node_hashing[u], pos[u]));
          for(auto v: CGraph[u]){
            if(node_hashing[v]<=node_hashing[u]){
              edgelist.push_back(make_pair(node_hashing[v], node_hashing[u]));
            }
          }
        }
 
        bliss::AbstractGraph* g=0; 

        //bliss::Digraph::SplittingHeuristic shs_directed = bliss::Digraph::shs_fsm;
        bliss::Graph::SplittingHeuristic shs_undirected = bliss::Graph::shs_fsm;
           
        if(strcmp(opt_splitting_heuristics, "f") == 0)
          shs_undirected = bliss::Graph::shs_f;
        else if(strcmp(opt_splitting_heuristics, "fs") == 0)
          shs_undirected = bliss::Graph::shs_fs;
        else if(strcmp(opt_splitting_heuristics, "fl") == 0)
          shs_undirected = bliss::Graph::shs_fl;
        else if(strcmp(opt_splitting_heuristics, "fm") == 0)
          shs_undirected = bliss::Graph::shs_fm;
        else if(strcmp(opt_splitting_heuristics, "fsm") == 0)
          shs_undirected = bliss::Graph::shs_fsm;
        else if(strcmp(opt_splitting_heuristics, "flm") == 0)
          shs_undirected = bliss::Graph::shs_flm;
        else
          _fatal("Illegal option -sh=%s, aborting", opt_splitting_heuristics);
      
        g = bliss::Graph::read_edges(DecTree[tree_id].vertex_list.size(), edgelist.size(), node_color, edgelist);
          
           
        ((bliss::Graph*)g)->set_splitting_heuristic(shs_undirected);
        g->set_verbose_level(verbose_level);
        g->set_verbose_file(verbstr);
        g->set_failure_recording(opt_use_failure_recording);
        g->set_component_recursion(opt_use_component_recursion);
        
         
        const unsigned int* cl = g->canonical_form(stats, &report_aut, stdout);

        
        for(int i=0; i<g->get_nof_vertices(); i++)
          perm[i]=cl[i];
        CombineCL(tree_id);
        

        stats.store(DecTree[tree_id].nof_nodes_s, DecTree[tree_id].max_level_s);
        for(auto u: DecTree[tree_id].vertex_list)
          node_hashing[u]=-1;

        for(int i=0; i<g->get_nof_vertices(); i++)
          perm[i]=-1;
        delete g; g = 0;  
        ;
      }
     }

  }

  return 0;
}

 
 

int CRD( ){
  construct_root();
  int no_rc=DecTree.size();


  for(int i=1; i<no_rc; i++){
     
    cr(i );
  }

  CombineST(0);


  return 0;
  
}





//*************************************************************************


static void
settings(const int argc, const char** argv, bliss::AbstractGraph* &g ){
  parse_options(argc, argv);
  
  /* Parse splitting heuristics */
  bliss::Digraph::SplittingHeuristic shs_directed = bliss::Digraph::shs_fsm;
  //bliss::Graph::SplittingHeuristic shs_undirected = bliss::Graph::shs_fsm;
  shs_undirected = bliss::Graph::shs_fsm;
  if(opt_directed)
    {
      if(strcmp(opt_splitting_heuristics, "f") == 0)
  shs_directed = bliss::Digraph::shs_f;
      else if(strcmp(opt_splitting_heuristics, "fs") == 0)
  shs_directed = bliss::Digraph::shs_fs;
      else if(strcmp(opt_splitting_heuristics, "fl") == 0)
  shs_directed = bliss::Digraph::shs_fl;
      else if(strcmp(opt_splitting_heuristics, "fm") == 0)
  shs_directed = bliss::Digraph::shs_fm;
      else if(strcmp(opt_splitting_heuristics, "fsm") == 0)
  shs_directed = bliss::Digraph::shs_fsm;
      else if(strcmp(opt_splitting_heuristics, "flm") == 0)
  shs_directed = bliss::Digraph::shs_flm;
      else
  _fatal("Illegal option -sh=%s, aborting", opt_splitting_heuristics);
    }
  else
    {
      if(strcmp(opt_splitting_heuristics, "f") == 0)
  shs_undirected = bliss::Graph::shs_f;
      else if(strcmp(opt_splitting_heuristics, "fs") == 0)
  shs_undirected = bliss::Graph::shs_fs;
      else if(strcmp(opt_splitting_heuristics, "fl") == 0)
  shs_undirected = bliss::Graph::shs_fl;
      else if(strcmp(opt_splitting_heuristics, "fm") == 0)
  shs_undirected = bliss::Graph::shs_fm;
      else if(strcmp(opt_splitting_heuristics, "fsm") == 0)
  shs_undirected = bliss::Graph::shs_fsm;
      else if(strcmp(opt_splitting_heuristics, "flm") == 0)
  shs_undirected = bliss::Graph::shs_flm;
      else
  _fatal("Illegal option -sh=%s, aborting", opt_splitting_heuristics);
    }



   return ;
}



int stat(){
  int n_se=0;
  int n_sec=0;
  for(int i=0; i<nodenum; i++){
    if(se[i]>=0)
      n_se++;
    else if(se[i]==-2)
      n_sec++;
  }
  cout<<"number of structural equivalent pruned "<<n_se<<endl
      <<"number of structural equivalent classes "<<n_sec<<endl;

  int n_uni=0;
  for(int i=0; i<nodenum; i++){
    if(unique_[i])
      n_uni++;
  }
  cout<<"number of unique vertices "<<n_uni<<endl;

  int singleton_leaf=0;
  int non_singleton_leaf=0;
  int max_depth=0;
  int t_error=0;
  for(int i=1; i<DecTree.size(); i++){
   /* if(DecTree[i].children.size()==0){
     cout<<i<<" "<<DecTree[i].vertex_list.size()<<" "<<se[DecTree[i].vertex_list[0]]<<" "<<DecTree[i].depth<<endl;
      t_error++;
      continue;
    }*/
    if(DecTree[i].children.size()>1)
      continue;
    if( DecTree[i].vertex_list.size()==1)
      singleton_leaf++;
    else if( DecTree[i].vertex_list.size()>1)
      non_singleton_leaf++;
    if(max_depth < DecTree[i].depth)
      max_depth=DecTree[i].depth;
  }
  cout<<"number of singleton leaf "<<singleton_leaf<<endl
      <<"number of non-singleton leaf "<<non_singleton_leaf<<endl
      <<"max depth "<<max_depth<<endl; 

  int ML=max_depth;
  int TN=0;
  int DTN=DecTree.size();
  TN=DTN;
  //cout<<"DTN "<<DTN<<endl;
  for(int i=1; i<DecTree.size(); i++){
    if(DecTree[i].children.size()==1 &&  DecTree[i].children[0]==-1){
      if(DecTree[i].nof_nodes_s!=0){
        TN+=(DecTree[i].nof_nodes_s-1);
        if(DecTree[i].depth+DecTree[i].max_level_s > ML)
          ML=DecTree[i].depth+DecTree[i].max_level_s;
      }
    }
}

cout<<"DecTree nodes "<<DTN<<endl;
//<<"Max level "<<ML<<endl<<"Tree nodes "<<TN<<endl;
 
cout<<"ave size "<<1.0*(nodenum-singleton_leaf)/non_singleton_leaf<<endl;
}

 

int print_can(){
  ofstream output("canon.txt");
  output<<nodenum<<endl<<edgenum<<endl;
  vector<pair<int,int> > EL;
  int pu, pv;

  for(int u=0; u<nodenum; u++){
    pu=L[u];
    for(auto v: Graph[u]){
      pv=L[v];
      if(pu<pv){
        EL.push_back(make_pair(pu, pv));
      }
      /*else if(pu == pv){
        cout<<"error u "<<u<<" "<<se[u]<<" "<<unique_[u]<<" "<<pos[u]<<"  "<<L[u]<<endl
            <<"error v "<<v<<" "<<se[v]<<" "<<unique_[v]<<" "<<pos[v]<<"  "<<L[v]<<endl;
      }*/
    }
  }
  sort(EL.begin(), EL.end());
  for(auto e: EL)
    output<<e.first<<" "<<e.second<<endl;

  ofstream out2("perm.txt");
  for(int i=0; i<nodenum; i++)
    out2<<i<<"  "<<L[i]<<endl;

  return 0;
}



int print_at(){
  ofstream output("at.txt");
  vector<int> sig(DecTree.size(), -1);
 
  sig[0]=0;
  int sig_nex=1;
  for(int i=0; i<DecTree.size(); i++){
    if(DecTree[i].children[0]==-1)
      continue;
    int pre=DecTree[i].children[0];
    sig[pre]=sig_nex;
    for(auto c: DecTree[i].children){
      if(DecTree[c].EL == DecTree[pre].EL){
        sig[c]=sig_nex;
      }
      else{
        pre=c;
        sig_nex++;
        sig[pre]=sig_nex;
      }
    }
  }

  for(int i=0; i<DecTree.size(); i++){
    output<<DecTree[i].vertex_list.size()<<endl;
    for(auto v: DecTree[i].vertex_list)
      output<<v<<" ";
    output<<endl;
    for(auto l: DecTree[i].labeling)
      output<<l<<" ";
    output<<endl;
    output<<DecTree[i].EL.size()<<endl; // num of edegs
    for(auto el: DecTree[i].EL)
      output<<el.first<<" "<<el.second<<" ";
    output<<endl;
    output<<DecTree[i].children.size()<<endl;
    for(auto c: DecTree[i].children)
      output<<c<<" ";
    output<<endl;
    output<<DecTree[i].parent<<endl<<sig[i]<<endl<<DecTree[i].depth<<endl;
  }
  return 0;
}

 

int
main(const int argc, const char** argv)
{
  
  bliss::AbstractGraph* g0 = 0;

  settings(argc, argv, g0 );

  read_graph(infilename);

  bliss::Timer timer;
 
  structural_equivalent();
 
  partition();

  simplify_graph();

  CRD( );

  if(verbose_level > 0)
    {
      fprintf(verbstr, "Total time:\t%.2f seconds\n", timer.get_duration());
      fflush(verbstr);
    }
 
  //stat();
  
  print_can();

  print_at();
  
  return 0;
}
