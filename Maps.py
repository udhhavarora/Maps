
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


# In[3]:


get_ipython().system(u'pip install folium')


# #### Let's import the folium library to plot maps later

# In[4]:


import folium


# In[5]:


df=pd.read_csv('https://cocl.us/datascience_survey_data',index_col=0)


# In[6]:


df.head()


# In[7]:


dfsorted=df.sort_values(['Very interested'], ascending=False)
dfsorted.head()


# In[8]:


dfsorted['Very interested']=round((dfsorted['Very interested']/2233)*100,2)
dfsorted['Somewhat interested']=round((dfsorted['Somewhat interested']/2233)*100,2)
dfsorted['Not interested']=round((dfsorted['Not interested']/2233)*100,2)


# In[9]:


dfsorted


# In[10]:


colors_list=['#5cb85c','#5bc0de','#d9534f']
ax = (dfsorted.div(dfsorted.sum(1), axis=0)).plot(kind='bar',figsize=(20,8),width = 0.8,color = colors_list,edgecolor=None)
plt.legend(labels=dfsorted.columns,fontsize= 14)
plt.title("Percentage of Respondents' Interest in Data Science Areas",fontsize= 16)
plt.xticks(fontsize=14)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
plt.yticks([])

# Add this loop to add the annotations
for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    ax.annotate('{:.0%}'.format(height), (x, y + height + 0.01))


# In[15]:


df1=pd.read_csv('https://cocl.us/sanfran_crime_dataset')


# In[17]:


df1.drop(['Category','Descript','DayOfWeek','Date','Time','Resolution','Address','X','Y','Location','PdId'], axis=1, inplace=True)
df1.rename(columns={'IncidntNum':'Count', 'PdDistrict':'Neighborhood'}, inplace=True)
df1.columns=list(map(str,df1.columns))
df1.set_index('Neighborhood',inplace=True)
df1.sort_values('Count',ascending=False)
df1=df1.groupby('Neighborhood').count()
df1.reset_index(inplace=True)
df1


# In[18]:


df1.head()


# In[20]:


from folium import plugins
get_ipython().system(u'wget --quiet https://cocl.us/sanfran_geojson -O world_countries.json')


# In[23]:


world_geodata=  r'world_countries.json'
latitude = 37.77
longitude = -122.42 #lat long of San Francisco
world_map=folium.Map(location=[latitude,longitude], zoom_start=12)
world_map.choropleth(
    geo_data=world_geodata,
    data=df1,
    columns=['Neighborhood','Count'],
    key_on='feature.properties.DISTRICT',
    fill_color='YlOrRd',
    fill_opacity = 0.7,
    line_opacity=0.2,
    legend_name='San Francisco Crime Rate')


world_map



# In[28]:


world_geodata=  r'world_countries.json'
threshold_scale = np.linspace(df1['Count'].min(),
                              df1['Count'].max(),
                              6, dtype=int)
threshold_scale = threshold_scale.tolist()
threshold_scale[-1] = threshold_scale[-1] + 1
latitude = 37.77
longitude = -122.42 #lat long of San Francisco
world_map=folium.Map(location=[latitude,longitude], zoom_start=12)
world_map.choropleth(
    geo_data=world_geodata,
    data=df1,
    columns=['Neighborhood','Count'],
    key_on='feature.properties.DISTRICT',
    fill_color='YlOrRd',
    threshold_scale=threshold_scale,
    fill_opacity = 0.7,
    line_opacity=0.2,
    legend_name='San Francisco Crime Rate'
)


world_map



# In[29]:


world_map.save('map.html')

