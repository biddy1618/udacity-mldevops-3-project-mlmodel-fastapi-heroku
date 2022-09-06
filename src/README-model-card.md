# Model Card

For additional information see the Model Card paper: https://arxiv.org/pdf/1810.03993.pdf

## Data Details

Data details can be found at [`src/README-data.md`](README-data.md) file.

## Model Details

The model analyzed in this card determines whether a person makes over 50k a year.

### Model selection

Model is built using scikit-learn's GradientBoostingClassifier (`from sklearn.ensemble.GradientBoostingClassifier`) and
is trained on the train-split of the data using train-validation-test split scheme.

### Model input-output formats

Input:
```json
{
    "age": 35,
    "workclass": "Private",
    "fnlgt": 323143,
    "education": "Assoc-voc",
    "education_num": 11,
    "marital_status": "Married-csv-spouse",
    "occupation": "Sales",
    "relationship": "Husbanb",
    "race": "White",
    "sex": "Male",
    "capital_gain": 0,
    "capital_loss": 0,
    "hours_per_week": 45,
    "native_country": "United-States"
}
```

Output:
```json
{
    "predcition": [">50K", "<=50K"]
}
```

## Intended Use

Given the demographics data of a person(s), one can use this model to predict whether or not he/she/they earn more than 50k
a year. This is a toy model and is not intented to use in commercial settings nor guarantees the truth of prediction.

## Training Data

Training data was obtained through train-test split using scikit-learn's `train_test_split` function with test-size of 0.2
and fixed random seed of 48. Further the train data was split to train and validation sets using same scheme. The model was
trained on the train data, and validated on validation data.

## Evaluation Data

The evaluation data was obtained through same scheme as above. In the scope of this project, it is called test data.

## Metrics

Metrics on the test data are as follows:

| Metric | Score |
|-|-|
| Precision | 0.77778 |
| Recall | 0.59584 |
| F1 score | 0.67476 |
| Average precision | 0.80804 |

Confusion matrix:

| | Predicted True | Predicted False |
|-|-|-|
| Actual False | 4707 | 262 |
| Actual True  | 622 | 917 |


More on the model slice metrics and plots
[here](https://studio.iterative.ai/user/biddy1618/projects/udacity-mldevops-3-project-mlmodel-fastapi-heroku-vja0jevasy).

## Ethical Considerations

This model doesn't quarantee the truthfulness of predictions and should be used with caution as it contains bias.
The model tends to under predict people of black race compared to white people. And for males, it tends to have
more false positives compared to female.

More on model bias can be found in this [notebook](eda/EDA.ipynb)

## Caveats and Recommendations

Model hasn't been hyper-tuned for this specific dataset. It was trained on default settings, and could potentially
perform better with good hyper-tuning.