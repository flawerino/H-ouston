"""
Frontend module for the Flask application.

This module defines a simple Flask application that serves 
as the frontend for the project.
"""

from flask import Flask, render_template
import requests  # Import the requests library to make HTTP requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
# Replace with a secure secret key
app.config['SECRET_KEY'] = 'your_secret_key'  

# Configuration for the FastAPI backend URL
# Replace with the actual URL of your FastAPI backend
FASTAPI_BACKEND_HOST = 'http://backend'  
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'


class QueryForm(FlaskForm):
    district_name = StringField('District Name:')
    submit = SubmitField('Get Theaters from our Super Backend')


@app.route('/')


def index():
    """
    Render the index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    # Fetch the date from the backend
    date_from_backend = fetch_date_from_backend()
    return render_template('index.html', date_from_backend = date_from_backend)


def fetch_date_from_backend():
    """
    Function to fetch the current date from the backend.

    Returns:
        str: Current date in ISO format.
    """
    # Adjust the URL based on your backend configuration
    backend_url = 'http://backend/get-date'  
    try:
        response = requests.get(backend_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json().get('date', 'Date not available')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching date from backend: {e}")
        return 'Date not available'


@app.route('/internal', methods = ['GET', 'POST'])


def internal():
    """
    Render the internal page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    form = QueryForm()
    error_message = None  # Initialize error message

    if form.validate_on_submit():
        district_name = form.district_name.data

        # Make a GET request to the FastAPI backend
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/query/{district_name}'
        response = requests.get(fastapi_url)
        print(response.content)

        if response.status_code == 200:
            # Extract and display the result from the FastAPI backend
            data = response.json()
            result = data.get('district_info', f'Error: District not available for {district_name}')
            return render_template('internal.html', form = form, result = result, error_message = error_message)
        else:
            error_message = f'Error: Unable to fetch District for {district_name} from our Super but limited Backend'

    return render_template('internal.html', form = form, result = None, error_message = error_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)