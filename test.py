"""Module for testing model pipeline functionality"""
import unittest
import pandas as pd
from io import StringIO
from contextlib import redirect_stdout
from model_pipe import PricePredictionPipeline


class TestPricePredictionPipeline(unittest.TestCase):

    def setUp(self):
        """creates a small synthetic dataset for testing."""
        self.df = pd.DataFrame({
            'feature1': [10, 20, 30, 40, 50],
            'feature2': ['A', 'B', 'A', 'B', 'A'],
            'price': [100, 200, 300, 400, 500]
        })
        self.pipeline = PricePredictionPipeline(self.df, target_column='price')

    def test_initialization_success(self):
        """Pipeline should initialize with correct target column."""
        self.assertEqual(self.pipeline.target_column, 'price')
        self.assertIsInstance(self.pipeline.X, pd.DataFrame)
        self.assertIsInstance(self.pipeline.y, pd.Series)

    def test_initialization_failure(self):
        """Pipeline should raise error if target column is missing."""
        with self.assertRaises(ValueError):
            PricePredictionPipeline(self.df, target_column='nonexistent')

    def test_training(self):
        """Pipeline should train without errors."""
        X_test, y_test = self.pipeline.train()
        self.assertFalse(X_test.empty)
        self.assertFalse(y_test.empty)

    def test_evaluation(self):
        """Evaluation should run and print metrics."""
        X_test, y_test = self.pipeline.train()
        buffer = StringIO()
        with redirect_stdout(buffer):
            self.pipeline.evaluate(X_test, y_test)
        output = buffer.getvalue()
        self.assertIn("MAE", output)
        self.assertIn("RMSE", output)
        self.assertIn("R²", output)

    def test_prediction(self):
        """Prediction should return a float."""
        self.pipeline.train()
        sample = pd.DataFrame([self.pipeline.X.iloc[0]])
        buffer = StringIO()
        with redirect_stdout(buffer):
            self.pipeline.predict_sample(sample)
        output = buffer.getvalue()
        self.assertIn("Predicted Price", output)


if __name__ == '__main__':
    unittest.main()
