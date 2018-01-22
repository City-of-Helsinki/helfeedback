[![Build status](https://travis-ci.org/City-of-Helsinki/helfeedback.svg?branch=master)](https://travis-ci.org/City-of-Helsinki/helfeedback)
[![codecov](https://codecov.io/gh/City-of-Helsinki/helfeedback/branch/master/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/helfeedback)
[![Requirements](https://requires.io/github/City-of-Helsinki/helfeedback/requirements.svg?branch=master)](https://requires.io/github/City-of-Helsinki/helfeedback/requirements/?branch=master)

# Palvelupalautejärjestelmä

API for receiving feedback from digital services

## Prerequisites

* PostgreSQL (>= 9.3)
* Python (>= 3.4)
* Redis

## Installation

### Database

Palvelupalautejärjestelmä runs on PostgreSQL. Install the server on Debian-based systems with:

```bash
sudo apt install postgresql
```

Then create a database user and the database itself as the `postgres` system user:

```bash
createuser <your username>
createdb -l fi_FI.UTF-8 -E UTF8 -T template0 -O <your username> helfeedback
```

### Message transport for Celery (Redis)

You will need a backend for [Celery](http://www.celeryproject.org/) as
Palvelupalautejärjestelmä uses that for running long lived tasks. The
default is Redis.

One way to install redis is to use docker, which is nice in development as
you can erase the datastore very easily.

### Code

Clone the repo:
```
git clone https://github.com/City-of-Helsinki/helfeedback.git
cd helfeedback
```

Create a python environment (we recommend using
[pyenv](https://github.com/pyenv/pyenv)). Note that the latter command must
be run within the helfeedback root-directory, as it defines the default
version to be used when in that directory:
```
pyenv virtualenv helfeedback-env
pyenv local helfeedback-env
```

Palvelupalautejärjestelmä makes use of [prequ](https://github.com/suutari/prequ/),
to manage the required versions of its Python requirements. Install the
requirements thusly:
```
pip install prequ
prequ sync requirements-dev.txt requirements.txt
```
You may omit the requirements-dev.txt, if you are not going to do
development in this environment.


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

## Upgrading dependencies

Palvelupalautejärjestelmä makes use of [prequ](https://github.com/suutari/prequ/), which
is similar to, but different from [pip-tools](https://github.com/nvie/pip-tools).

For practical purposes all you need to know is:
