// Integer local search for distance-five codes in the 16-dimensional cube.
// The caller supplies only its owned start. No external witness is read.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <stdexcept>
#include <vector>
using namespace std;
using Clock = chrono::steady_clock;
constexpr int U = 65536;
static double now() { return chrono::duration<double>(Clock::now().time_since_epoch()).count(); }
struct State {
    vector<int> masks, words;
    array<int,U> count{}, position{};
    array<unsigned char,U> inside{};
    vector<vector<int>> bucket;
    State(): bucket(1024) {
        for(int x=0;x<U;x++) {
            if(__builtin_popcount((unsigned)x)<5) masks.push_back(x);
            position[x]=x;
            bucket[0].push_back(x);
        }
    }
    void update(int w,int d) {
        for(int m:masks) {
            int x=w^m, old=count[x], p=position[x];
            int tail=bucket[old].back();
            bucket[old][p]=tail; position[tail]=p; bucket[old].pop_back();
            count[x]=old+d; position[x]=bucket[old+d].size(); bucket[old+d].push_back(x);
        }
    }
    void add(int w) { update(w,1); inside[w]=1; words.push_back(w); }
    void erase(int w) {
        update(w,-1); inside[w]=0;
        auto p=find(words.begin(),words.end(),w); *p=words.back(); words.pop_back();
    }
    void reset(const vector<int>& v) {
        while(!words.empty()) erase(words.back());
        for(int w:v) add(w);
    }
};
// Join pairs that conflict after translating exactly one endpoint by mask.
// Translating a connected component changes both endpoints of each such pair.
// Internal pair distances and every pair crossing its boundary stay feasible.
static void switch_component(State& s, mt19937& rng) {
    int mask=1<<(rng()%16), n=s.words.size();
    if(rng()%3==0) mask|=1<<(rng()%16);
    if(rng()%7==0) mask|=1<<(rng()%16);
    vector<int> parent(n); iota(parent.begin(),parent.end(),0);
    auto root=[&](int i) {while(parent[i]!=i) {parent[i]=parent[parent[i]];i=parent[i];} return i;};
    for(int i=0;i<n;i++) for(int j=0;j<i;j++) {
        int difference=s.words[i]^s.words[j];
        if(__builtin_popcount((unsigned)(difference^mask))<5)
            parent[root(i)]=root(j);
    }
    int selected=root(rng()%n);
    vector<int> moved;
    for(int i=0;i<n;i++) if(root(i)==selected) moved.push_back(s.words[i]);
    if((int)moved.size()==n) return;
    for(int w:moved) s.erase(w);
    for(int w:moved) s.add(w^mask);
    for(int w:s.words) if(s.count[w]!=1)
        throw runtime_error("component switch violated distance five");
}
// Greedy coloring gives an exact upper bound for this bounded clique search.
// A time cutoff affects search completeness, never feasibility.
struct Clique {
    using Bits = vector<uint64_t>;
    vector<Bits> adj;
    vector<int> vertices, best, chosen;
    int target, blocks;
    uint64_t nodes=0;
    double end;
    static bool any(const Bits& x) { for(auto z:x) if(z) return true; return false; }
    static int first(const Bits& x) {
        for(int k=0;k<(int)x.size();k++) if(x[k]) return 64*k+__builtin_ctzll(x[k]);
        return -1;
    }
    static void clear(Bits& x,int v) { x[v/64]&=~(uint64_t(1)<<(v%64)); }
    void expand(Bits p) {
        if(++nodes%64==0 && now()>=end) return;
        if(chosen.size()>best.size()) best=chosen;
        if((int)best.size()>=target) return;
        vector<int> order, bounds;
        Bits left=p;
        int color=0;
        while(any(left)) {
            color++;
            Bits independent=left;
            while(any(independent)) {
                int v=first(independent);
                order.push_back(v); bounds.push_back(color); clear(left,v); clear(independent,v);
                for(int k=0;k<blocks;k++) independent[k]&=~adj[v][k];
            }
        }
        for(int j=(int)order.size()-1;j>=0;j--) {
            if(chosen.size()+bounds[j]<=best.size() || now()>=end || (int)best.size()>=target) return;
            int v=order[j]; Bits next=p;
            for(int k=0;k<blocks;k++) next[k]&=adj[v][k];
            chosen.push_back(v); expand(next); chosen.pop_back(); clear(p,v);
        }
    }
    vector<int> solve(vector<int> v,const vector<int>& incumbent,int goal,double deadline) {
        vertices=move(v); target=goal; end=deadline; blocks=(vertices.size()+63)/64;
        adj.assign(vertices.size(),Bits(blocks));
        for(int i=0;i<(int)vertices.size();i++) for(int j=0;j<i;j++)
            if(__builtin_popcount((unsigned)(vertices[i]^vertices[j]))>=5) {
                adj[i][j/64]|=uint64_t(1)<<(j%64); adj[j][i/64]|=uint64_t(1)<<(i%64);
            }
        for(int w:incumbent) {
            auto p=find(vertices.begin(),vertices.end(),w);
            if(p!=vertices.end()) best.push_back(p-vertices.begin());
        }
        Bits p(blocks,~uint64_t(0));
        if(vertices.size()%64) p.back()=(uint64_t(1)<<(vertices.size()%64))-1;
        expand(p);
        vector<int> result; for(int i:best) result.push_back(vertices[i]); return result;
    }
};
int main() {
    unsigned seed; double seconds; int n;
    if(!(cin>>seed>>seconds>>n) || n<1 || n>600) return 2;
    vector<int> best(n); for(int& w:best) cin>>w;
    for(int i=0;i<n;i++) {
        if(best[i]<0 || best[i]>=U) return 3;
        for(int j=0;j<i;j++) if(__builtin_popcount((unsigned)(best[i]^best[j]))<5) return 3;
    }
    mt19937 rng(seed); State s; s.reset(best);
    double deadline=now()+max(0.0,seconds);
    uint64_t moves=0,cavities=0,improvements=0;
    array<uint64_t,U> tabu{};
    auto pick=[&](int level,uint64_t iteration,bool respect_tabu) {
        auto& b=s.bucket[level];
        if(b.empty()) return -1;
        for(int attempt=0;attempt<64;attempt++) {
            int w=b[rng()%b.size()];
            if(!s.inside[w] && (!respect_tabu || tabu[w]<=iteration)) return w;
        }
        int out=-1,seen=0;
        for(int w:b) if(!s.inside[w] && (!respect_tabu || tabu[w]<=iteration)) {
            if(rng()%++seen==0) out=w;
        }
        return out;
    };
    auto remember=[&]() {
        if(s.words.size()>best.size()) {
            best=s.words; improvements++;
            cerr<<"improvement "<<best.size()<<" moves "<<moves<<" cavities "<<cavities<<"\n";
        }
    };
    int epoch=0;
    vector<vector<int>> archive{best};
    while(now()<deadline) {
        epoch++;
        // Spend most time on a target with one additional word. The exact
        // conflict count is updated when a word is removed or inserted.
        s.reset(archive[rng()%archive.size()]); tabu.fill(0);
        for(int k=0;k<1+epoch%7;k++) switch_component(s,rng);
        while(!s.bucket[0].empty()) s.add(s.bucket[0][rng()%s.bucket[0].size()]);
        remember();
        if(archive[0].size()<best.size()) archive={best};
        int target=best.size()+1;
        int conflicts=0;
        for(int level=0;level<1024;level++) {
            int w=pick(level,moves,false);
            if(w>=0) {conflicts+=s.count[w];s.add(w);break;}
        }
        int lowest=conflicts;
        uint64_t last_gain=moves;
        double phase_end=min(deadline,now()+2.0);
        while(now()<phase_end) {
            moves++;
            if(conflicts==0) {remember();break;}
            int maximum=-1,out=-1,ties=0;
            // Neutral changes to unconflicted words reshape the cavity.
            bool scatter=(moves-last_gain>2000 && rng()%5==0);
            if(scatter) out=s.words[rng()%s.words.size()];
            else for(int w:s.words) {
                int bad=s.count[w]-1;
                if(bad>maximum) { maximum=bad;out=w;ties=1; }
                else if(bad==maximum && rng()%++ties==0) out=w;
            }
            conflicts-=s.count[out]-1; s.erase(out);
            tabu[out]=moves+5+rng()%24;
            int in=-1;
            for(int level=0;level<1024;level++) {
                // A feasible target overrides tabu restrictions.
                in=pick(level,moves,!(conflicts==0 && level==0));
                if(in>=0) break;
            }
            if(in<0) return 4;
            conflicts+=s.count[in]; s.add(in);
            if(conflicts<lowest) {lowest=conflicts;last_gain=moves;}
            if(conflicts==0) {remember();break;}
            // Long plateaus restart from an owned feasible code.
            if(moves-last_gain>18000) break;
        }
        cerr<<"target "<<target<<" least_conflicts "<<lowest<<" moves "<<moves<<"\n";
        // Multi-center cavities give independent feasible plateau moves.
        // Each repair tries random greedy sets, then exact bounded clique.
        s.reset(archive[rng()%archive.size()]);
        phase_end=min(deadline,now()+5.0);
        while(now()<phase_end) {
            cavities++;
            if(cavities%127==0) {
                switch_component(s,rng);
                while(!s.bucket[0].empty()) s.add(s.bucket[0][rng()%s.bucket[0].size()]);
                remember();
            }
            vector<int> removed;
            array<unsigned char,U> marked{};
            int centers=(cavities%11==0)?3:((cavities%4==0)?2:1);
            for(int center=0;center<centers;center++) {
                const int levels[]={1,2,3,4,5,6,8,10,12,16};
                int level=levels[rng()%10];
                int anchor=pick(level,moves,false);
                if(anchor<0) continue;
                for(int w:s.words) if(!marked[w] && __builtin_popcount((unsigned)(w^anchor))<5) {
                    marked[w]=1; removed.push_back(w);
                }
            }
            if(cavities%11==0) {
                int amount=4+rng()%61;
                for(int k=0;k<amount;k++) {
                    int w=s.words[rng()%s.words.size()];
                    if(!marked[w]) {marked[w]=1;removed.push_back(w);}
                }
            }
            // A whole Hamming neighborhood exposes replacements that no
            // union of minimum-conflict anchors contains. Keep the exact
            // removed code as the fallback for every bounded subproblem.
            if(cavities%3==0) {
                int anchor=rng()%U,amount=20+rng()%53;
                vector<pair<int,int>> ranked;
                for(int w:s.words)ranked.push_back({__builtin_popcount((unsigned)(w^anchor))*1024+(int)(rng()%1024),w});
                sort(ranked.begin(),ranked.end());
                for(int i=0;i<min(amount,(int)ranked.size());i++){
                    int w=ranked[i].second;if(!marked[w]){marked[w]=1;removed.push_back(w);}
                }
            }
            if(removed.empty()) continue;
            for(int w:removed) s.erase(w);
            vector<int> free=s.bucket[0],replacement=removed;
            for(int attempt=0;attempt<6;attempt++) {
                shuffle(free.begin(),free.end(),rng); vector<int> trial;
                for(int w:free) {
                    bool valid=true;
                    for(int v:trial) if(__builtin_popcount((unsigned)(w^v))<5) {valid=false;break;}
                    if(valid) trial.push_back(w);
                }
                if(trial.size()>replacement.size() || (trial.size()==replacement.size() && rng()%2)) replacement=move(trial);
                if(replacement.size()>removed.size()) break;
            }
            if(free.size()>640 && cavities%3==0) {
                shuffle(free.begin(),free.end(),rng);
                vector<int> limited=removed;
                for(int w:free)if(!marked[w]&&limited.size()<640)limited.push_back(w);
                free=move(limited);
            }
            if(free.size()<=640 && replacement.size()<=removed.size()) {
                double slice=(removed.size()<10?0.004:(removed.size()<30?0.04:0.12));
                Clique clique;
                replacement=clique.solve(free,replacement,removed.size()+1,min(phase_end,now()+slice));
            }
            for(int w:replacement) s.add(w);
            remember();
            if(archive[0].size()<best.size()) archive={best};
            if(s.words.size()==best.size() && cavities%97==0) {
                if(archive.size()<16) archive.push_back(s.words);
                else archive[1+rng()%15]=s.words;
            }
            // Occasional damage lets later cavities cross a size barrier.
            if(cavities%103==0 && s.words.size()>best.size()-3) {
                s.erase(s.words[rng()%s.words.size()]);
            }
            if(s.words.size()+5<best.size()) s.reset(best);
        }
    }
    for(int i=0;i<(int)best.size();i++) for(int j=0;j<i;j++)
        if(__builtin_popcount((unsigned)(best[i]^best[j]))<5) return 5;
    cout<<best.size()<<" "<<moves<<" "<<cavities<<" "<<improvements<<"\n";
    for(int w:best) cout<<w<<" "; cout<<"\n";
}
