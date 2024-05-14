# Data Analysis Project V1 

By Nadia Tarasova

This project aims to analyze network attacks by engineering specific features and running Random Forest for predictive modeling. Below are the steps taken, including data preprocessing, feature generation, model training, evaluation, and visualization.

## Project Setup

Ensure you have the required libraries installed:
```bash
pip install pandas numpy seaborn matplotlib scikit-learn
```

## Data Import

The dataset is imported from a CSV file. The `import_data` function handles this:
```python
def import_data():
    data = pd.read_csv("/path/to/your/data/stingar_data_full-20120562.csv")
    return data
```

## Data Formatting

The `format_data` function processes the raw data to get us a clean dataset:
```python
def format_data(data):
    data['d_time'] = pd.to_datetime(data['d_time']).values.astype(np.int64)
    # Additional processing for mean and standard deviation of time differences
    # ...
    return data_final
```

## Feature Engineering

### Basic Features

Here - the key features such as the mean time difference, standard deviation of time differences, and the number of unique sensors are generated:
```python
def generate_features(data):
    # Process to create features
    return features
```

### Honeypot Features

Features related to honeypot applications are generated:
```python
def generate_honeypot_features(data, features):
    # Process to create honeypot-related features
    return new_features
```

### IP Features

Additional features based on IP addresses are generated:
```python
def generate_ip_features(data, features):
    # Process to create IP-related features
    return features
```

### Password Features

Features related to password lengths are generated:
```python
def generate_password_features(data, features):
    # Process to create password-related features
    return features
```

## Model Training

The Random Forest Classifier is trained using the generated features:
```python
def train_random_forest(features):
    rf_data = features.copy()
    rf_data['danger'] = random.choices(population=[1, 0], weights=[0.75, 0.25], k=len(rf_data))
    train = rf_data[:8000]
    predictor_vars = ['mean_time_difference', 'sd_time_difference', 'sensor_number', 'length_password']
    X, y = train[predictor_vars], train.danger
    modelRandom = RandomForestClassifier(max_depth=25)
    modelRandom.fit(X, y)
    return {
        'modelRandom': modelRandom,
        'rf_data': rf_data,
        'predictor_vars': predictor_vars,
    }
```

## Model Evaluation

The trained model is evaluated on a test set with some randomly generated target data:
```python
def eval_random_forest(model, rf_data, predictor_vars):
    test = rf_data[8000:]
    predictions = model.predict(test[predictor_vars])
    test['predictions'] = predictions
    test['check'] = test.apply(check, axis=1)
    accuracy_total = len(test[test['check'] == 'Correct']) / len(test)
    danger = test[test['danger'] == 1]
    danger_accuracy = len(danger[danger['check'] == 'Correct']) / len(danger)
    return {
        'predictions': predictions,
        'test': test,
    }
```

## Results Visualization

The results are visualized using a confusion matrix:
```python
def visualize_rf_results(test, predictions):
    CM = confusion_matrix(test.danger, predictions)
    seaborn.heatmap(CM, annot=True)
    plt.show()
```

[![visual-output-28.png](https://i.postimg.cc/44MHWJvF/image-28.png)](https://postimg.cc/fkcbLQrx)


## Execution

The main execution block runs the entire process:
```python
if __name__ == '__main__':
    # code runs here
```

By following these steps, you can reproduce the analysis and gain insights into the network attack patterns using feature engineering and Random Forest Classifier.

---
