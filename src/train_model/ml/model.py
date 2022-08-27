'''
Module for training and evaluating model and making inferences.

Author: Dauren Baitursyn
Date: 26.08.22
'''
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import fbeta_score, precision_score, recall_score, \
    confusion_matrix, precision_recall_curve, average_precision_score


# Optional: implement hyperparameter tuning.
def train_model(X_train, y_train, random_state):
    '''
    Trains a machine learning model and returns it.

    Args:
        X_train (np.ndarray):
            Training data.
        y_train (np.array):
            Binarized labels.
        random_state (int):
            Random seed for model training.
    Returns:
        sklearn.ensemble.GradientBoostingClassifier:
            Trained machine learning model.
    '''
    gbc = GradientBoostingClassifier(random_state=random_state)
    gbc.fit(X_train, y_train)

    return gbc


def compute_model_metrics(y, preds):
    '''
    Validates the trained machine learning model using
    precision, recall, and F1.

    Args:
        y (np.array):
            Known labels, binarized.
        preds (np.array):
            Predicted labels, binarized.
    Returns:
        float: precision score
        float: recall score
        float: fbeta score
    '''
    fbeta = fbeta_score(y, preds, beta=1, zero_division=1)
    precision = precision_score(y, preds, zero_division=1)
    recall = recall_score(y, preds, zero_division=1)

    return precision, recall, fbeta


def get_confusion_matrix(y, preds):
    '''
    Calculate confusion matrix

    Args:
        y (np.array):
            Known labels, binarized.
        preds (np.array):
            Predicted labels, binarized.

    Returns:
        np.ndarray:
            Confusion Matrix.
    '''
    cm = confusion_matrix(y, preds)

    return cm


def get_precision_recall_curve(y, pred_probas):
    '''
    Calculate confusion matrix

    Args:
        y (np.array):
            Known labels, binarized.
        pred_probas (np.array):
            Predicted label scores.

    Returns:
        np.array: Precision values for all threshold values.
        np.array: Recall values for all threshold values.
        np.array: Threshold values.
        float: Average precision score.
    '''
    precisions, recalls, thresholds = precision_recall_curve(y, pred_probas)

    aps_score = average_precision_score(y, pred_probas)

    return precisions, recalls, thresholds, aps_score


def inference(model, X):
    '''
    Run model inferences and return the predictions.

    Args:
        model (sklearn.ensemble.GradientBoostingClassifier):
            Trained machine learning model.
        X (np.array):
            Data used for prediction.
    Returns:
        (np.ndarray):
            Probability predictions from the model.
    '''
    y_pred_proba = model.predict_proba(X)

    return y_pred_proba
