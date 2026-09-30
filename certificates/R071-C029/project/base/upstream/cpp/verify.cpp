// N17-C007: standalone C++17 exact certificate checker.
// Front-end adapted from Kleddamag's MIT general-rule checker; see ATTRIBUTION.md.
// Geometry backend derives from Guzhou's previously audited native exact engine.
#include "native_geometry.hpp"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <fstream>
#include <iostream>
#include <set>
#include <chrono>
#include <filesystem>
#include <iomanip>
namespace pt=boost::property_tree;
using J=pt::ptree;
static Z integer(const std::string& s){
    need(!s.empty(),"empty integer"); size_t i=s[0]=='-'?1:0;
    need(i<s.size(),"invalid integer"); Z z=0;
    for(;i<s.size();++i){need(s[i]>='0'&&s[i]<='9',"decimal integer required");z=z*10+(s[i]-'0');}
    return s[0]=='-'?-z:z;
}
static Z zi(const J& j){need(j.empty(),"scalar integer required");return integer(j.data());}
static I small(const Z& z){need(z>-LIMIT&&z<LIMIT,"integer outside safe range");return z.convert_to<I>();}
struct Q {
    Z n,d;
    Q(int a):Q(Z(a),Z(1)){}
    Q(Z a=0,Z b=1):n(a),d(b){need(d!=0,"zero denominator");if(d<0){n=-n;d=-d;}Z g=gcdz(n,d);n/=g;d/=g;}
    explicit Q(const std::string& s){auto p=s.find('/');Q v(p==std::string::npos?integer(s):integer(s.substr(0,p)),p==std::string::npos?Z(1):integer(s.substr(p+1)));n=v.n;d=v.d;}
    std::string str()const{return n.convert_to<std::string>()+"/"+d.convert_to<std::string>();}
};
static Q operator+(const Q&a,const Q&b){return Q(a.n*b.d+b.n*a.d,a.d*b.d);}
static Q operator-(const Q&a,const Q&b){return Q(a.n*b.d-b.n*a.d,a.d*b.d);}
static Q operator*(const Q&a,const Q&b){return Q(a.n*b.n,a.d*b.d);}
static Q operator/(const Q&a,const Q&b){return Q(a.n*b.d,a.d*b.n);}
static bool operator<(const Q&a,const Q&b){return a.n*b.d<b.n*a.d;}
static bool operator==(const Q&a,const Q&b){return a.n==b.n&&a.d==b.d;}
static bool operator<=(const Q&a,const Q&b){return !(b<a);}
static Q qa(const Q&a){return Q(a.n<0?-a.n:a.n,a.d);}
static std::array<Q,2> trig(const Q&t){return {Q(t.d*t.d-t.n*t.n,t.d*t.d+t.n*t.n),Q(2*t.n*t.d,t.d*t.d+t.n*t.n)};}
static std::vector<J> arr(const J&j){need(j.data().empty(),"array required");std::vector<J> v;for(const auto&x:j){need(x.first.empty(),"array member");v.push_back(x.second);}return v;}
static void no_duplicates(const J&j){std::set<std::string> seen;for(const auto&x:j){if(!x.first.empty())need(seen.insert(x.first).second,"duplicate JSON key");no_duplicates(x.second);}}
// SHA-256, fixed-width unsigned word operations only. Tested against Node crypto.
static std::string sha256(const std::string& s){
 const uint32_t K[64]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
 std::vector<unsigned char> data(s.begin(),s.end());uint64_t bits=uint64_t(data.size())*8;data.push_back(0x80);while(data.size()%64!=56)data.push_back(0);for(int i=7;i>=0;--i)data.push_back(static_cast<unsigned char>(bits>>(8*i)));
 uint32_t h[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};auto rr=[](uint32_t x,int k){return (x>>k)|(x<<(32-k));};
 for(size_t p=0;p<data.size();p+=64){uint32_t w[64];for(int i=0;i<16;++i)w[i]=(uint32_t(data[p+4*i])<<24)|(uint32_t(data[p+4*i+1])<<16)|(uint32_t(data[p+4*i+2])<<8)|uint32_t(data[p+4*i+3]);for(int i=16;i<64;++i){auto x=w[i-15],y=w[i-2];w[i]=w[i-16]+(rr(x,7)^rr(x,18)^(x>>3))+w[i-7]+(rr(y,17)^rr(y,19)^(y>>10));}uint32_t a=h[0],b=h[1],c=h[2],d=h[3],e=h[4],f=h[5],g=h[6],z=h[7];for(int i=0;i<64;++i){uint32_t t1=z+(rr(e,6)^rr(e,11)^rr(e,25))+((e&f)^(~e&g))+K[i]+w[i],t2=(rr(a,2)^rr(a,13)^rr(a,22))+((a&b)^(a&c)^(b&c));z=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2;}h[0]+=a;h[1]+=b;h[2]+=c;h[3]+=d;h[4]+=e;h[5]+=f;h[6]+=g;h[7]+=z;}
 std::ostringstream o;o<<std::hex<<std::setfill('0');for(auto x:h)o<<std::setw(8)<<x;return o.str();
}
struct Job {Q t,B,H;};
struct Feature {std::vector<int> ids;std::vector<I> co;I threshold,weight;std::vector<int> rules;};
struct Certificate {Model model;std::vector<Job> jobs;std::vector<Point> physical;std::vector<I> pw;std::vector<Feature> features;Z D,LD;I budget,required;Q L,A,margin;};
static bool fires(int mask,const std::vector<I>& co,I threshold,const std::vector<int>&rules){if(!rules.empty()){for(int w:rules)if((mask&w)==w)return true;return false;}I sum=0;for(size_t j=0;j<co.size();++j)if(mask&(1<<j))sum+=co[j];return sum>=threshold;}
static Certificate validate(const J& d){
 Certificate c;c.L=Q(d.get<std::string>("L"));c.A=Q(d.get<std::string>("A"));
 need(c.L==Q(4613,1000)&&Q(0)<c.A&&c.A<c.L,"container/parent");need(c.L/c.A==Q(d.get<std::string>("normalized_target")),"target identity");
 c.D=zi(d.get_child("coordinate_denominator"));need(c.D>0&&(c.L*Q(c.D)).d==1,"coordinate denominator");c.LD=(c.L*Q(c.D)).n;need(zi(d.get_child("weight_denominator"))>0,"weight denominator");
 Z budget=0,absolute=0;std::map<Point,int> lookup;
 for(const auto&row:arr(d.get_child("point_orbits"))){auto r=arr(row);need(r.size()==3,"point record");Z x=zi(r[0]),y=zi(r[1]),w=zi(r[2]);need(x>=0&&x<=c.LD&&y>=0&&y<=c.LD&&w>=0,"point orbit");I wi=small(w);std::set<Point> orbit;
  for(bool swap:{false,true})for(bool sx:{false,true})for(bool sy:{false,true}){Z u=swap?y:x,v=swap?x:y;if(sx)u=c.LD-u;if(sy)v=c.LD-v;orbit.insert({u,v});}
  for(const auto&p:orbit){int id=int(c.physical.size());need(lookup.emplace(p,id).second,"duplicate physical site");c.physical.push_back(p);c.model.sites.push_back({2*p[0]-c.LD,2*p[1]-c.LD});c.pw.push_back(wi);budget+=w;absolute+=w;if(wi)c.model.terms.push_back({{id},wi});}
 }
 need(!c.physical.empty()&&c.physical.size()<10000000,"site count");std::map<std::vector<I>,std::vector<std::pair<int,I>>> cache;
 for(const auto&g:arr(d.get_child("threshold_orbits"))){I w=small(zi(g.get_child("weight"))),k=small(zi(g.get_child("threshold")));need(w>=0&&k>=1,"weight/threshold");auto sets=arr(g.get_child("sets"));need(!sets.empty(),"empty feature orbit");int n=int(arr(sets[0]).size());need(n>=1&&n<=12,"supported Boolean arity is 1..12");
  std::vector<I> co(n,1);if(auto p=g.get_child_optional("coefficients")){auto v=arr(*p);need(int(v.size())==n,"coefficient count");for(int i=0;i<n;++i)co[i]=small(zi(v[i]));}I total=0;for(int j=0;j<n;++j){need(co[j]>0&&(j==0||co[j]<=co[j-1]),"positive sorted coefficients");need(co[j]<LIMIT/n,"coefficient sum bound");total+=co[j];}need(k<=total,"threshold too large");
  std::vector<int> rules;if(auto p=g.get_child_optional("winning_masks"))for(const auto&v:arr(*p)){I z=small(zi(v));need(z>0&&z<(1<<n),"winning mask");rules.push_back(int(z));}std::set<int> unique_rules(rules.begin(),rules.end());need(unique_rules.size()==rules.size(),"duplicate winning mask");for(int a:rules)for(int b:rules)need((a&b)!=0,"disjoint winning sets");
  std::vector<std::vector<int>> ss;for(const auto&s:sets){auto v=arr(s);need(int(v.size())==n,"feature arity");std::vector<int> ids;for(const auto&x:v){Z z=zi(x);need(z>=0&&z<c.physical.size(),"site id");ids.push_back(z.convert_to<int>());}need(std::set<int>(ids.begin(),ids.end()).size()==ids.size(),"duplicate feature site");ss.push_back(ids);}
  auto canonical=[&](std::vector<int> ids){if(rules.empty()){std::vector<std::pair<I,int>> pairs;for(int j=0;j<n;++j)pairs.push_back({-co[j],ids[j]});std::sort(pairs.begin(),pairs.end());for(int j=0;j<n;++j)ids[j]=pairs[j].second;}return ids;};
  std::set<std::vector<int>> expected,actual;for(bool swap:{false,true})for(bool sx:{false,true})for(bool sy:{false,true}){std::vector<int> ids;for(int i:ss[0]){Z x=c.physical[i][0],y=c.physical[i][1];if(swap)std::swap(x,y);if(sx)x=c.LD-x;if(sy)y=c.LD-y;auto it=lookup.find({x,y});need(it!=lookup.end(),"D4 site missing");ids.push_back(it->second);}expected.insert(canonical(ids));}for(const auto&s:ss)need(actual.insert(canonical(s)).second,"duplicate feature image");need(actual==expected,"incomplete D4 feature orbit");
  I cap=rules.empty()?total/k:1;budget+=Z(w)*ss.size()*cap;
  std::vector<I> key=co;key.push_back(-1);key.push_back(k);for(int z:rules)key.push_back(z);auto found=cache.find(key);
  if(found==cache.end()){
   int N=1<<n;std::vector<I> mobius(N);std::vector<int>wins;for(int mask=0;mask<N;++mask){mobius[mask]=fires(mask,co,k,rules)?1:0;if(mobius[mask])wins.push_back(mask);}need(mobius[0]==0,"empty capture wins");
   // Independent finite resource-capacity DP over all disjoint winning sets.
   std::vector<int> dp(N);for(int mask=1;mask<N;++mask)for(int hit:wins)if((mask&hit)==hit)dp[mask]=std::max(dp[mask],1+dp[mask^hit]);need(dp.back()<=cap,"invalid feature budget");
   for(int j=0;j<n;++j)for(int mask=0;mask<N;++mask)if(mask&(1<<j))mobius[mask]-=mobius[mask^(1<<j)];
   std::vector<std::pair<int,I>> expansion;for(int mask=1;mask<N;++mask)if(mobius[mask])expansion.push_back({mask,mobius[mask]});found=cache.emplace(key,expansion).first;
  }
  for(const auto&s:ss){c.features.push_back({s,co,k,w,rules});for(const auto&term:found->second){Z weight=Z(w)*term.second;absolute+=boost::multiprecision::abs(weight);need(absolute<LIMIT,"signed atom mass exceeds bound");if(weight!=0){std::vector<int> ids;for(int j=0;j<n;++j)if(term.first&(1<<j))ids.push_back(s[j]);c.model.terms.push_back({ids,small(weight)});}}}
 }
 need(absolute<LIMIT&&budget==zi(d.get_child("budget_units")),"budget / accumulator bound");c.budget=small(budget);c.required=small(zi(d.get_child("minimum_units")));need(c.required>0&&Z(17)*c.required>budget,"claimed counting surplus must be positive");
 Q cursor(0);bool first=true;
 for(const auto&row:arr(d.get_child("entries"))){auto v=arr(row);need(v.size()==4,"interval record");Q a(v[0].data()),b(v[1].data()),t(v[2].data()),B(v[3].data());need(a==cursor&&Q(0)<=a&&a<b&&b<Q(1)&&Q(0)<=t&&t<Q(1)&&Q(0)<B&&B<c.A,"interval chain/core");auto cs=trig(t);Q lo,hi;bool initial=true;
  for(const Q&u:{a,b}){auto uv=trig(u);Q dot=cs[0]*uv[0]+cs[1]*uv[1],cross=qa(cs[0]*uv[1]-cs[1]*uv[0]);need(Q(0)<dot&&cross<=dot,"angular support range");Q f=uv[0]+uv[1],s=dot+cross;if(initial){lo=f;hi=s;initial=false;}else{if(f<lo)lo=f;if(hi<s)hi=s;}}
  Q margin=c.A-B*hi;need(Q(0)<margin,"non-strict core");if(first||margin<c.margin)c.margin=margin;first=false;Q r=c.A*lo/Q(2);need(B*(cs[0]+cs[1])/Q(2)<=r&&r<c.L/Q(2),"parent centre envelope");c.jobs.push_back({t,B,c.L/Q(2)-r});cursor=b;
 }
 need(!c.jobs.empty()&&Q(1)<cursor*cursor+Q(2)*cursor,"incomplete orientation coverage");return c;
}
static std::string parameters(const Certificate& c,const Job& j){Z C=j.t.d*j.t.d-j.t.n*j.t.n,S=2*j.t.n*j.t.d,T=j.t.d*j.t.d+j.t.n*j.t.n;Q bh=j.B/Q(2);auto lcm=[](const Z&a,const Z&b)->Z{return a/gcdz(a,b)*b;};Z scale=lcm(lcm(2*c.D,bh.d),j.H.d);std::ostringstream o;o<<C<<' '<<S<<' '<<scale/(2*c.D)<<' '<<bh.n*(scale/bh.d)*T<<' '<<j.H.n*(scale/j.H.d);return o.str();}
int main(int argc,char**argv){try{
 need(sha256("")=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"&&sha256("abc")=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","SHA self-test");
 need(argc>=3,"usage: verify certificate.json output.json [--range start count | --validate-only]");std::ifstream f(argv[1],std::ios::binary);need(bool(f),"cannot open certificate");std::string raw((std::istreambuf_iterator<char>(f)),{});std::istringstream input(raw);J d;pt::read_json(input,d);no_duplicates(d);auto begin=std::chrono::steady_clock::now();Certificate c=validate(d);
 int from=0,to=int(c.jobs.size());bool validate_only=false;
 if(argc>3){std::string option=argv[3];if(option=="--validate-only"){need(argc==4,"arguments");validate_only=true;to=0;}else {need(option=="--range"&&argc==6,"range arguments");Z a=integer(argv[4]),b=integer(argv[5]);need(a>=0&&b>0&&a+b<=c.jobs.size(),"range bounds");from=a.convert_to<int>();to=(a+b).convert_to<int>();}}
 need(!std::filesystem::exists(argv[2]),"output already exists");std::ofstream out(argv[2],std::ios::binary);need(bool(out),"cannot create output");out<<"{\"certificate_sha256\":\""<<sha256(raw)<<"\",\"target\":\""<<(c.L/c.A).str()<<"\",\"budget_units\":"<<c.budget<<",\"required_units\":"<<c.required<<",\"start\":"<<from<<",\"end_exclusive\":"<<to<<",\"total_intervals\":"<<c.jobs.size()<<",\"minimum_strict_margin\":\""<<c.margin.str()<<"\",\"sites\":"<<c.physical.size()<<",\"signed_terms\":"<<c.model.terms.size()<<",\"rows\":[\n";I best=INF;bool passed=true;
 // Raising here also detects a failure during the header write above.
 out.exceptions(std::ios::failbit|std::ios::badbit);
 for(int i=from;i<to;++i){auto params=parameters(c,c.jobs[i]);auto result=scan(c.model,params.c_str(),0,false);std::istringstream rowin(result);J row;pt::read_json(rowin,row);I minimum=row.get<I>("minimum_units");best=std::min(best,minimum);passed=passed&&(minimum>=c.required);if(i>from)out<<",\n";out<<"{\"interval\":"<<i<<",\"minimum_units\":"<<minimum<<",\"cells\":"<<row.get<I>("cells")<<"}";out.flush();if((i-from)%64==0)std::cout<<"CPP_INTERVAL "<<i<<" "<<minimum<<std::endl;}
 double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();bool complete=!validate_only&&from==0&&to==int(c.jobs.size());std::string status=validate_only?"PASS_PREMISES_ONLY":!passed?"FAIL_INTERVAL_COVERAGE":complete?"PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION":"PASS_INTERVAL_PARTITION";
 out<<"\n],\"status\":\""<<status<<"\",\"seconds\":"<<seconds;if(!validate_only)out<<",\"minimum_units\":"<<best<<",\"surplus\":"<<Z(17)*best-c.budget;out<<"}\n";out.close();std::cout<<status<<" seconds="<<seconds<<std::endl;return passed?0:2;
 }catch(const std::exception&e){std::cerr<<"REJECT: "<<e.what()<<std::endl;return 1;}}
