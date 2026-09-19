"""Exact bounded-centre sweep / 精确受限中心扫描.

Adapted from the M12 centre-rectangle reduction (source hash in provenance).
Two accumulation backends SHARE this geometric reduction. No independent
geometric proof is claimed. All proof decisions use Fraction/integer arithmetic.
"""
from __future__ import annotations
from fractions import Fraction as Q
from bisect import bisect_left, bisect_right
from collections import defaultdict
from math import lcm

class GeometryError(ValueError):
    pass

def need(ok: bool, message: str) -> None:
    if not ok:
        raise GeometryError(message)

def trig(t: Q) -> tuple[Q, Q]:
    need(isinstance(t,Q) and 0 <= t < 1, 'half tangent must be rational in [0,1)')
    return (1-t*t)/(1+t*t), 2*t/(1+t*t)

class Tree:
    def __init__(self,n: int):
        need(n>0,'empty cells'); self.n=n; self.v=[0]*(4*n); self.z=[0]*(4*n)
    def add(self,a:int,b:int,w:int):
        need(0<=a<=b<=self.n,'invalid update range')
        def visit(i,lo,hi):
            if a<=lo and hi<=b:
                self.v[i]+=w; self.z[i]+=w; return
            mid=(lo+hi)//2
            if a<mid: visit(2*i,lo,mid)
            if b>mid: visit(2*i+1,mid,hi)
            self.v[i]=self.z[i]+min(self.v[2*i],self.v[2*i+1])
        if a<b: visit(1,0,self.n)
    def query(self,a:int,b:int):
        need(0<=a<b<=self.n,'invalid query range')
        def visit(i,lo,hi,carry):
            if a<=lo and hi<=b: return self.v[i]+carry
            carry+=self.z[i]; mid=(lo+hi)//2; vals=[]
            if a<mid: vals.append(visit(2*i,lo,mid,carry))
            if b>mid: vals.append(visit(2*i+1,mid,hi,carry))
            return min(vals)
        return visit(1,0,self.n,0)
    def first(self,a,b,value):
        # Bisection using exact range minima; called only for a new minimum.
        while b-a>1:
            m=(a+b)//2
            if self.query(a,m)==value: b=m
            else: a=m
        need(self.query(a,b)==value,'argmin disagreement')
        return a

class Direct:
    def __init__(self,n): self.v=[0]*n
    def add(self,a,b,w):
        for k in range(a,b): self.v[k]+=w
    def query(self,a,b): return min(self.v[a:b])
    def first(self,a,b,value):
        return next(i for i in range(a,b) if self.v[i]==value)

def clip(poly,axis,bound,lower):
    inside=lambda p: p[axis]>=bound if lower else p[axis]<=bound
    out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        ip,iq=inside(p),inside(q)
        if ip: out.append(p)
        if ip!=iq:
            a=(bound-p[axis])/(q[axis]-p[axis])
            out.append(tuple(p[k]+a*(q[k]-p[k]) for k in (0,1)))
    return out

def cell_point(poly,cell):
    ua,ub,va,vb=cell
    for axis,bound,lower in ((0,ua,True),(0,ub,False),(1,va,True),(1,vb,False)):
        poly=clip(poly,axis,bound,lower); need(bool(poly),'empty cell')
    poly=list(dict.fromkeys(poly))
    area=sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(poly,poly[1:]+poly[:1]))
    need(area!=0,'zero-area cell')
    p=tuple(sum(v[k] for v in poly)/len(poly) for k in (0,1))
    need(ua<p[0]<ub and va<p[1]<vb,'witness not in open cell')
    return p

def direct_mass(atoms, B:Q, t:Q, xy):
    c,s=trig(t); x,y=xy
    ids=[i for i,(a,b,w) in enumerate(atoms)
         if abs(c*(a-x)+s*(b-y))<=B/2 and abs(-s*(a-x)+c*(b-y))<=B/2]
    return sum((atoms[i][2] for i in ids),Q()),ids

def coverage(L:Q,B:Q,atoms,t:Q,inset:Q|None=None,backend='tree'):
    c,s=trig(t)
    need(L>0 and B>0 and isinstance(L,Q) and isinstance(B,Q),'positive rational sizes required')
    need(bool(atoms),'empty atom set')
    need(all(isinstance(a,Q) and isinstance(b,Q) and isinstance(w,Q) and 0<=a<=L and 0<=b<=L and w>=0 for a,b,w in atoms),'bad atom or negative mass')
    r=B*(c+s)/2 if inset is None else inset
    need(isinstance(r,Q) and B*(c+s)/2<=r<L/2,'unsupported/noncontained or degenerate centre domain')
    poly=[(c*x+s*y,-s*x+c*y) for x,y in ((r,r),(L-r,r),(L-r,L-r),(r,L-r))]
    rotated=[(c*x+s*y,-s*x+c*y,w) for x,y,w in atoms]
    scale=lcm(*(w.denominator for _,_,w in atoms))
    rect=[(u-B/2,u+B/2,v-B/2,v+B/2,int(w*scale)) for u,v,w in rotated]
    vs=sorted({v for _,_,a,b,_ in rect for v in (a,b)}|{v for _,v in poly})
    vi={v:i for i,v in enumerate(vs)}; events=defaultdict(list)
    for a,b,lo,hi,w in rect:
        events[a].append((vi[lo],vi[hi],w)); events[b].append((vi[lo],vi[hi],-w))
    for u,_ in poly: events[u]
    us=sorted(events); umin=min(u for u,_ in poly); umax=max(u for u,_ in poly)
    need(backend in ('tree','direct'),'unknown backend')
    accum=Tree(len(vs)-1) if backend=='tree' else Direct(len(vs)-1)
    best=None; cell=None; slabs=0
    lower=lambda u:max((c*u-(L-r))/s,(r-s*u)/c)
    upper=lambda u:min((c*u-r)/s,((L-r)-s*u)/c)
    for a,b in zip(us,us[1:]):
        for lo,hi,w in events[a]: accum.add(lo,hi,w)
        if b<=umin: continue
        if a>=umax: break
        need(umin<=a<b<=umax,'missing polygon event')
        lo,hi=(r,L-r) if s==0 else (min(lower(a),lower(b)),max(upper(a),upper(b)))
        need(lo<hi,'bad projection')
        first=max(0,bisect_right(vs,lo)-1);stop=min(len(vs)-1,bisect_left(vs,hi))
        need(first<stop,'empty reachable interval')
        val=accum.query(first,stop);slabs+=1
        if best is None or val<best:
            best=val;k=accum.first(first,stop,val);cell=(a,b,vs[k],vs[k+1])
    need(best is not None and cell is not None,'no full-dimensional cells')
    u,v=cell_point(poly,cell);xy=(c*u-s*v,s*u+c*v)
    mass,ids=direct_mass(atoms,B,t,xy)
    need(mass==Q(best,scale),'independent membership recount mismatch')
    need(all(r<x<L-r for x in xy),'invalid witness centre')
    return {'t':str(t),'core_side':str(B),'centre_inset':str(r),'minimum':str(mass),'centre_xy':list(map(str,xy)),'captured_indices':ids,'cell_uv':list(map(str,cell)),'slabs':slabs,'backend':backend,'direct_recount':True}
