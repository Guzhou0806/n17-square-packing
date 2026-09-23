"""Exact polygon-sweep checker for point and two-of-three threshold charges.
Threshold indicator = three pair-intersection indicators - twice triple.
"""
from fractions import Fraction as F
from pathlib import Path
from math import lcm
from bisect import bisect_left,bisect_right
import sys,json,time,hashlib
import numpy as np
from integer_sweep import accumulate,trig,need
ROOT=Path(__file__).resolve().parent

def expand(c):
 D=c.get('coordinate_denominator',100000);need(type(D) is int and D>0 and (F(c['L'])*D).denominator==1,'invalid coordinate scale');LD=int(F(c['L'])*D)
 points=[];weights=[];orbits=[]
 for x,y,w in c['point_orbits']:
  need(all(type(z) is int for z in (x,y,w)) and 0<=x<=LD and 0<=y<=LD and w>=0,'invalid point orbit')
  oo=sorted({(a,b) for u,v in [(x,y),(y,x)] for a in (u,LD-u) for b in (v,LD-v)})
  orbits.append(list(range(len(points),len(points)+len(oo))));points+=oo;weights.extend([w]*len(oo))
 need(len(set(points))==len(points),'duplicate point')
 lookup={p:i for i,p in enumerate(points)};triggers=[];tw=[]
 for entry in c['threshold_orbits']:
  group=entry['triples'];w=entry['weight'];need(type(w) is int and w>=0,'invalid trigger weight')
  for tri in group:need(len(tri)==3 and len(set(tri))==3 and all(type(i) is int and 0<=i<len(points) for i in tri),'invalid triple')
  expected=set()
  for swap in [False,True]:
   for sx in [False,True]:
    for sy in [False,True]:
     tri=[]
     for i in group[0]:
      x,y=points[i]
      if swap:x,y=y,x
      if sx:x=LD-x
      if sy:y=LD-y
      tri.append(lookup[(x,y)])
     expected.add(tuple(sorted(tri)))
  need(expected==set(tuple(tri) for tri in group) and len(expected)==len(group),'incomplete trigger orbit')
  triggers+=group;tw.extend([w]*len(group))
 budget=sum(weights)+sum(tw);absolute=sum(weights)+5*sum(tw)
 need(budget==c['budget_units'] and absolute<2**50,'budget/overflow')
 return points,weights,triggers,tw,D

def geometry(points,pw,triples,tw,D,t,B,H,meta=False):
 p,q=t.numerator,t.denominator;C=q*q-p*p;S=2*p*q;R=q*q+p*p
 LD=int(F(4613,1000)*D);scale=lcm(2*D,(B/2).denominator,H.denominator);factor=scale//(2*D)
 h=int(H*scale);half=int(B*scale/2)*R
 uv=[(C*(2*x-LD)*factor+S*(2*y-LD)*factor,-S*(2*x-LD)*factor+C*(2*y-LD)*factor) for x,y in points]
 rect={}
 def insert(indices,w):
  if not w:return
  xx=[uv[i][0] for i in indices];yy=[uv[i][1] for i in indices]
  z=(max(xx)-half,min(xx)+half,max(yy)-half,min(yy)+half)
  if z[0]<z[1] and z[2]<z[3]:rect[z]=rect.get(z,0)+w
 for i,w in enumerate(pw):insert([i],w)
 for (i,j,k),w in zip(triples,tw):
  insert([i,j],w);insert([i,k],w);insert([j,k],w);insert([i,j,k],-2*w)
 rect={r:w for r,w in rect.items() if w};rr=list(rect);ww=np.array(list(rect.values()),np.int64)
 poly=[(C*x+S*y,-S*x+C*y) for x,y in [(-h,-h),(h,-h),(h,h),(-h,h)]]
 xe=sorted({p[0] for p in poly}|{v for r in rr for v in r[:2]});ye=sorted({p[1] for p in poly}|{v for r in rr for v in r[2:]})
 xi={v:i for i,v in enumerate(xe)};yi={v:i for i,v in enumerate(ye)}
 ev=np.array(sorted([(xi[r[0]],i,1) for i,r in enumerate(rr)]+[(xi[r[1]],i,-1) for i,r in enumerate(rr)]),np.int64)
 yl=np.array([yi[r[2]] for r in rr],np.int64);yh=np.array([yi[r[3]] for r in rr],np.int64)
 first=np.full(len(xe)-1,-1,np.int64);last=first.copy();edges=[]
 for k,(u,v) in enumerate(poly):
  z,w=poly[(k+1)%4]
  if z==u:continue
  if z<u:u,v,z,w=z,w,u,v
  edges.append((u,z,w-v,v*(z-u)-u*(w-v),z-u))
 left=min(p[0] for p in poly);right=max(p[0] for p in poly)
 for k,(a,b) in enumerate(zip(xe,xe[1:])):
  if a<left or b>right:continue
  crossings=[]
  for u,z,m,n,d in edges:
   if u<=a and b<=z:crossings.extend([(m*a+n,d),(m*b+n,d)])
  need(len(crossings)==4,'polygon edge count');bn,bd=crossings[0];tn,td=bn,bd
  for n,d in crossings[1:]:
   if n*bd<bn*d:bn,bd=n,d
   if n*td>tn*d:tn,td=n,d
  first[k]=bisect_right(ye,bn//bd)-1;last[k]=bisect_left(ye,-((-tn)//td))
  need(0<=first[k]<last[k]<=len(ye)-1,'query range')
 arrays=(len(ye)-1,ev[:,0],ev[:,1],ev[:,2],yl,yh,ww,first,last)
 if meta:return arrays,dict(poly=poly,xe=xe,ye=ye,rect=rr,weights=list(map(int,ww)),C=C,S=S,R=R,scale=scale)
 return arrays

def validate(c):
 L=F(c['L']);A=F(c['A']);need(L==F(4613,1000) and 0<A<L,'wrong container/parent');den=c['weight_denominator'];need(type(den) is int and den>0,'denominator')
 data=expand(c);jobs=[];margins=[];cursor=F(0)
 for row in c['entries']:
  a,b,t,B=map(F,row);need(a==cursor and 0<=a<b<1 and 0<=t<1 and 0<B<A,'catalogue coverage')
  cc,ss=trig(t);f=[];g=[]
  for u in (a,b):
   c0,s0=trig(u);dot=cc*c0+ss*s0;cross=abs(cc*s0-ss*c0);need(dot>0 and dot>=cross,'angle range');f.append(c0+s0);g.append(dot+cross)
  margin=A-B*max(g);need(margin>0,'core not strict');margins.append(margin);r=A*min(f)/2
  need(B*(cc+ss)/2<=r<L/2,'parent envelope');jobs.append((t,B,L/2-r));cursor=b
 need(cursor*cursor+2*cursor>1,'angle gap');need(17*c['minimum_units']>c['budget_units'],'counting budget')
 return data,jobs,min(margins)

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--output',required=True);ap.add_argument('--direct',action='store_true');args=ap.parse_args()
 raw=Path(args.certificate).read_bytes();c=json.loads(raw);data,jobs,margin=validate(c);rows=[];start=time.monotonic()
 for k,job in enumerate(jobs):
  arrays=geometry(*data,*job);m,cells,win=accumulate(*arrays,direct=args.direct)
  need(m>=c['minimum_units'],'coverage fails at '+str(k));rows.append({'row':k,'minimum_units':int(m),'cells':int(cells),'slabs':int(np.count_nonzero(arrays[-2]>=0))})
  if k%100==0:print(k,int(m),round(time.monotonic()-start,1),flush=True)
 from collections import Counter
 result={'status':'PASS_EXACT_MOVABLE_SUPPORT_CERTIFICATE','certificate_sha256':hashlib.sha256(raw).hexdigest(),'bound':str(F(c['L'])/F(c['A'])),'intervals':len(rows),'minimum_units':min(r['minimum_units'] for r in rows),'budget_units':c['budget_units'],'minimum_margin':str(margin),'histogram':dict(Counter(r['minimum_units'] for r in rows)),'slabs':sum(r['slabs'] for r in rows),'cells':sum(r['cells'] for r in rows),'seconds':time.monotonic()-start,'rows':rows}
 Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
