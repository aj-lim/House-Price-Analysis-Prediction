"""module to build predictive model pipeline"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
from data_understanding import data_clean

"""remove outliers where price < 150,000 or price > 4,000,000"""
df_filtered = data_clean[~((data_clean['price'] < 150000) | (data_clean['price'] > 3500000))]

try:
    df = df_filtered
except FileNotFoundError:
    print("Error: Dataset file not found.")
    exit()

if df.empty or 'price' not in df.columns:
    print("Error: Dataset is empty or missing 'Price' column.")
    exit()


class BasePipeline:
    def __init__(self, df: pd.DataFrame, target_column: str):
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame.")

        self.df = df
        self.target_column = target_column
        self.X = df.drop(columns=[target_column])
        self.y = df[target_column]
        self.model = None

    def split_data(self, test_size=0.2, random_state=42):
        """split the dataset into train and test sets"""
        return train_test_split(self.X, self.y, test_size=test_size, random_state=random_state)


class PricePredictionPipeline(BasePipeline):
    def __init__(self, df: pd.DataFrame, target_column: str):
        super().__init__(df, target_column)  # Inherit from BasePipeline
        self._build_pipeline()

    def _build_pipeline(self):
        """build the preprocessing and model pipeline"""
        numeric_features = self.X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = self.X.select_dtypes(include=['object', 'category']).columns.tolist()

        numeric_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features)
            ]
        )

        self.model = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", XGBRegressor(
                objective="reg:squarederror",
                n_estimators=300,
                learning_rate=0.1,
                max_depth=6,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                n_jobs=-1
            ))
        ])

    def train(self, test_size=0.2, random_state=42):
        """train the pipeline"""
        X_train, X_test, y_train, y_test = self.split_data(test_size, random_state)
        self.model.fit(X_train, y_train)
        return X_test, y_test

    def evaluate(self, X_test, y_test):
        """evaluate model and print results"""
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        print(f"MAE  : {mae:.2f}")
        print(f"RMSE : {rmse:.2f}")
        print(f"R²   : {r2:.3f}")

    def predict_sample(self, sample_df: pd.DataFrame):
        """predict price for specific sample dataframe"""
        try:
            prediction = self.model.predict(sample_df)[0]
            print(f"The predicted price for this property is: {prediction:.2f}")
        except Exception as e:
            print(f"Prediction error: {e}")


pipeline = PricePredictionPipeline(df, target_column='price')
X_test, y_test = pipeline.train()
pipeline.evaluate(X_test, y_test)

"""predict for the first row of the dataset"""
sample = pd.DataFrame([pipeline.X.iloc[0]])
pipeline.predict_sample(sample)
