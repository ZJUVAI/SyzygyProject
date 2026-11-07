// Single-thread weighted tabu search. All constraints use integer residues.
#include <algorithm>
#include <chrono>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
static double now(){return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count();}
int main(){
 unsigned seed;double seconds;int nc,ne,modulus;cin>>seed>>seconds>>modulus>>nc>>ne;
 vector<vector<pair<int,int>>> cycles(nc),inc(ne);
 for(int c=0;c<nc;c++)for(int j=0;j<8;j++){int e,s;cin>>e>>s;cycles[c].push_back({e,s});inc[e].push_back({c,s});}
 vector<int> initial(ne);for(auto&v:initial)cin>>v;
 mt19937 rng(seed);double end=now()+seconds;int best_bad=nc;vector<int> best=initial;long long iterations=0;
 auto mod=[&](int x){x%=modulus;return x<0?x+modulus:x;};
 while(now()<end){
  vector<int> v=best; if(iterations==0){v=initial;}else for(int k=0;k<3+(int)(rng()%20);k++)v[rng()%ne]=rng()%modulus;
  vector<int> sums(nc),weight(nc,1);vector<vector<long long>> tabu(ne,vector<long long>(modulus));
  for(int c=0;c<nc;c++){for(auto[e,s]:cycles[c])sums[c]+=s*v[e];sums[c]=mod(sums[c]);}
  int stale=0;
  for(int step=0;step<100000&&now()<end;step++){
   vector<int> bad;for(int c=0;c<nc;c++)if(!sums[c])bad.push_back(c);
   if((int)bad.size()<best_bad){best_bad=bad.size();best=v;stale=0;}
   if(bad.empty()){cout<<iterations<<" 0\n";for(int x:v)cout<<x<<' ';cout<<'\n';return 0;}
   iterations++;stale++;int c=bad[rng()%bad.size()],be=-1,bv=-1,score=100000000,ties=0;
   for(auto[e,sign]:cycles[c]){
    vector<int> costs(modulus),raw(modulus);
    for(auto[j,s]:inc[e]){int r=mod(v[e]-s*sums[j]);costs[r]+=weight[j];raw[r]++;}
    for(int x=0;x<modulus;x++)if(x!=v[e]){
     if(tabu[e][x]>iterations&&(int)bad.size()+raw[x]-raw[v[e]]>=best_bad)continue;
     int delta=costs[x]-costs[v[e]];
     if(delta<score){score=delta;be=e;bv=x;ties=1;}else if(delta==score&&rng()%++ties==0){be=e;bv=x;}
    }
   }
   if(be<0)continue;
   for(auto[j,s]:inc[be])sums[j]=mod(sums[j]+s*(bv-v[be]));
   tabu[be][v[be]]=iterations+5+rng()%17;v[be]=bv;
   if(stale%100==0)for(int c:bad)weight[c]++;
   if(stale%4000==0){for(auto&w:weight)w=(w+1)/2;}
   if(stale>16000)break;
  }
 }
 cout<<iterations<<' '<<best_bad<<"\n";for(int x:best)cout<<x<<' ';cout<<'\n';
}
