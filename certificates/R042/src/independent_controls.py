"""Independent exact controls for the movable-support square certificate.
No project verifier imports; no floating point; stdlib only.
Universal core containment is reduced to rational quadratic minimization.
Boundary samples are evaluated from logical membership, not sweep rectangles.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import lcm
from itertools import product, combinations
import argparse, hashlib, json, random, time


def qminimum(poly,a,b):
    p0,p1,p2=poly
    def ev(u): return p0+p1*u+p2*u*u
    sites=[a,b]
    if p2>0:
        v=-p1/(2*p2)
        if a<v<b:sites.append(v)
    return min(map(ev,sites))


def rotate(p,L):return (L-p[1],p[0])
def orbit(p,L):
    out=set()
    for z in (p,(p[1],p[0])):
        for _ in range(4):out.add(z);z=rotate(z,L)
    return sorted(out)

def expand(c):
    D=c['coordinate_denominator']; L=Q(c['L']); Z=int(L*D)
    assert L*D==Z and D>0
    sites=[]; weights=[]
    for x,y,w in c['point_orbits']:
        assert all(type(a) is int for a in (x,y,w)) and w>=0
        oo=orbit((x,y),Z);sites.extend(oo);weights.extend([w]*len(oo))
    assert len(sites)==len(set(sites))
    indices={p:i for i,p in enumerate(sites)}
    triples=[]
    for atom in c['threshold_orbits']:
        tri=atom['triples'][0];expected=set()
        for refl in (False,True):
            shape=[sites[i] for i in tri]
            if refl:shape=[(y,x) for x,y in shape]
            for _ in range(4):
                expected.add(tuple(sorted(indices[p] for p in shape)))
                shape=[rotate(p,Z) for p in shape]
        assert expected==set(map(tuple,atom['triples']))
        assert len(expected)==len(atom['triples'])
        for t in atom['triples']:
            assert len(set(t))==3
            triples.append((tuple(t),atom['weight']))
    assert sum(weights)+sum(w for _,w in triples)==c['budget_units']
    return sites,weights,triples,D


def containment(c):
    A=Q(c['A']); L=Q(c['L']); minima=[];cursor=Q(0)
    for row in c['entries']:
        a,b,t,B=map(Q,row); assert a==cursor and a<b;cursor=b
        # Numerators of cos(theta(u)-theta(t)) and sin(...),
        # with positive common denominator (1+t^2)(1+u^2).
        cr=(1-t*t,4*t,-(1-t*t));sr=(-2*t,2*(1-t*t),2*t)
        for e,f in product((-1,1),repeat=2):
            poly=[-B*(e*cr[i]+f*sr[i]) for i in range(3)]
            poly[0]+=A*(1+t*t);poly[2]+=A*(1+t*t)
            minimum=qminimum(poly,a,b); assert minimum>0
            minima.append(minimum)
        width=lambda u:(1+2*u-u*u)/(1+u*u)
        r=A*min(width(a),width(b))/2
        assert qminimum((A-2*r,2*A,-A-2*r),a,b)>=0
        assert 0<r<L/2 and B*width(t)/2<=r
    assert cursor>0 and cursor*cursor+2*cursor>1
    return {'intervals':len(c['entries']),'quadratic_inequalities':4*len(c['entries']),
            'minimum_positive_quadratic_numerator':str(min(minima))}


def samples(c,sites,weights,triples,D):
    L=Q(c['L']); A=Q(c['A']);rng=random.Random(172029)
    selected=sorted(set([0,1,2,19,500,1500,3000,4500,6000,len(c['entries'])-2,len(c['entries'])-1]))
    result=[]; all_min=None
    for rowidx in selected:
        a,b,t,B=map(Q,c['entries'][rowidx]);ct=(1-t*t)/(1+t*t);st=2*t/(1+t*t)
        width=lambda u:(1+2*u-u*u)/(1+u*u)
        H=L/2-A*min(width(a),width(b))/2
        # Integer conversion performed only after independent Fraction rotations.
        half=B/2
        uv=[(ct*(Q(x,D)-L/2)+st*(Q(y,D)-L/2),-st*(Q(x,D)-L/2)+ct*(Q(y,D)-L/2)) for x,y in sites]
        scale=lcm(half.denominator,H.denominator,ct.denominator,st.denominator,*(z.denominator for p in uv for z in p))
        uvint=[(int(u*scale),int(v*scale)) for u,v in uv]; hh=int(half*scale)
        def legal(u,v):return abs(ct*u-st*v)<=H*scale and abs(st*u+ct*v)<=H*scale
        positive=[i for i,w in enumerate(weights) if w]
        trigger_sites=sorted({i for tri,_ in triples for i in tri})
        active=sorted(set(positive+trigger_sites))
        # Four domain corners and boundary midpoints, exact in physical coordinates.
        centres={((ct*x+st*y)*scale,(-st*x+ct*y)*scale) for x,y in product((-H,Q(0),H),repeat=2)}
        # Exact crossings of point-capture event lines, including events from
        # zero-point-weight threshold sites. Keep 40 legal crossings per row.
        events=set()
        attempts=0
        while len(events)<40 and attempts<30000:
            attempts+=1;i=rng.choice(active);j=rng.choice(active)
            u=Q(uvint[i][0]+rng.choice((-hh,hh)));v=Q(uvint[j][1]+rng.choice((-hh,hh)))
            if legal(u,v):events.add((u,v))
        centres.update(events)
        # Pair/triple rectangle corners independently create threshold coincidences.
        for tri,_ in triples[:24]:
            for subset in combinations(tri,2):
                xl=max(uvint[i][0] for i in subset)-hh;xh=min(uvint[i][0] for i in subset)+hh
                yl=max(uvint[i][1] for i in subset)-hh;yh=min(uvint[i][1] for i in subset)+hh
                if xl<=xh and yl<=yh:
                    for u,v in product((xl,xh),(yl,yh)):
                        if legal(u,v):centres.add((Q(u),Q(v)))
        mn=None;boundaryhits=0;signedchecks=0
        for u,v in centres:
            assert legal(u,v)
            inside={i for i in active if abs(u-uvint[i][0])<=hh and abs(v-uvint[i][1])<=hh}
            charge=sum(weights[i] for i in inside)
            for tri,w in triples:
                bits=[i in inside for i in tri]; logical=int(sum(bits)>=2)
                signed=bits[0]*bits[1]+bits[0]*bits[2]+bits[1]*bits[2]-2*bits[0]*bits[1]*bits[2]
                assert logical==signed;signedchecks+=1;charge+=w*logical
            assert charge>=c['minimum_units'],(rowidx,str(u),str(v),charge)
            mn=charge if mn is None else min(mn,charge)
            boundaryhits+=sum(abs(u-uvint[i][0])==hh or abs(v-uvint[i][1])==hh for i in active)
        all_min=mn if all_min is None else min(all_min,mn)
        result.append({'row':rowidx,'centres':len(centres),'minimum_charge':mn,'capture_boundary_hits':boundaryhits,'logical_signed_checks':signedchecks})
    return {'rows':result,'total_centres':sum(x['centres'] for x in result),'minimum_sampled_charge':all_min}


def main():
    p=argparse.ArgumentParser();p.add_argument('certificate');p.add_argument('--output',required=True);p.add_argument('--containment-only',action='store_true');a=p.parse_args();start=time.monotonic()
    raw=Path(a.certificate).read_bytes();c=json.loads(raw);sites,weights,triples,D=expand(c)
    result={'status':'PASS_INDEPENDENT_EXACT_CONTROLS','certificate_sha256':hashlib.sha256(raw).hexdigest(),'scope':'Universal rational quadratic containment plus selected direct logical boundary charges; not a replacement for all-centre sweep.'}
    result['containment']=containment(c)
    if not a.containment_only:result['boundary_samples']=samples(c,sites,weights,triples,D)
    result['seconds']=time.monotonic()-start
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
