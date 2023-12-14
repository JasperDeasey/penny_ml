from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import numpy as np
from data.database import sqlite_db
   

class RandomForestModel:
    def __init__(self, training_df, testing_df, n_estimators=100):
        self.model = RandomForestClassifier(n_estimators=n_estimators)
        self.train(training_df, testing_df)

    def train(self, train_df, test_df):
        print('Training model...')
        train_df.dropna(inplace=True)

        train_df['Time'] = pd.to_datetime(train_df['Time'])


        train_df.loc[:, 'Time'] = train_df['Time'].view('int64')

        # Training data
        X_train = train_df.drop('target_fn 0=same 1=dec 2=inc 3=both', axis=1)
        y_train = train_df['target_fn 0=same 1=dec 2=inc 3=both']

        # Create and train model
        self.model = RandomForestClassifier(n_estimators=100, n_jobs=-1)
        self.model.fit(X_train, y_train)

        if test_df is None:
            return

        test_df.dropna(inplace=True)
        test_df['Time'] = pd.to_datetime(test_df['Time'])
        test_df.loc[:, 'Time'] = test_df['Time'].view('int64')

        # Testing data
        X_test = test_df.drop('target_fn 0=same 1=dec 2=inc 3=both', axis=1)
        y_test = test_df['target_fn 0=same 1=dec 2=inc 3=both']

        # I also save this in the database to speed up future testing of model
        print('Done training.')

        # Make predictions
        predictions = self.model.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, predictions)}\n")

        predictions_df = pd.DataFrame(predictions, columns=['MODEL_PREDICTION'])

        probabilities = self.model.predict_proba(X_test)

        unique_classes = np.unique(y_train)
        prob_cols = [f"PROBABILITY_{i}" for i in range(len(unique_classes))]
        probabilities_df = pd.DataFrame(probabilities, columns=prob_cols)

        # adding the predictions and probabilities as new columns
        test_df = test_df.reset_index(drop=True)
        test_df = pd.concat([test_df, probabilities_df, predictions_df], axis=1)

        temp_df = test_df[prob_cols].copy()
        test_df['PROBABILITY'] = temp_df.max(axis=1)
        test_df.drop(columns=prob_cols, inplace=True)

        test_df['Time'] = pd.to_datetime(test_df['Time'])

        db = sqlite_db.LocalDatabase()
        db.replace_df(test_df, 'model_prediction')

    def predict(self, X):
        probabilities = self.model.predict_proba(X)
        max_prob_indices = np.argmax(probabilities, axis=1)[0]
        max_probs = probabilities[0, max_prob_indices]
        return Prediction(max_prob_indices, max_probs)


class Prediction:
    def __init__(self, prediction, probability):
        self.prediction = prediction
        self.probability = probability


if __name__ == '__main__':
    df = pd.read_csv('./data/historical_data/polygon_historical_trading_data_subset.csv')
    model = RandomForestModel()
    model.train(df)