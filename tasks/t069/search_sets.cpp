// Search finite integer sets with exact unsigned 128-bit sum/difference supports.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
using wide=__uint128_t;
int count(wide x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
double score(uint64_t a){
 int n=__builtin_popcountll(a);if(n<3)return -1;
 wide sums=0,diffs=0;uint64_t t=a;
 while(t){int k=__builtin_ctzll(t);t&=t-1;sums|=(wide)a<<k;diffs|=(wide)a<<(63-k);}
 int s=count(sums),d=count(diffs);if(d<=n)return -1;
 return log((double)s/n)/log((double)d/n);
}
int main(int argc,char**argv){
 double budget=stod(argv[1]);mt19937_64 rng(stoull(argv[2]));
 int n,x;cin>>n;uint64_t best=0;for(int i=0;i<n;i++){cin>>x;if(x<0||x>63)return 2;best|=1ULL<<x;}
 double bs=score(best);long long iterations=0,restarts=0;
 auto start=chrono::steady_clock::now();auto elapsed=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};
 while(elapsed()<budget){
  restarts++;int span;uint64_t a;
  if(restarts%3){a=best;span=min(63,63-__builtin_clzll(a)+(int)(rng()%12));}
  else{span=17+rng()%47;a=rng();if(span<63)a&=(1ULL<<(span+1))-1;}
  uint64_t mask=span==63?~0ULL:((1ULL<<(span+1))-1);
  if(restarts%4==0){int cut=1+rng()%span;uint64_t low=(1ULL<<cut)-1;a=((a&low)|((a&~low)<<1))&mask;}
  double current=score(a);int chain=2000+rng()%16000;
  double start_temp=(restarts%5==0)?.025:.006;
  for(int it=0;it<chain;it++){
   if((iterations&4095)==0 && elapsed()>=budget)break;
   iterations++;uint64_t trial=a;
   int flips=(rng()%10<7)?1:2+rng()%3;
   for(int k=0;k<flips;k++)trial^=1ULL<<(rng()%(span+1));
   double s=score(trial);if(s<0)continue;
   double progress=(double)it/chain,temp=start_temp*(1-progress)*(1-progress)+.00001;
   double u=(rng()>>11)*0x1.0p-53;
   if(s>=current || u<exp((s-current)/temp)){a=trial;current=s;}
   if(s>bs+1e-14){best=trial;bs=s;}
  }
 }
 cout<<iterations<<' '<<restarts<<'\n';for(int i=0;i<64;i++)if((best>>i)&1)cout<<i<<' ';cout<<'\n';
}
