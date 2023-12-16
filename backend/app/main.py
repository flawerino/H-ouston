"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd

app = FastAPI()

df = pd.read_csv('/app/app/data.csv', sep = ';')
# Converting all the numbers inside the dataframe as strings for JSON
df = df.astype(str)

# Creating a string with districts' name from CSV file


def print_province_names():
    print("Find the theaters in these districts:")
    # Checking the existence of "District" column
    if 'Provincia' not in df.columns:
        return "The dataframe does not contain any 'District' column"
    #Extracting the districts' names from the DataFrame
    province_names = df['Provincia'].unique()
    #Creating a string with all the names
    names_str = ', '.join(province_names)
    return names_str
# Chiamata alla funzione
result = print_province_names()
print(result)


@app.get('/csv_show')


def read_and_return_csv():
    aux = df['CAP'].values
    return{"CAP": str(aux.argmin())}

@app.get('/')


def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Hello": "Veneto"}

@app.get('/query/{district_name}')


def read_item(district_name: str):
    """
    Endpoint to query information based on district_name.
    Args:
        district_name (str): The name of the district.
    Returns:
        dict: Information for the provided district_name.
    """
    # Convert district_name to title case for consistency
    district_name = district_name.title()
    #small = df[df['Provincia'] == district_name][['Nome']]
    # Check if the district_name exists in the 'name' column of the DataFrame
    if district_name in df['Provincia'].values:
    # Get rows where 'Provincia' is equal to district_name
        district_info = df[df['Provincia'] == district_name].to_dict(orient='records')
        
        for info in district_info:
            print(info)
        
        return {"district_name": district_name, "district_info": district_info}
    else:
        return {"Error": "District not found"}
    
    """
    if district_name in df['Provincia'].values:
        # Get rows where 'Provincia' is equal to district_name
        district_info = df[df['Provincia'] == district_name].to_dict(orient='records')
        print(district_info)
        return {"district_name": district_name, "district_info": district_info}
    else:
        return {"Error": "District not found"}
    """


@app.get('/module/search/{district_name}')


def read_item_from_module(district_name: str):
    return {district_name}



@app.get('/get-date')


def get_date():
    """
    Endpoint to get the current date.

    Returns:
        dict: Current date in ISO format.
    """
    current_date = datetime.now().isoformat()
    return JSONResponse(content={"date":current_date})