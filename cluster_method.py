# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:29:16 2021

@author: young
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering
pip install tensorflow
from sklearn import decomposition
###k means
cluster_data.patch =cluster_data.patch.fillna(1)

data=cluster_data.values

# elbow 기법으로 cluster 객수 찾기
def elbow(X):
    sse =[]
    for i in range(1, 15):
        km = KMeans(n_clusters=i, algorithm='auto', random_state=42)
        km.fit(X)
        sse.append(km.inertia_)
    
    plt.plot(range(1,15), sse, marker = 'o')
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.show()

elbow(data)


#실루엣 기법

import numpy as np
from sklearn.metrics import silhouette_samples
from matplotlib import cm

def plotSilhouette(X, y_km):
    cluster_labels = np.unique(y_km)
    n_clusters = cluster_labels.shape[0]
    silhouette_vals = silhouette_samples(X, y_km, metric = 'euclidean')
    y_ax_lower, y_ax_upper = 0, 0
    yticks = []

    for i, c in enumerate(cluster_labels):
        c_silhouette_vals = silhouette_vals[y_km == c]
        c_silhouette_vals.sort()
        y_ax_upper += len(c_silhouette_vals)
        color = cm.jet(i/n_clusters)

        plt.barh(range(y_ax_lower, y_ax_upper), c_silhouette_vals, height=1.0,
                edgecolor='none', color=color)
        yticks.append((y_ax_lower + y_ax_upper)/2)
        y_ax_lower += len(c_silhouette_vals)

    silhoutte_avg = np.mean(silhouette_vals)
    plt.axvline(silhoutte_avg, color = 'red', linestyle='--')
    plt.yticks(yticks, cluster_labels+1)
    plt.ylabel('K')
    plt.xlabel('silhouette')
    plt.show()

k= 3
km = KMeans(n_clusters=k, algorithm='auto', random_state=42)
y_km = km.fit_predict(data)
plotSilhouette(data, y_km)


#클러스터링
k=7

model = KMeans(n_clusters = k, algorithm='auto')
model.fit(data)
predict = pd.DataFrame(model.predict(data))
predict.columns = ['predict']
label = model.fit(data).labels_


#데이터 합치기

final_df = pd.DataFrame(np.hstack((predict, data)))
cols = list(cluster_data.columns.values)
cols.insert(0, 'group')

final_df.columns = cols

#시각화
transformed = TSNE(n_components=2,learning_rate=300).fit_transform(data)
transformed.shape

xs = transformed[:,0]
ys = transformed[:,1]



plt.scatter(xs, ys, c=label, s=3, cmap='viridis')
plt.show()

##### 잘나옴
pca = decomposition.PCA(n_components=4).fit(data)
reduced_X = pca.transform(data)
print(pca.explained_variance_ratio_)

k=4
model = KMeans(init="k-means++", n_clusters=k, algorithm='auto', random_state=0)
model.fit(reduced_X)
y_pred = model.labels_

transformed = TSNE(n_components=2).fit_transform(data)

xs = transformed[:,0]
ys = transformed[:,1]

plt.scatter(xs, ys, c=y_pred, s=3, cmap='viridis')
plt.show()


df1 =pd.DataFrame(transformed)
df2=y_pred
df1['cluster']=df2



cluster0=df1[df1['cluster']== 0]
cluster1=df1[df1['cluster']== 1]
cluster2=df1[df1['cluster']== 2]
cluster3=df1[df1['cluster']== 3]


xs0 = cluster0.iloc[:,0]
xs1 = cluster1.iloc[:,0]
xs2 = cluster2.iloc[:,0]
xs3 = cluster3.iloc[:,0]


ys0 = cluster0.iloc[:,1]
ys1 = cluster1.iloc[:,1]
ys2 = cluster2.iloc[:,1]
ys3 = cluster3.iloc[:,1]

plt.scatter(xs0, ys0, c='gold', s=3, cmap='viridis')
plt.scatter(xs1, ys1, c='firebrick', s=3, cmap='viridis')
plt.scatter(xs2, ys2, c='forestgreen', s=3, cmap='viridis')
plt.scatter(xs3, ys3, c='crimson', s=3, cmap='viridis')
plt.legend(['cluster_0', 'cluster_1', 'cluster_2', 'cluster_3'])
plt.show()


km = KMeans(init="k-means++", n_clusters=k, algorithm='auto', random_state=0)
y_km = km.fit_predict(reduced_X)
plotSilhouette(reduced_X, y_km)


inform['cluster_nbr'] = y_pred
inform.to_excel("information_cluster4pca.xlsx")


###

agg = AgglomerativeClustering(n_clusters=4)
agg.fit(reduced_X)
assign = agg.fit_predict(reduced_X)
y_pred = agg.labels_


##합치기
a = assign.reshape(-1,1)
final_df = pd.DataFrame(np.hstack((a, data)))
cols = list(cluster_data.columns.values)
cols.insert(0, 'group')
final_df.columns = cols

transformed = TSNE(n_components=2).fit_transform(data)


plt.scatter(xs, ys, c=final_df['group'], s=2)
plt.style.use('ggplot')
plt.show()

pip install sklearn
from sklearn import mixture
model = mixture.GaussianMixture(n_components =6).fit(data)
labels = model.predict(data)

transformed = TSNE(n_components=2).fit_transform(data)
xs = transformed[:,0]
ys = transformed[:,1]

plt.scatter(xs, ys, c=y_pred, s=2, cmap='viridis')
plt.style.use('ggplot')
plt.show()


#차원 줄이기 후 클러스터링
from sklearn.cluster import DBSCAN

transformed = TSNE(n_components=2,learning_rate=300).fit_transform(data)

model = DBSCAN(eps = 0.2, min_samples=50, metric ='euclidean')
predict = model.fit(data)
y_pred = predict.labels_

dataset = pd.DataFrame({'Column1':transformed[:,0],'Column2':transformed[:,1]})
dataset['cluster_num'] = pd.Series(predict.labels_)

xs = transformed[:,0]
ys = transformed[:,1]


plt.scatter(xs, ys, c=y_pred, s=2, cmap='viridis')
plt.style.use('ggplot')
plt.show()
#하이러라키칼
