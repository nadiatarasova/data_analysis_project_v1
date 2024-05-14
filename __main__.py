# Import key packages
import pandas as pd
import numpy as np
import statistics
import seaborn as sns
import matplotlib.pyplot as plt

# Import neccessary Random Forest libabries
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import random

# Package for visualising classical Confusion Matrix
from sklearn.metrics import confusion_matrix
import seaborn

# Helper functions
from utils import check

# feature engineering functions
from feature_engineering import format_data, generate_features, generate_honeypot_features, generate_ip_features, generate_password_features



# import data
def import_data():
    data = pd.read_csv("/Users/nadia_t/Downloads/stingar_data_full-20120562.csv")
    return data



def train_random_forest(features):
    rf_data = features.copy()
    rf_data = rf_data[['src_ip','mean_time_difference','sd_time_difference','sensor_number','length_password']]
        #adding new column (random data) which should be our output. Potentionally we will have this column
    rf_data['danger'] = random.choices(population = [1,0],weights = [0.75,0.25], k = len(rf_data))
    train = rf_data[:8000]
    predictor_vars = ['mean_time_difference','sd_time_difference','sensor_number','length_password']
    X, y = train[predictor_vars], train.danger
    modelRandom = RandomForestClassifier(max_depth=25)
    # cross validation is a measure of how good the random forest is
    # i.e. how far its predictions are from the actual values
    modelRandomCV = cross_val_score(modelRandom,X,y,cv = 5)
    # below we are training the random forest model
    modelRandom.fit(X,y)
    return {
        modelRandom: modelRandom,
        rf_data: rf_data,
        predictor_vars: predictor_vars,
        modelRandomCV: modelRandomCV,
    }

def eval_random_forest(model, rf_data, predictor_vars):
    test = rf_data[8000:]
    # here we are using the train random forest model to make predictions
    predictions = model.predict(test[predictor_vars])
    test['predictions'] = predictions
    test['check'] = test.apply(check,axis = 1)

    accuracy_total = len(test[test['check'] == 'Correct'])/len(test)
    accuracy_total
    #Hard to predict random data. Hence, low accuracy.
    danger = test[test['danger'] == 1]
    danger_accuracy = len(danger[danger['check'] == 'Correct'])/len(danger)
    #As data is random it's hard to predict certain outcomes. Especially for "danger"(since "danger" label is only about 25% of our training data)
    danger_accuracy

    return {
        predictions,
        test
    }



def visualize_rf_results(test, predictions):
    CM = confusion_matrix(test.danger, predictions)
    # Visualize it as a heatmap
    seaborn.heatmap(CM)
    plt.show()

if __name__ == '__main__':

    data = import_data()
    data_final = format_data(data)
    features = generate_features(data_final)
    features = generate_honeypot_features(data_final, features)
    features = generate_ip_features(data_final, features)
    features = generate_password_features(data_final, features)

    # do the random forest executions here
    rf_context = train_random_forest(features)
    eval_context = eval_random_forest(rf_context.modelRandom, rf_context.rf_data, rf_context.predictor_vars)
    # visualize results in a 2x2 chart
    visualize_rf_results(eval_context.test, eval_context.predictions)




