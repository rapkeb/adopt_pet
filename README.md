
ChatGPT
AdoptPet Web Application

Overview

AdoptPet is a simple web application built with Flask, SQLAlchemy, and Flask-Migrate. It allows users to view and filter a list of pets available for adoption. Users can also leave their opinions on each pet. Additionally, registered users have the ability to add new pets for adoption.

Prerequisites

Python 3.x
Flask
Flask-SQLAlchemy
Flask-Migrate
Setup

Clone the repository:
bash
Copy code
git clone https://github.com/your-username/adoptPet.git
cd adoptPet
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Initialize the database:
bash
Copy code
python
from your_script_name import db
db.create_all()
exit()
Configuration

The application uses SQLite as its default database. The database file is named adoptPet.db, and it is created in the root directory.
The secret key for session management is set to "super secret key." Please replace it with a more secure key in production.
Usage

Run the application:
bash
Copy code
python your_script_name.py
Open your web browser and navigate to http://localhost:5000/.
Routes

/register: User registration page.
/login: User login page.
/logout: Logout the current user.
/: Homepage displaying a list of pets. Users can filter pets by their kind (e.g., dogs, cats).
/show_animal/int:id: Show details of a specific pet, including user opinions. Registered users can leave opinions.
/add_pet: Add a new pet for adoption (only accessible for registered users).
/delete_pet/int:id: Delete a pet and its associated opinions (only accessible for registered users).
/delete_opinion/int:id: Delete a user's opinion on a pet (only accessible for registered users).
Contributing

If you'd like to contribute to AdoptPet, please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Implement your changes.
Test thoroughly.
Submit a pull request.
License

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments

Flask: https://flask.palletsprojects.com/
SQLAlchemy: https://www.sqlalchemy.org/
Flask-Migrate: https://flask-migrate.readthedocs.io/
Thank you for using AdoptPet! If you encounter any issues or have suggestions, please feel free to create an issue on GitHub.
