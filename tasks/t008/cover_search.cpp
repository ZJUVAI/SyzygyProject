// Integer single-thread focused swap search. Output is an exact complete cover.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
static double now(){return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count();}
int main(){
 unsigned seed;double seconds;int n;cin>>seed>>seconds>>n;mt19937 rng(seed);
 vector<array<int,14>> best(n);for(auto&b:best)for(int&x:b)cin>>x;
 vector<array<int,4>> quads;vector<int> index(24*24*24*24,-1);
 auto id=[](int a,int b,int c,int d){return ((a*24+b)*24+c)*24+d;};
 for(int a=0;a<24;a++)for(int b=a+1;b<24;b++)for(int c=b+1;c<24;c++)for(int d=c+1;d<24;d++){
  index[id(a,b,c,d)]=quads.size();quads.push_back({a,b,c,d});
 }
 auto qid=[&](int a,int b,int c,int d){array<int,4>x{a,b,c,d};sort(x.begin(),x.end());return index[id(x[0],x[1],x[2],x[3])];};
 double end=now()+seconds;long long moves=0,restarts=0;int global_low=10626;
 while(now()<end&&best.size()>1){
  restarts++;auto blocks=best;blocks.erase(blocks.begin()+rng()%blocks.size());
  vector<int> count(quads.size()),weight(quads.size(),1);vector<unsigned> bm(blocks.size());
  for(int z=0;z<(int)blocks.size();z++){
   for(int x:blocks[z])bm[z]|=1u<<x;
   auto&b=blocks[z];for(int a=0;a<14;a++)for(int c=a+1;c<14;c++)for(int d=c+1;d<14;d++)for(int e=d+1;e<14;e++)count[qid(b[a],b[c],b[d],b[e])]++;
  }
  int missed=count_if(count.begin(),count.end(),[](int x){return !x;}),lowest=missed,stale=0;
  global_low=min(global_low,missed);
  for(int step=0;step<300000&&now()<end;step++){
   if(missed==0){best=blocks;cerr<<"improvement "<<best.size()<<" moves "<<moves<<'\n';break;}
   moves++;stale++;
   int q=rng()%quads.size();while(count[q])q=rng()%quads.size();
   auto target=quads[q];unsigned qm=0;for(int x:target)qm|=1u<<x;
   int z=-1,dist=5,ties=0;
   // Focus on a deficit, while random block choices connect larger moves.
   if(rng()%7==0)z=rng()%blocks.size();
   else for(int i=0;i<(int)blocks.size();i++){
    int d=__builtin_popcount(qm&~bm[i]);if(d<dist){dist=d;z=i;ties=1;}else if(d==dist&&rng()%++ties==0)z=i;
   }
   auto&b=blocks[z];vector<int> ins;for(int x:target)if(!(bm[z]&(1u<<x)))ins.push_back(x);
   if(ins.empty())return 4;
   int in=ins[rng()%ins.size()],out=-1,bestdelta=100000000,bties=0;
   vector<int> oldids,newids,chosenold,chosennew;
   for(int k=0;k<14;k++)if(!(qm&(1u<<b[k]))){
    oldids.clear();newids.clear();int delta=0;
    for(int a=0;a<14;a++)if(a!=k)for(int c=a+1;c<14;c++)if(c!=k)for(int d=c+1;d<14;d++)if(d!=k){
     int old=qid(b[a],b[c],b[d],b[k]),nw=qid(b[a],b[c],b[d],in);
     oldids.push_back(old);newids.push_back(nw);
     if(count[old]==1)delta+=weight[old];if(count[nw]==0)delta-=weight[nw];
    }
    if(delta<bestdelta){bestdelta=delta;out=k;chosenold=oldids;chosennew=newids;bties=1;}
    else if(delta==bestdelta&&rng()%++bties==0){out=k;chosenold=oldids;chosennew=newids;}
   }
   double temperature=0.6+min(4.0,stale/3000.0);
   if(bestdelta<=0||generate_canonical<double,32>(rng)<exp(-bestdelta/temperature)){
    for(int q:chosenold)if(--count[q]==0)missed++;
    for(int q:chosennew)if(count[q]++==0)missed--;
    bm[z]^=(1u<<b[out])|(1u<<in);b[out]=in;
    if(missed<lowest){lowest=missed;stale=0;global_low=min(global_low,missed);}
   }
   if(step%200==199)for(int q=0;q<(int)count.size();q++)if(!count[q])weight[q]++;
   if(step%2000==1999)for(int&w:weight)w=(w+1)/2;
   if(stale>18000)break;
  }
 }
 cout<<best.size()<<' '<<moves<<' '<<restarts<<' '<<global_low<<'\n';for(auto b:best){sort(b.begin(),b.end());for(int x:b)cout<<x<<' ';cout<<'\n';}
}
