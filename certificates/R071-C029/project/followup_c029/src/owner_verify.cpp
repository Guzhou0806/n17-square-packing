// A whole avoider component can force a distinct grid point to have no owner.
#define C029_PAIR_LIBRARY
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-function"
#include "pair_verify.cpp"
#pragma GCC diagnostic pop
static bool missed(const Box&b,const V&p,const Q&A,int face){
 if(face<0||face>3)return false;
 for(int i=0;i<2;i++)for(int j=0;j<2;j++)for(const Q&t:{b.lo[2],b.hi[2]}){V u=frame(t),n=face<2?u:perp(u);if(face%2)n=Q(-1)*n;V d{p.x-(i?b.hi[0]:b.lo[0]),p.y-(j?b.hi[1]:b.lo[1])};if(dot(n,d)<=A/Q(2))return false;}
 return true;
}
struct OS{long long nodes=0,split=0,pair=0,wall=0,grid=0,miss=0,anchor=0;int depth=0;};
static void walk(std::istream&f,const Spec&s,const Box&anc,const V&p,Box a,Box b,int dep,OS&st){need(dep<=80,"DEPTH_LIMIT");need(++st.nodes<=5000000,"NODE_LIMIT");st.depth=std::max(dep,st.depth);std::string op;need(bool(f>>op),"TREE_TRUNCATED");if(op=="X"){need(conflict(a,b,s.A),"UNPROVED_PAIR_OVERLAP");st.pair++;return;}int side,k;need(bool(f>>side>>k),"TREE_INDEX");need(side==0||side==1,"SIDE_INDEX");Box&v=side?b:a;
 if(op=="S"){need(k>=0&&k<3,"SPLIT_INDEX");st.split++;Q mid=(v.lo[k]+v.hi[k])/Q(2);Box aa=a,bb=b;(side?bb:aa).hi[k]=mid;walk(f,s,anc,p,aa,bb,dep+1,st);v.lo[k]=mid;walk(f,s,anc,p,a,b,dep+1,st);}
 else if(op=="W"){need(k>=0&&k<4&&wall(s,v,k),"UNPROVED_WALL");st.wall++;}
 else if(op=="P"){need(side==0&&k>=0&&k<16&&captures(s,v,k),"UNPROVED_AVOIDER_GRID_CAPTURE");st.grid++;}
 else if(op=="N"){need(side==1&&missed(v,p,s.A,k),"UNPROVED_REQUIRED_POINT_MISS");st.miss++;}
 else if(op=="A"){need(k==0&&conflict(anc,v,s.A),"UNPROVED_ANCHOR_OVERLAP");st.anchor++;}
 else need(false,"UNKNOWN_OPCODE");}
int main(int argc,char**argv){try{
 need(argc==7,"USAGE_SPEC_FRONTIER_CASES_ID_TREE_OUTPUT");need(!std::filesystem::exists(argv[6]),"FRESH_OUTPUT_REQUIRED");J sj=readj(argv[1]),fj=readj(argv[2]),j=readj(argv[3]);Spec s=spec(sj);need(j.get<std::string>("schema")=="n17.c029.component-forced-hole.v1","SCHEMA");std::string id=argv[4];J rec;int matches=0;for(auto&r:ja(j.get_child("cases")))if(r.get<std::string>("id")==id){rec=r;matches++;}need(matches==1,"CASE_ID");int g=rec.get<int>("component"),k=rec.get<int>("point");need(0<=g&&g<18&&0<=k&&k<16&&k!=s.anchor_point,"CASE_RANGE");auto groups=ja(fj.get_child("components"));need(groups.size()==18,"COMPONENT_COUNT");auto lo=ja(groups[g].get_child("index_lo")),hi=ja(groups[g].get_child("index_hi"));need(groups[g].get<int>("id")==g&&lo.size()==3&&hi.size()==3,"COMPONENT_ID");Box a;for(int d=0;d<3;d++){int l=std::stoi(lo[d].data()),h=std::stoi(hi[d].data());need(0<=l&&l<=h&&h<64,"COMPONENT_INDEX");a.lo[d]=s.root.lo[d]+(s.root.hi[d]-s.root.lo[d])*Q(l,64);a.hi[d]=s.root.lo[d]+(s.root.hi[d]-s.root.lo[d])*Q(h+1,64);}
 Box b=readbox(rec.get_child("root"));V p=s.grid[k];std::array<Q,2>pp{p.x,p.y};for(int d=0;d<2;d++)need(b.lo[d]==qmax(s.half,pp[d]-Q(3,4)*s.A)&&b.hi[d]==qmin(s.L-s.half,pp[d]+Q(3,4)*s.A),"OWNER_ROOT_COVERAGE");need(b.lo[2]==Q(0)&&b.hi[2]==Q(1),"OWNER_ALL_ANGLES");Box anc;auto raw=sj.get_child("anchor");Pose p0=pose(raw);std::array<Q,3>mid{p0.c.x,p0.c.y,p0.t},wd{getq(raw,"ex"),getq(raw,"ey"),getq(raw,"et")};for(int d=0;d<3;d++){anc.lo[d]=mid[d]-wd[d];anc.hi[d]=mid[d]+wd[d];}
 std::ifstream f(argv[5]);need(bool(f),"TREE_OPEN");std::string header;need(bool(f>>header)&&header=="C029_AVOID_OWNER_V1","TREE_HEADER");OS st;walk(f,s,anc,p,a,b,0,st);std::string extra;need(!(f>>extra),"TREE_EXTRA");need(st.nodes==2*st.split+1&&st.split+1==st.pair+st.wall+st.grid+st.miss+st.anchor,"TREE_COMPLETENESS");std::ostringstream o;o<<"{\"schema\":\"n17.c029.forced-hole-proof.v1\",\"id\":"<<quoted(id)<<",\"component\":"<<g<<",\"point\":"<<k<<",\"nodes\":"<<st.nodes<<",\"split\":"<<st.split<<",\"overlap\":"<<st.pair<<",\"wall\":"<<st.wall<<",\"grid\":"<<st.grid<<",\"required_point_miss\":"<<st.miss<<",\"anchor\":"<<st.anchor<<",\"max_depth\":"<<st.depth<<",\"cap\":"<<quoted(qs(s.T))<<",\"status\":\"PASS_COMPONENT_FORCES_UNOWNED_POINT\"}";write_new(argv[6],o.str());std::cout<<"PASS "<<id<<" nodes="<<st.nodes<<'\n';return 0;
}catch(const std::exception&e){std::cerr<<"REJECT "<<e.what()<<'\n';return 1;}}
