# Flask Modular app base

## Description
- This contains the base folder structure to be used for my flask backend deployment
- Folder structure is modularized to allow plug and play of new modules

## Installation
- make a clone of repository

### Install Dependencies
- Create a virtual environment

```bash
pip install virtualenv
virtualenv venv
```
- Activate the environment
linux:
```bash
source venv/bin/activate
```
- Install dependencies

```bash
pip install -r requirements.txt
```

### Set up the Database

With Postgres running, create a database:

```bash
createdb database_name
```

### Set up your Enviroment Variables
- create a .env file in the root folder with the following variables, example:
``` bash
DEBUG=True
DB_URI='postgresql://username:password@localhost:5432/database_name'
TEST_DB_URI='postgresql://username:password@localhost:5432/database_name_test'
```
Please make sure the database name matches which you created above

### Run App/Test

- using flask
``` bash
flask run
```

- top module package
``` bash
python run.py
```

- tests
``` bash
python run_tests.py
```
