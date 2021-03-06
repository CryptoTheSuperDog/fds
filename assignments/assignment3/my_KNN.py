import pandas as pd
import numpy as np
from collections import Counter

class my_KNN:

    def __init__(self, n_neighbors=5, metric="cosine", p=2):
        # metric = {"minkowski", "euclidean", "manhattan", "cosine"}
        # p value only matters when metric = "minkowski"
        # notice that for "cosine", 1 is closest and -1 is furthest
        # therefore usually cosine_dist = 1- cosine(x,y)
        self.n_neighbors = int(n_neighbors)
        self.metric = metric
        self.p = p

    def fit(self, X, y):
        # X: pd.DataFrame, independent variables, float
        # y: list, np.array or pd.Series, dependent variables, int or str
        self.classes_ = list(set(list(y)))
        self.X = X
        self.y = y
        return

    def dist(self,x):
        # Calculate distances of training data to a single input data point (distances from self.X to x)
        # Output np.array([distances to x])
        if self.metric == "minkowski":
        #(add all of them up -->(self.Xi - x)^p)^(1/p), p=1 manhattan, p=2 euclidean
            distances = []
            for idx, row in self.X.iterrows():
                dist = 0
                for i in range(len(row)):
                    xi = row[i]
                    yi = x[i]
                    dist += (abs(xi-yi))**self.p
                dist = dist**(1/self.p)
                distances.append(dist)


        elif self.metric == "euclidean":
            distances = []
            for idx, row in self.X.iterrows():
                dist = 0
                x_ = 0
                y_ = 0
                p = 2
                for i in range(len(row)):
                    xi = row[i]
                    yi = x[i]
                    dist += (abs(xi-yi))**p
                dist = dist ** (1/p)
                distances.append(dist)


        elif self.metric == "manhattan":
            distances = []
            for idx, row in self.X.iterrows():
                dist = 0
                p = 1
                for i in range(len(row)):
                    xi = row[i]
                    yi = x[i]
                    dist += ((abs(xi - yi))**p)**(1/p)
                distances.append(dist)


        elif self.metric == "cosine":
            distances = []
            for idx, row in self.X.iterrows():
                dist = 0
                x_ = 0
                y_ = 0
                for i in range(len(row)):
                    xi = row[i]
                    yi = x[i]
                    dist += (xi * yi) 
                    x_ = (xi ** 2)
                    y_ = (yi ** 2)
                x_ = x_**(1/2)
                y_ = y_**(1/2)
                xy = x_ * y_ 
                dist = (dist/xy)
                dist = 1 - dist
                distances.append(dist)

        else:
            raise Exception("Unknown criterion.")
        return distances

    def k_neighbors(self,x):
        # Return the stats of the labels of k nearest neighbors to a single input data point (np.array)
        # Output: Counter(labels of the self.n_neighbors nearest neighbors) e.g. {"Class A":3, "Class B":2}
        distances = self.dist(x)
        output = []
        for i in range(self.n_neighbors):
            mindex = distances.index(min(distances))
            minval = distances[mindex]
            output.append(self.y[mindex])
            distances.pop(mindex)
        output = Counter(output)
        return output

    def predict(self, X):
        # X: pd.DataFrame, independent variables, float
        # return predictions: list
        probs = self.predict_proba(X)
        predictions = [self.classes_[np.argmax(prob)] for prob in probs.to_numpy()]
        return predictions

    def predict_proba(self, X):
        # X: pd.DataFrame, independent variables, float
        # prob is a dict of prediction probabilities belonging to each categories
        # return probs = pd.DataFrame(list of prob, columns = self.classes_)
        probs = []
        try:
            X_feature = X[self.X.columns]
        except:
            raise Exception("Input data mismatch.")

        for x in X_feature.to_numpy():
            neighbors = self.k_neighbors(x)
            # Calculate the probability of data point x belonging to each class
            # e.g. prob = {"2": 1/3, "1": 2/3}
            prob = {key: neighbors[key]/float(self.n_neighbors) for key in self.y}
            probs.append(prob)
        probs = pd.DataFrame(probs, columns=self.classes_)
        return probs
