import requests,math,json
lat,lon=28.563197,-80.576820
q=f"""[out:json][timeout:60];(way(around:5000,{lat},{lon})["natural"="coastline"];way(around:8000,{lat},{lon})["railway"="rail"][!"service"];way(around:8000,{lat},{lon})["highway"~"^(motorway|trunk|primary|secondary|tertiary)$"];node(around:60000,{lat},{lon})["place"="city"];node(around:30000,{lat},{lon})["place"="town"];);out geom tags;"""
resp=requests.post('https://overpass.kumi.systems/api/interpreter',data={'data':q},headers={'User-Agent':'capstone-script'},timeout=120);print(resp.status_code,resp.text[:200]);r=resp.json()
def hv(a,b,c,d):
  R=6373.0;p=math.radians;dl=p(c-a);dn=p(d-b);x=math.sin(dl/2)**2+math.cos(p(a))*math.cos(p(c))*math.sin(dn/2)**2;return R*2*math.atan2(math.sqrt(x),math.sqrt(1-x))
best={}
for e in r['elements']:
  t=e.get('tags',{});k='coast' if t.get('natural') else 'rail' if 'railway' in t else 'road' if 'highway' in t else 'city:'+t.get('place')
  pts=e.get('geometry') or [{'lat':e['lat'],'lon':e['lon']}]
  for p in pts:
    dd=hv(lat,lon,p['lat'],p['lon'])
    if k not in best or dd<best[k][0]: best[k]=(round(dd,2),p['lat'],p['lon'],t.get('name',''))
print(json.dumps(best,indent=1));json.dump(best,open('build/prox.json','w'))
