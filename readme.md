- [Flask Quickstart](#flask-quickstart)
  - [Installation](#installation)
    - [Create an environment](#create-an-environment)
- [Tips](#tips)
  - [Reload app upon code changes](#reload-app-upon-code-changes)
- [Understanding pip](#understanding-pip)
  - [Installing Relevant Python Libraries](#installing-relevant-python-libraries)
  - [Understanding A Python Virtual ENV](#understanding-a-python-virtual-env)
    - [Creating a Virtual ENV using Venv](#creating-a-virtual-env-using-venv)
  - [Generating Requirements.txt](#generating-requirementstxt)
  - [How to start up this project](#how-to-start-up-this-project)
- [MongoDB](#mongodb)
  - [pymongo documentation](#pymongo-documentation)
- [Flask apispec](#flask-apispec)
- [API Breakdown](#api-breakdown)
  - [GET - /user/:id](#get---userid)
  - [POST - /user](#post---user)
  - [PUT - /user/:id](#put---userid)
  - [PATCH - /user/:id](#patch---userid)
  - [DELETE - /user/:id](#delete---userid)

# Flask Quickstart

A minimalistic flask application based on their [quick start](https://flask.palletsprojects.com/en/2.1.x/quickstart/)

## Installation

### Create an environment

```
> python -3 -m venv env
> env\Scripts\activate
> pip install Flask
```

# Tips

If a file is named app.py or wsgi.py, there's no need to set the FLASK_APP env.

```
$ export FLASK_APP=hello
$ python -m flask run
```

| To remove the export, run `unset FLASK_APP`

## Reload app upon code changes

```bash
$ export FLASK_ENV=development
$ flask run
```

```bash
FLASK_ENV=development flask run --port 8080
```

# Understanding pip

## Installing Relevant Python Libraries

`pip install fastapi uvicorn pandas`

## Understanding A Python Virtual ENV

A virtual environment is a separate Python environment where the Python interpreter, libraries, and scripts installed inside are isolated from other environments. You can think of it as an additional disposable Python installation on your computer that we can turn on and off at will, and which contains its packages. If we screw up your virtual environment, we can simply delete it and create a new one.

### Creating a Virtual ENV using Venv

```
> python -3 -m venv env
> source env\Scripts\activate
```

## Generating Requirements.txt

```
$ pip freeze > requirements.txt
$ pip install -r requirements.txt
```

## How to start up this project

```
$ python index.py
```

# MongoDB

## pymongo documentation

[https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html)

# Flask apispec

[https://pypi.org/project/flask-apispec/](https://pypi.org/project/flask-apispec/)

# API Breakdown

## GET - /user/:id


|Name|Type|Description|
| ------------- | ------ | ------------- |
|status|string|Success or Error|
|data|Object| User Object|

## POST - /user


|Name|Type|Description|
| ------------- | ------ | ------------- |
|status|string|Success or Error|
|data|Object| user id|

## PUT - /user/:id


|Name|Type|Description|
| ------------- | ------ | ------------- |
|status|string|Success or Error|
|message|string||

## PATCH - /user/:id


|Name|Type|Description|
| ------------- | ------ | ------------- |
|status|string|Success or Error|
|message|string||

## DELETE - /user/:id


|Name|Type|Description|
| ------------- | ------ | ------------- |
|status|string|Success or Error|
|message|string||