#pragma once
#define BOOST_BIND_GLOBAL_PLACEHOLDERS
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/rational.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <algorithm>
#include <array>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using Z=boost::multiprecision::cpp_int;
using Q=boost::rational<Z>;
using J=boost::property_tree::ptree;
inline void need(bool b,const std::string&s){if(!b)throw std::runtime_error(s);}
inline Z zi(const std::string&s){need(!s.empty()&&s.size()<10000,"BAD_INTEGER");size_t i=s[0]=='-'?1:0;need(i<s.size(),"BAD_INTEGER");Z x=0;for(;i<s.size();i++){need(s[i]>='0'&&s[i]<='9',"BAD_INTEGER");x=x*10+(s[i]-'0');}return s[0]=='-'?-x:x;}
inline Q qr(const std::string&s){auto p=s.find('/');need(p!=std::string::npos&&s.find('/',p+1)==std::string::npos,"BAD_RATIONAL");Z d=zi(s.substr(p+1));need(d>0,"POSITIVE_DENOMINATOR");return Q(zi(s.substr(0,p)),d);}
inline Q getq(const J&j,const std::string&s){return qr(j.get<std::string>(s));}
inline std::string qs(const Q&q){return q.numerator().str()+"/"+q.denominator().str();}
inline Q qa(const Q&q){return q<Q(0)?-q:q;}
inline Q qmin(const Q&a,const Q&b){return a<b?a:b;}
inline Q qmax(const Q&a,const Q&b){return a<b?b:a;}
inline void unique_json(const J&j){std::set<std::string>ks;bool object=false,array=false;for(const auto&kv:j){if(kv.first.empty())array=true;else{object=true;need(ks.insert(kv.first).second,"DUPLICATE_JSON_KEY");}unique_json(kv.second);}need(!(object&&array),"MIXED_JSON_NODE");}
inline J readj(const std::string&p){std::ifstream f(p);need(bool(f),"INPUT_OPEN");J j;boost::property_tree::read_json(f,j);unique_json(j);return j;}
inline void write_new(const std::string&p,const std::string&s){need(!std::filesystem::exists(p),"FRESH_OUTPUT_REQUIRED");std::ofstream f(p);need(bool(f),"OUTPUT_OPEN");f<<s<<'\n';need(bool(f),"OUTPUT_WRITE");}
inline std::string quoted(const std::string&s){std::ostringstream o;o<<std::quoted(s);return o.str();}
inline std::vector<J> ja(const J&j){std::vector<J>a;for(const auto&kv:j){need(kv.first.empty(),"ARRAY_EXPECTED");a.push_back(kv.second);}return a;}
struct V{Q x,y;};
inline V operator+(const V&a,const V&b){return {a.x+b.x,a.y+b.y};}
inline V operator-(const V&a,const V&b){return {a.x-b.x,a.y-b.y};}
inline V operator*(const Q&a,const V&b){return {a*b.x,a*b.y};}
inline Q dot(const V&a,const V&b){return a.x*b.x+a.y*b.y;}
inline Q cross(const V&a,const V&b){return a.x*b.y-a.y*b.x;}
inline V frame(const Q&t){Q d=Q(1)+t*t;return {(Q(1)-t*t)/d,Q(2)*t/d};}
inline V perp(const V&u){return {-u.y,u.x};}
struct Pose{V c;Q t;};
inline Pose pose(const J&j){return {{getq(j,"cx"),getq(j,"cy")},getq(j,"t")};}
inline Q point_margin(const Pose&p,const Q&A,const V&z){V d=z-p.c,u=frame(p.t);return A/Q(2)-qmax(qa(dot(u,d)),qa(dot(perp(u),d)));}
inline std::vector<V> vertices(const Pose&p,const Q&A){V u=frame(p.t),v=perp(u);std::vector<V>o;for(auto ab:std::array<std::array<int,2>,4>{{{{-1,-1}},{{1,-1}},{{1,1}},{{-1,1}}}})o.push_back(p.c+(A/Q(2))*(Q(ab[0])*u+Q(ab[1])*v));return o;}
inline Q radius(const Pose&p,const Q&A,const V&n){V u=frame(p.t);return A*(qa(dot(n,u))+qa(dot(n,perp(u))))/Q(2);}
inline bool disjoint(const Pose&a,const Q&A,const Pose&b,const Q&B){for(V n:std::array<V,4>{{frame(a.t),perp(frame(a.t)),frame(b.t),perp(frame(b.t))}})if(qa(dot(n,a.c-b.c))>=radius(a,A,n)+radius(b,B,n))return true;return false;}
inline bool fits(const Pose&p,const Q&A,const Q&L){for(const auto&v:vertices(p,A))if(v.x<Q(0)||L<v.x||v.y<Q(0)||L<v.y)return false;return true;}
