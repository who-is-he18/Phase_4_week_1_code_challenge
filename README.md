# Superheroes Flask API
This project is a Flask-based API for managing superheroes and their superpowers. It provides various endpoints to create, update, and retrieve information about heroes and their associated powers through a HeroPower relationship.

## Table of Contents
- Overview
- Tech Stack
- Setup and Installation
- Database Setup
- API Endpoints
- Validations
- Testing
- Postman Collection
- Contributing
- License

## Overview
This API allows users to:

1. Retrieve a list of heroes and their superpowers.
2. Retrieve a list of powers.
3. Assign powers to heroes with varying strengths.
4. Update descriptions for powers.
5. Models and Relationships
6. Hero: A hero with a name and super_name.
7. Power: A power with a name and a description of at least 20 characters.
8. HeroPower: A join table that connects Hero and Power with an additional strength attribute (Strong, Weak, or Average).

## Tech Stack
1. Backend: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-RESTful
2. Database: SQLite (default, but can be changed to other DBs like PostgreSQL)
3. Tools: Postman (for API testing), Pytest (for unit tests)

## Setup and Installation
#### Prerequisites
- Python 3.x
- Pipenv (for managing Python dependencies)
- Node.js and npm (optional, for running the React frontend)

#### Clone the Repository
```bash
git clone https://github.com/yourusername/superheroes-flask-api.git
cd superheroes-flask-api
```
#### Install Backend Dependencies
#### Install all Python dependencies:

```bash
pipenv install
```
#### Activate the Pipenv shell:
```bash
pipenv shell
```
#### Install Node dependencies for the frontend (optional):
```bash
npm install --prefix client
```
## Database Setup
#### Initialize the database and run migrations:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
#### Seed the database (optional):
```bash
python server/seed.py
```
### Run the Application
#### Start the Flask server (API):

```bash
python server/app.py
```
- The Flask server will run at http://localhost:5555.

### (Optional) Start the React frontend:
```bash
npm start --prefix client
```
- The frontend will be available at http://localhost:4000.

## API Endpoints
1. GET /heroes
- Retrieves a list of all heroes.
Response:

```json
[
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  },
  {
    "id": 2,
    "name": "Doreen Green",
    "super_name": "Squirrel Girl"
  }
]
```
2. GET /heroes/id
- Retrieves a specific hero by ID, including their powers.
Response:
```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
    {
      "id": 1,
      "hero_id": 1,
      "strength": "Strong",
      "power": {
        "id": 2,
        "name": "flight",
        "description": "gives the wielder the ability to fly through the skies"
      }
    }
  ]
}
```
3. GET /powers
Retrieves a list of all powers.
Response:

```json
[
  {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  }
]
```
3. GET /powers/id
Retrieves a specific power by ID.
Response:
```json
{
  "id": 1,
  "name": "super strength",
  "description": "gives the wielder super-human strengths"
}
```
4. PATCH /powers/
- Updates a power's description.
Request:
```json
{
  "description": "Updated description of at least 20 characters."
}
```
Response:

```json
{
  "id": 1,
  "name": "super strength",
  "description": "Updated description of at least 20 characters."
}
```
5. POST /hero_powers
- Assigns a power to a hero with a strength.
Request:
```json
{
  "strength": "Average",
  "power_id": 1,
  "hero_id": 3
}
```
Response:

```json
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Average",
  "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
  },
  "power": {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  }
}
```
## Validations
1. Power Model:
The description field must be at least 20 characters long. If the description is too short, an error will be raised.
2. HeroPower Model:
The strength field must be one of 'Strong', 'Weak', or 'Average'.

## Contributing
We welcome contributions! Please follow these steps:

1. Fork the repo.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes and commit them (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature-branch).
5. Create a new pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
