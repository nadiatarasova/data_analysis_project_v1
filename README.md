# Data Analysis Project V1 

By Nadia Tarasova)

This project aims to analyze network attacks by engineering specific features and running Random Forest for predictive modeling. Below are the steps taken, including data preprocessing, feature generation, model training, evaluation, and visualization.

Project Setup
Ensure you have the required libraries installed:

bash
Copy code
pip install pandas numpy seaborn matplotlib scikit-learn
Data Import
The dataset is imported from a CSV file. The import_data function handles this:

python
Copy code
def import_data():
    data = pd.read_csv("/path/to/your/data/stingar_data_full-20120562.csv")
    return data



