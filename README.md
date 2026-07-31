# 🏠 House Price Prediction CLI

A Python project that **cleanses**, **explores**, and **visualises** house price data, then builds a **predictive machine learning model** to estimate property prices.  
The project also includes a **Command-Line Interface (CLI)** for users to create their own predictions.

---

## 📌 Features
- **Data Understanding**: checks details of the raw data and carries out cleansing tasks.
- **Data Exploration**: Statistical analysis and visual insights of the data.
- **Data Visualisation**: Interactive plots to display patterns within the data.
- **Data Storage**: Connects to a MySQL database to store and persist data.
- **Predictive Modeling**: Trains and evaluates a regression model for price prediction.
- **User CLI**: Enables users to predict house prices directly from the terminal.

## 🚀 Installation and usage

## Clone the repository
```bash
git clone https://github.com/aj-lim/House-Price-Analysis-Prediction.git
cd House-Price-Analysis-Prediction
```

## Install dependencies
```bash
pip install -r requirements.txt
```
## Open the terminal and run the CLI
```bash
python cli.py
```
## Enter the required input values
- Number of bedrooms (must be an integer between 0 - 9)
- Number of bathrooms (must be between 0 - 8, can have up to 2 decimal places)
- Living area in square feet (must be an integer between 370 - 13540)
- Lot area in square feet (must be an integer between 638 - 1074218)
- Number of floors (must be between 0 - 3.5, can have up to 1 decimal place)
- Waterfront (yes/no)
- View rating (0-4)
- Condition rating (1-5)
- Above-ground area in square feet (must be an integer between 370 - 9410)
- Basement area in square feet (must be an integer between 0 - 4130)
- Year built (1900-2015)
- Year renovated (if never renovated enter 0)
- Address (street number and street name)
- City
- Zip code (between 98001 - 98354)
