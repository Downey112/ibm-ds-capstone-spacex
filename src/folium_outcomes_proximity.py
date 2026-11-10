import sys,json,math,pandas as pd,folium
d=sys.argv[1]
q=pd.read_csv(d+'/dash.csv')
sites={'CCAFS LC-40':(28.562302,-80.577356),'CCAFS SLC-40':(28.563197,-80.576820),'KSC LC-39A':(28.573255,-80.646895),'VAFB SLC-4E':(34.632834,-120.610745)}
def ring(site,zoom,fn,r=0.0012):
  c=sites[site];m=folium.Map(location=c,zoom_start=zoom,width=1400,height=750);rows=q[q['Launch Site']==site].reset_index()
  for i,x in rows.iterrows():
    a=2*math.pi*i/len(rows);p=(c[0]+r*math.sin(a),c[1]+r*math.cos(a)/0.88)
    folium.PolyLine([c,p],color='#555',weight=1).add_to(m)
    folium.Marker(p,icon=folium.Icon(color='green' if x['class'] else 'red',icon='ok-sign' if x['class'] else 'remove-sign')).add_to(m)
  folium.CircleMarker(c,radius=8,color='#d35400',fill=True).add_to(m)
  m.get_root().html.add_child(folium.Element(f'<div style="position:fixed;top:15px;left:60px;z-index:999;background:white;padding:10px 14px;font:bold 18px Arial;border:2px solid #333">{site}: {rows["class"].sum()} landed (green) / {(rows["class"]==0).sum()} not (red)</div>'))
  m.save(d+f'/{fn}.html')
ring('KSC LC-39A',17,'map_ksc',0.0011)
ring('CCAFS LC-40',16,'map_cca',0.0022)
pr=json.load(open(d+'/prox.json'));o=sites['CCAFS SLC-40']
m3=folium.Map(location=[28.55,-80.69],zoom_start=11,width=1400,height=750)
folium.CircleMarker(o,radius=8,color='#d35400',fill=True).add_to(m3)
for k,t,col in [('coast','Coastline','#0b6e4f'),('road','Highway','#7b2cbf'),('city:city','Titusville (city)','#1f4e79')]:
  dd,la,lo,_=pr[k];folium.PolyLine([o,(la,lo)],weight=4,color=col).add_to(m3);folium.CircleMarker((la,lo),radius=5,color=col,fill=True).add_to(m3)
L=f"""<div style="position:fixed;top:15px;right:15px;z-index:999;background:white;padding:12px 16px;font:16px Arial;border:2px solid #333;line-height:1.6">
<b>Distances from CCAFS SLC-40</b><br><span style="color:#0b6e4f">&#9632;</span> Coastline: {pr['coast'][0]:.2f} km<br>
<span style="color:#555">&#9632;</span> Railway (NASA rail line at pad): {pr['rail'][0]:.2f} km<br>
<span style="color:#7b2cbf">&#9632;</span> Highway (NASA Pkwy East): {pr['road'][0]:.2f} km<br>
<span style="color:#1f4e79">&#9632;</span> Nearest city (Titusville): {pr['city:city'][0]:.2f} km<br>
Nearest town (Cape Canaveral): {pr['city:town'][0]:.2f} km</div>"""
m3.get_root().html.add_child(folium.Element(L));m3.save(d+'/map_prox.html')
