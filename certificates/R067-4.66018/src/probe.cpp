// Exact actual-parent probes for fixed-charge falsification, never a global proof.
#define main certificate_checker_main
#include "verify.cpp"
#undef main
int main(int argc,char**argv){try{
 need(argc==5,"usage: probe certificate.json poses.json output.json target-rational");
 std::ifstream f(argv[1],std::ios::binary);need(bool(f),"certificate missing");std::string raw((std::istreambuf_iterator<char>(f)),{});std::istringstream in(raw);J d;pt::read_json(in,d);no_duplicates(d);auto cert=validate(d);
 Q target(argv[4]),A=cert.L/target;need(Q(0)<A&&A<cert.L,"target/parent");J poses;pt::read_json(argv[2],poses);no_duplicates(poses);need(!std::filesystem::exists(argv[3]),"output exists");std::ofstream out(argv[3]);need(bool(out),"output unavailable");
 out.exceptions(std::ios::failbit|std::ios::badbit);
 out<<"{\"status\":\"EXACT_FINITE_PARENT_PROBES_ONLY\",\"certificate_sha256\":\""<<sha256(raw)<<"\",\"target\":\""<<target.str()<<"\",\"rows\":[";bool first=true;
 for(const auto&pose:arr(poses)){Q t(pose.get<std::string>("t")),x(pose.get<std::string>("cx")),y(pose.get<std::string>("cy"));need(Q(0)<=t&&t<=Q(1),"probe angle 0..pi/2 required");auto cs=trig(t);Q radius=A*(qa(cs[0])+qa(cs[1]))/Q(2);need(radius<=x&&x<=cert.L-radius&&radius<=y&&y<=cert.L-radius,"illegal parent centre");std::vector<bool> open,closed;Z open_fee=0,closed_fee=0;
  for(size_t i=0;i<cert.physical.size();++i){Q dx=Q(cert.physical[i][0],cert.D)-x,dy=Q(cert.physical[i][1],cert.D)-y,u=qa(cs[0]*dx+cs[1]*dy),v=qa(Q(0)-cs[1]*dx+cs[0]*dy),h=A/Q(2);bool o=u<h&&v<h,b=u<=h&&v<=h;open.push_back(o);closed.push_back(b);if(o)open_fee+=cert.pw[i];if(b)closed_fee+=cert.pw[i];}
  for(const auto&g:cert.features){int om=0,cm=0;for(size_t j=0;j<g.ids.size();++j){if(open[g.ids[j]])om|=1<<j;if(closed[g.ids[j]])cm|=1<<j;}if(fires(om,g.co,g.threshold,g.rules))open_fee+=g.weight;if(fires(cm,g.co,g.threshold,g.rules))closed_fee+=g.weight;}
  if(!first)out<<',';first=false;out<<"{\"t\":\""<<t.str()<<"\",\"cx\":\""<<x.str()<<"\",\"cy\":\""<<y.str()<<"\",\"open_fee\":"<<open_fee<<",\"closed_fee\":"<<closed_fee<<",\"open_surplus\":"<<17*open_fee-cert.budget<<",\"closed_surplus\":"<<17*closed_fee-cert.budget<<"}";
 }
 out<<"]}\n";out.close();std::cout<<"EXACT_FINITE_PARENT_PROBES_ONLY\n";return 0;
 }catch(const std::exception&e){std::cerr<<"REJECT: "<<e.what()<<'\n';return 1;}}
