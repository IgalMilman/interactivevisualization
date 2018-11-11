import baseoperationclass
from sklearn.cluster import KMeans
import pandas as pd

CLUST_NUM = 3

class KMeansClustering(baseoperationclass.BaseOperationClass):

    _operation_name = 'K-Means Clustering'

    def __init__(self):
        self.parameters = {}
        self.parameters['clust_number'] = CLUST_NUM

    def doKmeans(self, dataset, params):
        model = KMeans(params['clust_number'])
        model.fit(dataset)
        clust_labels = model.predict(dataset)
        cent = model.cluster_centers_
        return (clust_labels, cent)

    def process_data(self, dataset):
        clust_labels, cent = self.doKmeans(dataset, self.parameters['clust_number'])
        kmeans = pd.DataFrame(clust_labels)
        dataset['cluster'] = kmeans.values
        return True