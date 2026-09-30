// Closed-box outer cover of the forced grid-avoiding second parent.
// Every removal has an exact universal reason; U leaves remain unresolved.
#include "common.hpp"
struct Box {std::array<Q,3> lo,hi;};
struct Spec {Q L,T,A,nt,eps,half,core;Pose anchor;Q ex,ey,et;std::vector<V>grid;Box root;int depth,anchor_point;};
static Spec spec(const J&j){
 need(j.get<std::string>("schema")=="n17.c028.second-anchor-atlas.v2","SCHEMA");
 need(j.get<int>("parent_count")==17&&j.get<int>("grid_order")==4,"GRID_DIMENSION");
 Spec s;s.L=getq(j,"L");s.T=getq(j,"cap");s.nt=getq(j,"near_t");s.eps=getq(j,"epsilon");s.depth=j.get<int>("max_depth");
 need(s.L>Q(0)&&s.T>Q(4)&&s.T<Q(5)&&s.nt>Q(0)&&s.nt<Q(2,5),"PARAMETER_DOMAIN");need(s.eps>Q(0)&&s.eps<Q(1,100),"ENDPOINT_STRICTNESS");need(s.depth>=0&&s.depth<=21,"DEPTH_RANGE");
 s.A=s.L/s.T;s.half=s.A/Q(2);Q alpha=Q(1)-s.eps,gap=(s.T-Q(2)*alpha)/Q(3);V u=frame(s.nt);need(gap>Q(0)&&gap*(u.x+u.y)<Q(1),"GRID_GAP");
 for(int y=0;y<4;y++)for(int x=0;x<4;x++)s.grid.push_back({s.A*(alpha+Q(x)*gap),s.A*(alpha+Q(y)*gap)});
 auto aj=j.get_child("anchor");s.anchor=pose(aj);s.ex=getq(aj,"ex");s.ey=getq(aj,"ey");s.et=getq(aj,"et");need(s.ex>Q(0)&&s.ey>Q(0)&&s.et>Q(0),"POSITIVE_ANCHOR_WIDTH");need(s.anchor.t-s.et>=Q(0)&&s.anchor.t+s.et<=Q(1),"ANCHOR_ANGLE_RANGE");
 Pose raw_anchor=s.anchor;Q raw_outer=s.A*(Q(1)+Q(2)*s.et)+Q(2)*(s.ex+s.ey);
 V au0=frame(s.anchor.t-s.et),au1=frame(s.anchor.t+s.et);Q ar=s.half*qmin(au0.x+au0.y,au1.x+au1.y);
 Q ax0=qmax(s.anchor.c.x-s.ex,ar),ax1=qmin(s.anchor.c.x+s.ex,s.L-ar),ay0=qmax(s.anchor.c.y-s.ey,ar),ay1=qmin(s.anchor.c.y+s.ey,s.L-ar);
 need(ax0<=ax1&&ay0<=ay1,"ANCHOR_WALL_BOX_EMPTY");s.anchor.c={(ax0+ax1)/Q(2),(ay0+ay1)/Q(2)};s.ex=(ax1-ax0)/Q(2);s.ey=(ay1-ay0)/Q(2);
 s.core=(s.A-Q(2)*(s.ex+s.ey))/(Q(1)+Q(2)*s.et);need(s.core>Q(0),"ANCHOR_CORE");s.anchor_point=j.get<int>("anchor_point_index");need(s.anchor_point>=0&&s.anchor_point<16,"ANCHOR_POINT_INDEX");need(point_margin(s.anchor,s.core,s.grid[s.anchor_point])>Q(0),"ANCHOR_GRID_CAPTURE");for(int k=0;k<16;k++)if(k!=s.anchor_point)need(point_margin(raw_anchor,raw_outer,s.grid[k])<Q(0),"ANCHOR_MULTIPLE_GRID_POSSIBLE");
 s.root={{s.half,s.half,s.nt},{s.L-s.half,s.L-s.half,(Q(1)-s.nt)/(Q(1)+s.nt)}};return s;
}
static bool wall(const Spec&s,const Box&b,int k){V a=frame(b.lo[2]),c=frame(b.hi[2]);Q r=s.half*qmin(a.x+a.y,c.x+c.y);switch(k){case 0:return b.hi[0]<r;case 1:return b.lo[0]>s.L-r;case 2:return b.hi[1]<r;case 3:return b.lo[1]>s.L-r;default:return false;}}
static bool corner_capture(const Spec&s,const Box&b,int k){
 if(k<0||k>3)return false;
 Q edge=s.grid[0].x;
 bool x=(k&1)?b.lo[0]>=s.L-edge:b.hi[0]<=edge;
 bool y=(k&2)?b.lo[1]>=s.L-edge:b.hi[1]<=edge;
 return x&&y;
}
static bool opposite(const Q&a,const Q&b){return (a<=Q(0)&&b>=Q(0))||(b<=Q(0)&&a>=Q(0));}
static bool captures(const Spec&s,const Box&b,int k){
 if(k<0||k>=16)return false;
 V p=s.grid[k];Q lim=s.A*Q(3,4);
 if(qmax(qa(p.x-b.lo[0]),qa(p.x-b.hi[0]))>lim||qmax(qa(p.y-b.lo[1]),qa(p.y-b.hi[1]))>lim)return false;
 V u0=frame(b.lo[2]),u1=frame(b.hi[2]),v0=perp(u0),v1=perp(u1);Q h2=s.half*s.half;
 for(int i=0;i<2;i++)for(int j=0;j<2;j++){
  V d={p.x-(i?b.hi[0]:b.lo[0]),p.y-(j?b.hi[1]:b.lo[1])};Q a=dot(u0,d),c=dot(u1,d),e=dot(v0,d),f=dot(v1,d);
  if(qa(a)>=s.half||qa(c)>=s.half||qa(e)>=s.half||qa(f)>=s.half)return false;
  if((opposite(e,f)||opposite(a,c))&&dot(d,d)>=h2)return false;
 }
 return true;
}
static bool overlaps_anchor(const Spec&s,const Box&b){
 V u=frame(s.anchor.t),v=perp(u);Q r=s.core/Q(2),h2=s.half*s.half;
 for(int i=0;i<2;i++)for(int j=0;j<2;j++){
  V d={ (i?b.hi[0]:b.lo[0])-s.anchor.c.x,(j?b.hi[1]:b.lo[1])-s.anchor.c.y};
  Q dx=qmax(Q(0),qa(dot(u,d))-r),dy=qmax(Q(0),qa(dot(v,d))-r);if(dx*dx+dy*dy>=h2)return false;
 }
 return true;
}
static bool kernel_overlap(const Spec&s,const Box&b){
 Q ex=(b.hi[0]-b.lo[0])/Q(2),ey=(b.hi[1]-b.lo[1])/Q(2),et=(b.hi[2]-b.lo[2])/Q(2);
 Q side=(s.A-Q(2)*(ex+ey))/(Q(1)+Q(2)*et);if(side<=Q(0))return false;
 Pose p{{(b.lo[0]+b.hi[0])/Q(2),(b.lo[1]+b.hi[1])/Q(2)},(b.lo[2]+b.hi[2])/Q(2)};
 return !disjoint(p,side,s.anchor,s.core);
}
static bool projections_below(const Q&dx0,const Q&dx1,const Q&dy0,const Q&dy1,const Q&t0,const Q&t1,const Q&bound){
 V u0=frame(t0),u1=frame(t1),v0=perp(u0),v1=perp(u1);Q b2=bound*bound;
 for(const Q&x:{dx0,dx1})for(const Q&y:{dy0,dy1}){V d{x,y};Q a=dot(u0,d),c=dot(u1,d),e=dot(v0,d),f=dot(v1,d);if(qa(a)>=bound||qa(c)>=bound||qa(e)>=bound||qa(f)>=bound)return false;if((opposite(a,c)||opposite(e,f))&&dot(d,d)>=b2)return false;}
 return true;
}
static bool joint_overlap(const Spec&s,const Box&b){
 Q a0=s.anchor.t-s.et,a1=s.anchor.t+s.et;Q rel(1);
 if(b.hi[2]<a0||a1<b.lo[2]){V x0=frame(a0),x1=frame(a1),y0=frame(b.lo[2]),y1=frame(b.hi[2]);rel=qmin(dot(x1,y0)+qa(cross(x1,y0)),dot(x0,y1)+qa(cross(x0,y1)));}
 Q bound=s.A*(Q(1)+rel)/Q(2),dx0=b.lo[0]-s.anchor.c.x-s.ex,dx1=b.hi[0]-s.anchor.c.x+s.ex,dy0=b.lo[1]-s.anchor.c.y-s.ey,dy1=b.hi[1]-s.anchor.c.y+s.ey;
 return projections_below(dx0,dx1,dy0,dy1,a0,a1,bound)&&projections_below(dx0,dx1,dy0,dy1,b.lo[2],b.hi[2],bound);
}
struct Stats {long long nodes=0,split=0,walls=0,points=0,anchor=0,kernel=0,joint=0,corner=0,unresolved=0;std::array<long long,7>vol{};std::array<long long,16>point_count{};std::vector<std::string>frontier;};
static void visit(const Spec&s,Box b,int depth,std::string path,Stats&st,bool gen,std::istream*in,std::ostream*out){
 need(depth<=s.depth,"TREE_TOO_DEEP");need(++st.nodes<=5000000,"TREE_SIZE");std::string op;int k=-1;
 if(gen){
  for(int i=0;i<4;i++)if(wall(s,b,i)){op="W";k=i;break;}
  if(op.empty())for(int i=0;i<4;i++)if(corner_capture(s,b,i)){op="C";k=i;break;}
  if(op.empty()&&overlaps_anchor(s,b))op="A";
  if(op.empty()&&kernel_overlap(s,b))op="K";
  if(op.empty()&&joint_overlap(s,b))op="J";
  if(op.empty())for(int i=0;i<16;i++)if(captures(s,b,i)){op="P";k=i;break;}
  if(op.empty()){if(depth==s.depth)op="U";else{op="S";k=depth%3;}}
  *out<<op;if(k>=0)*out<<' '<<k;*out<<'\n';
 }else{need(bool(*in>>op),"TREE_TRUNCATED");if(op=="S"||op=="W"||op=="P"||op=="C")need(bool(*in>>k),"TREE_MISSING_INDEX");}
 if(op=="S"){
  need(k>=0&&k<3&&depth<s.depth,"INVALID_SPLIT");need(k==depth%3,"SPLIT_SCHEDULE");st.split++;Q mid=(b.lo[k]+b.hi[k])/Q(2);Box a=b,c=b;a.hi[k]=mid;c.lo[k]=mid;visit(s,a,depth+1,path+'0',st,gen,in,out);visit(s,c,depth+1,path+'1',st,gen,in,out);return;
 }
 long long weight=1LL<<(s.depth-depth);
 if(op=="W"){need(k>=0&&k<4&&wall(s,b,k),"UNPROVED_WALL_LEAF");st.walls++;st.vol[0]+=weight;}
 else if(op=="P"){need(k>=0&&k<16&&captures(s,b,k),"UNPROVED_POINT_LEAF");st.points++;st.point_count[k]++;st.vol[1]+=weight;}
 else if(op=="C"){need(k>=0&&k<4&&corner_capture(s,b,k),"UNPROVED_CORNER_LEAF");st.corner++;st.vol[2]+=weight;}
 else if(op=="A"){need(overlaps_anchor(s,b),"UNPROVED_ANCHOR_LEAF");st.anchor++;st.vol[3]+=weight;}
 else if(op=="K"){need(kernel_overlap(s,b),"UNPROVED_KERNEL_LEAF");st.kernel++;st.vol[4]+=weight;}
 else if(op=="J"){need(joint_overlap(s,b),"UNPROVED_JOINT_LEAF");st.joint++;st.vol[5]+=weight;}
 else if(op=="U"){need(depth==s.depth,"PREMATURE_FRONTIER");st.unresolved++;st.frontier.push_back(path);st.vol[6]+=weight;}
 else need(false,"UNKNOWN_LEAF_OPCODE");
}
#ifndef C028_ATLAS_LIBRARY
int main(int argc,char**argv){try{
 need(argc==6,"USAGE_MODE_INPUT_TREE_FRESH_OUTPUT");std::string mode=argv[1];need(mode=="gen"||mode=="verify","MODE");need(!std::filesystem::exists(argv[5]),"FRESH_OUTPUT_REQUIRED");Spec s=spec(readj(argv[2]));
 // argv[3] is a reserved version selector, preventing accidental use of another tree protocol.
 need(std::string(argv[3])=="v2","PROTOCOL");Stats st;
 if(mode=="gen"){need(!std::filesystem::exists(argv[4]),"FRESH_TREE_REQUIRED");std::ofstream f(argv[4]);need(bool(f),"TREE_OPEN");f<<"C028_ATLAS_V2\n";visit(s,s.root,0,"",st,true,nullptr,&f);need(bool(f),"TREE_WRITE");}
 else{std::ifstream f(argv[4]);need(bool(f),"TREE_OPEN");std::string header;need(bool(f>>header)&&header=="C028_ATLAS_V2","TREE_HEADER");visit(s,s.root,0,"",st,false,&f,nullptr);std::string extra;need(!(f>>extra),"TREE_EXTRA_TOKENS");}
 need(st.vol[0]+st.vol[1]+st.vol[2]+st.vol[3]+st.vol[4]+st.vol[5]+st.vol[6]==(1LL<<s.depth),"INCOMPLETE_ROOT_VOLUME");
 std::ostringstream o;o<<"{\"schema\":\"n17.c028.atlas-result.v2\",\"scope\":\"complete outer cover of a forced grid-avoiding second parent; unresolved leaves are not feasible packings\",\"new_lower_bound\":false,\"cap\":"<<quoted(qs(s.T))<<",\"parent_side\":"<<quoted(qs(s.A))<<",\"anchor_core_side\":"<<quoted(qs(s.core))<<",\"anchor_grid_capture_count\":1,\"max_depth\":"<<s.depth<<",\"root\":[";
 for(int i=0;i<3;i++){if(i)o<<',';o<<'['<<quoted(qs(s.root.lo[i]))<<','<<quoted(qs(s.root.hi[i]))<<']';}
 o<<"],\"nodes\":"<<st.nodes<<",\"counts\":{\"split\":"<<st.split<<",\"wall\":"<<st.walls<<",\"grid_capture\":"<<st.points<<",\"corner_capture\":"<<st.corner<<",\"anchor_overlap\":"<<st.anchor<<",\"kernel_overlap\":"<<st.kernel<<",\"joint_overlap\":"<<st.joint<<",\"unresolved\":"<<st.unresolved<<"},\"dyadic_volume_units\":[";
 for(int i=0;i<7;i++){if(i)o<<',';o<<st.vol[i];}o<<"],\"volume_denominator\":"<<(1LL<<s.depth)<<",\"point_leaf_counts\":[";
 for(int i=0;i<16;i++){if(i)o<<',';o<<st.point_count[i];}o<<"],\"frontier_paths\":[";
 for(size_t i=0;i<st.frontier.size();i++){if(i)o<<',';o<<quoted(st.frontier[i]);}o<<"]}";write_new(argv[5],o.str());std::cout<<"PASS_COMPLETE_OUTER_ATLAS nodes="<<st.nodes<<" unresolved="<<st.unresolved<<"\n";return 0;
}catch(const std::exception&e){std::cerr<<"REJECT "<<e.what()<<'\n';return 1;}}

#endif
