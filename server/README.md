Python api example project

## Steps to run the api locally

#### 1. Pre-requisites
- Ensure [the poetry is installed](https://python-poetry.org/docs/#installation)

#### 2. Install dependencies
```
  poetry install
```

#### 3. Configure python venv in the IDE
- Check venv path of poetry by running `poetry env info` 
```
Virtualenv
Python:         3.8.10
Implementation: CPython
Path:           /home/koelkast/.cache/pypoetry/virtualenvs/python-api-example-R7RR5aY2-py3.8
Valid:          True

System
Platform: linux
OS:       posix
Python:   /usr
```
- Add the virtualenv path to your IDE's Python intepreter path 


#### 4. Launch the app (from root folder of project)
```
  uvicorn src.framework.web.main:app --reload
```
```
  Call the API running locally on: http://127.0.0.1:8000
```

## Code formatting
Save brainpower and let the [Black](https://black.readthedocs.io) does the work. 

Before commiting the code, run the following command:

```
  black ./src
```

The source code will be re-formatted by Black's sensible default config


---

### Run tests locally
Tests for DB access modules make the call to the PG instance, thus a local installation of PostgresSQL is required (Ver 12+)

Before testing locally, ensure the database is initiated by running the following commands.

```
export POSTGRES_USER=[your_db_user] POSTGRES_DB=[your_db_name]
./scripts/init-db.sh
```