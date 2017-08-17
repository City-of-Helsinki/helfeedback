[![Build status](https://travis-ci.org/City-of-Helsinki/helfeedback.svg?branch=master)](https://travis-ci.org/City-of-Helsinki/helfeedback)
[![codecov](https://codecov.io/gh/City-of-Helsinki/helfeedback/branch/master/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/helfeedback)
[![Requirements](https://requires.io/github/City-of-Helsinki/helfeedback/requirements.svg?branch=master)](https://requires.io/github/City-of-Helsinki/helfeedback/requirements/?branch=master)

# Palvelupalautejärjestelmä

API for receiving feedback from digital services

## Prerequisites

* PostgreSQL (>= 9.3)
* Python (>= 3.4)

## Installation

### Database

Palvelupalautejärjestelmä runs on PostgreSQL. Install the server on Debian-based systems with:

```bash
sudo apt install postgresql
```

Then create a database user and the database itself as the `postgres` system user:

```bash
createuser <your username>
createdb -l fi_FI.UTF8 -E UTF8 -T template0 -O <your username> helfeedback
```

### Code

Clone the repo:
```
git clone https://github.com/City-of-Helsinki/helfeedback.git
cd helfeedback
```

Initiate a virtualenv and install the Python requirements:
```
pyenv virtualenv helfeedback-env
pyenv local helfeedback-env
pip install -r requirements.txt
```

Create `local_settings.py` in the repo base dir containing the following line:
```
DEBUG = True
```

Run migrations:
```
python manage.py migrate
```

Create admin user:
```
python manage.py createsuperuser
```

Run dev server:
```
python manage.py runserver
```
and open your browser to http://127.0.0.1:8000/admin/ using the admin user credentials.
