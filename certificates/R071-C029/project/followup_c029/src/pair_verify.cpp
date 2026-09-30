// C029: exact universal conflict certificate, with independent BigInt checker.
#define C028_ATLAS_LIBRARY
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-function"
#include "../../followup_c028/src/atlas.cpp"
#include <regex>
#pragma GCC diagnostic pop
static bool conflict(const Box&a,const Box&b,const Q&A){
 Q rel(1);if(a.hi[2]<b.lo[2]||b.hi[2]<a.lo[2]){V x0=frame(a.lo[2]),x1=frame(a.hi[2]),y0=frame(b.lo[2]),y1=frame(b.hi[2]);rel=qmin(dot(x1,y0)+qa(cross(x1,y0)),dot(x0,y1)+qa(cross(x0,y1)));}
 Q r=A*(Q(1)+rel)/Q(2);Q dx0=b.lo[0]-a.hi[0],dx1=b.hi[0]-a.lo[0],dy0=b.lo[1]-a.hi[1],dy1=b.hi[1]-a.lo[1];
 return projections_below(dx0,dx1,dy0,dy1,a.lo[2],a.hi[2],r)&&projections_below(dx0,dx1,dy0,dy1,b.lo[2],b.hi[2],r);
}
static Box readbox(const J&j){auto x=ja(j);need(x.size()==3,"BOX_DIMENSION");Box b;for(int d=0;d<3;d++){auto y=ja(x[d]);need(y.size()==2,"BOX_INTERVAL");b.lo[d]=qr(y[0].data());b.hi[d]=qr(y[1].data());need(b.lo[d]<b.hi[d],"BOX_ORDER");}need(b.lo[2]>=Q(0)&&b.hi[2]<=Q(1),"ANGLE_CHART");return b;}
struct Count{long long nodes=0,split=0,overlap=0,wall=0,point=0,anchor=0;int depth=0;};
static void visit(std::istream&f,const Spec&s,const Box&anc,Box a,Box b,int dep,Count&st){need(dep<=80,"DEPTH_LIMIT");need(++st.nodes<=5000000,"NODE_LIMIT");st.depth=std::max(dep,st.depth);std::string op;need(bool(f>>op),"TREE_TRUNCATED");if(op=="X"){need(conflict(a,b,s.A),"UNPROVED_PAIR_OVERLAP");st.overlap++;return;}int side=-1,k=-1;need(bool(f>>side>>k),"TREE_INDEX");need(side==0||side==1,"SIDE_INDEX");Box&v=side?b:a;
 if(op=="S"){need(k>=0&&k<3,"SPLIT_INDEX");st.split++;Q mid=(v.lo[k]+v.hi[k])/Q(2);Box aa=a,bb=b;(side?bb:aa).hi[k]=mid;visit(f,s,anc,aa,bb,dep+1,st);v.lo[k]=mid;visit(f,s,anc,a,b,dep+1,st);}
 else if(op=="W"){need(k>=0&&k<4&&wall(s,v,k),"UNPROVED_WALL");st.wall++;}
 else if(op=="P"){need(k>=0&&k<16&&captures(s,v,k),"UNPROVED_GRID_CAPTURE");st.point++;}
 else if(op=="A"){need(k==0&&conflict(anc,v,s.A),"UNPROVED_ANCHOR_OVERLAP");st.anchor++;}
 else need(false,"UNKNOWN_OPCODE");}

#ifndef C029_PAIR_LIBRARY
int main(int argc,char**argv){try{need(argc==7,"USAGE_SPEC_FRONTIER_INPUT_PAIR_TREE_OUTPUT");need(!std::filesystem::exists(argv[6]),"FRESH_OUTPUT_REQUIRED");J sj=readj(argv[1]),fj=readj(argv[2]),j=readj(argv[3]);Spec s=spec(sj);need(j.get<std::string>("schema")=="n17.c029.component-pairs.v1","SCHEMA");need(getq(j,"L")==s.L&&getq(j,"cap")==s.T&&getq(j,"A")==s.A,"TARGET_IDENTITY");
 Box anc=readbox(j.get_child("anchor"));Pose raw=pose(sj.get_child("anchor"));std::array<Q,3> vv{raw.c.x,raw.c.y,raw.t},ww{getq(sj.get_child("anchor"),"ex"),getq(sj.get_child("anchor"),"ey"),getq(sj.get_child("anchor"),"et")};for(int d=0;d<3;d++)need(anc.lo[d]==vv[d]-ww[d]&&anc.hi[d]==vv[d]+ww[d],"ANCHOR_IDENTITY");auto grid=ja(j.get_child("grid"));need(grid.size()==16,"GRID_SIZE");for(int k=0;k<16;k++){auto p=ja(grid[k]);need(p.size()==2&&qr(p[0].data())==s.grid[k].x&&qr(p[1].data())==s.grid[k].y,"GRID_IDENTITY");}
 auto roots=ja(j.get_child("roots")),groups=ja(fj.get_child("components"));need(roots.size()==18&&groups.size()==18,"COMPONENT_COUNT");std::vector<Box> boxes;for(int n=0;n<18;n++){Box b=readbox(roots[n]);auto lo=ja(groups[n].get_child("index_lo")),hi=ja(groups[n].get_child("index_hi"));need(groups[n].get<int>("id")==n&&lo.size()==3&&hi.size()==3,"COMPONENT_ID");for(int d=0;d<3;d++){int l=std::stoi(lo[d].data()),h=std::stoi(hi[d].data());need(0<=l&&l<=h&&h<64,"COMPONENT_INDEX");need(b.lo[d]==s.root.lo[d]+(s.root.hi[d]-s.root.lo[d])*Q(l,64)&&b.hi[d]==s.root.lo[d]+(s.root.hi[d]-s.root.lo[d])*Q(h+1,64),"COMPONENT_ROOT");}boxes.push_back(b);}
 std::string pair=argv[4];need(std::regex_match(pair,std::regex("[0-9]+,[0-9]+")),"PAIR_ID");auto cut=pair.find(',');int i=std::stoi(pair.substr(0,cut)),k=std::stoi(pair.substr(cut+1));need(0<=i&&i<k&&k<18,"PAIR_RANGE");std::ifstream f(argv[5]);need(bool(f),"TREE_OPEN");std::string header;need(bool(f>>header)&&header=="C029_PAIR_V1","TREE_HEADER");Count st;visit(f,s,anc,boxes[i],boxes[k],0,st);std::string extra;need(!(f>>extra),"TREE_EXTRA");need(st.nodes==2*st.split+1&&st.split+1==st.overlap+st.wall+st.point+st.anchor,"TREE_COMPLETENESS");std::ostringstream o;o<<"{\"schema\":\"n17.c029.pair-proof.v1\",\"pair\":["<<i<<','<<k<<"],\"nodes\":"<<st.nodes<<",\"split\":"<<st.split<<",\"overlap\":"<<st.overlap<<",\"wall\":"<<st.wall<<",\"grid\":"<<st.point<<",\"anchor\":"<<st.anchor<<",\"max_depth\":"<<st.depth<<",\"cap\":"<<quoted(qs(s.T))<<",\"status\":\"PASS_CONTINUOUS_PAIR_EXCLUSION\"}";write_new(argv[6],o.str());std::cout<<"PASS pair="<<pair<<" nodes="<<st.nodes<<'\n';return 0;}catch(const std::exception&e){std::cerr<<"REJECT "<<e.what()<<'\n';return 1;}}

#endif
