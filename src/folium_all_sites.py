import sys,json,warnings;warnings.filterwarnings('ignore')
import pandas as pd,numpy as np,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt,seaborn as sns,folium
from folium.plugins import MarkerCluster
d=sys.argv[1];I=d+'/img/'
sns.set_theme(style='whitegrid',context='talk')
P={0:'#d1495b',1:'#2e86ab'}
df=pd.read_csv(d+'/p2.csv');df['Landed']=df['Class'].map({1:'Landed',0:'Did not land'})
pal={'Landed':P[1],'Did not land':P[0]}
def save(n):plt.tight_layout();plt.savefig(I+n,dpi=150);plt.close()
def scat(x,y,n,xl,yl):
  plt.figure(figsize=(12,5.5));sns.stripplot(data=df,x=x,y=y,hue='Landed',palette=pal,size=9,jitter=0.15,orient='h' if df[y].dtype==object else None)
  plt.xlabel(xl);plt.ylabel(yl);plt.legend(title='',loc='lower center',bbox_to_anchor=(0.5,1.0),ncol=2,frameon=False);save(n)
scat('FlightNumber','LaunchSite','flight_site.png','Flight number','Launch site')
scat('PayloadMass','LaunchSite','payload_site.png','Payload mass (kg)','Launch site')
o=df.groupby('Orbit')['Class'].mean().sort_values(ascending=False)*100
plt.figure(figsize=(12,5.5));ax=sns.barplot(x=o.index,y=o.values,color=P[1]);ax.bar_label(ax.containers[0],fmt='%.0f%%',fontsize=12)
plt.ylabel('Landing success rate (%)');plt.xlabel('Orbit');plt.ylim(0,110);save('orbit_rate.png')
scat('FlightNumber','Orbit','flight_orbit.png','Flight number','Orbit')
scat('PayloadMass','Orbit','payload_orbit.png','Payload mass (kg)','Orbit')
y=df.assign(Year=df.Date.str[:4]).groupby('Year')['Class'].mean()*100
plt.figure(figsize=(12,5.5));plt.plot(y.index,y.values,marker='o',lw=3,color=P[1])
for a,b in y.items():plt.annotate(f'{b:.0f}%',(a,b),textcoords='offset points',xytext=(0,10),ha='center',fontsize=12)
plt.ylabel('Landing success rate (%)');plt.xlabel('Year');plt.ylim(-5,105);save('yearly.png')
# Dash charts
q=pd.read_csv(d+'/dash.csv')
s=q[q['class']==1]['Launch Site'].value_counts()
plt.figure(figsize=(7,6));plt.pie(s.values,labels=s.index,autopct='%1.1f%%',colors=['#2e86ab','#f18f01','#6a994e','#a23b72'],textprops={'fontsize':13});plt.title('Share of successful launches by site');save('dash_pie_all.png')
k=q[q['Launch Site']=='KSC LC-39A']['class'].value_counts().sort_index()
plt.figure(figsize=(7,6));plt.pie(k.values,labels=['Failure (0)','Success (1)'],autopct='%1.1f%%',colors=[P[0],P[1]],textprops={'fontsize':14});plt.title('KSC LC-39A: success vs failure');save('dash_pie_ksc.png')
plt.figure(figsize=(12,5.5));sns.scatterplot(data=q,x='Payload Mass (kg)',y='class',hue='Booster Version Category',s=140,alpha=.8)
plt.yticks([0,1],['Failure','Success']);plt.ylabel('');plt.legend(title='Booster',loc='center right');save('dash_scatter.png')
# ML
m=json.load(open(d+'/ml.json'))
plt.figure(figsize=(11,5.5));n=list(m);x=np.arange(4)
b1=plt.bar(x-.2,[m[i]['cv']*100 for i in n],.4,label='Best CV score',color='#9fc5e8');b2=plt.bar(x+.2,[m[i]['test']*100 for i in n],.4,label='Test accuracy',color=P[1])
plt.bar_label(b1,fmt='%.1f',fontsize=12);plt.bar_label(b2,fmt='%.1f',fontsize=12);plt.xticks(x,n);plt.ylim(0,100);plt.ylabel('%');plt.legend(loc='lower right');save('ml_acc.png')
plt.figure(figsize=(7,5.5));sns.heatmap(np.array(m['Logistic Regression']['cm']),annot=True,fmt='d',cmap='Blues',cbar=False,annot_kws={'size':24},xticklabels=['did not land','landed'],yticklabels=['did not land','landed'])
plt.xlabel('Predicted');plt.ylabel('Actual');plt.title('Logistic Regression (test set, n=18)');save('cm.png')
# Folium
sites={'CCAFS LC-40':(28.562302,-80.577356),'CCAFS SLC-40':(28.563197,-80.576820),'KSC LC-39A':(28.573255,-80.646895),'VAFB SLC-4E':(34.632834,-120.610745)}
m1=folium.Map(location=[31,-100],zoom_start=5,width=1400,height=750)
for s_,c in sites.items():
  folium.Circle(c,radius=1000,color='#d35400',fill=True).add_to(m1)
  folium.Marker(c,icon=folium.DivIcon(html=f'<div style="font-size:16px;color:#d35400;font-weight:bold;white-space:nowrap">{s_}</div>')).add_to(m1)
m1.save(d+'/map_all.html')
m2=folium.Map(location=[28.567,-80.61],zoom_start=13,width=1400,height=750);mc=MarkerCluster(options={'disableClusteringAtZoom':12}).add_to(m2)
for _,r in q.iterrows():
  if r['Launch Site']=='VAFB SLC-4E':continue
  folium.Marker(sites[r['Launch Site']],icon=folium.Icon(color='white',icon_color='green' if r['class'] else 'red')).add_to(mc)
m2b=folium.Map(location=[28.567,-80.61],zoom_start=12,width=1400,height=750);mc2=MarkerCluster().add_to(m2b)
for _,r in q.iterrows():
  if r['Launch Site']=='VAFB SLC-4E':continue
  folium.Marker(sites[r['Launch Site']],icon=folium.Icon(color='white',icon_color='green' if r['class'] else 'red')).add_to(mc2)
m2b.save(d+'/map_cluster.html')
pr=json.load(open(d+'/prox.json'));o=sites['CCAFS SLC-40']
m3=folium.Map(location=[28.53,-80.66],zoom_start=11,width=1400,height=750)
folium.Marker(o,icon=folium.DivIcon(html='<div style="font-size:15px;font-weight:bold;color:#d35400">CCAFS SLC-40</div>')).add_to(m3)
lab={'coast':'Coastline','rail':'Railway','road':'Highway (NASA Pkwy E)','city:city':'Titusville'}
for k_,t in lab.items():
  dd,la,lo,_=pr[k_];folium.PolyLine([o,(la,lo)],weight=3,color='#1f4e79').add_to(m3)
  folium.Marker((la,lo),icon=folium.DivIcon(html=f'<div style="font-size:15px;font-weight:bold;color:#1f4e79;white-space:nowrap">{t}: {dd:.2f} km</div>')).add_to(m3)
m3.save(d+'/map_prox.html')
print('ok')
