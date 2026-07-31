import questionary
import pandas as pd
import re
from model_pipe import pipeline


def cli():
    questionary.press_any_key_to_continue("Welcome to the house price prediction"
                                          " calculator. To predict the price of a property,"
                                          " you will need to enter the following details:\n\n"
                                          "Number of bedrooms, number of bathrooms, living area (sqft),\n"
                                          "lot area (sqft), number of floors, waterfront, view, condition,\n"
                                          "above-ground area (sqft), basememt area (sqft), year built,\n"
                                          "year renovated, address, city and zip code\n\n"
                                          "Press any key to continue."
                                          ).ask()

    bedrooms = int(questionary.text(
        "Number of bedrooms (0-9):",
        validate=lambda val: (
                                     val.isdigit() and 0 <= int(val) <= 9
                             ) or "Please enter an integer between 0 and 9"
    ).ask())
    bathrooms = float(questionary.text(
        "Number of bathrooms (e.g., 1, 1.5, 2, 3.75):",
        validate=lambda val: (
                                     re.match(r"^\d+(\.\d{1,2})?$", val) and float(val) >= 0
                             ) or "Please enter a non-negative number with up to 2 decimal places"
    ).ask())
    sqft_living = int(questionary.text(
        "Square footage of living area (370 - 13540):",
        validate=lambda val: (
                                     val.isdigit() and 370 <= int(val) <= 13540
                             ) or "Please enter an integer between 370 and 13540"
    ).ask())
    sqft_lot = int(questionary.text(
        "Square footage of lot (638 - 1074218):",
        validate=lambda val: (
                                     val.isdigit() and 638 <= int(val) <= 1074218
                             ) or "Please enter an integer between 638 and 1074218"
    ).ask())
    floors = float(questionary.text(
        "Number of floors (0 - 3.5):",
        validate=lambda val: (
                                     re.match(r"^\d+(\.\d)?$", val) and 0 <= float(val) <= 3.5
                             ) or "Please enter a number between 0 and 3.5 with up to 1 decimal place"
    ).ask())
    waterfront = float(questionary.text("Waterfront (1=yes, 0=no):").ask())
    view = int(questionary.text(
        "View rating (0-4):",
        validate=lambda val: (
                                     val.isdigit() and 0 <= int(val) <= 4
                             ) or "Please enter an integer between 0 and 4"
    ).ask())
    condition = int(questionary.text(
        "Condition rating (1-5):",
        validate=lambda val: (
                                     val.isdigit() and 1 <= int(val) <= 5
                             ) or "Please enter an integer between 1 and 5"
    ).ask())
    sqft_above = int(questionary.text(
        "Square footage above ground (370 - 9410):",
        validate=lambda val: (
                                     val.isdigit() and 370 <= int(val) <= 9410
                             ) or "Please enter an integer between 370 and 9410"
    ).ask())
    sqft_basement = int(questionary.text(
        "Square footage of basement (0 - 4130):",
        validate=lambda val: (
                                     val.isdigit() and 0 <= int(val) <= 4130
                             ) or "Please enter an integer between 0 and 4130"
    ).ask())
    yr_built = int(questionary.text(
        "Year built (1900 - 2015):",
        validate=lambda val: (
                                     val.isdigit() and 1900 <= int(val) <= 2015
                             ) or "Please enter a year between 1900 and 2015"
    ).ask())
    yr_renovated = float(questionary.text("Year renovated (0 if never):").ask())
    street = questionary.text("Street address:").ask()
    city = questionary.text("City:").ask()
    zip_code = int(questionary.text(
        "Zip code (98001 - 98354):",
        validate=lambda val: (
                                     val.isdigit() and 98001 <= int(val) <= 98354
                             ) or "Please enter a zip code between 98001 and 98354"
    ).ask())

    input_df = pd.DataFrame([{
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "sqft_living": sqft_living,
        "sqft_lot": sqft_lot,
        "floors": floors,
        "waterfront": waterfront,
        "view": view,
        "condition": condition,
        "sqft_above": sqft_above,
        "sqft_basement": sqft_basement,
        "yr_built": yr_built,
        "yr_renovated": yr_renovated,
        "street": street,
        "city": city,
        "zip": zip_code
    }])

    pipeline.predict_sample(sample_df=input_df)
    print("Here is the data you entered:")
    print(input_df)


if __name__ == '__main__':
    cli()
