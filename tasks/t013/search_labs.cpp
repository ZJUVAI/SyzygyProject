// Exact integer tabu search. Input and output contain only candidate sequences.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 int n;cin>>n;vector<int> best(n);for(auto &v:best)cin>>v;
 double seconds=stod(argv[1]);mt19937_64 rng(stoull(argv[2]));
 auto start=chrono::steady_clock::now();
 auto elapsed=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};
 auto state=[&](const vector<int>&s,vector<int>&c,vector<int>&b){
  c.assign(n,0);b.assign(n*n,0);int e=0;
  for(int k=1;k<n;k++){for(int i=0;i<n-k;i++){c[k]+=s[i]*s[i+k];b[k*n+i]+=s[i+k];b[k*n+i+k]+=s[i];}e+=c[k]*c[k];}return e;
 };
 vector<int>c,b;int be=state(best,c,b);long long iterations=0,restarts=0;
 vector<vector<int>> elite{best}; vector<int> energies{be};
 while(elapsed()<seconds){
  restarts++;vector<int>s=elite[rng()%elite.size()];
  if(restarts%7==0){for(auto &v:s)v=(rng()&1)?1:-1;}
  else {int kick=2+rng()%max(3,n/7);for(int t=0;t<kick;t++)s[rng()%n]*=-1;}
  int e=state(s,c,b),le=e,stall=0;vector<int>local=s,tabu(n,0);
  // Long tabu chains explore basins; elites retain distinct low-energy states.
  for(int it=0;it<250*n && elapsed()<seconds;it++){
   int pos=-1,bd=1000000000,ties=0;
   for(int j=0;j<n;j++){
    int d=0;for(int k=1;k<n;k++){int h=b[k*n+j];d+=4*h*h-4*s[j]*c[k]*h;}
    if(tabu[j]>it && e+d>=be)continue;
    if(d<bd){bd=d;pos=j;ties=1;}else if(d==bd && rng()%++ties==0)pos=j;
   }
   if(pos<0)break;
   int old=s[pos];e+=bd;
   for(int k=1;k<n;k++){
    c[k]-=2*old*b[k*n+pos];
    if(pos-k>=0)b[k*n+pos-k]-=2*old;
    if(pos+k<n)b[k*n+pos+k]-=2*old;
   }
   s[pos]=-old;tabu[pos]=it+max(3,n/15)+rng()%max(4,n/10);iterations++;
   if(e<le){le=e;local=s;stall=0;}else stall++;
   if(e<be){be=e;best=s;}
   if(stall>8*n)break;
  }
  if(elite.size()<16 || le<*max_element(energies.begin(),energies.end())){
   bool duplicate=false;for(auto&v:elite)if(v==local){duplicate=true;break;}
   if(!duplicate){if(elite.size()<16){elite.push_back(local);energies.push_back(le);}else{int k=max_element(energies.begin(),energies.end())-energies.begin();elite[k]=local;energies[k]=le;}}
  }
 }
 vector<int>vc,vb;if(state(best,vc,vb)!=be)return 2;
 cout<<be<<' '<<iterations<<' '<<restarts<<'\n';for(int v:best)cout<<v<<' ';cout<<'\n';
}
