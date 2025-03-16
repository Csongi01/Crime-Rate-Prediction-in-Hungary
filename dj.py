import sqlite3

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_city_code(id):   
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT ID FROM City WHERE City = ?", (id,))
    city_code_row = cur.fetchone()
    if city_code_row:
        return city_code_row['ID']
    con.close()

def get_city(id):   
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT City FROM City WHERE ID = ?", (id,))
    city_code_row = cur.fetchone()
    if city_code_row:
        return city_code_row['City']
    con.close()

def get_crime(id):   
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT CrimeType FROM CrimeType WHERE Id = ?", (id,))
    city_code_row = cur.fetchone()
    if city_code_row:
        return city_code_row['CrimeType']
    con.close()

def get_population(id):   
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT Population FROM City WHERE Id = ?", (id,))
    city_code_row = cur.fetchone()
    if city_code_row:
        return city_code_row['Population']
    con.close()

def get_citycateg(id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT CityCategory FROM City WHERE Id = ?", (id,))
    city_code_row = cur.fetchone()
    if city_code_row:
        return city_code_row['CityCategory']
    con.close()

def get_city_category(id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("""SELECT Category  FROM CityCategory cc JOIN City c ON cc.ID = c.CityCategory 
            WHERE c.ID = ?    """, (id,))
    city_code_row = cur.fetchone()
    if city_code_row:
            return city_code_row['Category']
    con.close()



def get_crimecategory(citycateg, crime_rate):
    con = get_db_connection()
    cur = con.cursor()
    
    cur.execute("SELECT Low, Middle FROM CrimeCategory WHERE CityCategory = ?", (citycateg,))
    crime_categ_row = cur.fetchone()

    low_threshold = crime_categ_row['Low']
    middle_threshold = crime_categ_row['Middle']

    if crime_rate <= low_threshold:
        crime_category = "Low"
    elif crime_rate <= middle_threshold:
        crime_category = "Middle"
    else:
        crime_category = "High"
    con.close()
    return crime_category

def row_to_dict(row):
    return dict(zip(row.keys(), row))

def get_city_crime_types(city):
    con = get_db_connection()
    cur = con.cursor()
    
    cur.execute("SELECT Crime, CrimeID FROM CityCrime WHERE City = ?", (city,))
    rows = cur.fetchall()
    
    # Convert rows to a list of dictionaries
    crime_types = [row_to_dict(row) for row in rows]
    
    con.close()
    return crime_types

def get_out_of_valuec(city_category):
    out_of_map = {
        'Nagyváros': 100000,
        'Középváros': 1000,
        'Kisváros': 1000,
        'Nagyfalvak': 100,
        'Középfalvak': 100
    }
    
    return out_of_map.get(city_category, 'N/A')  # Default to 'N/A' if the category is not found


def get_out_of_value(citycateg):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT Low, Middle, High FROM CrimeCategory WHERE CityCategory = ?", (citycateg,))
    row = cur.fetchone()
    con.close()
    return row['Low'], row['Middle'], row['High']

   
# Yearly population changes based on the hungarian KSH data
population_changes = {
    2022: 830,
    2023: 797,
    2024: 627,
    2021: 769,
    2020: 772,
    2019: 778,
    2018: 772,
    2017: 7989,
    2016: 908,
    2015: 9259,
    2014: 931,
    2013: 2989,
    2012: 200,
    2001: 10200
}
default_future_change = population_changes[2024]


def get_adjusted_population(city_code, target_year):
    # Retrieve the population for the city in 2022
    base_population = get_population(city_code)
    
    # Calculate the cumulative population change from 2022 to the target year
    cumulative_change = 0
    if target_year >= 2022:
        for year in range(2022, target_year + 1):
            if year in population_changes:
                cumulative_change += population_changes[year]
            else:
                cumulative_change += default_future_change  # Use default change rate for future years
    else:
        for year in range(2022, target_year - 1, -1):
            if year in population_changes:
                cumulative_change -= population_changes[year]
            else:
                cumulative_change -= default_future_change  # Use default change rate for past years not in the data
    
    # Adjust the base population by the cumulative change
    adjusted_population = base_population + cumulative_change
    
    return adjusted_population

