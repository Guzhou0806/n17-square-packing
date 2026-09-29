// Unmodified geometric helper definitions from C010 adaptive_rounded.cpp; CLI main omitted.
// Conservative 1e-12 downward grid rounding of core side; local scan premises still exact.
// Research generator: every candidate core is recomputed. A prior complete
// partition seeds interval endpoints only; no prior numerical row is accepted.
#include <optional>
// Exact fixed-angle centre scans used for separation, not all-angle theorems.
#define main supplied_verify_main
#include "../../base/upstream/cpp/verify.cpp"
#undef main
struct V {Q x,y;};
static std::vector<V> clip(std::vector<V> p,int axis,const Q& bound,bool lower){
 std::vector<V> out;if(p.empty())return out;
 auto coord=[&](const V&v){return axis?v.y:v.x;};
 auto inside=[&](const V&v){return lower?bound<=coord(v):coord(v)<=bound;};
 for(size_t i=0;i<p.size();++i){const V&a=p[i],&b=p[(i+1)%p.size()];bool ai=inside(a),bi=inside(b);if(ai)out.push_back(a);if(ai!=bi){Q f=(bound-coord(a))/(coord(b)-coord(a));out.push_back({a.x+f*(b.x-a.x),a.y+f*(b.y-a.y)});}}
 return out;
}
static std::optional<V> sample_pose(const Certificate&c,const Job&job,const J&sample){
 auto b=arr(sample.get_child("box"));std::array<Q,4> box{Q(b[0].data()),Q(b[1].data()),Q(b[2].data()),Q(b[3].data())};
 auto p=parameters(c,job);std::istringstream in(p);Z C=get<Z>(in),S=get<Z>(in),factor=get<Z>(in),half=get<Z>(in),h=get<Z>(in);Z T=job.t.d*job.t.d+job.t.n*job.t.n,scale=factor*2*c.D;
 std::vector<V> poly;for(auto corner:std::array<std::array<int,2>,4>{{{-1,-1},{1,-1},{1,1},{-1,1}}}){Z x=corner[0]*h,y=corner[1]*h;poly.push_back({Q(C*x+S*y),Q(-S*x+C*y)});}
 poly=clip(poly,0,box[0],true);poly=clip(poly,0,box[1],false);poly=clip(poly,1,box[2],true);poly=clip(poly,1,box[3],false);if(poly.size()<3)return {};
 Q area(0),u(0),v(0);for(size_t i=0;i<poly.size();++i){auto&a=poly[i],&b=poly[(i+1)%poly.size()];area=area+a.x*b.y-a.y*b.x;u=u+a.x;v=v+a.y;}if(area==Q(0))return {};u=u/Q(Z(poly.size()));v=v/Q(Z(poly.size()));
 need(box[0]<u&&u<box[1]&&box[2]<v&&v<box[3],"cell centroid not interior");Q x=c.L/Q(2)+(Q(C)*u-Q(S)*v)/Q(scale*T*T),y=c.L/Q(2)+(Q(S)*u+Q(C)*v)/Q(scale*T*T);return V{x,y};
}
static I actual_open_fee(const Certificate&c,const Q&A,const Q&t,const V&p){
 auto cs=trig(t);Q r=A*(cs[0]+cs[1])/Q(2);need(r<=p.x&&p.x<=c.L-r&&r<=p.y&&p.y<=c.L-r,"actual witness illegal");
 Z C=t.d*t.d-t.n*t.n,S=2*t.n*t.d,T=t.d*t.d+t.n*t.n;
 Z limit=A.n*T*c.D*p.x.d*p.y.d,factor=2*A.d;
 std::vector<bool> hits;I fee=0;for(size_t i=0;i<c.physical.size();++i){Z dx=(c.physical[i][0]*p.x.d-p.x.n*c.D)*p.y.d,dy=(c.physical[i][1]*p.y.d-p.y.n*c.D)*p.x.d;bool hit=boost::multiprecision::abs(C*dx+S*dy)*factor<limit&&boost::multiprecision::abs(-S*dx+C*dy)*factor<limit;hits.push_back(hit);if(hit)fee+=c.pw[i];}
 for(const auto&g:c.features){int mask=0;for(size_t i=0;i<g.ids.size();++i)if(hits[g.ids[i]])mask|=1<<i;if(fires(mask,g.co,g.threshold,g.rules))fee+=g.weight;}return fee;
}
struct Accepted {Q a,b,t,B;I minimum,cells;int source,depth;};
struct Adaptive {
 Certificate c;Q A;I required;std::ofstream journal;std::vector<Accepted> accepted;std::vector<std::string> failures;int attempts=0,maxAttempts=512;std::string stopReason="";bool fatal=false,unresolved=false;
 Adaptive(Certificate cc,Q aa,const std::string&path):c(std::move(cc)),A(aa),required(c.budget/17+1),journal(path){if(const char* v=std::getenv("N17_MAX_CORE_ATTEMPTS")){maxAttempts=std::stoi(v);need(maxAttempts>0,"positive core attempt budget");}need(bool(journal),"journal unavailable");journal.exceptions(std::ios::failbit|std::ios::badbit);}
 void test(Q a,Q b,int source,int depth=0){
  if(fatal||unresolved)return;if(attempts>=maxAttempts){unresolved=true;stopReason="ATTEMPT_BUDGET";return;}Q t=(a+b)/Q(2);if(Q(414213,1000000)<t)t=Q(414213,1000000);auto cs=trig(t);Q lo(2),hi(0);
  for(const Q&u:{a,b}){auto uv=trig(u);Q dot=cs[0]*uv[0]+cs[1]*uv[1],cr=qa(cs[0]*uv[1]-cs[1]*uv[0]);need(Q(0)<dot&&cr<=dot,"endpoint range");if(uv[0]+uv[1]<lo)lo=uv[0]+uv[1];if(hi<dot+cr)hi=dot+cr;}
  Q r=A*lo/Q(2),B=A/hi,fit=Q(2)*r/(cs[0]+cs[1]);if(fit<B)B=fit;const Z grid=1000000000000LL;B=Q(B.n*grid/B.d-1,grid);need(Q(0)<B&&B<A&&Q(0)<A-B*hi&&B*(cs[0]+cs[1])/Q(2)<=r,"new core premise");Job job{t,B,c.L/Q(2)-r};
  auto raw=scan(c.model,parameters(c,job).c_str(),0,false);J result;std::istringstream input(raw);pt::read_json(input,result);I minimum=result.get<I>("minimum_units"),cells=result.get<I>("cells");++attempts;
  journal<<"{\"kind\":\"core\",\"source\":"<<source<<",\"depth\":"<<depth<<",\"a\":\""<<a.str()<<"\",\"b\":\""<<b.str()<<"\",\"t\":\""<<t.str()<<"\",\"B\":\""<<B.str()<<"\",\"minimum_units\":"<<minimum<<",\"cells\":"<<cells<<"}\n";journal.flush();
  if(minimum>=required){accepted.push_back({a,b,t,B,minimum,cells,source,depth});if(attempts%64==0)std::cout<<"ACCEPTED "<<accepted.size()<<" attempts="<<attempts<<std::endl;return;}
  std::cout<<"CORE_LOW source="<<source<<" depth="<<depth<<" t="<<t.str()<<" fee="<<minimum<<std::endl;
  Job parent{t,A,c.L/Q(2)-A*(cs[0]+cs[1])/Q(2)};auto praw=scan(c.model,parameters(c,parent).c_str(),32,false);J pres;std::istringstream pin(praw);pt::read_json(pin,pres);
  for(const auto&s:arr(pres.get_child("samples"))){auto p=sample_pose(c,parent,s);if(!p)continue;I fee=actual_open_fee(c,A,t,*p);if(fee<required){
   std::ostringstream f;f<<"{\"kind\":\"actual_parent_failure\",\"source\":"<<source<<",\"depth\":"<<depth<<",\"t\":\""<<t.str()<<"\",\"cx\":\""<<p->x.str()<<"\",\"cy\":\""<<p->y.str()<<"\",\"open_fee\":"<<fee<<",\"surplus\":"<<17*fee-c.budget<<'}';failures.push_back(f.str());journal<<f.str()<<'\n';journal.flush();fatal=true;std::cout<<"ACTUAL_PARENT_FAILURE fee="<<fee<<std::endl;return;}}
  if(depth>=10){unresolved=true;stopReason="DEPTH_LIMIT";std::cout<<"UNRESOLVED depth limit\n";return;}
  Q mid=(a+b)/Q(2);test(a,mid,source,depth+1);test(mid,b,source,depth+1);
 }
};
