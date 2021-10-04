from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import BaseEstimator
from sklearn.svm import LinearSVR
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV

from math import fabs
import numpy as np
import pandas as pd

class Cobra(BaseEstimator):

    def __init__(self, eps=None):
        self.eps = eps
        self.machines = {}
        self.machine_list = ['lasso', 'tree', 'ridge', 'random_forest', 'svm']
        self.alpha = len(self.machine_list)


    def __split_train_data(self, X, y, split_ratio):
        k = int(split_ratio*len(X))
        l = len(X) - k

        X_k = X[:k]
        y_k = y[:k]
        X_l = X[k+1:]
        y_l = y[k+1:]

        return X_k, y_k, X_l, y_l


    def fit(self, X, y, train_split_ratio=0.5):

        self.X = X
        self.y = y

        X_k, y_k, X_l, y_l = self.__split_train_data(self.X, self.y, train_split_ratio)

        self.X_l = X_l
        self.y_l = y_l
        
        random_state = np.random.randint(0, 100)

        # Training all the regressors.
        for machine in self.machine_list:
            try:
                if machine == 'lasso':
                    self.machines['lasso'] = linear_model.LassoCV(random_state=random_state).fit(X_k, y_k)
                if machine == 'tree':
                    self.machines['tree'] = DecisionTreeRegressor(random_state=random_state).fit(X_k, y_k)
                if machine == 'ridge':
                    self.machines['ridge'] = linear_model.RidgeCV().fit(X_k, y_k)
                if machine == 'random_forest':
                    self.machines['random_forest'] = RandomForestRegressor(random_state=random_state).fit(X_k, y_k)
                if machine == 'svm':
                    self.machines['svm'] = LinearSVR(random_state=random_state).fit(X_k, y_k)
                
            except ValueError:
                print("Machine not Found in List.")
                continue

        # Genarating Predictions from trained regressors.
        self.machine_predictions_ = {}
        self.all_predictions_ = np.array([])
        for machine_name in self.machine_list:
            self.machine_predictions_[machine_name] = self.machines[machine_name].predict(X_l)
            self.all_predictions_ = np.append(self.all_predictions_, self.machine_predictions_[machine_name])

        return self


    def optimal_threshold(self, num_grid_points=50):

        if self.eps is None:
            a, size = sorted(self.all_predictions_), len(self.all_predictions_)
            res = [a[i + 1] - a[i] for i in range(size) if i+1 < size]
            emin = min(res)
            emax = max(a) - min(a)
            erange = np.linspace(emin, emax, num_grid_points)
            tuned_params = [{'eps': erange}]
            print("Grid Search Start")

            # GridSearchCV uses 5-fold cross validation by default.
            clf = GridSearchCV(self, tuned_params, scoring="neg_mean_squared_error", n_jobs=-1)
            clf.fit(self.X, self.y)
            print("Grid Search Complete")
            self.eps = clf.best_params_["eps"]


    def predict(self, X_test):

        predicted_vals = []

        for x in X_test:
            x = x.reshape(1, -1)
            selection_table = np.zeros((len(self.X_l), self.alpha))

            for machine_index, machine_name in enumerate(self.machine_list):
                predicted_val = self.machines[machine_name].predict(x)

                for ind in range(0, len(self.X_l)):
                    if fabs(self.machine_predictions_[machine_name][ind] - predicted_val) <= self.eps:
                        selection_table[ind][machine_index] = 1


            selected_indices = []

            for ind in range(len(self.X_l)):
                if(np.sum(selection_table[ind]) == self.alpha):
                    selected_indices.append(ind)



            aggregated_val = 0
            for ind in selected_indices:
                aggregated_val += self.y_l[ind]

            if len(selected_indices) != 0:
                aggregated_val /= len(selected_indices)
            
            predicted_vals.append(aggregated_val)

        return predicted_vals    

  
    def calculate_R_square(self, y_pred, y_test):
        model_variance = sum((y_test - y_pred)**2)
        avg = sum(y_test)/len(y_test)
        temp = np.array([avg for i in y_test])
        avg_variance = sum((y_test- temp)**2)
        if(avg_variance != 0):
            return (1 - (model_variance/avg_variance))
        else:
            return -1

    def calculate_RMSE(self, y_pred, y_test):
        return np.sqrt(sum((y_pred- y_test)**2)/len(y_pred))
