// Exact certificates for orientation-sensitive Cartesian hitting grids.
#include "common.hpp"
static std::string run(const J&j){
 need(j.get<std::string>("schema")=="n17.c028.stabbing.v1","SCHEMA");
 need(j.get<int>("grid_order")==4&&j.get<int>("parent_count")==17,"GRID_CARDINALITY");
 Q L=getq(j,"L"),eps=getq(j,"endpoint_epsilon"),loss=getq(j,"spacing_loss");
 need(Q(0)<L&&Q(0)<eps&&eps<Q(1,100)&&Q(0)<loss&&loss<Q(1,100),"STRICT_ENDPOINT_AND_SPACING");
 auto seeds=ja(j.get_child("seeds")),targets=ja(j.get_child("targets"));need(seeds.size()==3&&!targets.empty()&&targets.size()<=16,"INPUT_COUNT");
 std::ostringstream o;o<<"{\"schema\":\"n17.c028.stabbing-result.v1\",\"new_lower_bound\":false,\"targets\":[";
 for(size_t it=0;it<targets.size();it++){
  const J&sp=targets[it];Q T=getq(sp,"cap"),t=getq(sp,"near_t"),t2=getq(sp,"two_t");
  need(Q(4)<T&&T<Q(5)&&Q(0)<t2&&t2<t&&t<Q(2,5),"PARAMETER_DOMAIN");
  Q A=L/T,alpha=Q(1)-eps,step=(T-Q(2)*alpha)/Q(3);V cs=frame(t);Q b=Q(1)/(cs.x+cs.y);
  need(Q(0)<step&&step<b,"NEAR_GRID_GAP");
  std::array<Q,4>p;for(int i=0;i<4;i++)p[i]=A*(alpha+Q(i)*step);
  need(p[0]<A&&L-A<p[3]&&p[0]+p[3]==L&&p[1]+p[2]==L,"GRID_ENDPOINTS_SYMMETRY");
  V c2=frame(t2);Q b2=Q(1)/(c2.x+c2.y),w=b2-loss,lo=T-alpha-Q(3)*w,hi=alpha;
  need(Q(0)<w&&w<b2&&lo<=hi,"MOVABLE_GRID_PHASE");
  Q rho=qmax(Q(0),qmax(lo-Q(1,2),(w-(hi-lo))/Q(2))),disk=Q(1,4)-Q(2)*rho*rho;
  need(Q(0)<disk,"MOVABLE_DISK_MARGIN");
  if(it)o<<',';
  o<<"{\"cap\":"<<quoted(qs(T))<<",\"near_t\":"<<quoted(qs(t))<<",\"two_t\":"<<quoted(qs(t2))<<",\"canonical_upper_t\":"<<quoted(qs((Q(1)-t)/(Q(1)+t)))<<",\"grid_gap_margin\":"<<quoted(qs(b-step))<<",\"moving_rho\":"<<quoted(qs(rho))<<",\"moving_disk_margin\":"<<quoted(qs(disk))<<",\"axis_points\":[";
  for(int i=0;i<4;i++){if(i)o<<',';o<<quoted(qs(p[i]));}o<<"],\"boxes\":[";int bi=0;
  for(const J&seed:seeds){Pose pp=pose(seed);Q ex=getq(seed,"ex"),ey=getq(seed,"ey"),et=getq(seed,"et");
   need(Q(0)<ex&&Q(0)<ey&&Q(0)<et&&t<pp.t-et&&(Q(1)+pp.t+et)*(Q(1)+pp.t+et)<Q(2),"SEED_DOMAIN");
   Q in=(A-Q(2)*(ex+ey))/(Q(1)+Q(2)*et);need(Q(0)<in,"POSITIVE_CORE");V uu=frame(pp.t),vv=perp(uu);
   for(int sw=0;sw<2;sw++)for(int fx=0;fx<2;fx++)for(int fy=0;fy<2;fy++){
    V C=pp.c,u=uu,v=vv;if(sw){std::swap(C.x,C.y);std::swap(u.x,u.y);std::swap(v.x,v.y);}if(fx){C.x=L-C.x;u.x=-u.x;v.x=-v.x;}if(fy){C.y=L-C.y;u.y=-u.y;v.y=-v.y;}
    int chosen=-1;Q margin(0);for(int y=0;y<4;y++)for(int x=0;x<4;x++){V d={p[x]-C.x,p[y]-C.y};Q m=in/Q(2)-qmax(qa(dot(u,d)),qa(dot(v,d)));if(Q(0)<m&&chosen<0){chosen=4*y+x;margin=m;}}
    need(chosen>=0,"BOX_WITHOUT_COMMON_GRID_POINT");if(bi)o<<',';
    o<<"{\"seed\":"<<quoted(seed.get<std::string>("id"))<<",\"transform\":"<<(4*sw+2*fx+fy)<<",\"point_index\":"<<chosen<<",\"core_side\":"<<quoted(qs(in))<<",\"point_margin\":"<<quoted(qs(margin))<<'}';bi++;
   }
  }
  need(bi==24,"BOX_COUNT");o<<"],\"union_capacity\":16,\"remaining_restricted_capacity\":15}";
 }
 o<<"]}";return o.str();
}
int main(int argc,char**argv){try{need(argc==3,"USAGE_INPUT_FRESH_OUTPUT");need(!std::filesystem::exists(argv[2]),"FRESH_OUTPUT_REQUIRED");write_new(argv[2],run(readj(argv[1])));std::cout<<"PASS_STABBING_AND_CONTINUOUS_CAPACITY\n";return 0;}catch(const std::exception&e){std::cerr<<"REJECT "<<e.what()<<'\n';return 1;}}
