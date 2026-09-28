// C010 extension: a rational shifted core covers each whole angle interval
// and a wall-adjacent strip of centres. Local coverage only.
// Exact one-dimensional separation along a legal container wall.
// All breakpoints, open endpoint states, and open cells are checked.
// This is not an all-orientation or full two-dimensional centre proof.
#define main inherited_verifier_main
#include "../upstream/cpp/verify.cpp"
#undef main
#include <optional>
struct Event { std::vector<int> starts, ends; };
struct Interval {Q lo,hi;int id;};
struct Witness {Q x; I fee; std::vector<int> counts;std::string kind;};
struct Result {Q t,A,y,left,right;I minimum;long states,events;std::string event_hash;std::vector<Witness> witnesses;};
static std::vector<int> orbit_sizes(const J&d,const Certificate&c){
 std::vector<int> z;for(auto&g:arr(d.get_child("threshold_orbits")))z.push_back(arr(g.get_child("sets")).size());
 for(auto&r:arr(d.get_child("point_orbits"))){auto a=arr(r);Z x=zi(a[0]),y=zi(a[1]);std::set<Point> ss;for(bool sw:{false,true})for(bool fx:{false,true})for(bool fy:{false,true}){Z u=sw?y:x,v=sw?x:y;if(fx)u=c.LD-u;if(fy)v=c.LD-v;ss.insert({u,v});}z.push_back(ss.size());}return z;
}
static Result sweep(const Certificate&c,const J&d,const Q&t,const Q&A,int keep,const std::optional<std::array<Q,3>>&domain={}){
 auto cs=trig(t);need(Q(0)<=t&&t<=Q(414213,1000000),"supported canonical wall angle");Q radius=A*(cs[0]+cs[1])/Q(2),y=radius,left=radius,right=c.L-radius;if(domain){left=(*domain)[0];right=(*domain)[1];y=(*domain)[2];}need(radius<=left&&right<=c.L-radius&&radius<=y&&y<=c.L-radius&&left<right,"legal core line");
 Q C(t.d*t.d-t.n*t.n),S(2*t.n*t.d),T(t.d*t.d+t.n*t.n),h=A*T/Q(2);std::map<Q,Event> ev;ev[left];ev[right];std::vector<Interval> intervals;
 for(size_t id=0;id<c.physical.size();++id){Q px(c.physical[id][0],c.D),py(c.physical[id][1],c.D);Q ku=C*px+S*(py-y),kv=Q(0)-S*px+C*(py-y);Q lo=(ku-h)/C,hi=(ku+h)/C;
  if(S==Q(0)){if(!(qa(kv)<h))continue;}else{Q l2=(Q(0)-h-kv)/S,u2=(h-kv)/S;if(lo<l2)lo=l2;if(u2<hi)hi=u2;}
  if(!(lo<hi)||hi<=left||right<=lo)continue;intervals.push_back({lo,hi,int(id)});
  if(left<=lo&&lo<right)ev[lo].starts.push_back(id);if(left<hi&&hi<=right)ev[hi].ends.push_back(id);
 }
 auto sizes=orbit_sizes(d,c);int nb=arr(d.get_child("threshold_orbits")).size(),nc=sizes.size();std::vector<int> f_orbit(c.features.size()),p_orbit(c.physical.size()),masks(c.features.size(),0),counts(nc,0);std::vector<unsigned char> hit(c.physical.size(),0);std::vector<std::vector<std::pair<int,int>>> incid(c.physical.size());
 size_t fi=0,pi=0;for(int j=0;j<nb;++j)for(int k=0;k<sizes[j];++k)f_orbit[fi++]=j;for(int j=nb;j<nc;++j)for(int k=0;k<sizes[j];++k)p_orbit[pi++]=j;need(fi==c.features.size()&&pi==c.physical.size(),"column ordering");
 for(size_t j=0;j<c.features.size();++j)for(size_t k=0;k<c.features[j].ids.size();++k)incid[c.features[j].ids[k]].push_back({int(j),1<<k});I fee=0;
 auto toggle=[&](int id,bool on){need(bool(hit[id])!=on,"duplicate or unordered site transition");hit[id]=on;int delta=on?1:-1;counts[p_orbit[id]]+=delta;fee+=delta*c.pw[id];for(auto [j,bit]:incid[id]){const auto&g=c.features[j];bool before=fires(masks[j],g.co,g.threshold,g.rules);if(on)masks[j]|=bit;else masks[j]&=~bit;bool after=fires(masks[j],g.co,g.threshold,g.rules);int df=int(after)-int(before);counts[f_orbit[j]]+=df;fee+=df*g.weight;}};
 for(auto&v:intervals)if(v.lo<left&&left<v.hi)toggle(v.id,true);
 std::string event_data;for(auto&[x,e]:ev){event_data+=x.str()+":";for(int i:e.ends)event_data+="-"+std::to_string(i)+",";for(int i:e.starts)event_data+="+"+std::to_string(i)+",";event_data+="\n";}
 Result r{t,A,y,left,right,INF,0,long(ev.size()),sha256(event_data),{}};
 auto record=[&](Q x,std::string kind){++r.states;r.minimum=std::min(r.minimum,fee);if(int(r.witnesses.size())>=keep&&fee>r.witnesses.back().fee)return;for(auto&w:r.witnesses)if(w.counts==counts)return;r.witnesses.push_back({x,fee,counts,kind});std::stable_sort(r.witnesses.begin(),r.witnesses.end(),[](auto&a,auto&b){return a.fee<b.fee;});if(int(r.witnesses.size())>keep)r.witnesses.pop_back();};
 for(auto it=ev.begin();it!=ev.end();++it){Q x=it->first;for(int id:it->second.ends)toggle(id,false);record(x,"boundary");for(int id:it->second.starts)toggle(id,true);auto next=std::next(it);if(next!=ev.end())record((x+next->first)/Q(2),"open_cell");}
 need(!r.witnesses.empty()&&r.minimum==r.witnesses[0].fee,"minimum witness");for(int x:counts)need(x>=0&&x<256,"byte capture range");return r;
}
int main(int argc,char**argv){try{
 need(argc==6,"usage: strip_sweep model.json jobs.json output.json witnesses.json keep-per-family");need(!std::filesystem::exists(argv[3])&&!std::filesystem::exists(argv[4]),"fresh output");int keep=std::stoi(argv[5]);need(keep>0&&keep<=4096,"keep range");std::ifstream f(argv[1],std::ios::binary);need(bool(f),"model missing");std::string raw((std::istreambuf_iterator<char>(f)),{});J d;std::istringstream in(raw);pt::read_json(in,d);no_duplicates(d);auto c=validate(d);J jobs;pt::read_json(argv[2],jobs);no_duplicates(jobs);std::ofstream out(argv[3]),poses(argv[4]);out.exceptions(std::ios::failbit|std::ios::badbit);poses.exceptions(std::ios::failbit|std::ios::badbit);
 out<<"{\"status\":\"EXACT_LOCAL_ANGLE_AND_WALL_STRIP_CORE_MINIMA_ONLY\",\"model_sha256\":\""<<sha256(raw)<<"\",\"budget_units\":"<<c.budget<<",\"rows\":[";poses<<'[';bool first=true,pfirst=true;int j=0;
 for(auto&job:arr(jobs)){Q target(job.get<std::string>("target")),a(job.get<std::string>("a")),b(job.get<std::string>("b")),W(job.get<std::string>("width")),P=c.L/target;
 need(Q(0)<=a&&a<b&&b<=Q(207107,500000)&&Q(0)<=W,"strip parameters");Q t=(a+b)/Q(2);if(Q(414213,1000000)<t)t=Q(414213,1000000);auto uv=trig(t),ca=trig(a),cb=trig(b);Q rlo=P*std::min(ca[0]+ca[1],cb[0]+cb[1])/Q(2),rhi=P*std::max(ca[0]+ca[1],cb[0]+cb[1])/Q(2);
 if(Q(414213,1000000)<b)rhi=P*Q(707107,1000000);
 Z grid=1000000000000LL;rlo=Q(rlo.n*grid/rlo.d,grid);rhi=Q((rhi.n*grid+rhi.d-1)/rhi.d,grid);
 Q H(0);for(const Q&u:{a,b}){auto z=trig(u);Q dot=uv[0]*z[0]+uv[1]*z[1],cr=qa(uv[0]*z[1]-uv[1]*z[0]);need(Q(0)<dot&&cr<=dot,"angle support range");H=std::max(H,dot+cr);}
 Q dy=(rhi-rlo+W)/Q(2),y0=(rlo+rhi+W)/Q(2),cap=std::min((P-Q(2)*dy)/H,Q(2)*rlo/(uv[0]+uv[1]));Q A=Q(cap.n*grid/cap.d-1,grid),strict=P-A*H-Q(2)*dy;
 need(Q(0)<A&&Q(0)<strict,"shifted-core strict containment");std::optional<std::array<Q,3>> domain=std::array<Q,3>{rlo,c.L-rlo,y0};auto r=sweep(c,d,t,A,keep,domain);if(!first)out<<',';first=false;out<<"{\"mode\":\"continuous_angle_wall_strip_shifted_core\",\"parent_A\":\""<<P.str()<<"\",\"a\":\""<<a.str()<<"\",\"b\":\""<<b.str()<<"\",\"width\":\""<<W.str()<<"\",\"dy_bound\":\""<<dy.str()<<"\",\"h_bound\":\""<<H.str()<<"\",\"strict_margin\":\""<<strict.str()<<"\",\"family\":"<<j<<",\"target\":\""<<target.str()<<"\",\"t\":\""<<t.str()<<"\",\"A\":\""<<A.str()<<"\",\"wall_y\":\""<<r.y.str()<<"\",\"left\":\""<<r.left.str()<<"\",\"right\":\""<<r.right.str()<<"\",\"minimum_open_fee\":"<<r.minimum<<",\"surplus\":"<<17*r.minimum-c.budget<<",\"states\":"<<r.states<<",\"events\":"<<r.events<<",\"event_sha256\":\""<<r.event_hash<<"\",\"witnesses\":[";bool wf=true;
 for(auto&w:r.witnesses){if(!wf)out<<',';wf=false;out<<"{\"cx\":\""<<w.x.str()<<"\",\"cy\":\""<<r.y.str()<<"\",\"kind\":\""<<w.kind<<"\",\"open_fee\":"<<w.fee<<",\"counts\":";numbers(out,w.counts);out<<'}';if(!pfirst)poses<<',';pfirst=false;poses<<"{\"t\":\""<<t.str()<<"\",\"cx\":\""<<w.x.str()<<"\",\"cy\":\""<<r.y.str()<<"\"}";}
 out<<"]}";out.flush();poses.flush();std::cout<<"WALL "<<j++<<" t="<<t.str()<<" min="<<r.minimum<<" states="<<r.states<<std::endl;
 }out<<"]}\n";poses<<"]\n";return 0;
}catch(const std::exception&e){std::cerr<<"REJECT "<<e.what()<<std::endl;return 1;}}
