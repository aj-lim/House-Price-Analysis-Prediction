"""
Database module used to input and store data
"""
import mysql.connector
from data_understanding import data_clean


def upload_dataframe(df):
    """function to upload the dataframe to MySQL"""
    """check that data exists in the dataframe"""
    if df.empty:
        print("No data to upload.")
        return

    """connect to MySQL"""
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password='Password123!',
        port='3306',
        database="house_price_data"
    )
    mycursor = mydb.cursor()

    """create table for storing data"""
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS house_prices (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            price DECIMAL(10, 2),
            bedrooms DECIMAL(10, 2),
            bathrooms DECIMAL(10, 2),
            sqft_living DECIMAL(10, 2),
            sqft_lot DECIMAL(10, 2),
            floors DECIMAL(10, 2),
            waterfront DECIMAL(10, 2),
            view DECIMAL(10, 2),
            `condition` DECIMAL(10, 2),  -- reserved word
            sqft_above DECIMAL(10, 2),
            sqft_basement DECIMAL(10, 2),
            yr_built INT,
            yr_renovated INT,
            street VARCHAR(255),
            city VARCHAR(255),
            zip INT
        );
    """)

    """insert query with placeholders"""
    insert_query = """
        INSERT INTO house_prices (
            price, bedrooms, bathrooms, sqft_living, sqft_lot, floors, 
            waterfront, view, `condition`, sqft_above, sqft_basement, 
            yr_built, yr_renovated, street, city, zip
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    """convert to tuples for executemany command"""
    data_tuples = [tuple(row) for row in df.itertuples(index=False, name=None)]

    """run insert statement"""
    mycursor.executemany(insert_query, data_tuples)
    mydb.commit()

    print(f"{mycursor.rowcount} rows inserted successfully.")

    """runs query on how many properties are in a particular zip code"""
    mycursor.execute('SELECT COUNT(*) FROM house_prices WHERE zip = "98125"')
    zip_list = mycursor.fetchall()
    if len(zip_list) > 0:
        for i in zip_list:
            print(f"Number of properties in this zip code: {i[0]}")
    else:
        print("No properties in this zip code")

    """runs query to list properties that have a price of 5 million or more"""
    mycursor.execute('SELECT street FROM house_prices WHERE price > 5000000')
    price_list = mycursor.fetchall()
    if len(price_list) > 0:
        for i in price_list:
            print(f"Properties in this price range: {i[0]}")
    else:
        print("No properties in this price range")

    """runs query to list properties built in certain timeframe which have been renovated"""
    mycursor.execute('SELECT street FROM house_prices WHERE yr_built '
                     'BETWEEN 1970 AND 1971 AND yr_renovated <> 0')
    built_renovated_list = mycursor.fetchall()
    if len(built_renovated_list) > 0:
        for i in built_renovated_list:
            print(f"Properties built in this timeframe which have been renovated: {i[0]}")
    else:
        print("No properties in this timeframe which have been renovated")

    mycursor.close()
    mydb.close()


if __name__ == "__main__":
    df = data_clean

    upload_dataframe(df)
