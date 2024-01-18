import pandas as pd
import pytest
from fastapi.testclient import TestClient
from app.main import app, print_province_names, district, city, capacity_statistics

# Fixture to load CSV data
@pytest.fixture
def sample_data():
    df_data = {
        'Provincia': ['District1', 'District1', 'District2', 'District3'],
        'Città': ['City1', 'City2', 'City3', 'City4'],
        'Genere locale': ['Theatre', 'CINEMA', 'CINEMA', 'Theatre'],
        'Capienza': [100, 200, 150, 120],
    }
    df = pd.DataFrame(df_data)
    return df.to_csv(index=False, sep=';')

# Test print_province_names function
def test_print_province_names(sample_data, capsys):
    with open('/app/app/data.csv', 'w') as f:
        f.write(sample_data)
    print_province_names()
    captured = capsys.readouterr()
    assert captured.out.strip() == 'District1, District2, District3'

# Test district function
def test_district_found(sample_data):
    df = pd.read_csv(pd.compat.StringIO(sample_data), sep=';')
    result = district('District1', df)
    assert result == {"district_name": "District1", "district_info": [{'Provincia': 'District1', 'Città': 'City1', 'Genere locale': 'Theatre', 'Capienza': 100}, {'Provincia': 'District1', 'Città': 'City2', 'Genere locale': 'CINEMA', 'Capienza': 200}]}

def test_district_not_found(sample_data):
    df = pd.read_csv(pd.compat.StringIO(sample_data), sep=';')
    result = district('UnknownDistrict', df)
    assert result == {"Error": "District not found"}

# Test city function
def test_city_found(sample_data):
    df = pd.read_csv(pd.compat.StringIO(sample_data), sep=';')
    result = city('City3', df)
    assert result == {"city_name": "City3", "city_info": [{'Provincia': 'District2', 'Città': 'City3', 'Genere locale': 'CINEMA', 'Capienza': 150}]}

def test_city_not_found(sample_data):
    df = pd.read_csv(pd.compat.StringIO(sample_data), sep=';')
    result = city('UnknownCity', df)
    assert result == {"Error": "City not found"}

# Test capacity_statistics function
def test_capacity_statistics(sample_data):
    df = pd.read_csv(pd.compat.StringIO(sample_data), sep=';')
    result = capacity_statistics('District1', df)
    assert result == {'mean': 150.0, 'median': 150.0, 'maximum': 200, 'minimum': 100}
