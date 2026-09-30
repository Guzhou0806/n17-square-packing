#define C028_ATLAS_LIBRARY
#if defined(__GNUC__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "atlas.cpp"
#if defined(__GNUC__)
#pragma GCC diagnostic pop
#endif
int main(int argc,char**argv){try{need(argc==3,"USAGE_INPUT_FRESH_OUTPUT");need(!std::filesystem::exists(argv[2]),"FRESH_OUTPUT_REQUIRED");auto j=readj(argv[1]);need(j.get<std::string>("schema")=="n17.c028.angular-predicates.v1","SCHEMA");std::ostringstream o;o<<"{\"schema\":\"n17.c028.angular-predicate-result.v1\",\"cases\":[";bool first=true;for(auto&c:ja(j.get_child("cases"))){auto x=ja(c.get_child("dx")),y=ja(c.get_child("dy")),t=ja(c.get_child("t"));need(x.size()==2&&y.size()==2&&t.size()==2,"INTERVAL_SHAPE");Q x0=qr(x[0].data()),x1=qr(x[1].data()),y0=qr(y[0].data()),y1=qr(y[1].data()),t0=qr(t[0].data()),t1=qr(t[1].data()),b=getq(c,"bound");need(x0<=x1&&y0<=y1&&Q(0)<=t0&&t0<=t1&&t1<=Q(1)&&b>Q(0),"PREDICATE_DOMAIN");bool v=projections_below(x0,x1,y0,y1,t0,t1,b);need(v==c.get<bool>("expected"),"PREDICATE_EXPECTATION");if(!first)o<<',';first=false;o<<"{\"id\":"<<quoted(c.get<std::string>("id"))<<",\"all_strictly_below\":"<<(v?"true":"false")<<'}';}o<<"]}";write_new(argv[2],o.str());std::cout<<"PASS_ANGULAR_PREDICATES\n";return 0;}catch(const std::exception&e){std::cerr<<"REJECT "<<e.what()<<'\n';return 1;}}
