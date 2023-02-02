# Sunrise Graph Generator 
A fun Python project that generates a graph of sunrise times based on data from the `https://api.sunrise-sunset.org` API.

## Purpose
This project is designed to create a graph of the sunrise hour for a given period of time and location. Simply provide the desired time frame and address, and the algorithm will plot the sunrise hour for each day within that range.

For example, inputting a period of January 1, 2020 to December 31, 2020 and a location of 'New York, US' will result in a graph of the sunrise hours in New York City for the entire year of 2020.


## Sunrise Graph Generator - Tech Stack
This project uses the following libraries to generate the sunrise graph:

- Tkinter: A GUI library for Python, used to create the user interface for this project.
- Pydantic: A data validation library that enforces type hints and provides a simple way to specify data validation for incoming data.
- Requests: A Python library for sending HTTP requests, used to retrieve data from the `https://api.sunrise-sunset.org` API.
- Geopy: A Python library for geographical calculations, used to convert addresses into latitude and longitude coordinates.

Additionally, the project also explores the use of threads to make the API requests, which helps to improve the overall performance of the program. The combination of these technologies results in a robust and efficient algorithm for generating sunrise graphs.


## Installation
To set up a virtual environment for this project, follow these steps on a Linux machine:
1. Install virtualenv using the following command:

    ````
    $ python -m pip install --user virtualenv
2. Create a virtual environment for this project:
    ````
    python3 -m venv env
3. Activate the virtual environment:
    ````
    $ source myenv/bin/activate
4. Install the packages listed in requirements.txt using the following command:
    ````
    $ pip install -r requirements.txt
5. On the root path, run:
    ````
    python __main__.py

This project was developed using Python 3.9.13. 

