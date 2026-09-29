#pragma once
// C016 geometric rule overlay. Original certificate checker is retained unchanged.
#include "../../work/src/adaptive_library.cpp"
static std::string file_raw(const std::string&p){std::ifstream f(p,std::ios::binary);need(bool(f),"input unavailable");return std::string((std::istreambuf_iterator<char>(f)),{});}
static J json_raw(const std::string&s){J j;std::istringstream in(s);pt::read_json(in,j);no_duplicates(j);return j;}
static Z cross3(const Point&o,const Point&a,const Point&b){return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0]);}
static bool on_segment(const Point&a,const Point&b,const Point&p){return cross3(a,b,p)==0&&std::min(a[0],b[0])<=p[0]&&p[0]<=std::max(a[0],b[0])&&std::min(a[1],b[1])<=p[1]&&p[1]<=std::max(a[1],b[1]);}
static bool segments_meet(const Point&a,const Point&b,const Point&c,const Point&d){Z u=cross3(a,b,c),v=cross3(a,b,d),w=cross3(c,d,a),z=cross3(c,d,b);if((u==0&&on_segment(a,b,c))||(v==0&&on_segment(a,b,d))||(w==0&&on_segment(c,d,a))||(z==0&&on_segment(c,d,b)))return true;return u*v<0&&w*z<0;}
static std::vector<Point> convex_hull(std::vector<Point> v){std::sort(v.begin(),v.end());v.erase(std::unique(v.begin(),v.end()),v.end());if(v.size()<2)return v;std::vector<Point>a,b;for(auto&p:v){while(a.size()>1&&cross3(a[a.size()-2],a.back(),p)<=0)a.pop_back();a.push_back(p);}for(auto it=v.rbegin();it!=v.rend();++it){while(b.size()>1&&cross3(b[b.size()-2],b.back(),*it)<=0)b.pop_back();b.push_back(*it);}a.pop_back();b.pop_back();a.insert(a.end(),b.begin(),b.end());return a;}
static bool in_hull(const Point&p,const std::vector<Point>&h){need(!h.empty(),"empty hull");if(h.size()==1)return p==h[0];if(h.size()==2)return on_segment(h[0],h[1],p);for(size_t j=0;j<h.size();j++)if(cross3(h[j],h[(j+1)%h.size()],p)<0)return false;return true;}
static bool hulls_meet(const std::vector<Point>&a,const std::vector<Point>&b){for(auto&p:a)if(in_hull(p,b))return true;for(auto&p:b)if(in_hull(p,a))return true;for(size_t i=0;i<a.size();i++)for(size_t j=0;j<b.size();j++)if(segments_meet(a[i],a[(i+1)%a.size()],b[j],b[(j+1)%b.size()]))return true;return false;}
using Family=std::vector<std::vector<int>>;
static Family image_family(const Feature&g,const std::vector<int>*tr=nullptr){Family key;for(int mask:g.rules){std::vector<int> ids;for(size_t j=0;j<g.ids.size();j++)if(mask&(1<<j))ids.push_back(tr?(*tr)[g.ids[j]]:g.ids[j]);std::sort(ids.begin(),ids.end());key.push_back(ids);}std::sort(key.begin(),key.end());return key;}
struct OverlayAudit{int orbits=0,images=0,truth_states=0,strict_states=0,disjoint_geometric_pairs=0;};
static OverlayAudit apply_geometric_overlay(Certificate&c,const J&base,const J&overlay,const std::string&base_sha){
 need(overlay.get<std::string>("schema")=="n17.convex_hull_rule_overlay.v1","overlay schema");need(overlay.get<std::string>("base_model_sha256")==base_sha,"overlay base identity");
 auto groups=arr(base.get_child("threshold_orbits"));std::vector<int> starts;int n=0;for(auto&g:groups){starts.push_back(n);n+=arr(g.get_child("sets")).size();}need(n==int(c.features.size()),"feature mapping");
 std::map<Point,int> lookup;for(size_t i=0;i<c.physical.size();i++)lookup[c.physical[i]]=i;std::vector<std::vector<int>> ts;
 for(bool sw:{false,true})for(bool fx:{false,true})for(bool fy:{false,true}){std::vector<int> t;for(auto p:c.physical){if(sw)std::swap(p[0],p[1]);if(fx)p[0]=c.LD-p[0];if(fy)p[1]=c.LD-p[1];need(lookup.count(p),"symmetry point");t.push_back(lookup.at(p));}ts.push_back(t);}
 OverlayAudit audit;std::set<int> used;
 for(auto&up:arr(overlay.get_child("upgrades"))){int oi=up.get<int>("orbit");need(0<=oi&&oi<int(groups.size())&&used.insert(oi).second,"duplicate/out-of-range upgrade");auto ii=arr(up.get_child("winning_masks_by_image"));int sz=arr(groups[oi].get_child("sets")).size();need(ii.size()==size_t(sz),"image count");
  for(int im=0;im<sz;im++){auto&g=c.features[starts[oi]+im];I cap=g.rules.empty()?std::accumulate(g.co.begin(),g.co.end(),I(0))/g.threshold:1;need(cap==1,"only capacity-one primitive may be upgraded");auto old=g;g.rules.clear();std::set<int> masks;std::vector<std::vector<Point>> hulls;
   for(auto&z:arr(ii[im])){int v=small(zi(z));need(v>0&&v<(1<<g.ids.size())&&masks.insert(v).second,"invalid geometric winning mask");g.rules.push_back(v);std::vector<Point> pp;for(size_t k=0;k<g.ids.size();k++)if(v&(1<<k))pp.push_back(c.physical[g.ids[k]]);hulls.push_back(convex_hull(pp));}
   need(!g.rules.empty(),"empty winning family");
   for(size_t a=0;a<g.rules.size();a++)for(size_t b=a+1;b<g.rules.size();b++){need((g.rules[a]&g.rules[b])!=g.rules[a]&&(g.rules[a]&g.rules[b])!=g.rules[b],"nonminimal geometric family");need(hulls_meet(hulls[a],hulls[b]),"disjoint convex winning hulls");if(!(g.rules[a]&g.rules[b]))audit.disjoint_geometric_pairs++;}
   for(int v=0;v<(1<<g.ids.size());v++){bool a=fires(v,old.co,old.threshold,old.rules),b=fires(v,g.co,g.threshold,g.rules);need(!a||b,"old winning mask lost");audit.truth_states++;if(b&&!a)audit.strict_states++;}
   audit.images++;
  }
  // Check the entire image multiset, including multiplicities. This does not
  // presume that the representative's label order is symmetry-canonical.
  std::multiset<Family> expected;for(int im=0;im<sz;im++)expected.insert(image_family(c.features[starts[oi]+im]));for(auto&tr:ts){std::multiset<Family> actual;for(int im=0;im<sz;im++)actual.insert(image_family(c.features[starts[oi]+im],&tr));need(actual==expected,"geometric rule D4 invariance");}
  audit.orbits++;
 }
 c.model.terms.clear();Z mass=0;
 for(size_t i=0;i<c.pw.size();i++)if(c.pw[i]){c.model.terms.push_back({{int(i)},c.pw[i]});mass+=c.pw[i];}
 for(auto&g:c.features){if(!g.weight)continue;int N=1<<g.ids.size();std::vector<I>a(N);for(int v=0;v<N;v++)a[v]=fires(v,g.co,g.threshold,g.rules);for(size_t j=0;j<g.ids.size();j++)for(int v=0;v<N;v++)if(v&(1<<j))a[v]-=a[v^(1<<j)];for(int v=1;v<N;v++)if(a[v]){std::vector<int> ids;for(size_t j=0;j<g.ids.size();j++)if(v&(1<<j))ids.push_back(g.ids[j]);Z ww=Z(a[v])*g.weight;mass+=boost::multiprecision::abs(ww);need(mass<LIMIT,"geometric signed atom safety");c.model.terms.push_back({ids,small(ww)});}}
 return audit;
}
static std::vector<unsigned char> geometric_counts(const Certificate&c,const J&base,const Q&A,const Q&t,const V&p,bool closed=false){
 auto cs=trig(t);Q rad=A*(qa(cs[0])+qa(cs[1]))/Q(2);need(Q(0)<A&&rad<=p.x&&p.x<=c.L-rad&&rad<=p.y&&p.y<=c.L-rad,"illegal finite square");
 Z C=t.d*t.d-t.n*t.n,S=2*t.n*t.d,T=t.d*t.d+t.n*t.n,lim=A.n*T*c.D*p.x.d*p.y.d,fac=2*A.d;std::vector<bool> hit(c.physical.size());
 for(size_t i=0;i<hit.size();i++){Z dx=(c.physical[i][0]*p.x.d-p.x.n*c.D)*p.y.d,dy=(c.physical[i][1]*p.y.d-p.y.n*c.D)*p.x.d;Z u=boost::multiprecision::abs(C*dx+S*dy)*fac,v=boost::multiprecision::abs(-S*dx+C*dy)*fac;hit[i]=closed?(u<=lim&&v<=lim):(u<lim&&v<lim);}
 std::vector<unsigned char> counts;size_t fi=0,pi=0;
 for(auto&g:arr(base.get_child("threshold_orbits"))){int n=arr(g.get_child("sets")).size(),z=0;for(int j=0;j<n;j++){auto&f=c.features[fi++];int mask=0;for(size_t k=0;k<f.ids.size();k++)if(hit[f.ids[k]])mask|=1<<k;if(fires(mask,f.co,f.threshold,f.rules))z++;}need(z<=255,"count byte");counts.push_back(z);}
 for(auto&row:arr(base.get_child("point_orbits"))){auto vv=arr(row);Z x=zi(vv[0]),y=zi(vv[1]);std::set<Point> orb;for(bool sw:{false,true})for(bool fx:{false,true})for(bool fy:{false,true}){Z u=sw?y:x,v=sw?x:y;if(fx)u=c.LD-u;if(fy)v=c.LD-v;orb.insert({u,v});}int z=0;for(size_t j=0;j<orb.size();j++)if(hit[pi++])z++;counts.push_back(z);}
 need(pi==c.physical.size()&&fi==c.features.size(),"counts exhausted");return counts;
}
static I counts_fee(const J&base,const std::vector<unsigned char>&v){size_t i=0;Z f=0;for(auto&g:arr(base.get_child("threshold_orbits")))f+=Z(v[i++])*zi(g.get_child("weight"));for(auto&g:arr(base.get_child("point_orbits")))f+=Z(v[i++])*zi(arr(g)[2]);need(i==v.size(),"count length");return small(f);}
