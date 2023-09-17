## Contact Management CLI

# Phase3 CLI Project

A simple CLI application for managing contacts built using Python, SQLAlchemy, and the command-line interface.

## Description

This CLI application allows users to manage their contacts, categorize them, and search for specific contacts using various search criteria. 
It uses SQLAlchemy for database management and provides a user-friendly command-line interface for interaction.

## Installation

After Forking, and copying the SSH, navigate to the folder you wish to clone the repo into and run:

```bash
git clone git@github.com:thinesh-12/phase3-project-Contact-Management.git5
```

## Usage
After cloning, run the following command to install the relavant dependancies to make the application function

# Install Dependencies
Once you've cloned the repository, navigate into the project folder and install the required dependencies using pipenv:
```bash
pipenv install && pipenv shell
```

# Seed Database (Optional):
To seed the database with some fake data to test out the features of the app run the following (optional) command:
```bash
python seeds.py
```

# Run the Application:
Then to start the app run the following command:

```bash
python cli.py
```

## Features 

Add new contacts with details such as name, phone number, email, and category.
Search for contacts using search terms and optional category filters.
Database-backed storage using SQLAlchemy.
User-friendly command-line interface.

## Future Improvements

Allow users to update and delete existing contacts.
Improve data validation and error handling for user inputs.
Add more options for managing and categorizing contacts.

## Resources
SQLAlchemy https://docs.sqlalchemy.org/en/20/
Faker  https://faker.readthedocs.io/en/master/

## License
This project is licensed under the MIT License - see the LICENSE file for details.
