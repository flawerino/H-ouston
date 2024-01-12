"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd

from .mymodules.function import district
from .mymodules.function import city

app = FastAPI()

df = pd.read_csv('/app/app/data.csv', sep = ';')
# Converting all the numbers inside the dataframe as strings for JSON
df = df.astype(str)


@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Hello": "Veneto"}

#Function 1
@app.get('/district/{district_name}')
def get_district(district_name: str):
    """
    if district_name in df['Provincia'].values:
        # Get rows where 'Provincia' is equal to district_name
        district_info = df[df['Provincia'] == district_name].to_dict(orient='records')
        print(district_info)
        return {"district_name": district_name, "district_info": district_info}
    else:
        return {"Error": "District not found"}
    """
    dist = district(district_name, df)
    return {"district_name": district_name, "district_info": dist}


#Function 2
@app.get('/city/{city_name}')
def get_city(city_name: str):
    """
    if city_name in df['Città'].values:
        # Get rows where 'Città' is equal to city_name
        city_info = df[df['Città'] == city_name].to_dict(orient='records')
        print(city_info)
        return {"city_name": city_name, "city_info": city_info}
    else:
        return {"Error": "City not found"}
    """
    cit = city(city_name, df)
    return {"city_name": city_name, "city_info": cit}


@app.get('/get-date')
def get_date():
    """
    Endpoint to get the current date.

    Returns:
        dict: Current date in ISO format.
    """
    current_date = datetime.now().isoformat()
    return JSONResponse(content={"date":current_date})