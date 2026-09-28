// Exact event geometry and sweep. No floating point or fixed-width coordinates.
// Resource budgets / angular containment remain the caller's responsibility.
#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <map>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
// Inline storage avoids heap churn for usual ~320-bit coordinates. MaxBits=0
// still permits arbitrary precision; this is NOT a fixed 512-bit integer.
using Z = boost::multiprecision::number<boost::multiprecision::cpp_int_backend<512,0,
    boost::multiprecision::signed_magnitude,boost::multiprecision::unchecked>>;
using I = std::int64_t;
using Point = std::array<Z,2>;
using Rect = std::array<Z,4>;
constexpr I LIMIT = I(1)<<50, INF = I(1)<<60;
static void need(bool b,const char* s){if(!b)throw std::runtime_error(s);}
template<class T> static T get(std::istream& in){T x;need(bool(in>>x),"malformed input");return x;}
static void end(std::istream& in){std::string s;need(!(in>>s),"trailing input");}
struct Term{std::vector<int> ids; I weight;};
struct Model{std::vector<Point> sites;std::vector<Term> terms;};
static Model parse(const char* text){
    std::istringstream in(text);need(get<int>(in)==1,"model version");
    int ns=get<int>(in),nt=get<int>(in);need(ns>0&&ns<10000000&&nt>=0&&nt<10000000,"model size");
    Model m;m.sites.resize(ns);for(auto& p:m.sites){p[0]=get<Z>(in);p[1]=get<Z>(in);}
    Z mass=0;for(int j=0;j<nt;++j){I w=get<I>(in);int k=get<int>(in);need(k>0&&k<=ns,"term size");
        Term t;t.weight=w;for(int z=0;z<k;++z){int i=get<int>(in);need(i>=0&&i<ns,"site index");t.ids.push_back(i);}
        auto ids=t.ids;std::sort(ids.begin(),ids.end());need(std::adjacent_find(ids.begin(),ids.end())==ids.end(),"duplicate site");
        mass+=boost::multiprecision::abs(Z(w));need(mass<LIMIT,"signed term mass exceeds safe sweep bound");m.terms.push_back(std::move(t));}
    end(in);return m;
}
// Python-style floor division (cpp_int division truncates toward zero).
static Z floorq(const Z& a,const Z& b){need(b>0,"denominator");Z q=a/b;if(a<0&&a%b!=0)--q;return q;}
static Z gcdz(Z a,Z b){if(a<0)a=-a;if(b<0)b=-b;while(b!=0){Z r=a%b;a=b;b=r;}return a;}
struct Edge{Z left,right,slope,intercept,den;};
struct Tree{
    int n;std::vector<I> mn,lazy;std::vector<int> arg;
    explicit Tree(int count){n=1;while(n<count)n*=2;mn.assign(2*n,0);lazy=mn;arg.resize(2*n);for(int j=0;j<n;++j)arg[n+j]=j;for(int j=n-1;j>0;--j)arg[j]=arg[2*j];}
    void add(int v,int l,int r,int a,int b,I d){if(b<=l||r<=a)return;if(a<=l&&r<=b){mn[v]+=d;lazy[v]+=d;return;}int mid=(l+r)/2;add(2*v,l,mid,a,b,d);add(2*v+1,mid,r,a,b,d);int c=mn[2*v]<=mn[2*v+1]?2*v:2*v+1;mn[v]=lazy[v]+mn[c];arg[v]=arg[c];}
    std::pair<I,int> query(int v,int l,int r,int a,int b)const{if(b<=l||r<=a)return {INF,-1};if(a<=l&&r<=b)return {mn[v],arg[v]};int mid=(l+r)/2;auto x=query(2*v,l,mid,a,b),y=query(2*v+1,mid,r,a,b);auto z=x.first<=y.first?x:y;z.first+=lazy[v];return z;}
};
static void quoted(std::ostream& o,const Z& x){o<<'"'<<x<<'"';}
template<class T>static void numbers(std::ostream& o,const std::vector<T>& v){o<<'[';for(size_t i=0;i<v.size();++i){if(i)o<<',';o<<v[i];}o<<']';}
static std::string scan(const Model& m,const char* parameters,int sample_count,bool detail){
    need(sample_count>=0&&sample_count<=128,"sample count");std::istringstream in(parameters);
    Z C=get<Z>(in),S=get<Z>(in),factor=get<Z>(in),half=get<Z>(in),h=get<Z>(in);end(in);
    need(C>=S&&S>=0&&C>0&&factor>0&&half>0&&h>0,"row parameters");
    std::vector<Point> uv;uv.reserve(m.sites.size());
    for(const auto& p:m.sites)uv.push_back({(C*p[0]+S*p[1])*factor,(-S*p[0]+C*p[1])*factor});
    std::map<Rect,I> rectangles;
    for(const auto& t:m.terms){if(!t.weight)continue;Z xmin=uv[t.ids[0]][0],xmax=xmin,ymin=uv[t.ids[0]][1],ymax=ymin;
        for(int i:t.ids){xmin=std::min(xmin,uv[i][0]);xmax=std::max(xmax,uv[i][0]);ymin=std::min(ymin,uv[i][1]);ymax=std::max(ymax,uv[i][1]);}
        Rect r{xmax-half,xmin+half,ymax-half,ymin+half};if(r[0]<r[1]&&r[2]<r[3])rectangles[r]+=t.weight;}
    std::vector<std::pair<Rect,I>> atoms;Z mass=0;for(const auto& a:rectangles)if(a.second){atoms.push_back(a);mass+=boost::multiprecision::abs(Z(a.second));}need(mass<LIMIT,"rectangle mass");
    std::vector<Point> polygon;for(auto p:std::array<std::array<int,2>,4>{{{-1,-1},{1,-1},{1,1},{-1,1}}}){Z x=p[0]*h,y=p[1]*h;polygon.push_back({C*x+S*y,-S*x+C*y});}
    std::vector<Z> xe,ye;for(const auto& p:polygon){xe.push_back(p[0]);ye.push_back(p[1]);}for(const auto& a:atoms){xe.push_back(a.first[0]);xe.push_back(a.first[1]);ye.push_back(a.first[2]);ye.push_back(a.first[3]);}
    auto unique=[](std::vector<Z>& v){std::sort(v.begin(),v.end());v.erase(std::unique(v.begin(),v.end()),v.end());};unique(xe);unique(ye);
    need(xe.size()>=2&&ye.size()>=2&&xe.size()<(1u<<28)&&ye.size()<(1u<<28),"event grid size");
    std::vector<int> first(xe.size()-1,-1),last(first.size(),-1);std::vector<Edge> edges;
    Z pleft=polygon[0][0],pright=pleft;
    for(size_t i=0;i<4;++i){auto p=polygon[i],q=polygon[(i+1)%4];pleft=std::min(pleft,p[0]);pright=std::max(pright,p[0]);if(p[0]==q[0])continue;if(p[0]>q[0])std::swap(p,q);
        Z dx=q[0]-p[0],dy=q[1]-p[1],g=gcdz(dx,dy);dx/=g;dy/=g;edges.push_back({p[0],q[0],dy,p[1]*dx-p[0]*dy,dx});}
    int slabs=0;I cells=0;
    for(size_t k=0;k+1<xe.size();++k){const Z& a=xe[k];const Z& b=xe[k+1];if(a<pleft||b>pright)continue;
        std::vector<std::pair<Z,Z>> vals;for(const auto& e:edges)if(e.left<=a&&b<=e.right){vals.push_back({e.slope*a+e.intercept,e.den});vals.push_back({e.slope*b+e.intercept,e.den});}
        need(vals.size()==4,"expected two polygon edges");auto less=[](const auto& x,const auto& y){return x.first*y.second<y.first*x.second;};
        auto bt=std::minmax_element(vals.begin(),vals.end(),less);need(less(*bt.first,*bt.second),"zero slab area");
        Z bottom=floorq(bt.first->first,bt.first->second),top=-floorq(-bt.second->first,bt.second->second);
        int lo=int(std::upper_bound(ye.begin(),ye.end(),bottom)-ye.begin())-1,hi=int(std::lower_bound(ye.begin(),ye.end(),top)-ye.begin());
        need(0<=lo&&lo<hi&&hi<int(ye.size()),"invalid legal range");first[k]=lo;last[k]=hi;++slabs;cells+=hi-lo;}
    need(slabs>0,"no legal cell");
    std::vector<int> ylo,yhi;std::vector<std::array<int,3>> events;
    auto index=[](const std::vector<Z>& v,const Z& x){return int(std::lower_bound(v.begin(),v.end(),x)-v.begin());};
    for(size_t j=0;j<atoms.size();++j){const auto& r=atoms[j].first;ylo.push_back(index(ye,r[2]));yhi.push_back(index(ye,r[3]));events.push_back({index(xe,r[0]),int(j),1});events.push_back({index(xe,r[1]),int(j),-1});}std::sort(events.begin(),events.end());
    Tree tree(int(ye.size())-1);size_t cursor=0;I best=INF;int ix=-1,iy=-1;std::vector<I> values(first.size(),INF);std::vector<int> indices(first.size(),-1),valid;
    for(size_t k=0;k<first.size();++k){while(cursor<events.size()&&events[cursor][0]==int(k)){auto e=events[cursor++];tree.add(1,0,tree.n,ylo[e[1]],yhi[e[1]],e[2]*atoms[e[1]].second);}if(first[k]<last[k]){auto v=tree.query(1,0,tree.n,first[k],last[k]);values[k]=v.first;indices[k]=v.second;valid.push_back(int(k));if(v.first<best){best=v.first;ix=int(k);iy=v.second;}}}
    need(ix>=0&&iy>=0,"missing minimum");std::vector<int> selected{ix};
    for(int b=0;b<sample_count;++b){size_t start=b*valid.size()/sample_count,stop=(b+1)*valid.size()/sample_count;if(start<stop){int win=valid[start];for(size_t j=start+1;j<stop;++j)if(values[valid[j]]<values[win])win=valid[j];selected.push_back(win);}}
    std::sort(selected.begin(),selected.end());selected.erase(std::unique(selected.begin(),selected.end()),selected.end());
    std::ostringstream out;out<<"{\"minimum_units\":"<<best<<",\"ix\":"<<ix<<",\"iy\":"<<iy<<",\"cells\":"<<cells<<",\"slabs\":"<<slabs<<",\"atoms\":"<<atoms.size()<<",\"samples\":[";
    for(size_t j=0;j<selected.size();++j){if(j)out<<',';int x=selected[j],y=indices[x];out<<"{\"ix\":"<<x<<",\"iy\":"<<y<<",\"value\":"<<values[x]<<",\"box\":[";quoted(out,xe[x]);out<<',';quoted(out,xe[x+1]);out<<',';quoted(out,ye[y]);out<<',';quoted(out,ye[y+1]);out<<"]}";}out<<']';
    if(detail){for(auto name:{"x_events","y_events"}){out<<",\""<<name<<"\":[";const auto& v=std::string(name)=="x_events"?xe:ye;for(size_t i=0;i<v.size();++i){if(i)out<<',';quoted(out,v[i]);}out<<']';}
        out<<",\"rectangles\":[";for(size_t j=0;j<atoms.size();++j){if(j)out<<',';out<<'[';for(const auto& x:atoms[j].first){quoted(out,x);out<<',';}out<<atoms[j].second<<']';}out<<']';
        out<<",\"first\":";numbers(out,first);out<<",\"last\":";numbers(out,last);out<<",\"values\":";numbers(out,values);out<<",\"indices\":";numbers(out,indices);}
    out<<'}';return out.str();
}
#ifdef _WIN32
#define API extern "C" __declspec(dllexport)
#else
#define API extern "C"
#endif
static thread_local std::string error;
API const char* n17_error(){return error.c_str();}
API void* n17_create(const char* text){try{error.clear();return new Model(parse(text));}catch(const std::exception& e){error=e.what();return nullptr;}}
API void n17_destroy(void* p){delete static_cast<Model*>(p);}
API char* n17_scan(void* p,const char* row,int samples,int detail){try{error.clear();need(p!=nullptr,"null model");auto s=scan(*static_cast<const Model*>(p),row,samples,detail!=0);auto out=static_cast<char*>(std::malloc(s.size()+1));need(out!=nullptr,"output allocation");std::memcpy(out,s.c_str(),s.size()+1);return out;}catch(const std::exception& e){error=e.what();return nullptr;}}
API void n17_free(void* p){std::free(p);}
