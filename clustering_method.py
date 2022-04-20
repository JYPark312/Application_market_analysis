# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 07:43:14 2021

@author: young
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering
from sklearn import decomposition
###k means

data=pd.read_excel('C:/Users/young/OneDrive/바탕 화면/논문 관련 자료/application clustering/end_data.xlsx')
cluster_data=data.drop(columns=['appname', 'price', 'k-means', 'agg', 'GMM', 'mini_batch_kmeans', 'category'])

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

elbow(cluster_data)

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

k= 4
km = KMeans(n_clusters=k, algorithm='auto', random_state=42)
y_km = km.fit_predict(cluster_data)
plotSilhouette(cluster_data, y_km)

#k-means
model = KMeans(n_clusters = 4, algorithm='auto')
model.fit(cluster_data)
predict = pd.DataFrame(model.predict(cluster_data))
predict.columns = ['predict']
label = model.fit(cluster_data).labels_
cluster_data['k-means']=label



#agg
agg = AgglomerativeClustering(n_clusters=4)
agg.fit(cluster_data)
assign = agg.fit_predict(cluster_data)
y_pred = agg.labels_
label = agg.fit(cluster_data).labels_

cluster_data['k-agg']=label



#GMM
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=4)
gmm.fit(cluster_data)
label = gmm.predict(cluster_data)

cluster_data['GMM']=label


#minibatch
from sklearn.cluster import MiniBatchKMeans
model = MiniBatchKMeans(n_clusters=4, batch_size=100)
model.fit(cluster_data)
label = model.fit(cluster_data).labels_

cluster_data['mini_batch_kmeans']=label

y_km = model.fit_predict(cluster_data)
plotSilhouette(cluster_data, y_km)

#SpectralClustering
from sklearn.cluster import SpectralClustering
model = SpectralClustering(n_clusters=4, assign_labels='discretize')
model.fit(cluster_data)
label = model.labels_
cluster_data['SpectralClustering'] = label

cluster_data.to_excel('clustering.xlsx')



