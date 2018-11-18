# Codeforces Rating and Rank Predictor

We used jupyter notebooks for development. Jupyter notebooks are stored in jupyter_ipynb. 
The outputs have been exported to jupyter_outputs. The python code has been exported to python_src.

## Perfomance at a glance

| Rating Predictor  | R2 Score | RMS Error |
|-------------------|----------|-----------|
| Linear Regression | 0.738    | 92.45     |
| XGBoost           | 0.827    | 75.11     |
| Random Forest     | 0.803    | 80.21     |

| Rank Predictor      | Accuracy |
|---------------------|----------|
| Logistic Regression | 0.60     |
| XGBoost             | 0.57     |
| Random Forest       | 0.55     |

## File order

1. User Analysis
2. getting_problemData.py
3. User Problem Analysis
4. Final Feature
5. EDA
6. train

## Note
The model takes about 30 seconds to train. So you can just run the train.py file to check the accuracy. 
